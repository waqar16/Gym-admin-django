from django.db.models import Q
from django_filters import rest_framework as filters
from .models import GymMember, Membership, GymAttendance, GymIncomeExpense, GymInout

class GymMemberFilter(filters.FilterSet):
    global_search = filters.CharFilter(method='filter_global_search', label='Search')

    def filter_global_search(self, queryset, name, value):
        """
        Custom filter to perform a Search across multiple fields.
        The search will be case-insensitive and will match partial text.
        """
        if value:
            # Perform a case-insensitive search across multiple fields
            print(f"Filtering with value: {value}")
            return queryset.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(email__icontains=value) |
                Q(mobile__icontains=value) |
                Q(username__icontains=value) |
                Q(address__icontains=value)
            )
        print("No value provided for search")
        return queryset

    class Meta:
        model = GymMember
        fields = []


class MembershipFilter(filters.FilterSet):
    global_search = filters.CharFilter(method='filter_global_search', label='Search')

    def filter_global_search(self, queryset, name, value):
        """Perform a case-insensitive search across multiple fields in Membership model."""
        if value:
            return queryset.filter(
                Q(membership_label__icontains=value) |
                Q(membership_class__icontains=value) |
                Q(membership_description__icontains=value) |
                Q(membership_amount__icontains=value) |
                Q(installment_amount__icontains=value) |
                Q(signup_fee__icontains=value)
            )
        return queryset

    class Meta:
        model = Membership
        fields = []


class GymAttendanceFilter(filters.FilterSet):
    global_search = filters.CharFilter(method='filter_global_search', label='Search')

    def filter_global_search(self, queryset, name, value):
        """Custom filter to perform a Search across multiple fields in the GymAttendance model."""
        if value:
            return queryset.filter(
                Q(user_id__icontains=value) |
                Q(class_id__icontains=value) |
                Q(status__icontains=value) |
                Q(role_name__icontains=value)
            )
        return queryset

    class Meta:
        model = GymAttendance
        fields = []


# GymIncomeExpense Filter
class GymIncomeExpenseFilter(filters.FilterSet):
    global_search = filters.CharFilter(method='filter_global_search', label='Search')

    def filter_global_search(self, queryset, name, value):
        """Perform Search across multiple fields in GymIncomeExpense."""
        if value:
            return queryset.filter(
                Q(invoice_type__icontains=value) |
                Q(invoice_label__icontains=value) |
                Q(supplier_name__icontains=value) |
                Q(entry__icontains=value) |
                Q(payment_status__icontains=value) |
                Q(total_amount__icontains=value) |
                Q(receiver_id__icontains=value) |
                Q(invoice_date__icontains=value) |
                Q(delete_reason__icontains=value) |
                Q(mp_id__icontains=value)
            )
        return queryset

    class Meta:
        model = GymIncomeExpense
        fields = []


class GymInoutFilter(filters.FilterSet):
    global_search = filters.CharFilter(method='filter_global_search', label='Search')

    def filter_global_search(self, queryset, name, value):
        """Perform Search across multiple fields in GymInout."""
        if value:
            return queryset.filter(
                Q(member_id__icontains=value) |
                Q(member_reg_code__icontains=value)
            )
        return queryset

    class Meta:
        model = GymInout
        fields = []