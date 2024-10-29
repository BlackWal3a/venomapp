from django.db import models
from django.contrib.auth.models import User 


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    units = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    dark_mode = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_geo_date = models.DateField(blank=True, null=True)
    end_geo_date = models.DateField(blank=True, null=True)
    start_supplier_date = models.DateField(blank=True, null=True)
    end_supplier_date = models.DateField(blank=True, null=True)
    is_selected = models.BooleanField(default=False)
    provider1 = models.CharField(max_length=50, blank=True, null=True)
    provider2 = models.CharField(max_length=50, blank=True, null=True)
    rates = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  # New field for notes
    update1 = models.CharField(max_length=50, blank=True, null=True)
    suppliers_global_selection = models.IntegerField(blank=True, null=True)
    supplier_name_filter = models.CharField(max_length=100, blank=True, null=True)
    geography_global_selection = models.IntegerField(blank=True, null=True)
    time_global_selection = models.IntegerField(blank=True, null=True)
    time_by_filter = models.IntegerField(blank=True, null=True)
    time_chart_type = models.IntegerField(blank=True, null=True)
    aircraft_chart_type = models.IntegerField(blank=True, null=True)
    geography_filter_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
from django.db import models

class NormalUser(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # This would store plain text passwords, which is not recommended!

    def __str__(self):
        return self.username

from django.db import models
from django.contrib.auth.models import User

class BiteReport(models.Model):
    username = models.CharField(max_length=255, unique=True)
    place_of_bite = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    date = models.DateField()
    time_since_bite = models.CharField(max_length=100)  # You can choose a different field type depending on the input format
    symptom = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.place_of_bite

from django.contrib.auth.models import User

class EmergencyData(models.Model):
    username = models.CharField(max_length=255)
    nom_complet = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    sexe = models.CharField(max_length=10)
    poids = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    taille = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    date_heure_envenimation = models.CharField(max_length=255)
    lieu_envenimation = models.CharField(max_length=255)
    activite = models.CharField(max_length=255)
    lieu_morsure = models.CharField(max_length=255)
    nombre_morsures = models.IntegerField(null=True, blank=True)
    recidivistes = models.CharField(max_length=255)
    type_animal = models.CharField(max_length=255)
    taille_animal = models.CharField(max_length=255, blank=True, null=True)
    couleur_animal = models.CharField(max_length=255, blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pression = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    clinical_symptoms = models.TextField(null=True, blank=True)
    action_message = models.TextField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    antecedents = models.TextField(null=True, blank=True)
    animal_image = models.ImageField(upload_to='animal_images/', null=True, blank=True)  # New field

    def __str__(self):
        return f"Emergency data for {self.nom_complet}"

