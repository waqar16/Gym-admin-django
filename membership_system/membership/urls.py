from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberDataViewSet
# from .views import CustomLogin, TokenRefreshViewWithAdminPermission
# from .views import (
#     TotalMembersAPIView,
#     ActiveMembersAPIView,
#     LeftMembersAPIView,
#     TotalRevenueAPIView,
#     TotalExpensesAPIView,
#     IncomeExpenseAPIView,
#     MembershipCountsAPIView,
#     MonthlyIncomeExpenseProfitAPIView,
#     AuthenticationCheckAPIView,
# )

# Default router for viewsets
router = DefaultRouter()
router.register(r'members', MemberDataViewSet)
# router.register(r'expenses', ExpenseDataViewSet)
# router.register(r'memberships', MembershipDataViewSet)
# router.register(r'payments', PaymentDataViewSet)

# # Register APIViews manually
urlpatterns = [
    # Include the default router URLs
    path('api/', include(router.urls)),
]

#     # Register APIViews
#     path('api/total-members/', TotalMembersAPIView.as_view(), name='total-members'),
#     path('api/active-members/', ActiveMembersAPIView.as_view(), name='active-members'),
#     path('api/left-members/', LeftMembersAPIView.as_view(), name='left-members'),
#     path('api/total-revenue/', TotalRevenueAPIView.as_view(), name='total-revenue'),
#     path('api/total-expenses/', TotalExpensesAPIView.as_view(), name='total-expenses'),
#     path('api/income-expense/', IncomeExpenseAPIView.as_view(), name='income-expense'),
#     path('api/membership-counts/', MembershipCountsAPIView.as_view(), name='membership-counts'),
#     path('api/monthly-income-expense-profit/', MonthlyIncomeExpenseProfitAPIView.as_view(), name='monthly-income-expense-profit'),

#     # Token Authentication Endpoints
#     path('api/token/', CustomLogin.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshViewWithAdminPermission.as_view(), name='token_refresh'),
#     path('api/auth-check/', AuthenticationCheckAPIView.as_view(), name='auth-check'),
# ]
