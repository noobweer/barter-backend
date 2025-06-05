from rest_framework.decorators import permission_classes
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .services.ads_service import *
from .serializers import AdSerializer, ExchangeSerializer, CategorySerializer, ConditionSerializer
from .services.exchanges_service import *
from .services.helper_service import *


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
        data = request.data

        delete_result = AdsService().delete_ad(username, data)
        return Response(delete_result)


@permission_classes([IsAuthenticated])
class EditAdView(APIView):
    def post(self, request):
        username = request.user.username
        data = request.data

        edit_result = AdsService().edit_ad(username, data)
        return Response(edit_result)


class AdsCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'created_at'
    cursor_query_param = 'cursor'


@permission_classes([IsAuthenticated])
class AdsView(APIView):
    pagination_class = AdsCursorPagination

    def post(self, request):
        username = request.user.username
        data = request.data
        ads_result = AdsService().all_ads(data)

        if isinstance(ads_result, int):
            return Response({'error': 'Invalid filters'}, status=ads_result)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(ads_result, request, view=self)
        serialized_data = AdSerializer(result_page, many=True).data

        return paginator.get_paginated_response(serialized_data)


@permission_classes([IsAuthenticated])
class CreateExchangeView(APIView):
    def post(self, request):
        data = request.data

        create_result = ExchangeService().create_exchange(data)
        return Response(create_result)


@permission_classes([IsAuthenticated])
class EditExchangeView(APIView):
    def post(self, request):
        username = request.user.username
        data = request.data

        edit_result = ExchangeService().edit_exchange(username, data)
        return Response(edit_result)


@permission_classes([IsAuthenticated])
class ExchangesView(APIView):

    def post(self, request):
        data = request.data
        exchanges_result = ExchangeService().all_exchanges(data)

        if isinstance(exchanges_result, int):
            return Response({'error': 'Invalid filters'}, status=exchanges_result)

        serialized_data = ExchangeSerializer(exchanges_result, many=True).data

        return Response(serialized_data)


# Planned to expand the data provided about the user
@permission_classes([IsAuthenticated])
class UserInfoView(APIView):
    def get(self, request):
        username = request.user.username
        return Response({"account": username})


@permission_classes([IsAuthenticated])
class CategoriesView(APIView):
    def get(self, request):
        categories = HelperService().get_categories()
        serialized_data = CategorySerializer(categories, many=True).data
        return Response(serialized_data)


@permission_classes([IsAuthenticated])
class ConditionsView(APIView):
    def get(self, request):
        conditions = HelperService().get_conditions()
        serialized_data = CategorySerializer(conditions, many=True).data
        return Response(serialized_data)
