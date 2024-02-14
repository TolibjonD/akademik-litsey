from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator , MaxValueValidator

from django.utils import timezone
import uuid
from datetime import timedelta

# Create your models here.

class PendingContracts(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='KT')

class VerifiedContracts(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='TD')

class CustomUser(AbstractUser):
    IDNumber = models.CharField(max_length=10, help_text="Passport raqam va seriyasini kiriting", blank=True, null=True)
    biografiya = models.TextField(help_text="O'zingiz haqingizda qo'shimcha qiling", blank=True, null=True)
    telefon = models.CharField(max_length=30, help_text="Telefon raqamingiz", blank=True, null=True)
    tavallud_sanasi = models.DateField(blank=True, null=True)
    rasmingiz = models.ImageField(upload_to="students/", default="default_student.jpg")

    def __str__(self):
        return f"{self.username}"
    
    

class Fanlar(models.Model):
    class Meta:
        verbose_name_plural = "Fanlar"
    fan_nomi = models.CharField(max_length = 120)
    fan_haqida = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fan_nomi}"

class Teachers(models.Model):
    class Meta:
        verbose_name_plural = "Teachers"
    ismi = models.CharField(max_length=60)
    familiyasi = models.CharField(max_length=60)
    telefon = models.CharField(max_length=30)
    email = models.EmailField()
    biografiya = models.TextField()
    rasmi = models.ImageField(upload_to="teachers/", default="default_teacher.jpg")
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        return f"{self.ismi} {self.familiyasi}"

    def __str__(self):
        return f"{self.ismi} {self.familiyasi}"

DUE_DATE = timezone.now() + timedelta(days=100)
class Shartnoma(models.Model):
    class Meta:
        verbose_name_plural = "Shartnomalar"
    class ContractStatus(models.TextChoices):
        KUTILMOQDA = 'KT', 'Tasdiqlash kutilmoqda'
        TASDIQLANMADI = 'TDM', 'Tasdiqlanmadi'
        TASDIQLANDI = 'TD', 'Tasdiqlandi'
    talaba = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fanlar, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, blank=True, null=True)
    shartnoma_id = models.UUIDField(default=uuid.uuid4)
    boshlanish_sanasi = models.DateField(default=timezone.now)
    tugash_sanasi = models.DateField(default=DUE_DATE)
    baho = models.IntegerField(validators = [MinValueValidator(2), MaxValueValidator(5)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField()
    status = models.CharField(max_length=3, choices=ContractStatus.choices, default=ContractStatus.KUTILMOQDA)

    objects = models.Manager()
    pendings = PendingContracts()
    verified_contracts = VerifiedContracts()

    def __str__(self):
        return f"{self.talaba.username} is studying at {self.fan.fan_nomi}"


class Contact(models.Model):
    class Meta:
        verbose_name_plural = "Xabarlar"
    ism = models.CharField(max_length=50)
    email = models.EmailField()
    telefon = models.CharField(max_length=30)
    xabar = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.ism}"