from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import *
from ..models import *

User = get_user_model()


def new_case_list(request):
    title = "Case List"
    template = 'senior_officer/new_case_list.html'
    cases = Case.objects.filter(registerer__station__district__region=request.user.station.district.region).exclude(id__in=CaseInvestigator.objects.all().values("case__id"))
    total = Case.objects.filter(registerer__station__district__region=request.user.station.district.region).exclude(id__in=CaseInvestigator.objects.all().values("case__id")).count()
    form = AssignInvestigatorForm()

    context = {
        'title': title,
        'total': total,
        'cases': cases,
        'form': form
    }
    return render(request, template, context)


def save_assigned_investigator(request, get_case):
    case = get_object_or_404(Case, id=get_case)
    if request.method == "POST":
        form = AssignInvestigatorForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.case = case
            save_form.is_active = True
            save_form.save()
            messages.success(request, 'Assigned Investigator Successfully')
            return redirect('POLICE:new_case_list')


def regional_cases(request):
    title = "Regional Cases Reports"

    template = 'senior_officer/regional_cases.html'

    cases = CaseInvestigator.objects.filter(case__registerer__station__district__region=request.user.station.district.region)
    total = CaseInvestigator.objects.filter(case__registerer__station__district__region=request.user.station.district.region).count()

    context = {
        'title': title,
        'total': total,
        'cases': cases,
    }
    return render(request, template, context)


def regional_cases_report(request, code):
    title = "Regional Cases Progress"

    rb_number = get_object_or_404(Case, id=code)
    template = 'senior_officer/regional_cases_report.html'
    # get_object_or_404(Staff, user=request.user)
    get_investigation = CaseInvestigator.objects.filter(case=rb_number).first()
    cases = InvestigationRecord.objects.filter(case_investigator__case=rb_number).order_by('-id')
    total = InvestigationRecord.objects.filter(case_investigator__case=rb_number).count()

    context = {
        'title': title,
        'total': total,
        'report': cases,
        'investigation': get_investigation,
    }
    return render(request, template, context)

