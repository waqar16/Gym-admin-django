from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .CustomPagination import CustomPageNumberPagination
from .utils import generate_pdf_receipt
from .models import (
                     GymMember,
                     Membership,
                     GymIncomeExpense,
                     GymInout,
                     )
from .serializers import (
                          GymMemberSerializer,
                          MembershipSerializer,
                          GymIncomeExpenseSerializer,
                          GymInoutSerializer,
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
    queryset = GymInout.objects.all()
    serializer_class = GymInoutSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GymInoutFilter


# class GymAttendanceViewSet(viewsets.ModelViewSet):
#     queryset = GymAttendance.objects.all()
#     serializer_class = GymAttendanceSerializer
#     permission_classes = [AllowAny]
#     pagination_class = CustomPageNumberPagination
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = GymAttendanceFilter
    
#     def list(self, request, *args, **kwargs):
#         """
#         Custom list view to group by attendance date and list all members with their attendance status.
#         """
#         # Get the date from query parameters or default to today if not provided
#         attendance_date = request.query_params.get('date', None)
        
#         if attendance_date:
#             # Filter GymAttendance records by the provided date
#             attendance_data = GymAttendance.objects.filter(attendance_date=attendance_date)
#         else:
#             # If no date is provided, return the attendance data for all dates
#             attendance_data = GymAttendance.objects.all()

#         # Fetch all members (role='member')
#         members = GymMember.objects.filter(role_name='member')

#         # Prepare the final response structure
#         response_data = []
        
#         for member in members:
#             # Check if the member has an attendance record for the provided date
#             attendance = attendance_data.filter(user_id=member.member_id, attendance_date=attendance_date).first()
            
#             # Set status to 'present' if attendance exists, otherwise 'absent'
#             status = attendance.status if attendance else 'absent'

#             member_info = {
#                 'user_id': member.member_id,
#                 'status': status,
#             }
#             response_data.append(member_info)

#         # Return the final list of members and their statuses
#         return Response(response_data)


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