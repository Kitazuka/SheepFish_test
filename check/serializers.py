from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from check.models import Printer, Check
from check.tasks import create_pdf_file


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("id", "api_key", "check_type", "point_id")


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ("id", "printer_id", "type", "order", "status", "pdf_file")
        read_only_fields = ("id", "status", "pdf_file")


class CheckCreateSerializer(serializers.ModelSerializer):
    point_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Check
        fields = ["point_id", "type", "order"]

    def create(self, validated_data):
        with transaction.atomic():
            type = validated_data["type"]
            order = validated_data["order"]
            point_id = validated_data["point_id"]
            printers = Printer.objects.filter(
                point_id=point_id, check_type=type
            )

            if printers:
                for printer in printers:
                    check = Check.objects.create(
                        printer_id=printer, type=type, order=order
                    )
                    create_pdf_file.delay(check.id)
            else:
                raise ValidationError(
                    {"error": f"We don't have printers for this check here"}
                )
            return point_id

    def to_representation(self, point_id):
        return {
            "success": f"checks was created for all printer of point №{point_id}"
        }
