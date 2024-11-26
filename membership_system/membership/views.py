from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MemberData, ExpenseData, MembershipData, PaymentData
from .serializers import MemberDataSerializer, ExpenseDataSerializer, MembershipDataSerializer, PaymentDataSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db import models


class MemberDataViewSet(viewsets.ModelViewSet):
    queryset = MemberData.objects.all()
    serializer_class = MemberDataSerializer
    permission_classes = [IsAuthenticated]


class TotalMembersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_members = MemberData.objects.count()
        return Response({'total_members': total_members})


class ActiveMembersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        active_members = MemberData.objects.filter(status='active').count()
        return Response({'active_members': active_members})


class TotalExpensesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_expenses = ExpenseData.objects.aggregate(total_expenses=models.Sum('amount'))['total_expenses']
        return Response({'total_expenses': total_expenses})


class IncomeExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        period = request.query_params.get('period', 'monthly')  # monthly, yearly, weekly
        today = timezone.now()

        if period == 'monthly':
            start_date = today.replace(day=1)
            end_date = today.replace(day=28) + timedelta(days=4)  # Just go to next month

        elif period == 'yearly':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(year=today.year + 1, month=1, day=1)

        elif period == 'weekly':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=7)

        else:
            start_date = today
            end_date = today

        income = PaymentData.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).aggregate(total_income=Sum('amount'))['total_income'] or 0
        expenses = ExpenseData.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

        return Response({'income': income, 'expenses': expenses, 'profit_loss': income - expenses})


class LeftMembersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        left_members = MemberData.objects.filter(status='left').count()
        return Response({'left_members': left_members})


class TotalRevenueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_revenue = PaymentData.objects.aggregate(total_revenue=models.Sum('amount'))['total_revenue']
        return Response({'total_revenue': total_revenue})


class ExpenseDataViewSet(viewsets.ModelViewSet):
    queryset = ExpenseData.objects.all()
    serializer_class = ExpenseDataSerializer
    permission_classes = [IsAuthenticated]


class MembershipCountsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        membership_counts = {}
        memberships = MembershipData.objects.all()

        for membership in memberships:
            membership_counts[membership.name] = MemberData.objects.filter(membership=membership.name).count()

        return Response(membership_counts)

class MonthlyIncomeExpenseProfitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        months = PaymentData.objects.values('payment_date__year', 'payment_date__month').distinct()
        results = []

        for month in months:
            start_date = timezone.datetime(month['payment_date__year'], month['payment_date__month'], 1)
            end_date = start_date + timedelta(days=31)  # Next month
            end_date = end_date.replace(day=1)  # Reset to first day of next month

            income = PaymentData.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).aggregate(total_income=Sum('amount'))['total_income'] or 0
            expenses = ExpenseData.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

            results.append({
                'from': start_date,
                'to': end_date,
                'income': income,
                'expense': expenses,
                'profit_loss': income - expenses,
            })

        return Response(results)


class MembershipDataViewSet(viewsets.ModelViewSet):
    queryset = MembershipData.objects.all()
    serializer_class = MembershipDataSerializer
    permission_classes = [IsAuthenticated]


class PaymentDataViewSet(viewsets.ModelViewSet):
    queryset = PaymentData.objects.all()
    serializer_class = PaymentDataSerializer
    permission_classes = [IsAuthenticated]


class TokenRefreshViewWithAdminPermission(TokenRefreshView):
    permission_classes = [IsAuthenticated]


class CustomLogin(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Issue JWT token for authenticated user
                from rest_framework_simplejwt.tokens import RefreshToken
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials.'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        

class AuthenticationCheckAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'You are authenticated!'})