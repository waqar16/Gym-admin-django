# from django.db import models


# class MemberData(models.Model):
#     STATUS_CHOICES = [
#         ('active', 'Active'),
#         ('left', 'Left'),
#     ]
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     phone = models.IntegerField(unique=True)
#     image = models.ImageField(upload_to='member_images/', blank=True, null=True)
#     joining_date = models.DateTimeField(auto_now_add=True)
#     dob = models.DateField()
#     address = models.TextField(blank=True, null=True)
#     membership = models.ForeignKey(
#         'MembershipData',
#         on_delete=models.CASCADE,
#         related_name='members',  # Allows reverse lookup (membership.members.all())
#     )
#     membership_starting_date = models.DateField()
#     membership_ending_date = models.DateField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
#     attendance_details = models.JSONField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


# class ExpenseData(models.Model):
#     expense_name = models.CharField(max_length=200)
#     label = models.CharField(max_length=100, blank=True, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField()

#     def __str__(self):
#         return self.expense_name


# class MembershipData(models.Model):
#     name = models.CharField(max_length=100)
#     duration_days = models.IntegerField()
#     fee = models.DecimalField(max_digits=10, decimal_places=2)
#     registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class PaymentData(models.Model):
#     membership_name = models.CharField(max_length=100)
#     name_of_member = models.CharField(max_length=100)
#     member_id = models.IntegerField(default=0)
#     label = models.CharField(max_length=100, blank=True, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField()

#     def __str__(self):
#         return f"Payment for {self.name_of_member}"





# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class Activity(models.Model):
    cat_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity'


class ActivityVideo(models.Model):
    activity_id = models.IntegerField(blank=True, null=True)
    video = models.TextField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_video'


class Adminconfig(models.Model):
    application_expiredate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adminconfig'


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class ClassBooking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    class_id = models.IntegerField(blank=True, null=True)
    booking_date = models.DateField(blank=True, null=True)
    booking_type = models.CharField(max_length=50, blank=True, null=True)
    booking_amount = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class_booking'


class ClassSchedule(models.Model):
    class_name = models.CharField(max_length=100, blank=True, null=True)
    assign_staff_mem = models.IntegerField(blank=True, null=True)
    assistant_staff_member = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    class_fees = models.IntegerField(blank=True, null=True)
    days = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.CharField(max_length=30, blank=True, null=True)
    end_time = models.CharField(max_length=30, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class_schedule'


class ClassScheduleList(models.Model):
    class_id = models.IntegerField(blank=True, null=True)
    days = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.CharField(max_length=20, blank=True, null=True)
    end_time = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class_schedule_list'


class GeneralSetting(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    start_year = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    office_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    date_format = models.CharField(max_length=15, blank=True, null=True)
    calendar_lang = models.TextField(blank=True, null=True)
    gym_logo = models.CharField(max_length=200, blank=True, null=True)
    cover_image = models.CharField(max_length=200, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=100, blank=True, null=True)
    chest = models.CharField(max_length=100, blank=True, null=True)
    waist = models.CharField(max_length=100, blank=True, null=True)
    thing = models.CharField(max_length=100, blank=True, null=True)
    arms = models.CharField(max_length=100, blank=True, null=True)
    fat = models.CharField(max_length=100, blank=True, null=True)
    member_can_view_other = models.IntegerField(blank=True, null=True)
    staff_can_view_own_member = models.IntegerField(blank=True, null=True)
    enable_sandbox = models.IntegerField(blank=True, null=True)
    paypal_email = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    enable_alert = models.IntegerField(blank=True, null=True)
    reminder_days = models.CharField(max_length=100, blank=True, null=True)
    reminder_message = models.CharField(max_length=255, blank=True, null=True)
    enable_message = models.IntegerField(blank=True, null=True)
    left_header = models.CharField(max_length=100, blank=True, null=True)
    footer = models.CharField(max_length=100, blank=True, null=True)
    system_installed = models.IntegerField(blank=True, null=True)
    enable_rtl = models.IntegerField(blank=True, null=True)
    datepicker_lang = models.TextField(blank=True, null=True)
    time_zone = models.CharField(max_length=20)
    system_version = models.TextField(blank=True, null=True)
    sys_language = models.CharField(max_length=20)
    header_color = models.CharField(max_length=10, blank=True, null=True)
    sidemenu_color = models.CharField(max_length=10, blank=True, null=True)
    stripe_secret_key = models.TextField(blank=True, null=True)
    stripe_publishable_key = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'general_setting'


class GymAccessright(models.Model):
    controller = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    menu = models.TextField(blank=True, null=True)
    menu_icon = models.TextField(blank=True, null=True)
    menu_title = models.TextField(blank=True, null=True)
    member = models.IntegerField(blank=True, null=True)
    staff_member = models.IntegerField(blank=True, null=True)
    accountant = models.IntegerField(blank=True, null=True)
    page_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_accessright'


class GymAssignWorkout(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    level_id = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    direct_assign = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_assign_workout'


class GymAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    class_id = models.IntegerField(blank=True, null=True)
    attendance_date = models.DateField(blank=True, null=True, auto_now_add=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    attendance_by = models.IntegerField(blank=True, null=True)
    role_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_attendance'


class GymDailyWorkout(models.Model):
    workout_id = models.IntegerField(blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    record_date = models.DateField(blank=True, null=True)
    result_measurment = models.CharField(max_length=50, blank=True, null=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    assigned_by = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    time_of_workout = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    reminder_status = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_daily_workout'


class GymEventPlace(models.Model):
    place = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_event_place'


class GymGroup(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_group'


class GymIncomeExpense(models.Model):
    invoice_type = models.CharField(max_length=100, blank=True, null=True)
    invoice_label = models.CharField(max_length=100, blank=True, null=True)
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    entry = models.TextField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    receiver_id = models.IntegerField(blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    is_active = models.IntegerField(db_column='is_Active', blank=True, null=True)  # Field name made lowercase.
    delete_reason = models.CharField(max_length=500, blank=True, null=True)
    mp_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_income_expense'


class GymInout(models.Model):
    member_id = models.CharField(max_length=100, blank=True, null=True)
    in_time = models.DateTimeField(blank=True, null=True)
    out_time = models.DateTimeField(blank=True, null=True)
    member_reg_code = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'gym_inout'


class GymInterestArea(models.Model):
    interest = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_interest_area'


class GymLevels(models.Model):
    level = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_levels'


class GymMeasurement(models.Model):
    result_measurment = models.CharField(max_length=100, blank=True, null=True)
    result = models.FloatField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    result_date = models.DateField(blank=True, null=True)
    image = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_measurement'


class GymMember(models.Model):
    activated = models.IntegerField(blank=True, null=True)
    role_name = models.TextField(blank=True, null=True)
    member_id = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=300, blank=True, null=True)
    is_exist = models.IntegerField()
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    member_type = models.TextField(blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    s_specialization = models.CharField(max_length=255, blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    assign_class = models.IntegerField(blank=True, null=True)
    assign_group = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=10, blank=True, null=True)
    height = models.CharField(max_length=10, blank=True, null=True)
    chest = models.CharField(max_length=10, blank=True, null=True)
    waist = models.CharField(max_length=10, blank=True, null=True)
    thing = models.CharField(max_length=10, blank=True, null=True)
    arms = models.CharField(max_length=10, blank=True, null=True)
    fat = models.CharField(max_length=10, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='members/', blank=True, null=True)
    assign_staff_mem = models.IntegerField(blank=True, null=True)
    intrested_area = models.IntegerField(blank=True, null=True)
    g_source = models.IntegerField(blank=True, null=True)
    referrer_by = models.IntegerField(blank=True, null=True)
    inquiry_date = models.DateField(blank=True, null=True)
    trial_end_date = models.DateField(blank=True, null=True)
    selected_membership = models.CharField(max_length=100, blank=True, null=True)
    membership_status = models.TextField(blank=True, null=True)
    membership_valid_from = models.DateField(blank=True, null=True)
    membership_valid_to = models.DateField(blank=True, null=True)
    first_pay_date = models.DateField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    alert_sent = models.IntegerField(blank=True, null=True)
    admin_alert = models.IntegerField(blank=True, null=True)
    alert_send_date = models.DateField(blank=True, null=True)
    members_reg_number = models.CharField(max_length=10, blank=True, null=True)
    fingerprint = models.TextField(db_column='FingerPrint', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gym_member'


class GymMemberClass(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    assign_class = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_member_class'


class GymMessage(models.Model):
    sender = models.IntegerField(blank=True, null=True)
    receiver = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    subject = models.CharField(max_length=150, blank=True, null=True)
    message_body = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_message'


class GymNewsletter(models.Model):
    api_key = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_newsletter'


class GymNotice(models.Model):
    notice_title = models.CharField(max_length=100, blank=True, null=True)
    notice_for = models.TextField(blank=True, null=True)
    class_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_notice'


class GymNutrition(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    day = models.CharField(max_length=50, blank=True, null=True)
    breakfast = models.TextField(blank=True, null=True)
    midmorning_snack = models.TextField(blank=True, null=True)
    lunch = models.TextField(blank=True, null=True)
    afternoon_snack = models.TextField(blank=True, null=True)
    dinner = models.TextField(blank=True, null=True)
    afterdinner_snack = models.TextField(blank=True, null=True)
    start_date = models.CharField(max_length=20, blank=True, null=True)
    expire_date = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_nutrition'


class GymNutritionData(models.Model):
    day_name = models.CharField(max_length=30, blank=True, null=True)
    nutrition_time = models.CharField(max_length=30, blank=True, null=True)
    nutrition_value = models.TextField(blank=True, null=True)
    nutrition_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_nutrition_data'


class GymProduct(models.Model):
    product_name = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_product'


class GymReservation(models.Model):
    event_name = models.CharField(max_length=100, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    start_time = models.CharField(max_length=20, blank=True, null=True)
    end_time = models.CharField(max_length=20, blank=True, null=True)
    place_id = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_reservation'


class GymRoles(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_roles'


class GymSource(models.Model):
    source_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_source'


class GymStore(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    sell_date = models.DateField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    sell_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_store'


class GymUserWorkout(models.Model):
    user_workout_id = models.IntegerField(blank=True, null=True)
    workout_name = models.IntegerField(blank=True, null=True)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    kg = models.FloatField(blank=True, null=True)
    rest_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_user_workout'


class GymWorkoutData(models.Model):
    day_name = models.CharField(max_length=15, blank=True, null=True)
    workout_name = models.CharField(max_length=100, blank=True, null=True)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    kg = models.FloatField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    workout_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gym_workout_data'


class InstallmentPlan(models.Model):
    number = models.IntegerField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'installment_plan'


class Membership(models.Model):
    membership_label = models.CharField(max_length=100, blank=True, null=True)
    membership_cat_id = models.IntegerField(blank=True, null=True)
    membership_length = models.IntegerField(blank=True, null=True)
    membership_class_limit = models.CharField(max_length=20, blank=True, null=True)
    limit_days = models.IntegerField(blank=True, null=True)
    limitation = models.CharField(max_length=20, blank=True, null=True)
    install_plan_id = models.IntegerField(blank=True, null=True)
    membership_amount = models.FloatField(blank=True, null=True)
    membership_class = models.CharField(max_length=255, blank=True, null=True)
    installment_amount = models.FloatField(blank=True, null=True)
    signup_fee = models.FloatField(blank=True, null=True)
    gmgt_membershipimage = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by_id = models.IntegerField(blank=True, null=True)
    membership_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membership'


class MembershipActivity(models.Model):
    activity_id = models.IntegerField(blank=True, null=True)
    membership_id = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membership_activity'


class MembershipHistory(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    selected_membership = models.IntegerField(blank=True, null=True)
    assign_staff_mem = models.IntegerField(blank=True, null=True)
    intrested_area = models.IntegerField(blank=True, null=True)
    g_source = models.IntegerField(blank=True, null=True)
    referrer_by = models.IntegerField(blank=True, null=True)
    inquiry_date = models.DateField(blank=True, null=True)
    trial_end_date = models.DateField(blank=True, null=True)
    membership_valid_from = models.DateField(blank=True, null=True)
    membership_valid_to = models.DateField(blank=True, null=True)
    first_pay_date = models.DateField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membership_history'


class MembershipPayment(models.Model):
    mp_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField(blank=True, null=True)
    membership_id = models.IntegerField(blank=True, null=True)
    membership_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    membership_status = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    isprinted = models.TextField(db_column='IsPrinted', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    signupfee = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(db_column='is_Active', blank=True, null=True)  # Field name made lowercase.
    delete_reason = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membership_payment'


class MembershipPaymentHistory(models.Model):
    payment_history_id = models.BigAutoField(primary_key=True)
    mp_id = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    paid_by_date = models.DateField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    trasaction_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membership_payment_history'


class Specialization(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'specialization'
