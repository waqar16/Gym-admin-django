from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberDataViewSet, ExpenseDataViewSet, MembershipDataViewSet, PaymentDataViewSet
from .views import CustomLogin, TokenRefreshViewWithAdminPermission

router = DefaultRouter()
router.register(r'members', MemberDataViewSet)
router.register(r'expenses', ExpenseDataViewSet)
router.register(r'memberships', MembershipDataViewSet)
router.register(r'payments', PaymentDataViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', CustomLogin.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshViewWithAdminPermission.as_view(), name='token_refresh'),
]
