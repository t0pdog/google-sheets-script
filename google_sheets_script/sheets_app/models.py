from django.db import models


class Orders(models.Model):
    """
    Модель для добавления в базу данных
    значений из Google таблицы:
    №, № заказа, стоимость заказа в $ и в Руб, срок поставки.
    """
    number = models.PositiveSmallIntegerField(
        verbose_name='№', unique=True
        )
    order_number = models.PositiveIntegerField(
        verbose_name='заказ №', primary_key=True
        )
    price_usd = models.PositiveIntegerField(
        verbose_name='стоимость,$'
        )
    price_rub = models.FloatField(
        verbose_name='стоимость,руб'
        )
    shipping_date = models.DateTimeField(
        verbose_name='срок поставки'
        )

    def __str__(self) -> str:
        return "Номер заказа" + str(self.order_number)
