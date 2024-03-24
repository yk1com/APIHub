import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.core.files.base import ContentFile
from utils.qr_generator import QRCodeManager
from utils.utils import getNow

class GenerateQRCodeView(APIView):
    def post(self, request):
        data = request.data.get('data')
        if not data:
            return Response({"error": "Data field is required"}, status=status.HTTP_400_BAD_REQUEST)

        file_name = f"{getNow()}.png"
        version = request.data.get('version', 1)
        box_size = request.data.get('box_size', 10)
        border = request.data.get('border', 4)

        # Ensure media directory exists
        media_dir = os.path.join(settings.BASE_DIR, 'media')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        qr_manager = QRCodeManager(media_dir)
        qr_manager.create_qr_code(
            data,
            file_name=file_name,
            version=version,
            box_size=box_size,
            border=border
        )

        # Get the file path
        file_path = os.path.join(media_dir, file_name)
        download_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)

        return Response({"message": f"QR code generated. Download from: {download_url}", "download_link":download_url}, status=status.HTTP_201_CREATED)

class ReadQRCodeView(APIView):
    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "Image file is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure media directory exists
        media_dir = os.path.join(settings.BASE_DIR, 'media')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Save the uploaded image
        image_path = os.path.join(media_dir, image_file.name)
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        qr_manager = QRCodeManager(media_dir)
        qr_data = qr_manager.read_qr_code(image_path)

        return Response({"qr_data": qr_data}, status=status.HTTP_200_OK)

