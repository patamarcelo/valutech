from django.db import models
import datetime
import uuid


# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.db.models import FileField




def get_file_path(instance, filename):
    stor = FileSystemStorage()
    f = FileField(storage=stor)
    ext       = filename.split('.')[-1]
    date_file = datetime.datetime.now().strftime('%Y%m%d')
    file_name  = f'api-binance-django-mp/{instance.first_name}/{date_file}_{str(uuid.uuid4())[:8]}.{ext}'
    return f.generate_filename(None, file_name)

class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é Obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True) padrao como False
        extra_fields.setdefault('is_superuser', False)        
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('image', None)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)
    
    
    

class CustomUsuario(AbstractUser):
    email      = models.EmailField('E-mail', unique=True)
    fone       = models.CharField('Telefone', max_length=15)
    first_name = models.CharField('First Name', max_length=15)
    last_name  = models.CharField('Last Name', max_length=15)
    last_name  = models.CharField('Last Name', max_length=15)
    is_staff   = models.BooleanField('Membro da equipe', default=False)
    image      = models.ImageField(upload_to='images/', default='images/User1.jpg', blank=True)
    
    api_key    = models.CharField('Api Key', max_length=200, blank=True, null=True)
    api_secret = models.CharField('Api Secret', max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']

    


    def __str__(self):
        return self.email

    objects = UsuarioManager()