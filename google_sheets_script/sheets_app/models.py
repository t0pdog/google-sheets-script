from django.db import models


class Orders(models.Model):
    """
    Model to add to the database
     values from Google spreadsheet:
     №, order №, order value in $ and RUB, delivery time.
    """
    number = models.PositiveSmallIntegerField(
        verbose_name='№', unique=True
        )
    order_number = models.PositiveIntegerField(
        verbose_name='Order №', primary_key=True
        )
    price_usd = models.PositiveIntegerField(
        verbose_name='Price,$'
        )
    price_rub = models.FloatField(
        verbose_name='Price,RUB'
        )
    shipping_date = models.DateTimeField(
        verbose_name='Delivery date'
        )

    def __str__(self) -> str:
        return "Order №" + str(self.order_number)
