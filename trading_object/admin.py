from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from trading_object.models import TradingObject, Product


@admin.action(description="Очищение задолженности перед поставщиком")
def debt_clearing(modeladmin, request, queryset):
    """
    Кастомное действие администратора для обнуления задолженности поставщика у выбранных объектов торговой сети.

    Args:
        modeladmin: Экземпляр администратора модели.
        request: Запрос HTTP.
        queryset: Выборка объектов для применения действия.
    """
    # Обновление задолженности для выбранных объектов в queryset, устанавливая значение в 0
    queryset.update(debt=0)


@admin.register(TradingObject)
class TradingObjectAdmin(admin.ModelAdmin):
    """
    Администраторская панель для управления объектами торговой сети.

    Отображает основные атрибуты объекта, позволяет фильтровать по городу,
    выполнять поиск по названию и стране, а также предоставляет возможность
    обнулить задолженность перед поставщиком для выбранных объектов.

    Отображаемые поля:
        - name: Название объекта торговой сети
        - type_trading_object: Тип торгового объекта
        - country: Страна объекта торговой сети
        - city: Город объекта торговой сети
        - street: Улица объекта торговой сети
        - house_number: Номер дома объекта торговой сети
        - supplier: Поставщик (ссылка на другой объект торговой сети)
        - debt: Задолженность перед поставщиком
        - created_at: Время создания объекта торговой сети
     Доступные фильтры:
         - 'city': Фильтрация по городу
     Поля для поиска:
         - 'name': Поиск по названию объекта торговой сети
         - 'country': Поиск по стране

    Доступные действия:
        - debt_clearing: Обнулить задолженность перед поставщиком для выбранных объектов.
    """

    list_display = (
        "name",
        "type_trading_object",
        "country",
        "city",
        "street",
        "house_number",
        "supplier_link",
        "debt",
        "created_at",
    )
    list_filter = ("city",)
    search_fields = ("name", "country")
    actions = [debt_clearing]

    def supplier_link(self, obj):
        """
        Метод для создания ссылки на страницу "Поставщика".

        Args:
            obj: Экземпляр объекта торговой сети.

        Returns:
            str: HTML-код для отображения ссылки.
        """
        if obj.supplier:
            url = reverse(
                "admin:trading_object_tradingobject_change", args=[obj.supplier.id]
            )
            return format_html('<a href="{}">{}</a>', url, obj.supplier)
        return "-"

    supplier_link.short_description = "Поставщик"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Администраторская панель для управления товарами.

    Отображает основные атрибуты товара, такие как название, модель,
    дату выпуска и продавца. Предоставляет возможность фильтрации по
    продавцу и поиска по названию и модели товара.

    Отображаемые поля:
        - name: Название товара
        - model: Модель товара
        - release_date: Дата выпуска товара
        - seller: Продавец товара

    Доступные фильтры:
        - 'seller': Фильтрация по продавцу

    Поля для поиска:
        - 'name': Поиск по названию товара
        - 'model': Поиск по модели товара
    """

    list_display = ("name", "model", "release_date", "seller")
    list_filter = ("seller",)
    search_fields = ("name", "model")
