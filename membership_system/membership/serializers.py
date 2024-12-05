from rest_framework import serializers
from .models import GymMember, Membership, GymIncomeExpense, GymInout, GymAttendance, MembershipPayment


class GymMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        return representation


class MembershipPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPayment
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = '__all__'


class GymIncomeExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymIncomeExpense
        fields = '__all__'    


# class GymInoutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GymInout
#         fields = '__all__'


class GymAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymAttendance
        fields = '__all__'
        


# class ExpenseDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExpenseData
#         fields = '__all__'


# class MembershipDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MembershipData
#         fields = '__all__'


# class PaymentDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentData
#         fields = '__all__'


class GymMemberSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        fields = ['first_name', 'last_name', 'membership_valid_from', 'membership_valid_to','membership_status', 'image']
        
        
class GymInoutSerializer(serializers.ModelSerializer):
    # Create a method field to fetch the member information based on member_id
    member_info = serializers.SerializerMethodField()

    def get_member_info(self, obj):
        try:
            # Fetch the member based on member_id (you can also use `filter()` if needed)
            member = GymMember.objects.get(member_id=obj.member_id)
            return GymMemberSimpleSerializer(member).data
        except GymMember.DoesNotExist:
            return None

    class Meta:
        model = GymInout
        fields = ['id', 'in_time', 'out_time', 'member_reg_code', 'member_info']