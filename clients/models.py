from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)             # Mijoz ismi
    email = models.EmailField()                         # Email manzili
    phone = models.CharField(max_length=15)             # Telefon raqami
    company = models.CharField(max_length=100, blank=True)  # Kompaniya nomi (ixtiyoriy)
    notes = models.TextField(blank=True)                # Izoh (ixtiyoriy)

    def __str__(self):
        return self.name
