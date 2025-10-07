from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Company, Contact, Deal, Task, Pipeline, Stage, Activity
from .forms import CompanyForm, ContactForm, DealForm, TaskForm, PipelineForm, StageForm, ActivityForm


@login_required
def dashboard(request):
    """Main CRM dashboard"""
    user = request.user
    
    # Statistics
    total_contacts = Contact.objects.filter(owner=user).count()
    total_companies = Company.objects.filter(owner=user).count()
    total_deals = Deal.objects.filter(owner=user, status='open').count()
    total_deal_value = Deal.objects.filter(owner=user, status='open').aggregate(Sum('value'))['value__sum'] or 0
    
    # Recent items
    recent_contacts = Contact.objects.filter(owner=user)[:5]
    recent_deals = Deal.objects.filter(owner=user)[:5]
    upcoming_tasks = Task.objects.filter(owner=user, completed=False).order_by('due_date')[:5]
    recent_activities = Activity.objects.filter(owner=user)[:10]
    
    # Deals by stage
    deals_by_stage = Deal.objects.filter(owner=user, status='open').values('stage__name').annotate(count=Count('id'), total=Sum('value'))
    
    # Additional statistics
    total_completed_tasks = Task.objects.filter(owner=user, completed=True).count()
    total_revenue = Deal.objects.filter(owner=user, status='won').aggregate(Sum('value'))['value__sum'] or 0
    average_deal_size = Deal.objects.filter(owner=user, status='won').aggregate(Avg('value'))['value__avg'] or 0
    overdue_tasks = Task.objects.filter(owner=user, completed=False, due_date__lt=timezone.now()).count()

    context = {
        'total_contacts': total_contacts,
        'total_companies': total_companies,
        'total_deals': total_deals,
        'total_deal_value': total_deal_value,
        'recent_contacts': recent_contacts,
        'recent_deals': recent_deals,
        'upcoming_tasks': upcoming_tasks,
        'recent_activities': recent_activities,
        'deals_by_stage': deals_by_stage,
    }
    
    context.update({
        'total_completed_tasks': total_completed_tasks,
        'total_revenue': total_revenue,
        'average_deal_size': average_deal_size,
        'overdue_tasks': overdue_tasks,
    })
    
    return render(request, 'crm/dashboard.html', context)


# Contact Views
@login_required
def contact_list(request):
    """List all contacts"""
    contacts = Contact.objects.filter(owner=request.user)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        contacts = contacts.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Filter by company
    company_id = request.GET.get('company')
    if company_id:
        contacts = contacts.filter(company_id=company_id)
    
    # Pagination
    paginator = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    contacts_page = paginator.get_page(page_number)
    
    return render(request, 'crm/contact_list.html', {'contacts': contacts_page, 'search_query': search_query})


@login_required
def contact_detail(request, pk):
    """Contact detail view"""
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    activities = Activity.objects.filter(contact=contact)
    tasks = Task.objects.filter(contact=contact)
    deals = Deal.objects.filter(contact=contact)
    
    return render(request, 'crm/contact_detail.html', {
        'contact': contact,
        'activities': activities,
        'tasks': tasks,
        'deals': deals,
    })


@login_required
def contact_create(request):
    """Create new contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            messages.success(request, _('Contact created successfully.'))
            return redirect('crm:contact_detail', pk=contact.pk)
    else:
        form = ContactForm(user=request.user)
    
    return render(request, 'crm/contact_form.html', {'form': form, 'action': 'create'})


@login_required
def contact_update(request, pk):
    """Update contact"""
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Contact updated successfully.'))
            return redirect('crm:contact_detail', pk=contact.pk)
    else:
        form = ContactForm(instance=contact, user=request.user)
    
    return render(request, 'crm/contact_form.html', {'form': form, 'contact': contact, 'action': 'update'})


@login_required
def contact_delete(request, pk):
    """Delete contact"""
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, _('Contact deleted successfully.'))
        return redirect('crm:contact_list')
    
    return render(request, 'crm/contact_confirm_delete.html', {'contact': contact})


# Company Views
@login_required
def company_list(request):
    """List all companies"""
    companies = Company.objects.filter(owner=request.user)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        companies = companies.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(industry__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(companies, 20)
    page_number = request.GET.get('page')
    companies_page = paginator.get_page(page_number)
    
    return render(request, 'crm/company_list.html', {'companies': companies_page, 'search_query': search_query})


@login_required
def company_detail(request, pk):
    """Company detail view"""
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    contacts = Contact.objects.filter(company=company)
    deals = Deal.objects.filter(company=company)
    activities = Activity.objects.filter(company=company)
    
    return render(request, 'crm/company_detail.html', {
        'company': company,
        'contacts': contacts,
        'deals': deals,
        'activities': activities,
    })


@login_required
def company_create(request):
    """Create new company"""
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, _('Company created successfully.'))
            return redirect('crm:company_detail', pk=company.pk)
    else:
        form = CompanyForm()
    
    return render(request, 'crm/company_form.html', {'form': form, 'action': 'create'})


@login_required
def company_update(request, pk):
    """Update company"""
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, _('Company updated successfully.'))
            return redirect('crm:company_detail', pk=company.pk)
    else:
        form = CompanyForm(instance=company)
    
    return render(request, 'crm/company_form.html', {'form': form, 'company': company, 'action': 'update'})


@login_required
def company_delete(request, pk):
    """Delete company"""
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    if request.method == 'POST':
        company.delete()
        messages.success(request, _('Company deleted successfully.'))
        return redirect('crm:company_list')
    
    return render(request, 'crm/company_confirm_delete.html', {'company': company})


# Deal Views
@login_required
def deal_list(request):
    """List all deals"""
    deals = Deal.objects.filter(owner=request.user)
    
    # Filter by status
    status = request.GET.get('status', 'open')
    if status:
        deals = deals.filter(status=status)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        deals = deals.filter(Q(name__icontains=search_query))
    
    # Pagination
    paginator = Paginator(deals, 20)
    page_number = request.GET.get('page')
    deals_page = paginator.get_page(page_number)
    
    return render(request, 'crm/deal_list.html', {'deals': deals_page, 'status': status, 'search_query': search_query})


@login_required
def deal_detail(request, pk):
    """Deal detail view"""
    deal = get_object_or_404(Deal, pk=pk, owner=request.user)
    activities = Activity.objects.filter(deal=deal)
    tasks = Task.objects.filter(deal=deal)
    
    return render(request, 'crm/deal_detail.html', {
        'deal': deal,
        'activities': activities,
        'tasks': tasks,
    })


@login_required
def deal_create(request):
    """Create new deal"""
    if request.method == 'POST':
        form = DealForm(request.POST, user=request.user)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.owner = request.user
            deal.save()
            
            # Create activity
            Activity.objects.create(
                owner=request.user,
                deal=deal,
                activity_type='deal_created',
                title=_('Deal created'),
                description=f'{_("Deal")} "{deal.name}" {_("was created")}'
            )
            
            messages.success(request, _('Deal created successfully.'))
            return redirect('crm:deal_detail', pk=deal.pk)
    else:
        form = DealForm(user=request.user)
    
    return render(request, 'crm/deal_form.html', {'form': form, 'action': 'create'})


@login_required
def deal_update(request, pk):
    """Update deal"""
    deal = get_object_or_404(Deal, pk=pk, owner=request.user)
    old_status = deal.status
    
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal, user=request.user)
        if form.is_valid():
            deal = form.save()
            
            # Track status changes
            if deal.status != old_status:
                if deal.status == 'won':
                    deal.actual_close_date = timezone.now().date()
                    deal.save()
                    Activity.objects.create(
                        owner=request.user,
                        deal=deal,
                        activity_type='deal_won',
                        title=_('Deal won'),
                        description=f'{_("Deal")} "{deal.name}" {_("was won")}'
                    )
                elif deal.status == 'lost':
                    deal.actual_close_date = timezone.now().date()
                    deal.save()
                    Activity.objects.create(
                        owner=request.user,
                        deal=deal,
                        activity_type='deal_lost',
                        title=_('Deal lost'),
                        description=f'{_("Deal")} "{deal.name}" {_("was lost")}'
                    )
            
            messages.success(request, _('Deal updated successfully.'))
            return redirect('crm:deal_detail', pk=deal.pk)
    else:
        form = DealForm(instance=deal, user=request.user)
    
    return render(request, 'crm/deal_form.html', {'form': form, 'deal': deal, 'action': 'update'})


@login_required
def deal_delete(request, pk):
    """Delete deal"""
    deal = get_object_or_404(Deal, pk=pk, owner=request.user)
    if request.method == 'POST':
        deal.delete()
        messages.success(request, _('Deal deleted successfully.'))
        return redirect('crm:deal_list')
    
    return render(request, 'crm/deal_confirm_delete.html', {'deal': deal})


# Task Views
@login_required
def task_list(request):
    """List all tasks"""
    tasks = Task.objects.filter(Q(owner=request.user) | Q(assigned_to=request.user))
    
    # Filter by completion
    completed = request.GET.get('completed')
    if completed == 'true':
        tasks = tasks.filter(completed=True)
    elif completed == 'false':
        tasks = tasks.filter(completed=False)
    
    # Pagination
    paginator = Paginator(tasks, 20)
    page_number = request.GET.get('page')
    tasks_page = paginator.get_page(page_number)
    
    return render(request, 'crm/task_list.html', {'tasks': tasks_page, 'completed': completed})


@login_required
def task_create(request):
    """Create new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            if not task.assigned_to:
                task.assigned_to = request.user
            task.save()
            messages.success(request, _('Task created successfully.'))
            return redirect('crm:task_list')
    else:
        form = TaskForm(user=request.user)
    
    return render(request, 'crm/task_form.html', {'form': form, 'action': 'create'})


@login_required
def task_update(request, pk):
    """Update task"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            if task.completed and not task.completed_at:
                task.completed_at = timezone.now()
            task.save()
            messages.success(request, _('Task updated successfully.'))
            return redirect('crm:task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    
    return render(request, 'crm/task_form.html', {'form': form, 'task': task, 'action': 'update'})


@login_required
def task_delete(request, pk):
    """Delete task"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, _('Task deleted successfully.'))
        return redirect('crm:task_list')
    
    return render(request, 'crm/task_confirm_delete.html', {'task': task})


# Pipeline Views
@login_required
def pipeline_list(request):
    """List all pipelines"""
    pipelines = Pipeline.objects.filter(owner=request.user)
    return render(request, 'crm/pipeline_list.html', {'pipelines': pipelines})


@login_required
def pipeline_create(request):
    """Create new pipeline"""
    if request.method == 'POST':
        form = PipelineForm(request.POST)
        if form.is_valid():
            pipeline = form.save(commit=False)
            pipeline.owner = request.user
            pipeline.save()
            messages.success(request, _('Pipeline created successfully.'))
            return redirect('crm:pipeline_list')
    else:
        form = PipelineForm()
    
    return render(request, 'crm/pipeline_form.html', {'form': form, 'action': 'create'})

