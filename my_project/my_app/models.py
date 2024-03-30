from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    ville = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default = "No description found")
    notice = models.TextField(default = "No notice found")
    price = models.IntegerField(default = 0)

    def __str__(self) -> str:
        return self.name

class Symptome(models.Model):
    name = models.CharField(max_length = 255)
    dangerousity = models.IntegerField(default = 0)
    description = models.TextField(default = "No description found")

    def __str__(self) -> str:
        return self.name

class MedicineSymptome(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    symptome = models.ForeignKey(Symptome, on_delete=models.CASCADE)
    efficacity = models.IntegerField(default = 0)

    def __str__(self) -> str:
        return str(self.medicine) + "_" + str(self.symptome) + "_" + str(self.efficacite)

    class Meta:
        # Définition de la clé primaire composite
        constraints = [
            models.UniqueConstraint(fields=['medicine', 'symptome'], name='unique_medicine_symptome')
        ]

class PatientMedicine(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dateOfPurchase = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default = 0)
    totalPrice = models.IntegerField(default = 0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient', 'medicine'], name='unique_patient_medicine')
        ]

