from rest_framework import mixins, viewsets

from check.models import Check, Printer
from check.serializers import CheckSerializer, PrinterSerializer, CheckCreateSerializer


class CheckViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CheckCreateSerializer
        return CheckSerializer


class PrinterViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
