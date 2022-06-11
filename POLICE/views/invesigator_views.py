from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import *
from ..models import *

User = get_user_model()


def investigation_list(request):
    title = "Investigations List"
    template = 'investigation/investigation_list.html'
    # get_investigator = get_object_or_404(Staff, user=request.user)
    get_investigator = request.user
    cases = CaseInvestigator.objects.filter(investigator=get_investigator)
    total = CaseInvestigator.objects.filter(investigator=get_investigator).count()

    context = {
        'title': title,
        'total': total,
        'cases': cases,
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


def investigation_report_list(request, code):
    rb_number = get_object_or_404(Case, id=code)
    title = "Investigations Report"
    template = 'investigation/investigation_report.html'
    # get_investigator = get_object_or_404(Staff, user=request.user)
    get_investigator = request.user
    get_investigation = CaseInvestigator.objects.filter(case=rb_number).first()
    cases = InvestigationRecord.objects.filter(case_investigator__case=rb_number).order_by('-id')
    total = InvestigationRecord.objects.filter(case_investigator__case=rb_number).count()

    context = {
        'title': title,
        'total': total,
        'report': cases,
        'investigation':get_investigation,
    }
    return render(request, template, context)


def create_report(request, investigation):
    title = "Investigation Report Form"
    template = 'investigation/investigation_report_form.html'
    get_investigated_case = get_object_or_404(CaseInvestigator, id=investigation)
    get_investigator = request.user
    get_complainant=Complainant.objects.filter(id=get_investigated_case.case.complainant.id).first()
    form = InvestigationReportForm()
    if request.method == "POST":
        form = InvestigationReportForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.case_investigator = get_investigated_case
            save_form.save()

            return redirect('POLICE:investigation_report_list', code=get_investigated_case.case.id)
    context = {
        'title': title,
        'complainant': get_investigated_case,
        'form': form,
        'complaint':get_complainant
    }
    return render(request, template, context)
# def create_case(request, get_user):
#     title = "Case registration"
#     template = 'police/case_registration.html'
#     get_user = get_object_or_404(Complainant, user__username=get_user)
#     get_staff = get_object_or_404(Staff, user=request.user)
#     form = CaseForm()
#     if request.method == "POST":
#         form = CaseForm(request.POST)
#         if form.is_valid():
#             save_form = form.save(commit=False)
#             save_form.complainant = get_user
#             save_form.registerer = get_staff
#
#             save_form.save()
#
#             return redirect('POLICE:case_list')
#     context = {
#         'title': title,
#         'complainant': get_user,
#         'form': form
#     }
#     return render(request, template, context)
#
#
# @login_required(login_url='/user-authentication/')
# def search_complainant(request):
#     if request.user.is_staff or request.user.is_superuser:
#         if request.method == "GET":
#             try:
#                 code = request.GET.get('complainant_code', False)
#                 get_account = Complainant.objects.filter(code=code).order_by('-id').first()
#
#                 return redirect('POLICE:complainant_details', code=get_account.code)
#             except:
#                 pass
#
#         return render(request, 'police/search_complainant.html')
#     else:
#         return redirect('POLICE:logout')
#
#
# def complainant_details(request, code):
#     get_complainant = get_object_or_404(Complainant, code=code)
#     get_complainant_cases = Case.objects.filter(complainant=get_complainant).order_by('-id')
#
#     context = {
#         'get_cases': get_complainant_cases,
#         'complainant': get_complainant,
#
#     }
#     return render(request, 'police/complainant_cases.html', context)
#
#
# def add_complainant_case(request, get_code):
#     title = "Case registration"
#     template = 'police/case_registration.html'
#     get_user = get_object_or_404(Complainant, code=get_code)
#     get_staff = get_object_or_404(Staff, user=request.user)
#     form = CaseForm()
#     if request.method == "POST":
#         form = CaseForm(request.POST)
#         if form.is_valid():
#             save_form = form.save(commit=False)
#             save_form.complainant = get_user
#             save_form.registerer = get_staff
#
#             save_form.save()
#
#             return redirect('POLICE:complainant_details', code=get_user.code)
#     context = {
#         'title': title,
#         'complainant': get_user,
#         'form': form
#     }
#     return render(request, template, context)
