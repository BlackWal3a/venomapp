from django.contrib import admin
from .models import Invoice, UnitConversion, DeliveryOrder
from import_export.admin import ImportExportModelAdmin  
from import_export import resources
  
class InvoiceResource(resources.ModelResource):

    class Meta:
        model = Invoice
        fields = ('Id', 'Code', 'StartDate', 'EndDate', 'TotalQuantity', 'AmountTaxFree', 'AmountIncludingTax', 'TaxesAmount', 'NumberDeliveryOrder', 'InvoiceNature', 'CurrencyCode', 'Currency', 'UnitCode', 'Unit', 'UnitType', 'ConsumerCode', 'Consumer', 'ProviderCode', 'Provider', 'Address', 'Phone', 'Fax', 'Mail', 'RefuelingPointCode', 'RefuelingPoint', 'StopOverCode', 'StopOver', 'TownCode', 'Town', 'CountryCode', 'Country')
  # Include 'Id' field in the list of fields
        import_id_fields = ['Id']  # Specify the 'Id' field as the primary key during import

# Register your resource with admin
class InvoiceAdmin(ImportExportModelAdmin):
    resource_class = InvoiceResource
    list_display = ['Id', 'Code', 'StartDate', 'EndDate', 'TotalQuantity', 'AmountTaxFree', 'AmountIncludingTax', 'TaxesAmount', 'NumberDeliveryOrder', 'InvoiceNature', 'CurrencyCode', 'Currency', 'UnitCode', 'Unit', 'UnitType', 'ConsumerCode', 'Consumer', 'ProviderCode', 'Provider', 'Address', 'Phone', 'Fax', 'Mail', 'RefuelingPointCode', 'RefuelingPoint', 'StopOverCode', 'StopOver', 'TownCode', 'Town', 'CountryCode', 'Country']
    
   #Create import UnitConversion 
   
class UnitConversionResource(resources.ModelResource):

    class Meta:
        model = UnitConversion
        fields = ('Id', 'Value', 'FromCode', 'FromName', 'ToCode', 'ToName')
  # Include 'Id' field in the list of fields
        import_id_fields = ['Id']  # Specify the 'Id' field as the primary key during import

# Register your resource with admin
class UnitConversionAdmin(ImportExportModelAdmin):
    resource_class = UnitConversionResource
    list_display = ['Id', 'Value', 'FromCode', 'FromName', 'ToCode', 'ToName']
       
    #Create import UnitConversion 

class DeliveryOrderResource(resources.ModelResource):

    class Meta:
        model = DeliveryOrder
        fields = ('Id','Code', 'Quantity', 'StartOperation', 'StopOperation', 'FlightsDate', 'AircraftCode','Aircraft', 'ProviderCode', 'Provider', 'UnitCode', 'Unit', 'StopOverCode','StopOver', 'TownCode', 'Town','CountryCode', 'Country')
        import_id_fields = ['Id']  # Specify 'Code' as the primary key during import

# Register your resource with admin
class DeliveryOrderAdmin(ImportExportModelAdmin):
    resource_class = DeliveryOrderResource
    list_display = ['Id','Code', 'Quantity', 'StartOperation', 'StopOperation', 'FlightsDate', 'AircraftCode','Aircraft', 'ProviderCode', 'Provider', 'UnitCode', 'Unit', 'StopOverCode','StopOver', 'TownCode', 'Town','CountryCode', 'Country']
       
admin.site.register(UnitConversion, UnitConversionAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(DeliveryOrder,DeliveryOrderAdmin)
