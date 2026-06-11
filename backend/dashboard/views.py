from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import EnergyRecord, Chart
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors
from io import BytesIO
from .serializers import (
    EnergyRecordSerializer,
    ChartSerializer
)
@api_view(["POST"])
def register(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():

        return Response(
            {"error": "User already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response(
        {"message": "User created"}
    )

class EnergyRecordViewSet(ModelViewSet):

    queryset = EnergyRecord.objects.all()
    serializer_class = EnergyRecordSerializer

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

    serializer_class = (
        EnergyRecordSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        chart_id = (
            self.request.query_params.get(
                "chart"
            )
        )

        queryset = (
            EnergyRecord.objects.filter(
                user=self.request.user
            )
        )

        if chart_id:

            queryset = queryset.filter(
                chart_id=chart_id
            )

        return queryset

    def perform_create(
        self,
        serializer
    ):

        serializer.save(
            user=self.request.user
        )


class ChartViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        ChartSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Chart.objects.filter(
            user=self.request.user
        )

    def perform_create(
        self,
        serializer
    ):

        serializer.save(
            user=self.request.user
        )

class ChartViewSet(ModelViewSet):

    serializer_class = ChartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Chart.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )
def export_excel(request):

    wb = Workbook()

    ws = wb.active

    ws.title = "Energy Data"

    ws.append([
        "Month",
        "Consumption",
        "Cost",
        "Peak Load",
        "Efficiency"
    ])

    records = EnergyRecord.objects.all()

    for record in records:

        ws.append([
            record.month,
            record.consumption,
            record.cost,
            record.peak_load,
            record.efficiency
        ])

    response = HttpResponse(
        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="energy.xlsx"'

    wb.save(response)

    return response

def export_pdf(request):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    data = [[
        "Month",
        "Consumption",
        "Cost",
        "Peak",
        "Efficiency"
    ]]

    records = EnergyRecord.objects.all()

    for record in records:

        data.append([
            record.month,
            record.consumption,
            record.cost,
            record.peak_load,
            record.efficiency
        ])

    table = Table(data)

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.whitesmoke
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            )
        ])
    )

    doc.build([table])

    pdf = buffer.getvalue()

    buffer.close()

    response = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="energy.pdf"'

    return response