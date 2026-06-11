from django.urls import path, include
from .views import register
from .views import export_excel, export_pdf
from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    EnergyRecordViewSet,
    ChartViewSet
)

router = DefaultRouter()

router.register(
    r'energy',
    EnergyRecordViewSet,
    basename='energy'
)

router.register(
    r'charts',
    ChartViewSet,
    basename='charts'
)

urlpatterns = [
path(
    "register/",
    register
),
    path(
        '',
        include(router.urls)
    ),
    path(
    'export/excel/',
    export_excel
),

path(
    'export/pdf/',
    export_pdf
),
]