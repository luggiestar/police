from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import StaffRegistrationForm
from ..models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('POLICE:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'police/change_password.html', {
        'form': form
    })


def staff_entry(request):
    title = "Staff List"
    template = 'police/staff_entry.html'
    get_staff = User.objects.all().order_by('-id')
    form = StaffRegistrationForm()

    if request.method == "POST":
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            get_username = form.cleaned_data['phone']
            get_pas = form.cleaned_data['last_name']
            make_password_upper_case = get_pas.upper()
            save_form.username = get_username
            save_form.is_staff = True
            save_form.set_password(make_password_upper_case)
            save_form.save()
            messages.success(request, f'{get_pas} created successfully!')

            return redirect('POLICE:staff_list')

    context = {
        'title': title,
        'form': form,
        'staff': get_staff
    }
    return render(request, template, context)


def update_staff(request, object_pk):
    try:
        instance = User.objects.get(id=object_pk)
    except User.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('POLICE:staff_list')
    else:
        form = StaffRegistrationForm(instance=instance)
    context_dict = {'form': form, 'instance': instance}
    return render(request, 'police/update_user.html', context_dict)


def delete_user(request, object_pk):
    if request.user.is_staff:
        instance = User.objects.filter(id=object_pk).first()
        instance.delete()

        return redirect('POLICE:staff_list')


def change_status(request, object_pk):
    if request.user.is_staff:
        instance = User.objects.filter(id=object_pk).first()
        if instance.is_active:
            instance.is_active = False
            instance.save()

        else:
            instance.is_active = True
            instance.save()

        return redirect('POLICE:staff_list')
