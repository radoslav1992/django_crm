from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Invoice, InvoiceItem, Offer, OfferItem, Payment
from .forms import InvoiceForm, InvoiceItemForm, OfferForm, OfferItemForm, PaymentForm
from django.forms import inlineformset_factory


# Invoice Views
@login_required
def invoice_list(request):
    """List all invoices"""
    invoices = Invoice.objects.filter(owner=request.user)
    
    status = request.GET.get('status')
    if status:
        invoices = invoices.filter(status=status)
    
    paginator = Paginator(invoices, 20)
    page_number = request.GET.get('page')
    invoices_page = paginator.get_page(page_number)
    
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices_page, 'status': status})


@login_required
def invoice_detail(request, pk):
    """Invoice detail view"""
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_create(request):
    """Create new invoice"""
    InvoiceItemFormSet = inlineformset_factory(
        Invoice, InvoiceItem, form=InvoiceItemForm,
        extra=3, can_delete=True
    )
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.owner = request.user
            invoice.save()
            
            formset.instance = invoice
            formset.save()
            
            invoice.calculate_totals()
            
            # Generate QR code if payment URL provided
            if invoice.payment_url:
                invoice.generate_qr_code()
            
            messages.success(request, _('Invoice created successfully.'))
            return redirect('invoices:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    
    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'formset': formset,
        'action': 'create'
    })


@login_required
def invoice_update(request, pk):
    """Update invoice"""
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    InvoiceItemFormSet = inlineformset_factory(
        Invoice, InvoiceItem, form=InvoiceItemForm,
        extra=1, can_delete=True
    )
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice)
        
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.save()
            invoice.calculate_totals()
            
            # Generate QR code if payment URL provided
            if invoice.payment_url and not invoice.qr_code:
                invoice.generate_qr_code()
            
            messages.success(request, _('Invoice updated successfully.'))
            return redirect('invoices:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)
    
    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'formset': formset,
        'invoice': invoice,
        'action': 'update'
    })


@login_required
def invoice_delete(request, pk):
    """Delete invoice"""
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, _('Invoice deleted successfully.'))
        return redirect('invoices:invoice_list')
    
    return render(request, 'invoices/invoice_confirm_delete.html', {'invoice': invoice})


@login_required
def invoice_pdf(request, pk):
    """Generate PDF for invoice"""
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    
    # Simple HTML response for now, can be enhanced with reportlab
    html = render_to_string('invoices/invoice_pdf.html', {'invoice': invoice})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    
    # For simplicity, returning HTML. In production, use reportlab or weasyprint
    return HttpResponse(html)


# Offer Views
@login_required
def offer_list(request):
    """List all offers"""
    offers = Offer.objects.filter(owner=request.user)
    
    status = request.GET.get('status')
    if status:
        offers = offers.filter(status=status)
    
    paginator = Paginator(offers, 20)
    page_number = request.GET.get('page')
    offers_page = paginator.get_page(page_number)
    
    return render(request, 'invoices/offer_list.html', {'offers': offers_page, 'status': status})


@login_required
def offer_detail(request, pk):
    """Offer detail view"""
    offer = get_object_or_404(Offer, pk=pk, owner=request.user)
    return render(request, 'invoices/offer_detail.html', {'offer': offer})


@login_required
def offer_create(request):
    """Create new offer"""
    OfferItemFormSet = inlineformset_factory(
        Offer, OfferItem, form=OfferItemForm,
        extra=3, can_delete=True
    )
    
    if request.method == 'POST':
        form = OfferForm(request.POST)
        formset = OfferItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            offer = form.save(commit=False)
            offer.owner = request.user
            offer.save()
            
            formset.instance = offer
            formset.save()
            
            offer.calculate_totals()
            
            messages.success(request, _('Offer created successfully.'))
            return redirect('invoices:offer_detail', pk=offer.pk)
    else:
        form = OfferForm()
        formset = OfferItemFormSet()
    
    return render(request, 'invoices/offer_form.html', {
        'form': form,
        'formset': formset,
        'action': 'create'
    })


@login_required
def offer_update(request, pk):
    """Update offer"""
    offer = get_object_or_404(Offer, pk=pk, owner=request.user)
    OfferItemFormSet = inlineformset_factory(
        Offer, OfferItem, form=OfferItemForm,
        extra=1, can_delete=True
    )
    
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        formset = OfferItemFormSet(request.POST, instance=offer)
        
        if form.is_valid() and formset.is_valid():
            offer = form.save()
            formset.save()
            offer.calculate_totals()
            
            messages.success(request, _('Offer updated successfully.'))
            return redirect('invoices:offer_detail', pk=offer.pk)
    else:
        form = OfferForm(instance=offer)
        formset = OfferItemFormSet(instance=offer)
    
    return render(request, 'invoices/offer_form.html', {
        'form': form,
        'formset': formset,
        'offer': offer,
        'action': 'update'
    })


@login_required
def offer_delete(request, pk):
    """Delete offer"""
    offer = get_object_or_404(Offer, pk=pk, owner=request.user)
    if request.method == 'POST':
        offer.delete()
        messages.success(request, _('Offer deleted successfully.'))
        return redirect('invoices:offer_list')
    
    return render(request, 'invoices/offer_confirm_delete.html', {'offer': offer})


@login_required
def offer_convert_to_invoice(request, pk):
    """Convert offer to invoice"""
    offer = get_object_or_404(Offer, pk=pk, owner=request.user)
    
    if offer.converted_to_invoice:
        messages.warning(request, _('This offer has already been converted to an invoice.'))
        return redirect('invoices:offer_detail', pk=offer.pk)
    
    # Create invoice from offer
    from datetime import timedelta
    invoice = Invoice.objects.create(
        owner=request.user,
        contact=offer.contact,
        company=offer.company,
        invoice_number=f"INV-{offer.offer_number}",
        invoice_date=offer.offer_date,
        due_date=offer.valid_until,
        client_name=offer.client_name,
        client_email=offer.client_email,
        client_address=offer.client_address,
        currency=offer.currency,
        tax_rate=offer.tax_rate,
        status='draft',
        template=offer.template,
        notes=offer.notes,
        terms=offer.terms,
    )
    
    # Copy items
    for offer_item in offer.items.all():
        InvoiceItem.objects.create(
            invoice=invoice,
            description=offer_item.description,
            quantity=offer_item.quantity,
            unit_price=offer_item.unit_price,
            total=offer_item.total,
            order=offer_item.order,
        )
    
    invoice.calculate_totals()
    
    # Update offer
    offer.converted_to_invoice = invoice
    offer.status = 'accepted'
    offer.save()
    
    messages.success(request, _('Offer converted to invoice successfully.'))
    return redirect('invoices:invoice_detail', pk=invoice.pk)


# Payment Views
@login_required
def payment_list(request):
    """List all payments"""
    payments = Payment.objects.filter(owner=request.user)
    
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    payments_page = paginator.get_page(page_number)
    
    return render(request, 'invoices/payment_list.html', {'payments': payments_page})


@login_required
def payment_create(request):
    """Create new payment"""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.owner = request.user
            payment.save()
            
            # Update invoice if linked
            if payment.invoice:
                invoice = payment.invoice
                invoice.paid_amount += payment.amount
                payment.is_matched = True
                
                if invoice.is_paid:
                    invoice.status = 'paid'
                else:
                    invoice.status = 'partially_paid'
                invoice.save()
                payment.save()
            else:
                # Try to auto-match
                payment.match_to_invoice()
            
            messages.success(request, _('Payment recorded successfully.'))
            return redirect('invoices:payment_list')
    else:
        form = PaymentForm()
    
    return render(request, 'invoices/payment_form.html', {'form': form, 'action': 'create'})


# Email sending views
@login_required
def invoice_send_email(request, pk):
    """Send invoice email to client"""
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    
    if not invoice.client_email:
        messages.error(request, _('Cannot send email: Client email address is missing.'))
        return redirect('invoices:invoice_detail', pk=invoice.pk)
    
    try:
        invoice.send_email(request=request)
        messages.success(request, _('Invoice email sent successfully to {email}').format(email=invoice.client_email))
    except Exception as e:
        messages.error(request, _('Failed to send email: {error}').format(error=str(e)))
    
    return redirect('invoices:invoice_detail', pk=invoice.pk)


@login_required
def offer_send_email(request, pk):
    """Send offer email to client"""
    offer = get_object_or_404(Offer, pk=pk, owner=request.user)
    
    if not offer.client_email:
        messages.error(request, _('Cannot send email: Client email address is missing.'))
        return redirect('invoices:offer_detail', pk=offer.pk)
    
    try:
        offer.send_email(request=request)
        messages.success(request, _('Offer email sent successfully to {email}').format(email=offer.client_email))
    except Exception as e:
        messages.error(request, _('Failed to send email: {error}').format(error=str(e)))
    
    return redirect('invoices:offer_detail', pk=offer.pk)

