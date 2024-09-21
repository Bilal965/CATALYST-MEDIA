from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    founded_year = models.IntegerField(null=True, blank=True,db_index=True)
    industry = models.CharField(max_length=255,db_index=True)
    country = models.CharField(max_length=255,db_index=True)
    domain = models.CharField(max_length=255,db_index=True)
    linkedin_url = models.CharField(max_length=255,db_index=True)
    locality= models.CharField(max_length=255,db_index=True)
    current_employee_estimate=models.IntegerField(null=True, blank=True,db_index=True)
    total_employee_estimate=models.IntegerField(null=True, blank=True,db_index=True)      

    def __str__(self):
        return self.name
class User(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name
