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


class GymInoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymInout
        fields = '__all__'


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
