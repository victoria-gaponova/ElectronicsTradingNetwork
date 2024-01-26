from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


from trading_object.models import TradingObject
from trading_object.permissions import IsActiveEmployeePermission
from trading_object.serializers import TradingObjectSerializer


class TradingObjectViewSet(viewsets.ModelViewSet):
    """
     ViewSet для модели TradingObject.

     Описание:
     Этот ViewSet предоставляет стандартные CRUD-операции (Create, Read, Update, Delete) для объектов TradingObject
     с использованием модели и сериализатора, определенных выше. Данный класс обеспечивает взаимодействие между API-точками
     и моделью TradingObject, позволяя выполнять различные операции с данными.

     Поля:
     - queryset: Указывает, какие объекты модели TradingObject должны быть доступны в этом ViewSet. Здесь используется
       queryset, возвращающий все объекты модели.
     - serializer_class: Указывает, какой сериализатор использовать для преобразования данных. В данном случае,
       указывается TradingObjectSerializer.
     - permission_classes: Список классов разрешений, определяющих, кто имеет доступ к представлению. В данном случае,
    указывается ваше пользовательское разрешение IsActiveEmployeePermission.
     - filter_backends: Указывает, какие фильтры использовать для фильтрации объектов. В данном случае, используется
       DjangoFilterBackend для поддержки фильтрации по заданным полям.
     - filterset_fields: Указывает поля, по которым можно осуществлять фильтрацию с использованием DjangoFilterBackend.

     Пример использования:
     - GET /trading_object/ - Получить список всех объектов TradingObject.
     - GET /trading_object/1/ - Получить детали объекта TradingObject с идентификатором 1.
     - POST /trading_object/ - Создать новый объект TradingObject.
     - PUT /trading_object/1/ - Обновить объект TradingObject с идентификатором 1.
     - DELETE /trading_object/1/ - Удалить объект TradingObject с идентификатором 1.
     - GET /trading_object/?country=Россия - Получить список объектов TradingObject в России.
    """

    queryset = TradingObject.objects.all()
    serializer_class = TradingObjectSerializer
    permission_classes = [IsActiveEmployeePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]
