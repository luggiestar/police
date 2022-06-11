import os

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm

from .models import *

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username',)


class UploadForm(forms.Form):

    def validate_file_extension(value):
        from django.core.exceptions import ValidationError

        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.csv']
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Invalid file extension ')

    excel_file = forms.FileField(label='Excel File (.csv)', required=False, validators=[validate_file_extension])


class EntryForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'sex', 'phone', 'residency')


class StaffRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'title', 'sex', 'phone', 'station')


class AssignInvestigatorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignInvestigatorForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['investigator'].queryset = User.objects.filter(title="senior")

    class Meta:
        model = CaseInvestigator
        fields = ('investigator',)


class CaseForm(ModelForm):
    class Meta:
        model = Case
        fields = ('crime', 'description',)


class InvestigationReportForm(ModelForm):
    class Meta:
        model = InvestigationRecord
        fields = ('status', 'description',)


class DateInput(forms.DateInput):
    input_type = 'date'

# class RegistrationForm(ModelForm):
#     class Meta:
#         model = Student
#         fields = ('dob', 'parent_phone','residency')
#         widgets = {
#             'dob': DateInput(),
#         }


# class CoordinatorForm(ModelForm):
#     class Meta:
#         model = Coordinator
#         fields = ('staff', 'rank')


# class AcademicEventForm(ModelForm):
#     class Meta:
#         model = AcademicEvent
#         fields = ('year', 'event', 'rank', 'deadline')
#         widgets = {
#             'deadline': DateInput(),
#
#         }


# class CombinationSubjectForm(ModelForm):
#     class Meta:
#         model = CombinationSubject
#         fields = ('combination', 'subject')


# class SubjectForm(ModelForm):
#     class Meta:
#         model = Subject
#         fields = ('name', 'is_core')
