from decimal import Decimal
from .models import UnitConversion

def convert_quantity(quantity, from_unit_code, to_unit_code):
    # Convert quantity to Decimal if it's not already
    if not isinstance(quantity, Decimal):
        quantity = Decimal(quantity)
    
    # If from_unit_code is equal to to_unit_code, no conversion needed
    if from_unit_code == to_unit_code or from_unit_code == 'OPS':
        return float(quantity)
    # Retrieve the conversion rate from the database
    try:
        conversion = UnitConversion.objects.get(FromCode=from_unit_code, ToCode=to_unit_code)
    except UnitConversion.DoesNotExist:
        raise ValueError("Conversion rate not found for provided units")

    # Calculate the converted quantity
    converted_quantity = float(quantity * Decimal(conversion.Value))

    return converted_quantity

