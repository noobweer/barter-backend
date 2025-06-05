from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
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
@extend_schema(
    tags=["Объявления"],
    summary="Создание объявления",
    description="Создает новое объявление от имени авторизованного пользователя.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "example": "iPhone 13"},
                "description": {"type": "string", "example": "Хорошее состояние"},
                "category": {"type": "string", "example": "Техника"},
                "condition": {"type": "string", "example": "Б/у"}
            },
            "required": ["title", "description", "category", "condition"]
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "is_created": {"type": "boolean"},
                "message": {"type": "string"}
            }
        },
        400: {"description": "Ошибка валидации или данных"}
    },
    examples=[
        OpenApiExample(
            "Успешное создание",
            value={
                "is_created": True,
                "message": "Объявление успешно создано"
            },
            response_only=True
        ),
        OpenApiExample(
            "Ошибка ввода",
            value={
                "is_created": False,
                "message": "Некорректная категория"
            },
            response_only=True
        )
    ]
)
@permission_classes([IsAuthenticated])
class CreateAdView(APIView):
    def post(self, request):
        username = request.user.username
        data = request.data

        create_result = AdsService().create_ad(username, data)
        return Response(create_result)


@extend_schema(
    tags=["Объявления"],
    summary="Удаление объявления",
    description="Удаляет объявление по ID, если оно принадлежит пользователю.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "ad_id": {"type": "integer", "example": 123}
            },
            "required": ["ad_id"]
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "is_deleted": {"type": "boolean"},
                "message": {"type": "string"}
            }
        },
        400: {"description": "Некорректный ID или объявление не принадлежит пользователю"}
    },
    examples=[
        OpenApiExample(
            "Успех",
            value={"is_deleted": True, "message": "Объявление удалено"},
            response_only=True
        ),
        OpenApiExample(
            "Ошибка удаления",
            value={"is_deleted": False, "message": "Объявление не найдено"},
            response_only=True
        )
    ]
)
@permission_classes([IsAuthenticated])
class DeleteAdView(APIView):
    def post(self, request):
        username = request.user.username
        data = request.data

        delete_result = AdsService().delete_ad(username, data)
        return Response(delete_result)


@extend_schema(
    tags=["Объявления"],
    summary="Редактирование объявления",
    description="Изменяет заголовок, описание, категорию и состояние объявления, если оно принадлежит пользователю.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "ad_id": {"type": "integer", "example": 123},
                "title": {"type": "string", "example": "iPhone 13 (обновлённый)"},
                "description": {"type": "string", "example": "Полностью рабочий"},
                "category": {"type": "string", "example": "Электроника"},
                "condition": {"type": "string", "example": "Новое"}
            },
            "required": ["ad_id", "title", "description", "category", "condition"]
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "is_edited": {"type": "boolean"},
                "message": {"type": "string"}
            }
        },
        400: {"description": "Ошибка валидации или прав доступа"}
    },
    examples=[
        OpenApiExample(
            "Успех",
            value={"is_edited": True, "message": "Объявление обновлено"},
            response_only=True
        ),
        OpenApiExample(
            "Ошибка редактирования",
            value={"is_edited": False, "message": "Объявление не найдено"},
            response_only=True
        )
    ]
)
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


@extend_schema(
    tags=["Объявления"],
    summary="Получение объявлений с фильтрацией",
    description="Возвращает список объявлений с возможностью фильтрации по ключевому слову, категории и состоянию.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Ключевое слово для поиска в заголовке или описании",
                    "example": "телефон"
                },
                "category": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Список категорий для фильтрации",
                    "example": ["Техника", "Часы"]
                },
                "condition": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Список состояний товара для фильтрации",
                    "example": ["Новое", "Б/у"]
                }
            },
            "required": {}
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "next": {"type": "string", "nullable": True},
                "previous": {"type": "string", "nullable": True},
                "results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "number"},
                            "user": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "category": {"type": "object", "properties": {"name": {"type": "string"}}},
                            "condition": {"type": "object", "properties": {"name": {"type": "string"}}}
                        }
                    }
                }
            },
        },
        400: {"description": "Ошибка фильтрации или неверные параметры"}
    },
    examples=[
        OpenApiExample(
            "Пример успешного ответа",
            value={
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "user": "admin",
                        "title": "iPhone 13",
                        "description": "Отличное состояние",
                        "category": {"name": "Техника"},
                        "condition": {"name": "Б/у"}
                    }
                ]
            },
            response_only=True
        )
    ]
)
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


@extend_schema(
    tags=["Обмены"],
    summary="Создание предложения обмена",
    description="Создает новое предложение обмена между двумя объявлениями.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "ad_sender_id": {"type": "integer", "example": 123},
                "ad_receiver_id": {"type": "integer", "example": 456},
                "comment": {"type": "string", "example": "Хочу обменять ваше объявление на моё", "required": False}
            },
            "required": ["ad_sender_id", "ad_receiver_id"]
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "is_created": {"type": "boolean"},
                "message": {"type": "string"}
            }
        },
        400: {"description": "Ошибка создания предложения обмена"}
    },
    examples=[
        OpenApiExample(
            "Успешное создание",
            value={"is_created": True, "message": "Предложение создано успешно"},
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            "Ошибка создания",
            value={"is_created": False, "message": "Неверный ad_sender_id"},
            response_only=True,
            status_codes=["400"]
        )
    ]
)
@permission_classes([IsAuthenticated])
class CreateExchangeView(APIView):
    def post(self, request):
        data = request.data

        create_result = ExchangeService().create_exchange(data)
        return Response(create_result)


@extend_schema(
    tags=["Обмены"],
    summary="Редактирование статуса предложения обмена",
    description="Изменяет статус предложения обмена (например, принимает или отклоняет обмен).",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "exchange_id": {"type": "integer", "example": 789},
                "status": {"type": "string", "enum": ["pending", "accepted", "declined", "Ожидает", "Принято", "Отклонено"], "example": "accepted"}
            },
            "required": ["exchange_id", "status"]
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "is_edited": {"type": "boolean"},
                "message": {"type": "string"}
            }
        },
        400: {"description": "Ошибка редактирования предложения обмена"}
    },
    examples=[
        OpenApiExample(
            "Успех",
            value={"is_edited": True, "message": "Статус предложения обмена успешно изменен"},
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            "Ошибка редактирования",
            value={"is_edited": False, "message": "Неверный exchange_id"},
            response_only=True,
            status_codes=["400"]
        )
    ]
)
@permission_classes([IsAuthenticated])
class EditExchangeView(APIView):
    def post(self, request):
        username = request.user.username
        data = request.data

        edit_result = ExchangeService().edit_exchange(username, data)
        return Response(edit_result)


@extend_schema(
    tags=["Обмены"],
    summary="Получение списка предложений обмена",
    description="Возвращает список всех предложений обмена с возможностью фильтрации по отправителю, получателю и статусу.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "sender_username": {"type": "string", "example": "user1"},
                "receiver_username": {"type": "string", "example": "user2"},
                "status": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["pending", "accepted", "declined", "Ожидает", "Принято", "Отклонено"]},
                    "example": ["accepted", "declined"]
                }
            }
        }
    },
)
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
@extend_schema(
    tags=["Пользователь"],
    summary="Информация о текущем пользователе",
    description="Возвращает имя авторизованного пользователя.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "account": {"type": "string", "example": "admin"}
            }
        }
    },
    examples=[
        OpenApiExample(
            "Успешный ответ",
            value={"account": "admin"},
            response_only=True,
            status_codes=["200"]
        )
    ]
)
@permission_classes([IsAuthenticated])
class UserInfoView(APIView):
    def get(self, request):
        username = request.user.username
        return Response({"account": username})


@extend_schema(
    tags=["Справочники"],
    summary="Получение всех категорий",
    description="Возвращает список всех доступных категорий товаров.",
    responses=CategorySerializer(many=True),
    examples=[
        OpenApiExample(
            "Пример ответа",
            value={"id": 1, "name": "Техника"},
            response_only=True,
            status_codes=["200"]
        )
    ]
)
@permission_classes([IsAuthenticated])
class CategoriesView(APIView):
    def get(self, request):
        categories = HelperService().get_categories()
        serialized_data = CategorySerializer(categories, many=True).data
        return Response(serialized_data)


@extend_schema(
    tags=["Справочники"],
    summary="Получение всех состояний товара",
    description="Возвращает список всех возможных состояний товара (например, 'Новое', 'Б/у').",
    responses=ConditionSerializer(many=True),
    examples=[
        OpenApiExample(
            "Пример ответа",
            value={"id": 1, "name": "Новое"},
            response_only=True,
            status_codes=["200"]
        )
    ]
)
@permission_classes([IsAuthenticated])
class ConditionsView(APIView):
    def get(self, request):
        conditions = HelperService().get_conditions()
        serialized_data = CategorySerializer(conditions, many=True).data
        return Response(serialized_data)
