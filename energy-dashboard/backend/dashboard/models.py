from django.db import models
from django.contrib.auth.models import User


class Chart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class EnergyRecord(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    chart = models.ForeignKey(
        Chart,
        on_delete=models.CASCADE
    )

    month = models.CharField(
        max_length=50
    )

    consumption = models.FloatField()

    cost = models.FloatField()

    peak_load = models.FloatField()

    efficiency = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.month