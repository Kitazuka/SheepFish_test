from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class CheckCreateSerializer(serializers.ModelSerializer):
    point_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Check
        fields = ["point_id", "type", "order"]

    def create(self, validated_data):
        type = validated_data["type"]
        order = validated_data["order"]
        point_id = validated_data["point_id"]
        printers = Printer.objects.filter(point_id=point_id)

        if printers:
            for printer in printers:
                Check.objects.create(printer_id=printer, type=type, order=order)
        else:
            raise ValidationError({"error": f"incorrect point_id: {point_id}"})

        return point_id

    def to_representation(self, point_id):
        return {"success": f"checks was created for all printer of point №{point_id}"}
