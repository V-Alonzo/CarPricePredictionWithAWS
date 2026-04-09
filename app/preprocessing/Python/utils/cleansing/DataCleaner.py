import pandas as pd
from pandas import DataFrame
from utils.cleansing.CleaningFunctions import CLEAN_FUNCTIONS_MAPPING

CATEGORIES = ["Manufacturer","Model","Category","Fuel type","Gear box type","Drive wheels","Doors","Wheel","Color", "Leather interior"]
NUMERICAL_COLUMNS = ["Levy","Prod. year","Engine volume","Mileage", "Cylinders","Airbags"]
TARGET_COLUMN = "Price"

def SCALER_FUNCTION(data, minValue = None, maxValue = None, printFormula = False, columnName = None):
    minValue = data.min() if minValue is None else minValue
    maxValue = data.max() if maxValue is None else maxValue

    if printFormula:
        columnToPrint = data.name if columnName is None else columnName
        print(f'"{columnToPrint.replace("_cleaned", "")}" : (x : number) => (x - {minValue}) / ({maxValue} - {minValue}),')

    if pd.isna(minValue) or pd.isna(maxValue) or maxValue == minValue:
        return pd.Series(0.0, index=data.index)

    return (data - minValue) / (maxValue - minValue)

def standarizeCategoricalData(data : DataFrame) -> DataFrame:    
    scaledDataframe = pd.factorize(data)[0]
    scaledDataframe = SCALER_FUNCTION(scaledDataframe)
    return scaledDataframe

def performSmoothTargetEncoding(data : DataFrame, column : str, smoothingParamenter : int = 10) -> tuple[DataFrame, float]:
    #Calculate the global mean of the target variable
        globalMean = data[TARGET_COLUMN].mean()

        # Aggregation: count and mean for each category in the categorical column
        agg = data.groupby(column)[TARGET_COLUMN].agg(["count", "mean"])
        counts = agg["count"]
        means = agg["mean"]

        #Calculate smoothed means.
        smoothedMeans = (counts * means + smoothingParamenter * globalMean) / (counts + smoothingParamenter)

        #Return the results
        return smoothedMeans, globalMean


def _prepareFeatureColumns(data : DataFrame) -> tuple[DataFrame, DataFrame]:
    categoricalInformation = data[CATEGORIES].copy()
    numericalInformation = data[NUMERICAL_COLUMNS].copy()

    for column in CATEGORIES:
        cleanedColumnName = column + "_cleaned"

        if column in CLEAN_FUNCTIONS_MAPPING:
            categoricalInformation[cleanedColumnName] = CLEAN_FUNCTIONS_MAPPING[column](categoricalInformation)
        else:
            print(f"No cleaning function defined for column: {column}")

    for column in NUMERICAL_COLUMNS:
        cleanedColumnName = column + "_cleaned"

        if column in CLEAN_FUNCTIONS_MAPPING:
            numericalInformation[cleanedColumnName] = CLEAN_FUNCTIONS_MAPPING[column](numericalInformation)
        elif column == "Engine volume":
            isTurbo = numericalInformation[column].str.contains("T", case=False, na=False)
            numericalInformation[cleanedColumnName] = numericalInformation[column].str.replace(r'[^0-9.]', '', regex=True).str.strip()
            numericalInformation["isTurbo"] = isTurbo.astype(int)
        elif column == "Levy":
            numericalInformation[cleanedColumnName] = numericalInformation[column].str.replace(r'-', '0', regex=False).str.strip()
        else:
            print(f"No cleaning function defined for column: {column}")
            numericalInformation[cleanedColumnName] = numericalInformation[column]

        try:
            numericalInformation[cleanedColumnName] = pd.to_numeric(numericalInformation[cleanedColumnName], errors='coerce')
        except KeyError:
            numericalInformation[column] = pd.to_numeric(numericalInformation[column], errors='coerce')

    return categoricalInformation, numericalInformation

def removeOutliers(data : DataFrame, column : str) -> DataFrame:
    initial_rows = len(data)
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    dataframe = data[
        (data[column] >= lower_bound) & (data[column] <= upper_bound)
    ].copy()

    removed_rows = initial_rows - len(dataframe)
    print(
        f"Filas originales: {initial_rows}, Filas eliminadas por outlier en {column}: {removed_rows}, "
        f"Filas restantes: {len(dataframe)}"
    )
    return dataframe


def cleanData(trainData : DataFrame, testData : DataFrame) -> tuple[DataFrame, DataFrame]:
    trainCategoricalInformation, trainNumericalInformation = _prepareFeatureColumns(trainData)
    testCategoricalInformation, testNumericalInformation = _prepareFeatureColumns(testData)

    for column in CATEGORIES:
        cleanedColumnName = column + "_cleaned"

        encodingData = pd.concat(
            [trainCategoricalInformation[cleanedColumnName], trainData[TARGET_COLUMN]],
            axis=1,
        )
        smoothedMeans, globalMean = performSmoothTargetEncoding(encodingData, cleanedColumnName)

        trainCategoricalInformation[column + "_scaled"] = trainCategoricalInformation[cleanedColumnName].map(smoothedMeans).fillna(globalMean)
        testCategoricalInformation[column + "_scaled"] = testCategoricalInformation[cleanedColumnName].map(smoothedMeans).fillna(globalMean)


    for column in NUMERICAL_COLUMNS:
        cleanedColumnName = column + "_cleaned"
        minValue = trainNumericalInformation[cleanedColumnName].min()
        maxValue = trainNumericalInformation[cleanedColumnName].max()

        trainNumericalInformation[column + "_scaled"] = SCALER_FUNCTION(
            trainNumericalInformation[cleanedColumnName],
            minValue=minValue,
            maxValue=maxValue,
            printFormula=True,
            columnName=cleanedColumnName,
        )

        testNumericalInformation[column + "_scaled"] = SCALER_FUNCTION(
            testNumericalInformation[cleanedColumnName],
            minValue=minValue,
            maxValue=maxValue,
            printFormula=False,
            columnName=cleanedColumnName,
        )

    cleanedTrainDataframe = pd.concat(
        [trainCategoricalInformation, trainNumericalInformation, trainData[TARGET_COLUMN]],
        axis=1,
    )
    cleanedTestDataframe = pd.concat(
        [testCategoricalInformation, testNumericalInformation, testData[TARGET_COLUMN]],
        axis=1,
    )

    cleanedTrainDataframe = removeOutliers(cleanedTrainDataframe, TARGET_COLUMN)
    cleanedTestDataframe = removeOutliers(cleanedTestDataframe, TARGET_COLUMN)

    cleanedTrainDataframe.to_csv("data/cleanedTrainCarPricePrediction.csv", index=False, float_format='%.7f')
    cleanedTestDataframe.to_csv("data/cleanedTestCarPricePrediction.csv", index=False, float_format='%.7f')
    pd.concat([cleanedTrainDataframe, cleanedTestDataframe], axis=0).to_csv(
        "data/cleanedCarPricePrediction.csv", index=False, float_format='%.7f'
    )

    return cleanedTrainDataframe, cleanedTestDataframe
