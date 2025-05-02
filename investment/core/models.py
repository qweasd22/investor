from django.db import models
from django.core.exceptions import ValidationError

class Client(models.Model):
    
    
    OWNERSHIP_TYPES = (
        ('ООО', 'Общество с ограниченной ответственностью'),
        ('ИП', 'Индивидуальный предприниматель'),
        ('АО', 'Акционерное общество'),
    )
    
    name = models.CharField('Название', max_length=255)
    ownership_type = models.CharField(
        'Тип собственности', 
        max_length=50, 
        choices=OWNERSHIP_TYPES
    )
    address = models.TextField('Адрес')
    phone = models.CharField('Телефон', max_length=20)
    
    def __str__(self):
        return f"{self.name} ({self.ownership_type})"

class Security(models.Model):
    SECURITY_TYPES = (
        ('stock', 'Акция'),
        ('bond', 'Облигация'),
        ('etf', 'ETF'),
        ('other', 'Другое'),
    )
    
    code = models.CharField('Код', max_length=50, unique=True)
    name = models.CharField('Название', max_length=200)
    security_type = models.CharField('Тип', max_length=20, choices=SECURITY_TYPES)
    min_amount = models.DecimalField('Мин. сумма', max_digits=15, decimal_places=2)
    rating = models.PositiveIntegerField('Рейтинг')
    last_year_yield = models.DecimalField('Доходность (%)', max_digits=5, decimal_places=2)
    issuer = models.CharField('Эмитент', max_length=200)
    currency = models.CharField('Валюта', max_length=3, default='RUB')

    def clean(self):
        if self.rating < 1 or self.rating > 10:
            raise ValidationError("Рейтинг должен быть от 1 до 10")
        if self.min_amount < 0:
            raise ValidationError("Минимальная сумма не может быть отрицательной")

    def __str__(self):
        return f"{self.code} ({self.name})"

class QuoteHistory(models.Model):
    security = models.ForeignKey(
        'Security', 
        on_delete=models.CASCADE, 
        related_name='quotes'
    )
    quote = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    date = models.DateField('Дата')

    class Meta:
        ordering = ['-date']
        verbose_name = 'История котировок'
        verbose_name_plural = 'История котировок'

    def __str__(self):
        return f"{self.security.code} - {self.quote} ({self.date})"
    def get_change(self):
        prev_quote = QuoteHistory.objects.filter(
            security=self.security,
            date__lt=self.date
        ).order_by('-date').first()
        
        if prev_quote and prev_quote.quote != 0:
            change = ((self.quote - prev_quote.quote) / prev_quote.quote) * 100
            return round(change, 2)
        return None

from decimal import Decimal
class Deposit(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2
    )
    interest_rate = models.DecimalField(
        'Процентная ставка',
        max_digits=5, 
        decimal_places=2
    )
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')

    def __str__(self):
        return f"Депозит {self.client.name} ({self.amount})"
    @property
    def get_profit(self):
        """Расчет прибыли с использованием Decimal"""
        days = Decimal((self.end_date - self.start_date).days)
        rate = self.interest_rate / Decimal(100)
        return self.amount * rate * (days / Decimal(365))
    
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("Дата окончания должна быть позже даты начала")
        if self.interest_rate < 1 or self.interest_rate > 20:
            raise ValidationError("Процентная ставка должна быть в диапазоне 1-20%")

class Investment(models.Model):
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    security = models.ForeignKey(
        'Security',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Ценная бумага'
    )
    deposit = models.ForeignKey(
        'Deposit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Депозит'
    )
    amount = models.DecimalField(
        'Сумма инвестиции',
        max_digits=15,
        decimal_places=2
    )
    purchase_date = models.DateField('Дата покупки')
    sale_date = models.DateField(
        'Дата продажи',
        null=True,
        blank=True
    )

    def clean(self):
        # Используем атрибуты объекта, а не cleaned_data
        if self.security and self.deposit:
            raise ValidationError("Нельзя выбрать оба актива одновременно")

        if not (self.security or self.deposit):
            raise ValidationError("Выберите ценную бумагу или депозит")

        if self.sale_date and self.sale_date < self.purchase_date:
            raise ValidationError("Дата продажи не может быть раньше покупки")

        if self.security and self.amount < self.security.min_amount:
            raise ValidationError(
                f"Минимальная сумма для {self.security.code}: {self.security.min_amount}"
            )

    def __str__(self):
        return f"Инвестиция {self.client.name} ({self.amount})"