from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import *
from ..models import *

User = get_user_model()


def case_list(request):
    title = "Case List"
    template = 'police/case_list.html'
    cases = Case.objects.all()
    total = Case.objects.all().count()
    form = EntryForm()

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            get_username = form.cleaned_data['phone']
            get_password = form.cleaned_data['last_name']
            make_password_upper_case = get_password.upper()
            save_form.username = get_username
            save_form.title = "complaint"
            save_form.set_password(make_password_upper_case)
            save_form.save()

            return redirect('POLICE:case_registration', get_user=get_username)

    context = {
        'title': title,
        'total': total,
        'cases': cases,
        'form': form
    }
    return render(request, template, context)


def create_case(request, get_user):
    title = "Case registration"
    template = 'police/case_registration.html'
    get_user = get_object_or_404(Complainant, user__username=get_user)
    get_staff = User.objects.filter(id=request.user.id, title="registerer")

    form = CaseForm()
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.complainant = get_user
            # save_form.registerer = request.user
            save_form.registerer = get_staff

            save_form.save()

            return redirect('POLICE:case_list')
    context = {
        'title': title,
        'complainant': get_user,
        'form': form
    }
    return render(request, template, context)


@login_required(login_url='/user-authentication/')
def search_complainant(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "GET":
            try:
                code = request.GET.get('complainant_code', False)
                get_account = Complainant.objects.filter(code=code).order_by('-id').first()

                return redirect('POLICE:complainant_details', code=get_account.code)
            except:
                pass

        return render(request, 'police/search_complainant.html')
    else:
        return redirect('POLICE:logout')


def complainant_details(request, code):
    get_complainant = get_object_or_404(Complainant, code=code)
    get_complainant_cases = Case.objects.filter(complainant=get_complainant).order_by('-id')

    context = {
        'get_cases': get_complainant_cases,
        'complainant': get_complainant,

    }
    return render(request, 'police/complainant_cases.html', context)


def add_complainant_case(request, get_code):
    title = "Case registration"
    template = 'police/case_registration.html'
    get_user = get_object_or_404(Complainant, code=get_code)
    get_staff = User.objects.filter(id=request.user.id, title="registerer")
    form = CaseForm()
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.complainant = get_user
            # save_form.registerer = request.user
            save_form.registerer = get_staff

            save_form.save()

            return redirect('POLICE:complainant_details', code=get_user.code)
    context = {
        'title': title,
        'complainant': get_user,
        'form': form
    }
    return render(request, template, context)
