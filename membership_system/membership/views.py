from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .CustomPagination import CustomPageNumberPagination
from .models import (
                     GymMember,
                     Membership,
                     GymIncomeExpense,
                     GymInout,
                     GymAttendance,
                     )
from .serializers import (
                          GymMemberSerializer,
                          MembershipSerializer,
                          GymIncomeExpenseSerializer,
                          GymInoutSerializer,
                          GymAttendanceSerializer,
                          )
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from .filters import (
                      GymMemberFilter,
                      MembershipFilter,
                      GymInoutFilter,
                      GymAttendanceFilter,
                      GymIncomeExpenseFilter,
                      )
from django.db.models import FloatField, F, Q, Value
from django.db.models.functions import ExtractMonth, ExtractYear, Coalesce


class MemberDataViewSet(viewsets.ModelViewSet):
    queryset = GymMember.objects.filter(role_name__iexact='member')
    serializer_class = GymMemberSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GymMemberFilter
    
    def list(self, request, *args, **kwargs):
        query_type = self.request.query_params.get('query', None)

        if query_type == 'total-members':
            total_members = GymMember.objects.filter(role_name__iexact='member').count()
            return Response({'total_members': total_members}, status=200)
        
        elif query_type == 'active-members':
            active_members = GymMember.objects.filter(role_name__iexact='member', membership_status__iexact='continue').count()
            return Response({'active_members': active_members}, status=200)

        return super().list(request, *args, **kwargs)


class MemberShipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MembershipFilter


class GymIncomeExpenseViewSet(viewsets.ModelViewSet):
    queryset = GymIncomeExpense.objects.all()
    serializer_class = GymIncomeExpenseSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GymIncomeExpenseFilter

    def list(self, request, *args, **kwargs):
        query_type = self.request.query_params.get('query', None)

        if query_type == 'total-revenue':
            total_revenue = self.queryset.filter(invoice_type='income').aggregate(
                total=Sum('total_amount', output_field=FloatField())
            )
            return Response({'total_revenue': total_revenue['total'] or 0}, status=200)
        
        elif query_type == 'invoice-type-income':
            invoice_type_income = self.queryset.filter(invoice_type__iexact='income')
            paginated_data = self.paginate_queryset(invoice_type_income)
            if paginated_data is not None:
                serializer = self.get_serializer(paginated_data, many=True)
                return self.get_paginated_response(serializer.data)

        elif query_type == 'invoice-type-expense':
            invoice_type_expense = self.queryset.filter(invoice_type__iexact='expense')
            paginated_data = self.paginate_queryset(invoice_type_expense)
            if paginated_data is not None:
                serializer = self.get_serializer(paginated_data, many=True)
                return self.get_paginated_response(serializer.data)

        elif query_type == 'total-expenses':
            total_expenses = self.queryset.filter(invoice_type='expense').aggregate(
                total=Sum('total_amount', output_field=FloatField())
            )
            return Response({'total_expenses': total_expenses['total'] or 0}, status=200)
        
        elif query_type == 'income-expense':
            total_revenue = self.queryset.filter(invoice_type='income').aggregate(
                total=Sum('total_amount', output_field=FloatField())
            )
            total_expenses = self.queryset.filter(invoice_type='expense').aggregate(
                total=Sum('total_amount', output_field=FloatField())
            )
            return Response({
                'total_revenue': total_revenue['total'] or 0,
                'total_expenses': total_expenses['total'] or 0
            }, status=200)

        elif query_type == 'monthly-income-expense-profit':
            # Query with separate year and month annotations
            monthly_data = (
                self.queryset.annotate(
                    year=ExtractYear('invoice_date'),  # Extract year
                    month=ExtractMonth('invoice_date')  # Extract month
                )
                .values('year', 'month')
                .annotate(
                    total_revenue=Coalesce(
                        Sum(
                            'total_amount',
                            filter=Q(invoice_type='income'),
                            output_field=FloatField()
                        ),
                        Value(0),  # Replace NULL with 0
                        output_field=FloatField()
                    ),
                    total_expenses=Coalesce(
                        Sum(
                            'total_amount',
                            filter=Q(invoice_type='expense'),
                            output_field=FloatField()
                        ),
                        Value(0),  # Replace NULL with 0
                        output_field=FloatField()
                    ),
                )
                .annotate(
                    profit=F('total_revenue') - F('total_expenses')
                )
                .order_by('-year', '-month')  # Order by most recent year and month
            )
            # Apply pagination
            paginator = self.pagination_class()
            paginated_data = paginator.paginate_queryset(list(monthly_data), request, view=self)

            # Return paginated response
            return paginator.get_paginated_response({'monthly_data': paginated_data})
        # Default behavior
        return super().list(request, *args, **kwargs)


class GymInoutViewSet(viewsets.ModelViewSet):
    queryset = GymInout.objects.all()
    serializer_class = GymInoutSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GymInoutFilter


class GymAttendanceViewSet(viewsets.ModelViewSet):
    queryset = GymAttendance.objects.all()
    serializer_class = GymAttendanceSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GymAttendanceFilter


# Global in-memory store to hold the current finger mode and member ID
current_finger_mode = None
current_member_id = None


class FingerModeView(APIView):
    """
    A class to handle getting and setting finger mode for fingerprint operations.
    This stores the mode temporarily without using session IDs.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """Endpoint to get the current finger mode."""
        if current_finger_mode is not None:
            return Response({"finger_mode": current_finger_mode, "member_id": current_member_id}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No finger mode set"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Endpoint to set the current finger mode."""
        global current_finger_mode, current_member_id
        
        finger_mode = request.data.get('finger_mode')
        member_id = request.data.get('member_id')
        
        if finger_mode is None:
            return Response({"error": "finger_mode is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if finger_mode not in ['register', 'attendance']:
            return Response({"error": "Invalid finger_mode choices are 'register' and 'attendance'"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Store the data temporarily in global variables (overwritten with each request)
        current_finger_mode = finger_mode
        current_member_id = member_id
        
        return Response({"message": "Finger mode updated successfully"}, status=status.HTTP_200_OK)

# class TotalMembersAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         total_members = MemberData.objects.count()
#         return Response({'total_members': total_members})


# class ActiveMembersAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         active_members = MemberData.objects.filter(status='active').count()
#         return Response({'active_members': active_members})


# class TotalExpensesAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         total_expenses = ExpenseData.objects.aggregate(total_expenses=models.Sum('amount'))['total_expenses']
#         return Response({'total_expenses': total_expenses})


# class IncomeExpenseAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         period = request.query_params.get('period', 'monthly')  # monthly, yearly, weekly
#         today = timezone.now()

#         if period == 'monthly':
#             start_date = today.replace(day=1)
#             end_date = today.replace(day=28) + timedelta(days=4)  # Just go to next month

#         elif period == 'yearly':
#             start_date = today.replace(month=1, day=1)
#             end_date = today.replace(year=today.year + 1, month=1, day=1)

#         elif period == 'weekly':
#             start_date = today - timedelta(days=today.weekday())
#             end_date = start_date + timedelta(days=7)

#         else:
#             start_date = today
#             end_date = today

#         income = PaymentData.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).aggregate(total_income=Sum('amount'))['total_income'] or 0
#         expenses = ExpenseData.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

#         return Response({'income': income, 'expenses': expenses, 'profit_loss': income - expenses})


# class LeftMembersAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         left_members = MemberData.objects.filter(status='left').count()
#         return Response({'left_members': left_members})


# class TotalRevenueAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         total_revenue = PaymentData.objects.aggregate(total_revenue=models.Sum('amount'))['total_revenue']
#         return Response({'total_revenue': total_revenue})


# class ExpenseDataViewSet(viewsets.ModelViewSet):
#     queryset = ExpenseData.objects.all()
#     serializer_class = ExpenseDataSerializer
#     permission_classes = [IsAuthenticated]


# class MembershipCountsAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         membership_counts = {}
#         memberships = MembershipData.objects.all()

#         for membership in memberships:
#             membership_counts[membership.name] = MemberData.objects.filter(membership=membership.name).count()

#         return Response(membership_counts)

# class MonthlyIncomeExpenseProfitAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         months = PaymentData.objects.values('payment_date__year', 'payment_date__month').distinct()
#         results = []

#         for month in months:
#             start_date = timezone.datetime(month['payment_date__year'], month['payment_date__month'], 1)
#             end_date = start_date + timedelta(days=31)  # Next month
#             end_date = end_date.replace(day=1)  # Reset to first day of next month

#             income = PaymentData.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).aggregate(total_income=Sum('amount'))['total_income'] or 0
#             expenses = ExpenseData.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

#             results.append({
#                 'from': start_date,
#                 'to': end_date,
#                 'income': income,
#                 'expense': expenses,
#                 'profit_loss': income - expenses,
#             })

#         return Response(results)


# class MembershipDataViewSet(viewsets.ModelViewSet):
#     queryset = MembershipData.objects.all()
#     serializer_class = MembershipDataSerializer
#     permission_classes = [IsAuthenticated]


# class PaymentDataViewSet(viewsets.ModelViewSet):
#     queryset = PaymentData.objects.all()
#     serializer_class = PaymentDataSerializer
#     permission_classes = [IsAuthenticated]


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