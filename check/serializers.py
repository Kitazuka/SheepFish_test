from rest_framework import serializers

from check.models import Printer, Check


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("id", "api_key", "check_type", "point_id")


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ("id", "printer_id", "type", "order", "status", "pdf_file")
        read_only_fields = ("id", "status", "pdf_file")
