from django.db import models
from datetime import date 

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Employee(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_joining = models.DateField(default=date.today)