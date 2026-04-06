import django_filters
from .models import Transaction
from django import forms


class TransactionFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(widget=forms.DateTimeInput(attrs={'type': 'date'}), field_name='date', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(widget=forms.DateTimeInput(attrs={'type': 'date'}), field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['type_of', 'category', 'start_date', 'end_date']