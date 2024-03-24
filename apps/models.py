from django.db import models
from django.contrib.auth.models import (AbstractUser, AbstractBaseUser,
                                        BaseUserManager, PermissionsMixin)
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _

STATUS = (
    ('Активна', 'Активна'),
    ('Бронь', 'Бронь'),
    ('Куплена', 'Куплена'),
    ('Расрочка', 'Расрочка'),
    ('Бартер', 'Бартер'),
)


class Users(models.Model):
    full_name = models.CharField(max_length=255, blank=True, verbose_name="ФИО")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Номер телефона")
    contract_number = models.CharField(max_length=150, blank=True, verbose_name="Номер договора")
    status_choices = models.CharField(max_length=150, blank=True, choices=STATUS, verbose_name="Статус")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Клиенты"
        verbose_name_plural = "Клиенты"


class Apartaments(models.Model):
    number = models.IntegerField(null=True, blank=True, verbose_name="Номер квартиры")
    objects_ap = models.CharField(max_length=150, blank=True, verbose_name="Объект")
    floor = models.IntegerField(blank=True, verbose_name="Этаж")
    ap = models.FloatField(blank=True, verbose_name="Кв")
    date_at = models.DateField(blank=True, verbose_name="Дата")
    status_choices = models.CharField(max_length=100, blank=True, choices=STATUS, verbose_name="Статус")
    price = models.DecimalField(max_digits=1000000, decimal_places=2, verbose_name="Цена")
    client = models.ForeignKey(Users, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Клиент")
    info = models.CharField(max_length=150, blank=True, verbose_name="Информация о статусе")

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = "Квартиры"
        verbose_name_plural = "Квартиры"


class CustomManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Manager(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    full_name = models.CharField(_('full name'), max_length=30, blank=True)
    count = models.CharField(_('count'),max_length=99999, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name="manager_groups",
        related_query_name="manager",
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name="manager_user_permissions",
        related_query_name="manager",
        help_text=_('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджер"
