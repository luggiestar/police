from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'POLICE'
urlpatterns = [
    # path('', index, name="index"),
    path('', login_view, name="login"),

    path('chart/', chart_view, name="chart"),

    path('ussd/', ussd, name="ussd"),
    path('case-list', case_list, name="case_list"),
    path('assign-staff-complaint', generate_code, name="generate_code"),
    path('user-management', user_management, name="user_management"),
    path('update-user/<object_pk>', update_staff, name="update_staff"),
    path('delete-user/<object_pk>', delete_user, name="delete_user"),
    path('change-user-status/<object_pk>', change_status, name="change_status"),
    path('regional-cases', regional_cases, name="regional_cases"),
    path('account-change-password', change_password, name='change_password'),
    path('my-case-list', my_case_list, name="my_case_list"),
    path('add-investigation-report/<investigation>', create_report, name="create_report"),
    path('investigation-list/', investigation_list, name="investigation_list"),
    path('investigation-report/<code>/', investigation_report_list, name="investigation_report_list"),
    path('my-case-report/<code>/', my_case_report_list, name="my_case_report_list"),
    path('regional-cases-report/<code>/', regional_cases_report, name="regional_cases_report"),
    path('new-case-list', new_case_list, name="new_case_list"),
    path('search-complainant', search_complainant, name="search_complainant"),
    path('case-registration/<get_user>', create_case, name="case_registration"),
    path('add-complaint-case-registration/<get_code>', add_complainant_case, name="add_complainant_case"),
    path('save-assigned-investigator/<get_case>', save_assigned_investigator, name="save_assigned_investigator"),
    path('complainant-case-history/<code>', complainant_details, name="complainant_details"),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
