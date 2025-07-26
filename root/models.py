from django.db import models
from django.core.validators import RegexValidator

class ContactUs(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField()
    phone_validator = RegexValidator(
        regex=r'^0\d{10}$',
        message='شماره موبایل باید با 0 شروع شود، شامل فقط اعداد باشد و 11 رقم داشته باشد.',
    )
    phone = models.CharField(max_length=11, validators=[phone_validator])
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.email


class Skills(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Team(models.Model):
    fullname = models.CharField(max_length=200)
    skills = models.ForeignKey(
        Skills, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField()
    image = models.ImageField("team", default="default.png")
    instagram = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.fullname


class Faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.question
