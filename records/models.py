from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.name

class PhoneRecord(models.Model):
    DEFAULT_PREFIX = "92"

    phone_last = models.CharField(max_length=4, null=True, blank=True)
    phone_4 = models.CharField(max_length=4, null=True, blank=True)
    phone_6 = models.CharField(max_length=6, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)  # Теперь при удалении организации номера тоже удаляются
    port_asl = models.CharField(max_length=6, null=True, blank=True)
    stan = models.CharField(max_length=6, null=True, blank=True)
    lin = models.CharField(max_length=6, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    status_id = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.phone_4 and not self.phone_6:
            self.phone_6 = f"{self.DEFAULT_PREFIX}{self.phone_4}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_6 or self.phone_4

class FailureType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class DamageRecord(models.Model):
    phone_record = models.ForeignKey(PhoneRecord, on_delete=models.CASCADE)  # Если удаляется номер, удаляются и записи о повреждениях
    failure_type = models.ForeignKey(FailureType, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Запись повреждения {self.phone_record.phone_4} / {self.phone_record.phone_6}"
