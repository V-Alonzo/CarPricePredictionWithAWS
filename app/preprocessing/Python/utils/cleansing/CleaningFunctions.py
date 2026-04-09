from pandas import DataFrame

def cleanMileage(data : DataFrame) -> DataFrame:
    mileageDataframe = data["Mileage"]
    mileageDataframe = mileageDataframe.str.replace(r'[^0-9]', '', regex=True).str.strip()
    return mileageDataframe

def cleanColor(data : DataFrame) -> DataFrame:
    colorDataframe = data["Color"]
    colorDataframe = colorDataframe.str.upper()
    return colorDataframe

def cleanWheel(data : DataFrame) -> DataFrame:
    wheelDataframe = data["Wheel"]
    wheelDataframe = wheelDataframe.str.upper()
    return wheelDataframe

def cleanDoors(data : DataFrame) -> DataFrame:
    doorsDataframe = data["Doors"]
    doorsDataframe = doorsDataframe.str.upper()
    doorsDataframe = doorsDataframe.str.replace(r'[^1-9]', ' ', regex=True).str.strip()
    return doorsDataframe

def cleanDriveWheels(data : DataFrame) -> DataFrame:
    driveWheelsDataframe = data["Drive wheels"]
    driveWheelsDataframe = driveWheelsDataframe.str.upper()
    return driveWheelsDataframe

def cleanGearBoxType(data : DataFrame) -> DataFrame:
    gearBoxTypeDataframe = data["Gear box type"]    
    gearBoxTypeDataframe = gearBoxTypeDataframe.str.upper()
    return gearBoxTypeDataframe

def cleanFuelType(data : DataFrame) -> DataFrame:
    fuelTypeDataframe = data["Fuel type"]
    fuelTypeDataframe = fuelTypeDataframe.str.upper()
    return fuelTypeDataframe

def cleanManufacturer(data : DataFrame) -> DataFrame:
    manufacturerDataframe = data["Manufacturer"]
    manufacturerDataframe = manufacturerDataframe.replace("სხვა", "Other")
    return manufacturerDataframe

def cleanCategory(data : DataFrame) -> DataFrame:
    categoryDataframe = data["Category"].str.upper()
    return categoryDataframe

def cleanLeatherInterior(data : DataFrame) -> DataFrame:
    leatherInteriorDataframe = data["Leather interior"]
    leatherInteriorDataframe = leatherInteriorDataframe.str.upper()
    return leatherInteriorDataframe

def cleanModel(data : DataFrame) -> DataFrame:
    modelDataframe = data["Model"]

    #Diccionario de reemplazos (Errores tipográficos y traducciones)
    replacements = {
        r'HYBID|HIBRYD|ჰიბრიდი': 'HYBRID',
        r'PLAGIN': 'PLUG-IN',
        r'KOMPRESOR': 'KOMPRESSOR',
        r'DIZEL|<DIESEL>': 'DIESEL',
        r'ტურბო': 'TURBO',
        r'SUPER!!!': '',
        r'CADI$': '',
        r'GOLF GOLF': 'GOLF'
    }

    #Convertir todo a mayúsculas.
    modelDataframe = modelDataframe.str.upper()

    for pattern, replacement in replacements.items():
        modelDataframe = modelDataframe.str.replace(pattern, replacement, regex=True)
    
    #Se eliminan los caracteres especiales.
    modelDataframe = modelDataframe.str.replace(r'[^A-Z0-9\s\-.]', ' ', regex=True).str.strip()

    #Se eliminan los espacios extra.
    modelDataframe = modelDataframe.str.replace(r'\s+', ' ', regex=True).str.strip()

    return modelDataframe


CLEAN_FUNCTIONS_MAPPING = {
    "Manufacturer": cleanManufacturer,
    "Model": cleanModel,
    "Category": cleanCategory,
    "Fuel type": cleanFuelType,
    "Gear box type": cleanGearBoxType,
    "Drive wheels": cleanDriveWheels,
    "Doors": cleanDoors,
    "Wheel": cleanWheel,
    "Color": cleanColor,
    "Leather interior": cleanLeatherInterior,
    "Mileage": cleanMileage
    }