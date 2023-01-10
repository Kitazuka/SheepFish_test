import os
from rest_framework.exceptions import ValidationError

from SheepFish_test.settings import MEDIA_ROOT
from check.pdf_creator import wkhtmltopdf_create_pdf_request
from check.models import Check, Printer

from celery import shared_task


@shared_task
def create_pdf_file(check_id: int) -> None:
    check = Check.objects.get(id=check_id)
    response = wkhtmltopdf_create_pdf_request(check)
    path_to_pdf = os.path.join("pdf", f"{check.id}_{check.type}.pdf")

    if os.path.exists(path_to_pdf):
        raise ValidationError(
            {f"Error": f"Pdf for check №{check.id} already exists"}
        )
    with open(os.path.join(MEDIA_ROOT, path_to_pdf), "wb") as file:
        file.write(response.content)
        check.pdf_file.name = path_to_pdf
        check.status = "rendered"
        check.save()


@shared_task
def create_pdf_for_all_checks_without_pdf() -> None:
    for check in Check.objects.filter(status="new"):
        create_pdf_file.delay(check.id)


@shared_task
def print_converted_checks() -> None:
    for printer in Printer.objects.all():
        for check in printer.checks.filter(status="rendered"):
            printer.print_check(check)
