from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.shortcuts import reverse

ROLE_CHOICES = (
    (0, 'Employee'),
    (1, 'Coordinator'),
    (2, 'Administrator'),
)

MEASUREMENTS = (
        (0, 'Kg'),
        (1, 'Gr'),
        (2, 'Mg'),
        (3, 'Mkg')
    )

STATUS_FILD = (
        (0, 'New'),
        (1, 'Approved'),
        (2, 'Rejected'),
    )

GROUPS = (
    (0, 'Meat'),
    (1, 'Fish'),
    (2, 'Vegetables'),
    (3, 'Fruit'),
    (4, 'Groats'),
)


class Items(models.Model):

    item_id = models.AutoField(primary_key=True)
    item_group = models.IntegerField(choices=GROUPS, default=0)
    unit_measurement = models.IntegerField(choices=MEASUREMENTS, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.CharField(max_length=256)
    storage_location = models.CharField(max_length=256)
    contact_person = models.CharField(max_length=256)
    photo = models.ImageField(upload_to='images', blank=True)

    class Meta:
        verbose_name_plural = 'Items'

    def __str__(self):
        return f'Item from group: {self.get_group()}, status: {self.status}, ID: {self.pk}'

    def update(self, item_group=None, unit_measurement=None, quantity=None, price=None, status=None,
               storage_location=None, contact_person=None, photo=None):

        if item_group is not None:
            self.item_group = item_group

        if unit_measurement is not unit_measurement:
            self.unit_measurement = unit_measurement

        if quantity is not None:
            self.quantity = quantity

        if price is not None:
            self.price = price

        if status is not None:
            self.status = status

        if storage_location is not None:
            self.storage_location = storage_location

        if contact_person is not None:
            self.contact_person = contact_person

        if photo is not None:
            self.photo = photo

        self.save()

    @staticmethod
    def get_by_id(item_id):
        try:
            return Items.objects.get(pk=item_id)
        except:
            return None

    @staticmethod
    def get_absolute_url():
        return reverse('list-goods')

    def get_measurement(self):
        return MEASUREMENTS[self.unit_measurement][1]

    def get_group(self):
        return GROUPS[self.item_group][1]


class Orders(models.Model):

    request_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=20, blank=True)
    item_id = models.ForeignKey(Items, related_name='orders', on_delete=models.CASCADE, null=True)
    employee_name = models.CharField(max_length=20)
    unit_measurement = models.IntegerField(choices=MEASUREMENTS, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    comment = models.CharField(blank=True, max_length=256)
    status = models.IntegerField(choices=STATUS_FILD, default=0)

    class Meta:
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.pk}, {self.status}'

    @staticmethod
    def get_absolute_url():
        return reverse('home')

    def get_status(self):
        return STATUS_FILD[self.unit_measurement][1]

    def get_measurement(self):
        return MEASUREMENTS[self.unit_measurement][1]


class RequestRows(models.Model):

    request_row_id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(Orders, related_name='orders', on_delete=models.CASCADE, null=True)
    item_id = models.ForeignKey(Items, related_name='item', on_delete=models.CASCADE, null=True)
    unit_measurement = models.IntegerField(choices=MEASUREMENTS, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    comment = models.CharField(blank=True, max_length=256)

    class Meta:
        verbose_name_plural = 'Request Rows Directory'

    def __str__(self):
        return f'RequestRowsDirectory {self.request_id}, {self.item_id}'

    def get_measurement(self):
        return MEASUREMENTS[self.unit_measurement][1]


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('role', 2)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
            This class represents a basic user. \n
            Attributes:
            -----------
            param first_name: Describes first name of the user
            type first_name: str max length=20
            param last_name: Describes last name of the user
            type last_name: str max length=20
            param email: Describes the email of the user
            type email: str, unique, max length=100
            param password: Describes the password of the user
            type password: str
            param role: user role, default role (0, 'Employee')
            type updated_at: int (choices)
        """

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=20, default=None, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, default=None)
    password = models.CharField(default=None, max_length=255)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} is {self.role}"

    @staticmethod
    def create(email, password, first_name=None, last_name=None):
        """
        :param first_name: first name of a user
        :type first_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :return: a new user object which is also written into the DB
        """
        if len(first_name) <= 20 and len(last_name) <= 20 and len(email) <= 100 and len(
                email.split('@')) == 2 and len(CustomUser.objects.filter(email=email)) == 0:
            custom_user = CustomUser(email=email, password=password, first_name=first_name,
                                     last_name=last_name)
            custom_user.save()
            return custom_user
        return None

    def get_role_name(self):
        """
        returns str role name
        """
        return ROLE_CHOICES[self.role][1]

