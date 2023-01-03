from django.contrib import admin

from check.models import Check, Printer


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ["name", "api_key", "check_type", "point_id"]
    list_filter = ["check_type"]


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ["id", "printer_id", "type", "status"]
    list_filter = ["printer_id", "type", "status"]

