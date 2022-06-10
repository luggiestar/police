from django.db import models
from django.conf import settings


class Zone(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name = "zone"
        verbose_name_plural = "zone"

    def __str__(self):
        return "{0}".format(self.name)


class Region(models.Model):
    name = models.CharField(max_length=40, unique=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=False, related_name="Zonal")

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "region"

    def __str__(self):
        return "{0}".format(self.name)


class District(models.Model):
    name = models.CharField(max_length=40, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False, related_name="Region")

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "District"

    def __str__(self):
        return "{0}".format(self.name)


class Station(models.Model):
    name = models.CharField(max_length=40, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=False, related_name="District")

    class Meta:
        verbose_name = "Police Station"
        verbose_name_plural = "Police Station"

    def __str__(self):
        return "{0}".format(self.name)
