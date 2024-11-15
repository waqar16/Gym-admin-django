from django.contrib import admin
from .models import MemberData, ExpenseData, MembershipData, PaymentData


# Register the MemberData model
class MemberDataAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'dob', 'membership', 'membership_starting_date', 'membership_ending_date')
    search_fields = ('first_name', 'last_name', 'phone', 'membership')
    list_filter = ('membership', 'membership_starting_date', 'membership_ending_date')

# Register the ExpenseData model
class ExpenseDataAdmin(admin.ModelAdmin):
    list_display = ('expense_name', 'amount', 'payment_date')
    search_fields = ('expense_name', 'label')
    list_filter = ('payment_date',)

# Register the MembershipData model
class MembershipDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'fee', 'registration_fee', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

# Register the PaymentData model
class PaymentDataAdmin(admin.ModelAdmin):
    list_display = ('membership_name', 'name_of_member', 'amount', 'payment_date')
    search_fields = ('membership_name', 'name_of_member', 'label')
    list_filter = ('payment_date',)

# Register your models
admin.site.register(MemberData, MemberDataAdmin)
admin.site.register(ExpenseData, ExpenseDataAdmin)
admin.site.register(MembershipData, MembershipDataAdmin)
admin.site.register(PaymentData, PaymentDataAdmin)
