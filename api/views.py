from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TransactionFilter
from .models import User, Transaction
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    TransactionSerializer,
    DashboardSerializer,
)
from .permissions import IsAdmin, IsAnalystOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    search_fields = ['notes', 'category']

    def get_queryset(self):
        user = self.request.user
        target_user_id = self.request.query_params.get('user_id')

        if user.role == User.Role.VIEWER:
            return Transaction.objects.filter(user=user, is_deleted=False)

        if target_user_id:
            return Transaction.objects.filter(user_id=target_user_id, is_deleted=False)
        return Transaction.objects.filter(is_deleted=False)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAnalystOrAdmin()]
        return [IsAuthenticated(), IsAdmin()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        target_user_id = self.request.query_params.get('user_id')

        if user.role == User.Role.VIEWER:
            transactions = Transaction.objects.filter(user=user, is_deleted=False)
        else:
            if target_user_id:
                transactions = Transaction.objects.filter(user_id=target_user_id, is_deleted=False)
            else:
                transactions = Transaction.objects.filter(is_deleted=False)

        total_income = transactions.filter(
            type_of=Transaction.Type.INCOME
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expenses = transactions.filter(
            type_of=Transaction.Type.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or 0

        net_balance = total_income - total_expenses

        category_totals = {}
        categories = transactions.values('category').annotate(
            total=Sum('amount')
        )
        for entry in categories:
            category_totals[entry['category']] = entry['total']

        recent = transactions.order_by('-created_at')[:5]

        monthly_trends = (
            transactions
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(
                income=Sum('amount', filter=Q(type_of=Transaction.Type.INCOME)),
                expenses=Sum('amount', filter=Q(type_of=Transaction.Type.EXPENSE)),
            )
            .order_by('-month')[:6]
        )

        trends = []
        for entry in monthly_trends:
            trends.append({
                'month': entry['month'].strftime('%Y-%m'),
                'income': entry['income'] or 0,
                'expenses': entry['expenses'] or 0,
            })

        data = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'category_totals': category_totals,
            'recent_transactions': TransactionSerializer(recent, many=True).data,
            'monthly_trends': trends
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)