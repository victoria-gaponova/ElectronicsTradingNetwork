from rest_framework import serializers

from trading_object.models import TradingObject


class TradingObjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели TradingObject.

    Описание:
    Этот сериализатор используется для преобразования объектов модели TradingObject в JSON и наоборот.
    Он наследуется от ModelSerializer, что упрощает создание сериализатора для модели Django.

    Поля:
    - model: Указывает, что сериализатор должен использовать модель TradingObject.
    - fields: Включает все поля модели в сериализатор. Может быть настроено вручную, но здесь используется '__all__'.
    - read_only_fields: Указывает, что поле 'debt' должно быть доступно только для чтения при создании или обновлении объекта.
    """

    class Meta:
        model = TradingObject
        fields = "__all__"
        read_only_fields = [
            "debt",
        ]
