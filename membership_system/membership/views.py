from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MemberData, ExpenseData, MembershipData, PaymentData
from .serializers import MemberDataSerializer, ExpenseDataSerializer, MembershipDataSerializer, PaymentDataSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status



class MemberDataViewSet(viewsets.ModelViewSet):
    queryset = MemberData.objects.all()
    serializer_class = MemberDataSerializer
    permission_classes = [IsAuthenticated]

class ExpenseDataViewSet(viewsets.ModelViewSet):
    queryset = ExpenseData.objects.all()
    serializer_class = ExpenseDataSerializer
    permission_classes = [IsAuthenticated]

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