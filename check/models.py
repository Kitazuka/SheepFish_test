from django.db import models


class TypeChoices(models.TextChoices):
    CLIENT = "Client"
    KITCHEN = "Kitchen"


class Printer(models.Model):
    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=255, unique=True)
    check_type = models.CharField(max_length=50, choices=TypeChoices.choices)
    point_id = models.IntegerField()

    @staticmethod
    def print_check(check: "Check"):
        print(check.order)
        check.status = "printed"
        check.save()

    def __str__(self):
        return self.name


class Check(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = "new"
        RENDERED = "rendered"
        PRINTED = "printed"

    printer_id = models.ForeignKey(
        Printer, on_delete=models.CASCADE, related_name="checks"
    )
    type = models.CharField(max_length=50, choices=TypeChoices.choices)
    order = models.JSONField()
    status = models.CharField(
        max_length=50, choices=StatusChoices.choices, default="new"
    )
    pdf_file = models.FileField(upload_to="media/pdf", null=True)

    def __str__(self):
        return f"{self.id}: {self.status}"
