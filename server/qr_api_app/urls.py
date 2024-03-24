# qr_api_app/urls.py
from django.urls import path
from .views import GenerateQRCodeView, ReadQRCodeView

urlpatterns = [
    path('generate/', GenerateQRCodeView.as_view(), name='generate'),
    path('read/', ReadQRCodeView.as_view(), name='read'),
]
