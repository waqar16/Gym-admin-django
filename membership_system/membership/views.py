from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .CustomPagination import CustomPageNumberPagination
from .utils import generate_pdf_receipt
from datetime import timedelta
from .models import (
                     GymMember,
                     Membership,
                     GymIncomeExpense,
                     GymInout,
                     MembershipPayment,
                     )
from .serializers import (
                          GymMemberSerializer,
                          MembershipSerializer,
                          GymIncomeExpenseSerializer,
                          GymInoutSerializer,
                          MembershipPaymentSerializer,
                          )
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.db.models import Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .filters import (
                      GymMemberFilter,
                      MembershipFilter,
                      GymInoutFilter,
                      GymIncomeExpenseFilter,
                      MembershipPaymentFilter,
                      )
from django.db.models import FloatField, F, Q, Value
from django.db.models.functions import ExtractMonth, ExtractYear, Coalesce


class MemberDataViewSet(viewsets.ModelViewSet):
    queryset = GymMember.objects.filter(role_name__iexact='member')
    serializer_class = GymMemberSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GymMemberFilter

    def perform_update(self, serializer):
        super().perform_update(serializer)
        
        # Get the member object after saving
        member = serializer.instance

        if member.membership_valid_to and member.membership_valid_to < timezone.now().date():
            member.membership_status = 'expired'
        else:
            member.membership_status = 'continue'

        # Save the updated membership status
        member.save()
    
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
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MembershipFilter


class MemberShipPaymentViewSet(viewsets.ModelViewSet):
    queryset = MembershipPayment.objects.all()
    serializer_class = MembershipPaymentSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MembershipPaymentFilter
    
    def list(self, request, *args, **kwargs):
        query_type = self.request.query_params.get('query', None)
        
        if query_type == 'download-receipt':
            mp_id = self.request.query_params.get('mp_id', None)
            if not mp_id:
                return Response({"error": "mp_id is required"}, status=400)

            mp = get_object_or_404(MembershipPayment, mp_id=mp_id)
            member_id = mp.member_id
            return generate_pdf_receipt(mp, member_id)
        
        return super().list(request, *args, **kwargs)


class AcceptPaymentView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # amount = request.data.get('amount')
        member_id = request.data.get('member_id')
        membership_class = request.data.get('membership_class')

        if not all([member_id, membership_class]):
            return Response({"error": "Missing required fields member_id and membership_class"}, status=status.HTTP_400_BAD_REQUEST)
        
        member = get_object_or_404(GymMember, member_id=member_id)
        
        valid_membership_classes = ['Regular Monthly', '3 month Cardio', 'Cardio Monthly', '3 Month Gym']
        if membership_class not in valid_membership_classes:
            return Response({"error": f"Invalid membership class. Choices are {', '.join(valid_membership_classes)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        if membership_class == "Regular Monthly":
            updated_date_to_expire = timezone.now() + timedelta(days=30)
            amount = Membership.objects.get(membership_class='Regular Monthly').membership_amount
        elif membership_class == "3 month Cardio":
            updated_date_to_expire = timezone.now() + timedelta(days=90)
            amount = Membership.objects.get(membership_class='3 month Cardio').membership_amount
        elif membership_class == "Cardio Monthly":
            updated_date_to_expire = timezone.now() + timedelta(days=30)
            amount = Membership.objects.get(membership_class='Cardio Monthly').membership_amount
        elif membership_class == "3 Month Gym":
            updated_date_to_expire = timezone.now() + timedelta(days=90)
            amount = Membership.objects.get(membership_class='3 Month Gym').membership_amount
        
        member.membership_valid_from = timezone.now()
        member.membership_valid_to = updated_date_to_expire
        member.selected_membership = membership_class
        member.membership_status = 'continue'
        member.save()

        payment_data = {
            'member_id': member.member_id,
            'membership_id': Membership.objects.get(membership_label=membership_class).id,
            'membership_amount': amount,
            'paid_amount': amount,
            'start_date': timezone.now(),
            'end_date': updated_date_to_expire,
            'membership_status': 'Continue',
            'created_date': timezone.now(),
            'is_active': True,
        }
        payment_serializer = MembershipPaymentSerializer(data=payment_data)
        if payment_serializer.is_valid():
            payment_serializer.save()
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Payment accepted and member record updated."}, status=status.HTTP_200_OK)
    

class GymIncomeExpenseViewSet(viewsets.ModelViewSet):
    queryset = GymIncomeExpense.objects.all()
    serializer_class = GymIncomeExpenseSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GymIncomeExpenseFilter

    def list(self, request, *args, **kwargs):
        query_type = self.request.query_params.get('query', None)
        
        if query_type == 'download-receipt':
            income_id = self.request.query_params.get('income_id', None)
            if not income_id:
                return Response({"error": "income_id is required"}, status=400)

            income = get_object_or_404(GymIncomeExpense, pk=income_id, invoice_type='income')
            return generate_pdf_receipt(income)

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
                        Value(0),
                        output_field=FloatField()
                    ),
                    total_expenses=Coalesce(
                        Sum(
                            'total_amount',
                            filter=Q(invoice_type='expense'),
                            output_field=FloatField()
                        ),
                        Value(0),
                        output_field=FloatField()
                    ),
                )
                .annotate(
                    profit=F('total_revenue') - F('total_expenses')
                )
                .order_by('-year', '-month')  # Order by most recent year and month
            )
            paginator = self.pagination_class()
            paginated_data = paginator.paginate_queryset(list(monthly_data), request, view=self)

            return paginator.get_paginated_response({'monthly_data': paginated_data})
        # Default behavior
        return super().list(request, *args, **kwargs)


class GymInoutViewSet(viewsets.ModelViewSet):
    queryset = GymInout.objects.all().order_by('-in_time')[:1000]
    serializer_class = GymInoutSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GymInoutFilter


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
            return Response({"mode": current_finger_mode, "member_id": current_member_id}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No finger mode set"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Endpoint to set the current finger mode."""
        global current_finger_mode, current_member_id
        
        finger_mode = request.data.get('mode')
        member_id = request.data.get('member_id')
        
        if finger_mode is None:
            return Response({"error": "Mode is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if finger_mode not in ['register', 'attendance']:
            return Response({"error": "Invalid mode! Choices are 'register' and 'attendance'"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Store the data temporarily in global variables (overwritten with each request)
        current_finger_mode = finger_mode
        current_member_id = member_id
        
        return Response({"message": "Mode has been updated."}, status=status.HTTP_200_OK)


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