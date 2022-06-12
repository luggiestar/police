from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from datetime import datetime, timedelta

from ..models import *


class Crime(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name = "Crime"
        verbose_name_plural = "Crime"

    def __str__(self):
        return "{0}".format(self.name)


class Status(models.Model):
    name = models.CharField(max_length=40, unique=True)
    code = models.CharField(max_length=4, unique=True)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"

    def __str__(self):
        return "{0}".format(self.name)


class Case(models.Model):
    rb = models.CharField("RB", max_length=50, unique=True, null=False)
    description = RichTextField(null=True, blank=True)
    complainant = models.ForeignKey('Complainant', on_delete=models.CASCADE, null=False,
                                    related_name="complainant_case")
    registerer = models.ForeignKey('User', on_delete=models.CASCADE, null=False, related_name="staff_registerer")
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, null=False, related_name="case_crime")
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Case"

    def __str__(self):
        return "{0}-{1}".format(self.complainant, self.rb)


class CaseInvestigator(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=False,
                             related_name="investigation_case")
    investigator = models.ForeignKey('User', on_delete=models.CASCADE, null=False, related_name="cas_investigator")
    is_active = models.BooleanField("status", default=True)
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Case Investigator"
        verbose_name_plural = "Case Investigator"

    def __str__(self):
        return "{0}-{1}".format(self.case, self.investigator)


class InvestigationRecord(models.Model):
    case_investigator = models.ForeignKey(CaseInvestigator, on_delete=models.CASCADE, null=False,
                                          related_name="case_investigator")
    description = RichTextField(null=True, blank=True)

    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=False, related_name="case_status")
    is_active = models.BooleanField("status", default=True)
    report_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Investigation Record"
        verbose_name_plural = "Investigation Record"

    def __str__(self):
        return "{0}-{1}".format(self.case_investigator, self.status)


class Chart(models.Model):
    complaint = models.ForeignKey('Complainant', on_delete=models.CASCADE, related_name="complaint_tracking"
                                                                                        "")
    start_date = models.DateField()
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    week_number = models.CharField(max_length=2, blank=True, editable=False)
    finish_date = models.DateField(null=True, blank=True, editable=False)

    # string representation method
    def __str__(self):
        return str(self.complaint)

    # overiding the save method
    def save(self, *args, **kwargs):
        print(self.start_date.isocalendar()[1])
        if self.week_number == "":
            self.week_number = self.start_date.isocalendar()[1]

            date_obj = datetime.strptime(str(self.start_date), '%Y-%m-%d')

            start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
            end_of_week = start_of_week + timedelta(days=6)
            self.finish_date = end_of_week
        super().save(*args, **kwargs)
