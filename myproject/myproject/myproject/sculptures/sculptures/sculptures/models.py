from django.db import models
from django.contrib.auth.models import User

class Sculpture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_code = models.CharField(max_length=36, unique=True)
    image = models.ImageField(upload_to='sculptures/')
    animal_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal_type} - {self.unique_code}"
