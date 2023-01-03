from django.shortcuts import render
from rest_framework import mixins, viewsets

from check.models import Check, Printer
from check.serializers import CheckSerializer, PrinterSerializer


class CheckViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer


class PrinterViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
