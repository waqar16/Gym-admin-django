from rest_framework import serializers
from .models import MemberData, ExpenseData, MembershipData, PaymentData


class MemberDataSerializer(serializers.ModelSerializer):
    membership_name = serializers.CharField(source='membership.name', read_only=True)
    
    class Meta:
        model = MemberData
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        return representation


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
