from django.db import models


class MemberData(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('left', 'Left'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField(unique=True)
    image = models.ImageField(upload_to='member_images/', blank=True, null=True)
    joining_date = models.DateTimeField(auto_now_add=True)
    dob = models.DateField()
    address = models.TextField(blank=True, null=True)
    membership = models.CharField(max_length=100)
    membership_starting_date = models.DateField()
    membership_ending_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    attendance_details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ExpenseData(models.Model):
    expense_name = models.CharField(max_length=200)
    label = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()

    def __str__(self):
        return self.expense_name


class MembershipData(models.Model):
    name = models.CharField(max_length=100)
    duration_days = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PaymentData(models.Model):
    membership_name = models.CharField(max_length=100)
    name_of_member = models.CharField(max_length=100)
    member_id = models.IntegerField(default=0)
    label = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()

    def __str__(self):
        return f"Payment for {self.name_of_member}"
