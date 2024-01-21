from django.db import models

NULLABLE = {"blank": True, "null": True}


class TradingNetworkObject(models.Model):
    """
       Модель, представляющая объект торговой сети.

       Поля:
       - name: Название объекта торговой сети
       - type_trade_object: Тип торгового объекта (фабрика, розничная сеть, индивидуальный предприниматель)
       - email: Электронная почта объекта торговой сети (уникальное значение)
       - country: Страна объекта торговой сети
       - city: Город объекта торговой сети
       - street: Улица объекта торговой сети
       - house_number: Номер дома объекта торговой сети
       - supplier: Ссылка на другой объект торговой сети, который является поставщиком (может быть NULL)
       - dept: Задолженность перед поставщиком (число с фиксированной точностью)
       - created_at: Время создания объекта торговой сети (автоматически устанавливается при создании)

       Методы:
       - __str__: Метод, возвращающий строковое представление объекта торговой сети (название объекта торговой сети).
       - trade_object_level: Свойство, возвращающее уровень иерархии объекта торговой сети.

       Константы:
       - FACTORY: Константа, представляющая уровень фабрики (0).
       - RETAIL_CHAIN: Константа, представляющая уровень розничной сети (1).
       - INDIVIDUAL_ENTREPRENEUR: Константа, представляющая уровень индивидуального предпринимателя (2).
   """

    FACTORY = 0
    RETAIL_CHAIN = 1
    INDIVIDUAL_ENTREPRENEUR = 2

    TRADE_OBJECT_CHOICES = (
        (FACTORY, 'Factory'),
        (RETAIL_CHAIN, 'Retail chain'),
        (INDIVIDUAL_ENTREPRENEUR, 'Individual entrepreneur'),
    )
    name = models.CharField(max_length=250, verbose_name='Название объекта торговой сети')
    type_trade_object = models.IntegerField(
        choices=TRADE_OBJECT_CHOICES,
        verbose_name='Тип торгового объекта',
    )
    email = models.EmailField(unique=True, verbose_name='Электронная почта объекта торговой сети')
    country = models.CharField(max_length=150, verbose_name='Страна объекта торговой сети')
    city = models.CharField(max_length=150, verbose_name='Город объекта торговой сети')
    street = models.CharField(max_length=150, verbose_name='Улица объекта торговой сети')
    house_number = models.CharField(max_length=20, verbose_name='Номер дома объекта торговой сети')
    supplier = models.ForeignKey('self', **NULLABLE, on_delete=models.SET_NULL, related_name='clients',
                                 verbose_name='Поставщик')
    dept = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Задолженность перед поставщиком')
    created_at = models.TimeField(auto_now_add=True, verbose_name='Время создания объекта торговой сети')

    def __str__(self):
        return self.name

    @property
    def trade_object_level(self):
        """
                Определяет и возвращает уровень иерархии объекта торговой сети.

                Returns:
                    int: Уровень иерархии объекта торговой сети.
                """
        # Завод всегда находится на 0 уровне
        if self.type_trade_object == self.FACTORY:
            return 0

        # Если поставщик не указан, уровень торгового объекта максимальный из возможных
        if not self.supplier:
            return max(self.RETAIL_CHAIN, self.INDIVIDUAL_ENTREPRENEUR)
        # Уровень торгового объекта определяется в зависимости от поставщика
        return self.supplier.trade_object_level + 1


class Product(models.Model):
    """
       Модель, представляющая продукт.

       Поля:
       - name: Название продукта
       - model: Модель продукта
       - release_date: Дата выхода на рынок (автоматически устанавливается при создании)
       - seller: Ссылка на объект торговой сети, который является продавцом (при удалении продавца, все связанные продукты удаляются)

       Методы:
          __str__: Метод, возвращающий строковое представление продукта (название продукта).
       """

    name = models.CharField(max_length=250, verbose_name='Название продукта')
    model = models.CharField(max_length=150, verbose_name='Модель продукта')
    release_date = models.DateField(auto_now_add=True, verbose_name='Дата выхода на рынок')
    seller = models.ForeignKey(TradingNetworkObject, on_delete=models.CASCADE, related_name='products',
                               verbose_name='Продавец')

    def __str__(self):
        return self.name
