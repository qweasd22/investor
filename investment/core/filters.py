import django_filters
from .models import Security, Investment, Client, Deposit
from django.db.models import Q
class SecurityFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Поиск')
    min_yield = django_filters.NumberFilter(field_name='last_year_yield', lookup_expr='gte')
    
    class Meta:
        model = Security
        fields = ['security_type', 'rating']

    def filter_search(self, queryset, name, value):
    
        return queryset.filter(
            Q(code__icontains=value) | 
            Q(issuer__icontains=value)
        ).distinct()

class InvestmentFilter(django_filters.FilterSet):
    client = django_filters.CharFilter(field_name='client__name', lookup_expr='icontains')
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    
    class Meta:
        model = Investment
        fields = ['client', 'security', 'deposit']



# filters.py
class DepositFilter(django_filters.FilterSet):
    client = django_filters.ModelChoiceFilter(queryset=Client.objects.all())
    
    class Meta:
        model = Deposit
        fields = ['client', 'interest_rate']