from django.contrib import admin

from .models import Client, Security, Investment, Deposit, QuoteHistory

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'security', 'deposit', 'amount', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('client__name', 'security__code')


admin.site.register(Client)
admin.site.register(Security)
admin.site.register(Deposit)
admin.site.register(QuoteHistory)
