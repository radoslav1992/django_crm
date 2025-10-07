"""
AI Assistant services using Gemini API
"""
import google.generativeai as genai
from django.conf import settings
from django.utils.translation import gettext as _
from apps.crm.models import Contact, Company, Deal, Task
import json

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiAssistant:
    """Gemini AI Assistant for CRM"""
    
    def __init__(self, user):
        self.user = user
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    def get_crm_context(self):
        """Get relevant CRM data as context"""
        contacts_count = Contact.objects.filter(owner=self.user).count()
        companies_count = Company.objects.filter(owner=self.user).count()
        deals_count = Deal.objects.filter(owner=self.user, status='open').count()
        tasks_count = Task.objects.filter(owner=self.user, completed=False).count()
        
        context = f"""
You are a helpful CRM assistant. The user has:
- {contacts_count} contacts
- {companies_count} companies
- {deals_count} open deals
- {tasks_count} pending tasks

Help them manage their CRM effectively. Provide practical advice, insights, and actionable recommendations.
Always respond in a professional yet friendly tone.
"""
        return context
    
    def chat(self, message, conversation_history=None):
        """Send a message to Gemini and get response"""
        try:
            # Build conversation context
            context = self.get_crm_context()
            
            # Build message history
            if conversation_history:
                messages = [{'role': msg.role, 'parts': [msg.content]} 
                           for msg in conversation_history]
            else:
                messages = []
            
            # Add system context
            full_prompt = f"{context}\n\nUser: {message}"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            return response.text
        
        except Exception as e:
            return f"{_('Error communicating with AI')}: {str(e)}"
    
    def generate_email_draft(self, contact, purpose):
        """Generate email draft for a contact"""
        try:
            prompt = f"""
Generate a professional email for the following:
Contact: {contact.full_name}
Company: {contact.company.name if contact.company else 'N/A'}
Position: {contact.position or 'N/A'}
Purpose: {purpose}

Write a professional, personalized email that is friendly yet business-appropriate.
Include a subject line.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"{_('Error generating email')}: {str(e)}"
    
    def analyze_deal(self, deal):
        """Analyze a deal and provide insights"""
        try:
            prompt = f"""
Analyze this sales deal and provide insights:

Deal: {deal.name}
Value: {deal.value} {deal.currency}
Stage: {deal.stage.name if deal.stage else 'N/A'}
Status: {deal.status}
Probability: {deal.probability}%
Expected Close: {deal.expected_close_date}

Provide:
1. Risk assessment
2. Recommendations to improve win probability
3. Suggested next actions
"""
            
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"{_('Error analyzing deal')}: {str(e)}"
    
    def suggest_tasks(self, deal=None, contact=None):
        """Suggest tasks based on context"""
        try:
            if deal:
                context = f"Deal: {deal.name}, Stage: {deal.stage.name if deal.stage else 'N/A'}"
            elif contact:
                context = f"Contact: {contact.full_name}, Company: {contact.company.name if contact.company else 'N/A'}"
            else:
                context = "General CRM management"
            
            prompt = f"""
Based on this context: {context}

Suggest 3-5 specific, actionable tasks to help move things forward.
Format as a numbered list with clear action items.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"{_('Error generating tasks')}: {str(e)}"
    
    def generate_template_content(self, template_type, style='professional'):
        """Generate content for invoice/offer templates"""
        try:
            prompt = f"""
Generate {style} content for a {template_type} template.

Include:
1. Header text
2. Footer text
3. Terms and conditions (3-5 key points)

Make it appropriate for a Bulgarian business context, but write in English.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"{_('Error generating template content')}: {str(e)}"
    
    def generate_complete_template(self, user_prompt, template_type='invoice'):
        """Generate complete HTML/CSS template based on user description"""
        try:
            available_variables = """
Available template variables to use:
- {{invoice_number}} or {{offer_number}} - Document number
- {{invoice_date}} or {{offer_date}} - Document date
- {{due_date}} - Due date (for invoices)
- {{valid_until}} - Valid until date (for offers)
- {{client_name}} - Client/customer name
- {{client_address}} - Client address
- {{client_email}} - Client email
- {{client_phone}} - Client phone
- {{company_name}} - Your company name
- {{company_address}} - Your company address
- {{company_email}} - Your company email
- {{company_phone}} - Your company phone
- {{company_tax_id}} - Company tax ID/VAT number
- {{logo_url}} - Company logo URL
- {{items}} - Line items (iterate with {% for item in items %})
  - item.description - Item description
  - item.quantity - Quantity
  - item.unit_price - Unit price
  - item.total - Line total
- {{subtotal}} - Subtotal amount
- {{tax_rate}} - Tax rate percentage
- {{tax_amount}} - Tax amount
- {{discount}} - Discount amount
- {{total}} - Grand total
- {{notes}} - Additional notes
- {{payment_terms}} - Payment terms
- {{bank_details}} - Bank account details
"""
            
            prompt = f"""
You are an expert web designer specializing in creating professional invoice and offer templates.

User wants a {template_type} template with this description:
"{user_prompt}"

{available_variables}

Generate a complete, professional HTML template with embedded CSS that:
1. Is modern, clean, and professional
2. Uses the template variables listed above appropriately
3. Includes proper styling with colors, fonts, and layout
4. Is print-friendly and PDF-ready
5. Has a responsive design
6. Includes a header with logo placeholder, company info, and client info
7. Has a clean table for line items
8. Shows subtotal, tax, and total clearly
9. Includes footer with payment terms and notes
10. Uses Django template syntax for variables (double curly braces) and tags (curly brace percent)

Return ONLY the complete HTML with embedded <style> tags. Do NOT include any explanations or markdown formatting.
The template should be production-ready and beautiful.

Make it match the user's description while maintaining professional quality.
"""
            
            response = self.model.generate_content(prompt)
            
            # Clean up the response - remove markdown code blocks if present
            html_content = response.text.strip()
            if html_content.startswith('```html'):
                html_content = html_content[7:]
            elif html_content.startswith('```'):
                html_content = html_content[3:]
            if html_content.endswith('```'):
                html_content = html_content[:-3]
            
            return html_content.strip()
        
        except Exception as e:
            return f"{_('Error generating template')}: {str(e)}"
    
    def refine_template(self, current_html, user_feedback):
        """Refine an existing template based on user feedback"""
        try:
            prompt = f"""
You are an expert web designer. The user has a template and wants to improve it.

Current HTML template:
{current_html[:3000]}  # Limit to avoid token issues

User feedback:
"{user_feedback}"

Modify the template according to the user's feedback while maintaining:
1. All existing template variables
2. Professional quality
3. Clean, modern design
4. Print-friendly layout

Return ONLY the complete modified HTML. Do NOT include explanations or markdown formatting.
"""
            
            response = self.model.generate_content(prompt)
            
            # Clean up the response
            html_content = response.text.strip()
            if html_content.startswith('```html'):
                html_content = html_content[7:]
            elif html_content.startswith('```'):
                html_content = html_content[3:]
            if html_content.endswith('```'):
                html_content = html_content[:-3]
            
            return html_content.strip()
        
        except Exception as e:
            return f"{_('Error refining template')}: {str(e)}"
    
    def smart_search(self, query):
        """Perform smart search across CRM data"""
        try:
            # Get relevant data
            contacts = Contact.objects.filter(owner=self.user)[:10]
            companies = Company.objects.filter(owner=self.user)[:10]
            deals = Deal.objects.filter(owner=self.user)[:10]
            
            context = f"""
Search query: {query}

Available data:
Contacts: {[f"{c.full_name} - {c.email}" for c in contacts]}
Companies: {[f"{c.name} - {c.industry}" for c in companies]}
Deals: {[f"{d.name} - {d.value} {d.currency}" for d in deals]}

Provide relevant results and insights based on the query.
"""
            
            response = self.model.generate_content(context)
            return response.text
        
        except Exception as e:
            return f"{_('Error performing search')}: {str(e)}"

