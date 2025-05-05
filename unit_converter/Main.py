from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

def convert_length(value, from_unit, to_unit):
    units = {
        'millimeter': 1000,
        'centimeter': 100,
        'meter': 1,
        'kilometer': 0.001,
        'inch': 39.3701,
        'foot': 3.28084,
        'yard': 1.09361,
        'mile': 0.000621371
    }
    value_in_meters = value / units[from_unit]
    return value_in_meters * units[to_unit]

def convert_weight(value, from_unit, to_unit):
    units = {
        'milligram': 1000,
        'gram': 1,
        'kilogram': 0.001,
        'ounce': 0.035274,
        'pound': 0.00220462
    }
    value_in_grams = value / units[from_unit]
    return value_in_grams * units[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'Celsius' and to_unit == 'Fahrenheit':
        return (value * 9/5) + 32
    elif from_unit == 'Celsius' and to_unit == 'Kelvin':
        return value + 273.15
    elif from_unit == 'Fahrenheit' and to_unit == 'Celsius':
        return (value - 32) * 5/9
    elif from_unit == 'Fahrenheit' and to_unit == 'Kelvin':
        return (value - 32) * 5/9 + 273.15
    elif from_unit == 'Kelvin' and to_unit == 'Celsius':
        return value - 273.15
    elif from_unit == 'Kelvin' and to_unit == 'Fahrenheit':
        return (value - 273.15) * 9/5 + 32
    else:
        return value


class ConversionRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    unit_type: str


@app.post("/convert")
async def convert(data: ConversionRequest):
    value = data.value
    from_unit = data.from_unit
    to_unit = data.to_unit
    unit_type = data.unit_type

    if unit_type == 'length':
        result = convert_length(value, from_unit, to_unit)
    elif unit_type == 'weight':
        result = convert_weight(value, from_unit, to_unit)
    elif unit_type == 'temperature':
        result = convert_temperature(value, from_unit, to_unit)
    else:
        return {"error": "Invalid unit type"}

    return {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "converted_value": result
    }
