# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BaseCase(models.Model):
    case_id = models.AutoField(primary_key=True)
    case_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    content = models.TextField()
    project = models.ForeignKey('BaseProject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'base_case'


class BaseEnvironment(models.Model):
    env_id = models.AutoField(primary_key=True)
    env_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    private_key = models.CharField(max_length=50)
    project = models.ForeignKey('BaseProject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'base_environment'


class BaseInterface(models.Model):
    if_id = models.AutoField(primary_key=True)
    if_name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    method = models.CharField(max_length=4)
    data_type = models.CharField(max_length=4)
    is_sign = models.IntegerField()
    description = models.CharField(max_length=100)
    request_header_param = models.TextField()
    request_body_param = models.TextField()
    response_header_param = models.TextField()
    response_body_param = models.TextField()
    project = models.ForeignKey('BaseProject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'base_interface'


class BasePlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    content = models.TextField()
    environment = models.ForeignKey(BaseEnvironment, models.DO_NOTHING)
    project = models.ForeignKey('BaseProject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'base_plan'


class BaseProject(models.Model):
    prj_id = models.AutoField(primary_key=True)
    prj_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    sign = models.ForeignKey('BaseSign', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'base_project'


class BaseReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_name = models.CharField(max_length=255)
    content = models.TextField()
    case_num = models.IntegerField(blank=True, null=True)
    pass_num = models.IntegerField(blank=True, null=True)
    fail_num = models.IntegerField(blank=True, null=True)
    error_num = models.IntegerField(blank=True, null=True)
    plan = models.ForeignKey(BasePlan, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'base_report'


class BaseSign(models.Model):
    sign_id = models.AutoField(primary_key=True)
    sign_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'base_sign'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Idoxu(models.Model):
    stu_id = models.IntegerField()
    c_name = models.CharField(max_length=20, blank=True, null=True)
    istester = models.CharField(max_length=50, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'idoxu'


class Istester(models.Model):
    id = models.IntegerField(primary_key=True)
    unname = models.CharField(max_length=20)
    sex = models.CharField(max_length=4, blank=True, null=True)
    brith = models.TextField(blank=True, null=True)  # This field type is a guess.
    department = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    idoxu = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'istester'


class SignEvent(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.IntegerField()
    address = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    create_time = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'sign_event'

class SignGuest(models.Model):
    realname = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=254)
    sign = models.IntegerField()
    create_time = models.DateTimeField()
    event = models.ForeignKey(SignEvent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sign_guest'


class SignReg(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sign_reg'

def __str__(self):
    return self.realname