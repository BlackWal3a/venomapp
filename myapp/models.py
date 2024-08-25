from django.db import models

class UnitConversion(models.Model):
    Id = models.IntegerField(primary_key=True)
    Value = models.DecimalField(max_digits=50,decimal_places=20)
    FromCode = models.CharField(max_length=100)
    FromName = models.CharField(max_length=100)
    ToCode = models.CharField(max_length=100)
    ToName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.FromCode  # You can choose any field to represent the object in string format


class Invoice(models.Model):
    Id = models.IntegerField(primary_key=True)
    Code = models.CharField(max_length=100, null=True)
    StartDate = models.CharField(max_length=100)  # Allowed null values for dates
    EndDate = models.CharField(max_length=100)    # Allowed null values for dates
    TotalQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    AmountTaxFree = models.DecimalField(max_digits=10, decimal_places=2)
    AmountIncludingTax = models.DecimalField(max_digits=10, decimal_places=2)
    TaxesAmount = models.DecimalField(max_digits=10, decimal_places=2)
    NumberDeliveryOrder = models.CharField(max_length=100)
    InvoiceNature = models.CharField(max_length=100)
    CurrencyCode = models.CharField(max_length=10)
    Currency = models.CharField(max_length=100)
    UnitCode = models.CharField(max_length=100)
    Unit = models.CharField(max_length=100)
    UnitType = models.CharField(max_length=100)
    ConsumerCode = models.CharField(max_length=100)
    Consumer = models.CharField(max_length=100)
    ProviderCode = models.CharField(max_length=100)
    Provider = models.CharField(max_length=100)
    Address = models.CharField(max_length=255, null=True)
    Phone = models.CharField(max_length=20, null=True)
    Fax = models.CharField(max_length=20, null=True)
    Mail = models.EmailField(null=True)
    RefuelingPointCode = models.CharField(max_length=100, null=True)
    RefuelingPoint = models.CharField(max_length=100, null=True)
    StopOverCode = models.CharField(max_length=100, null=True)
    StopOver = models.CharField(max_length=100, null=True)
    TownCode = models.CharField(max_length=100, null=True)
    Town = models.CharField(max_length=100, null=True)
    CountryCode = models.CharField(max_length=100, null=True)
    Country = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Code  # You can choose any field to represent the object in string format

class DeliveryOrder(models.Model):
    Id = models.IntegerField(primary_key=True)
    Code = models.CharField(max_length=100, null=True)
    Quantity = models.DecimalField(max_digits=10, decimal_places=2)
    StartOperation = models.CharField(max_length=100)  # Allowed null values for dates
    StopOperation = models.CharField(max_length=100)  # Allowed null values for dates
    FlightsDate = models.CharField(max_length = 100)
    AircraftCode = models.CharField(max_length=100, null=True)
    Aircraft = models.CharField(max_length=100, null=True)
    ProviderCode = models.CharField(max_length=100, null=True)
    Provider = models.CharField(max_length=100, null=True)
    UnitCode = models.CharField(max_length=100)
    Unit = models.CharField(max_length=100)
    StopOverCode = models.CharField(max_length=100, null=True)
    StopOver = models.CharField(max_length=100, null=True)
    TownCode = models.CharField(max_length=100, null=True)
    Town = models.CharField(max_length=100, null=True)
    CountryCode = models.CharField(max_length=100, null=True)
    Country = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Code  # You can choose any field to represent the object in string format