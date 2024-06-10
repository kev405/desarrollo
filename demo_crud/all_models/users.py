from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, phone=None, role=None):
        if not email:
            raise ValueError(_('Los usuarios deben tener una dirección de correo electrónico'))

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, phone=None, role=None):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            phone=phone,
            role=role
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    # Campos personalizados
    ROLE_CHOICES = [
        ('gerente', 'Gerente'),
        ('director_obra', 'Director de obra'),
        ('capataz_obra', 'Capataz de obra'),
        ('peon', 'Peón'),
        ('ayudante_albanil', 'Ayudante de albañil'),
    ]
    email = models.EmailField(unique=True, verbose_name=_('Correo electrónico'))
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    phone = models.CharField(max_length=15, verbose_name=_('Teléfono'))
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name=_('Rol'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' # Campo que se usará como nombre de usuario
    REQUIRED_FIELDS = ['name'] # Campos requeridos al crear usuarios
   

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff