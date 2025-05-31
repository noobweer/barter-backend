from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .services.ads_services import *


# Create your views here.
@permission_classes([IsAuthenticated])
class CreateAdView(APIView):
    def post(self, request):
        username = request.user.username
        data = request.data

        create_result = AdsService().create_ad(username, data)
        return Response(create_result)


@permission_classes([IsAuthenticated])
class DeleteAdView(APIView):
    def post(self, request):
        username = request.user.username
        data = request.body

        delete_result = AdsService().delete_ad(username, data)
        return Response(delete_result)


@permission_classes([IsAuthenticated])
class EditAdView(APIView):
    def post(self, request):
        username = request.user.username
        data = request.body

        edit_result = AdsService().edit_ad(username, data)
        return Response(edit_result)
