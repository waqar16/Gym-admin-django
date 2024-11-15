from rest_framework import serializers
from .models import MemberData, ExpenseData, MembershipData, PaymentData

class MemberDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberData
        fields = '__all__'

class ExpenseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseData
        fields = '__all__'

class MembershipDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipData
        fields = '__all__'

class PaymentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentData
        fields = '__all__'
