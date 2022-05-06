from django.db import models

# Create your models here.
class ADebt(models.Model):
    a_debt_time = models.TimeField(primary_key=True)
    a_debt_date = models.DateField()
    a_debt_open = models.CharField(max_length=8)
    a_debt_close = models.CharField(max_length=8)
    a_debt_high = models.CharField(max_length=8)
    a_debt_low = models.CharField(max_length=8)
    a_debt_volume = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'a_debt'
        unique_together = (('a_debt_time', 'a_debt_date'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:

        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:

        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:

        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:

        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_title = models.CharField(max_length=50)
    class_article = models.TextField()
    class_photo = models.CharField(max_length=100)

    class Meta:

        managed = True
        db_table = 'class'


class Corn(models.Model):
    corn_time = models.TimeField(primary_key=True)
    corn_date = models.DateField()
    corn_open = models.CharField(max_length=8)
    corn_close = models.CharField(max_length=8)
    corn_high = models.CharField(max_length=8)
    corn_low = models.CharField(max_length=8)
    corn_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'corn'
        unique_together = (('corn_time', 'corn_date'),)


class Dcboard(models.Model):
    dcboard_id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', models.DO_NOTHING)
    dcboard_title = models.CharField(max_length=50)
    dcboard_releasetime = models.DateTimeField()
    dcboard_content = models.TextField()
    dcboard_likes = models.IntegerField()
    dcboard_uploads = models.CharField(max_length=200)

    class Meta:

        managed = True
        db_table = 'dcboard'
        unique_together = (('dcboard_id', 'member'),)


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
    id = models.BigAutoField(primary_key=True)
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


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', models.DO_NOTHING)
    dcboard = models.ForeignKey(Dcboard, models.DO_NOTHING)
    feedback_content = models.TextField()

    class Meta:

        managed = True
        db_table = 'feedback'
        unique_together = (('feedback_id', 'member'),)


class Futures(models.Model):
    futures_id = models.CharField(primary_key=True, max_length=10)
    futures_name = models.CharField(max_length=10)
    futures_deposit = models.CharField(max_length=10)

    class Meta:

        managed = True
        db_table = 'futures'


class History(models.Model):
    member = models.OneToOneField('Member', models.DO_NOTHING)
    futures = models.ForeignKey(Futures, models.DO_NOTHING)
    buy_qty = models.IntegerField(blank=True, null=True)
    buy_mon = models.IntegerField(blank=True, null=True)
    buy_time = models.DateField(blank=True, null=True)
    sell_qty = models.IntegerField(blank=True, null=True)
    sell_mon = models.IntegerField(blank=True, null=True)
    sell_time = models.DateField(blank=True, null=True)
    record = models.IntegerField(blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:

        managed = True
        db_table = 'history'
        unique_together = (('member', 'futures'),)


class IndexClass(models.Model):
    index_class_id = models.AutoField(primary_key=True)
    index_class_title = models.CharField(max_length=50)
    index_class_article = models.TextField()
    index_class_photo = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'index_class'

class IntelligentStrategy(models.Model):
    intelligent_strategy_id = models.CharField(primary_key=True, max_length=50)
    futures = models.ForeignKey(Futures, models.DO_NOTHING)
    member = models.ForeignKey('Member', models.DO_NOTHING)
    intelligent_strategy_algorithm = models.CharField(max_length=10)
    intelligent_strategy_long_short = models.CharField(max_length=11, default='')
    intelligent_strategy_money_manage = models.CharField(max_length=11, default='')
    intelligent_strategy_stop_pl = models.CharField(max_length=11, default='')

    class Meta:
        managed = True
        db_table = 'intelligent_strategy'
        # unique_together = (('intelligent_strategy_id', 'member_id'),)

class Member(models.Model):
    member_id = models.CharField(primary_key=True, max_length=50)
    member_password = models.CharField(max_length=50)
    member_name = models.CharField(max_length=50)
    member_gender = models.CharField(max_length=50)
    member_birth = models.DateField()
    member_photo = models.CharField(max_length=100)
    member_phone = models.CharField(max_length=50)
    member_email = models.CharField(max_length=50)
    member_twd = models.CharField(max_length=50)
    member_usd = models.CharField(max_length=50)

    class Meta:

        managed = True
        db_table = 'member'


class MiniDow(models.Model):
    mini_dow_time = models.TimeField(primary_key=True)
    mini_dow_date = models.DateField()
    mini_dow_open = models.CharField(max_length=8)
    mini_dow_close = models.CharField(max_length=8)
    mini_dow_high = models.CharField(max_length=8)
    mini_dow_low = models.CharField(max_length=8)
    mini_dow_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'mini_dow'
        unique_together = (('mini_dow_time', 'mini_dow_date'),)


class MiniNastaq(models.Model):
    mini_nastaq_time = models.TimeField(primary_key=True)
    mini_nastaq_date = models.DateField()
    mini_nastaq_open = models.CharField(max_length=8)
    mini_nastaq_close = models.CharField(max_length=8)
    mini_nastaq_high = models.CharField(max_length=8)
    mini_nastaq_low = models.CharField(max_length=8)
    mini_nastaq_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'mini_nastaq'
        unique_together = (('mini_nastaq_time', 'mini_nastaq_date'),)


class MiniRussell(models.Model):
    mini_russell_time = models.TimeField(primary_key=True)
    mini_russell_date = models.DateField()
    mini_russell_open = models.CharField(max_length=8)
    mini_russell_close = models.CharField(max_length=8)
    mini_russell_high = models.CharField(max_length=8)
    mini_russell_low = models.CharField(max_length=8)
    mini_russell_volume = models.CharField(max_length=8)


    class Meta:

        managed = True
        db_table = 'mini_russell'
        unique_together = (('mini_russell_time', 'mini_russell_date'),)


class MiniSp(models.Model):
    mini_sp_time = models.TimeField(primary_key=True)
    mini_sp_date = models.DateField()
    mini_sp_open = models.CharField(max_length=8)
    mini_sp_close = models.CharField(max_length=8)
    mini_sp_high = models.CharField(max_length=8)
    mini_sp_low = models.CharField(max_length=8)
    mini_sp_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'mini_sp'
        unique_together = (('mini_sp_time', 'mini_sp_date'),)


class Mtx(models.Model):
    mtx_time = models.TimeField(primary_key=True)
    mtx_date = models.DateField()
    mtx_open = models.CharField(max_length=8)
    mtx_close = models.CharField(max_length=8)
    mtx_high = models.CharField(max_length=8)
    mtx_low = models.CharField(max_length=8)
    mtx_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'mtx'
        unique_together = (('mtx_time', 'mtx_date'),)


class News(models.Model):
    news_id = models.IntegerField(primary_key=True)
    news_title = models.TextField(blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_time = models.TextField(blank=True, null=True)
    news_author = models.TextField(blank=True, null=True)
    news_photo = models.TextField(blank=True, null=True)
    news_area = models.BigIntegerField(blank=True, null=True)
    news_type = models.BigIntegerField(blank=True, null=True)
    news_category = models.BigIntegerField(blank=True, null=True)

    class Meta:

        managed = True
        db_table = 'news'


class Soy(models.Model):
    soy_time = models.TimeField(primary_key=True)
    soy_date = models.DateField()
    soy_open = models.CharField(max_length=8)
    soy_close = models.CharField(max_length=8)
    soy_high = models.CharField(max_length=8)
    soy_low = models.CharField(max_length=8)
    soy_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'soy'
        unique_together = (('soy_time', 'soy_date'),)


class Te(models.Model):
    te_time = models.TimeField(primary_key=True)
    te_date = models.DateField()
    te_open = models.CharField(max_length=8)
    te_close = models.CharField(max_length=8)
    te_high = models.CharField(max_length=8)
    te_low = models.CharField(max_length=8)
    te_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'te'
        unique_together = (('te_time', 'te_date'),)


class TechnicalStrategry(models.Model):
    technical_strategy_id = models.CharField(primary_key=True, max_length=50)
    member = models.ForeignKey(Member, models.DO_NOTHING)
    futures = models.ForeignKey(Futures, models.DO_NOTHING)
    technical_strategry_period = models.CharField(max_length=10)
    technical_strategry_start = models.DateField()
    technical_strategry_end = models.DateField()
    technical_strategy_long_short = models.CharField(max_length=11, default='')
    technical_strategy_stop_pl = models.CharField(max_length=11, default='')
    technical_strategy_money_manage = models.CharField(max_length=11, default='')
    technical_strategry_enter = models.CharField(max_length=11, default='')
    technical_strategry_exit = models.CharField(max_length=11, default='')

    class Meta:

        managed = True
        db_table = 'technical_strategry'
        unique_together = (('technical_strategy_id', 'member'),)


class Tf(models.Model):
    tf_time = models.TimeField(primary_key=True)
    tf_date = models.DateField()
    tf_open = models.CharField(max_length=8)
    tf_close = models.CharField(max_length=8)
    tf_high = models.CharField(max_length=8)
    tf_low = models.CharField(max_length=8)
    tf_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'tf'
        unique_together = (('tf_time', 'tf_date'),)


class Tx(models.Model):
    tx_time = models.TimeField(primary_key=True)
    tx_date = models.DateField()
    tx_open = models.CharField(max_length=8)
    tx_close = models.CharField(max_length=8)
    tx_high = models.CharField(max_length=8)
    tx_low = models.CharField(max_length=8)
    tx_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'tx'
        unique_together = (('tx_time', 'tx_date'),)


class Wheat(models.Model):
    wheat_time = models.TimeField(primary_key=True)
    wheat_date = models.DateField()
    wheat_open = models.CharField(max_length=8)
    wheat_close = models.CharField(max_length=8)
    wheat_high = models.CharField(max_length=8)
    wheat_low = models.CharField(max_length=8)
    wheat_volume = models.CharField(max_length=8)

    class Meta:

        managed = True
        db_table = 'wheat'
        unique_together = (('wheat_time', 'wheat_date'),)



class Newscontent(models.Model):
    news_id = models.IntegerField(primary_key=True)
    news_title = models.TextField(blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_time = models.TextField(blank=True, null=True)
    news_author = models.TextField(blank=True, null=True)
    news_photo = models.TextField(blank=True, null=True)
    news_area = models.BigIntegerField(blank=True, null=True)
    member_id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:

        managed = True
        db_table = 'news_content' 