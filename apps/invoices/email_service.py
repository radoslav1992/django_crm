"""
Resend Email Service for sending invoices, offers, and custom email templates
"""
import resend
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from typing import Optional, Dict, Any
import logging
import ssl
import os

logger = logging.getLogger(__name__)

# Configure SSL for Resend API
try:
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
except ImportError:
    logger.warning("certifi not installed - SSL verification may fail")

# Suppress SSL warnings if in development
import urllib3
if settings.DEBUG:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ResendEmailService:
    """Service for sending emails via Resend API"""
    
    def __init__(self, user):
        """
        Initialize Resend service with user's API key
        
        Args:
            user: User instance with resend_api_key configured
        """
        self.user = user
        if user.has_resend_configured():
            resend.api_key = user.resend_api_key
            self.from_email = user.resend_from_email
            self.from_name = user.resend_from_name or user.get_full_name() or user.username
        else:
            # Fallback to settings if user hasn't configured Resend
            resend.api_key = settings.RESEND_API_KEY
            self.from_email = settings.RESEND_FROM_EMAIL
            self.from_name = settings.RESEND_FROM_NAME
    
    def _format_from_address(self) -> str:
        """Format the from address with name"""
        if self.from_name:
            return f"{self.from_name} <{self.from_email}>"
        return self.from_email
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_text: Optional[str] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[list] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Send an email via Resend
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML body of the email
            plain_text: Plain text version (optional)
            reply_to: Reply-to email address (optional)
            attachments: List of attachments (optional)
            tags: Dictionary of tags for tracking (optional)
        
        Returns:
            Response from Resend API
        """
        try:
            params = {
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content,
            }
            
            # Add optional parameters
            if plain_text:
                params["text"] = plain_text
            
            if reply_to:
                params["reply_to"] = reply_to
            
            if attachments:
                params["attachments"] = attachments
            
            if tags:
                params["tags"] = tags
            
            # Send email via Resend with SSL configuration
            try:
                response = resend.Emails.send(params)
            except Exception as ssl_error:
                # If SSL fails and we're in debug mode, try with a workaround
                if settings.DEBUG and "SSL" in str(ssl_error):
                    logger.warning(f"SSL error in DEBUG mode, attempting workaround: {ssl_error}")
                    # In development, you can use Django's email backend as fallback
                    from django.core.mail import EmailMessage
                    email = EmailMessage(
                        subject=subject,
                        body=html_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[to_email],
                    )
                    email.content_subtype = "html"
                    email.send(fail_silently=False)
                    logger.info(f"Email sent via Django fallback (development mode)")
                    return {"success": True, "id": "dev-fallback", "note": "Sent via Django email backend (SSL workaround)"}
                else:
                    raise
            
            logger.info(f"Email sent successfully to {to_email} via Resend. ID: {response.get('id')}")
            return {"success": True, "id": response.get("id"), "response": response}
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error sending email via Resend: {error_msg}")
            
            # Provide helpful error message
            if "SSL" in error_msg or "certificate" in error_msg.lower():
                error_msg = (
                    "SSL Certificate Error: Please run '/Applications/Python 3.12/Install Certificates.command' "
                    "or install certifi: pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org certifi"
                )
            
            return {"success": False, "error": error_msg}
    
    def _sanitize_tag_value(self, value: str) -> str:
        """
        Sanitize tag value to only contain ASCII letters, numbers, underscores, or dashes.
        Resend API requirement.
        """
        import re
        # Remove non-ASCII characters and replace spaces with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', str(value))
        # Remove consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Trim underscores from start/end
        return sanitized.strip('_')[:100]  # Limit to 100 chars
    
    def send_invoice_email(self, invoice, request=None, email_template_id=None) -> Dict[str, Any]:
        """
        Send invoice email to client
        
        Args:
            invoice: Invoice instance
            request: Django request object for building absolute URLs
            email_template_id: Optional custom email template ID
        
        Returns:
            Response dictionary with success status
        """
        from django.urls import reverse
        
        if not invoice.client_email:
            return {"success": False, "error": _("Client email is required")}
        
        # Build PDF URL
        if request:
            pdf_url = request.build_absolute_uri(
                reverse('invoices:invoice_pdf', kwargs={'pk': invoice.pk})
            )
        else:
            pdf_url = f"{settings.SITE_URL}{reverse('invoices:invoice_pdf', kwargs={'pk': invoice.pk})}"
        
        # Prepare template context
        context = {
            'invoice': invoice,
            'contact_name': invoice.client_name,
            'client_name': invoice.client_name,
            'contact_email': invoice.client_email,
            'client_email': invoice.client_email,
            'company_name': invoice.company.name if invoice.company else '',
            'invoice_number': invoice.invoice_number,
            'invoice_date': invoice.invoice_date,
            'due_date': invoice.due_date,
            'total_amount': invoice.total_amount,
            'currency': invoice.currency,
            'payment_url': invoice.payment_url or '',
            'pdf_url': pdf_url,
            'sender_name': self.from_name,
            'sender_company': self.from_name,
            'sender_email': self.from_email,
            'user': self.user,
        }
        
        # Use custom template if provided
        if email_template_id:
            try:
                from apps.templates.models import EmailTemplate
                email_template = EmailTemplate.objects.get(id=email_template_id, owner=self.user)
                logger.info(f"Using custom email template: {email_template.name} (ID: {email_template_id})")
                subject, html_content, plain_text = email_template.render(context)
                # Track template usage
                email_template.increment_usage()
            except EmailTemplate.DoesNotExist:
                logger.error(f"Email template with ID {email_template_id} not found for user {self.user.username}")
                return {"success": False, "error": _("Email template not found")}
            except Exception as e:
                logger.error(f"Error rendering email template {email_template_id}: {str(e)}")
                return {"success": False, "error": _("Error rendering template: ") + str(e)}
        else:
            # Use default template
            logger.info(f"Using default invoice email template")
            subject = f"{_('Invoice')} {invoice.invoice_number}"
            html_content = render_to_string('invoices/email_invoice.html', context)
            
            # Plain text version for default template
            plain_text = f"""
{_('Dear')} {invoice.client_name},

{_('Please find your invoice')} {invoice.invoice_number}.

{_('Invoice Details')}:
- {_('Invoice Number')}: {invoice.invoice_number}
- {_('Date')}: {invoice.invoice_date}
- {_('Due Date')}: {invoice.due_date}
- {_('Total Amount')}: {invoice.total_amount} {invoice.currency}

{_('View and download your invoice here')}: {pdf_url}

{_('Thank you for your business!')}

{_('Best regards')},
{self.from_name}
            """
        
        # Send email with sanitized tags
        result = self.send_email(
            to_email=invoice.client_email,
            subject=subject,
            html_content=html_content,
            plain_text=plain_text,
            reply_to=self.user.email if self.user.email else None,
            tags={
                "type": "invoice",
                "invoice_id": str(invoice.id),
                "invoice_number": self._sanitize_tag_value(invoice.invoice_number),
            }
        )
        
        return result
    
    def send_offer_email(self, offer, request=None, email_template_id=None) -> Dict[str, Any]:
        """
        Send offer email to client
        
        Args:
            offer: Offer instance
            request: Django request object for building absolute URLs
            email_template_id: Optional custom email template ID
        
        Returns:
            Response dictionary with success status
        """
        from django.urls import reverse
        
        if not offer.client_email:
            return {"success": False, "error": _("Client email is required")}
        
        # Build PDF URL
        if request:
            pdf_url = request.build_absolute_uri(
                reverse('invoices:offer_pdf', kwargs={'pk': offer.pk})
            )
        else:
            pdf_url = f"{settings.SITE_URL}{reverse('invoices:offer_pdf', kwargs={'pk': offer.pk})}"
        
        # Prepare template context
        context = {
            'offer': offer,
            'contact_name': offer.client_name,
            'client_name': offer.client_name,
            'contact_email': offer.client_email,
            'client_email': offer.client_email,
            'company_name': offer.company.name if offer.company else '',
            'offer_number': offer.offer_number,
            'offer_date': offer.offer_date,
            'valid_until': offer.valid_until,
            'total_amount': offer.total_amount,
            'currency': offer.currency,
            'pdf_url': pdf_url,
            'sender_name': self.from_name,
            'sender_company': self.from_name,
            'sender_email': self.from_email,
            'user': self.user,
        }
        
        # Use custom template if provided
        if email_template_id:
            try:
                from apps.templates.models import EmailTemplate
                email_template = EmailTemplate.objects.get(id=email_template_id, owner=self.user)
                logger.info(f"Using custom email template: {email_template.name} (ID: {email_template_id})")
                subject, html_content, plain_text = email_template.render(context)
                # Track template usage
                email_template.increment_usage()
            except EmailTemplate.DoesNotExist:
                logger.error(f"Email template with ID {email_template_id} not found for user {self.user.username}")
                return {"success": False, "error": _("Email template not found")}
            except Exception as e:
                logger.error(f"Error rendering email template {email_template_id}: {str(e)}")
                return {"success": False, "error": _("Error rendering template: ") + str(e)}
        else:
            # Use default template
            logger.info(f"Using default offer email template")
            subject = f"{_('Offer')} {offer.offer_number}"
            html_content = render_to_string('invoices/email_offer.html', context)
            
            # Plain text version for default template
            plain_text = f"""
{_('Dear')} {offer.client_name},

{_('Please find your offer')} {offer.offer_number}.

{_('Offer Details')}:
- {_('Offer Number')}: {offer.offer_number}
- {_('Date')}: {offer.offer_date}
- {_('Valid Until')}: {offer.valid_until}
- {_('Total Amount')}: {offer.total_amount} {offer.currency}

{_('View and download your offer here')}: {pdf_url}

{_('We look forward to working with you!')}

{_('Best regards')},
{self.from_name}
            """
        
        # Send email with sanitized tags
        result = self.send_email(
            to_email=offer.client_email,
            subject=subject,
            html_content=html_content,
            plain_text=plain_text,
            reply_to=self.user.email if self.user.email else None,
            tags={
                "type": "offer",
                "offer_id": str(offer.id),
                "offer_number": self._sanitize_tag_value(offer.offer_number),
            }
        )
        
        return result
    
    def send_custom_email(
        self,
        to_email: str,
        subject: str,
        template_html: str,
        context: Dict[str, Any] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a custom email using an email template
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            template_html: HTML template content (can include Django template variables)
            context: Dictionary of context variables for the template
            reply_to: Reply-to email address (optional)
        
        Returns:
            Response dictionary with success status
        """
        from django.template import Template, Context
        
        try:
            # Render the template with context
            template = Template(template_html)
            html_content = template.render(Context(context or {}))
            
            # Send email
            result = self.send_email(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                reply_to=reply_to or (self.user.email if self.user.email else None),
                tags={
                    "type": "custom",
                    "user_id": str(self.user.id),
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error sending custom email: {str(e)}")
            return {"success": False, "error": str(e)}

