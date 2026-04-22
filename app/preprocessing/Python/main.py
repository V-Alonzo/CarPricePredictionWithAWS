import pandas as pd
from utils.cleansing.DataCleaner import cleanData
from utils.JSONBuilder import buildJSON
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import pandas as pd

from scipy.stats import spearmanr

carsDataframe = pd.read_csv("app/preprocessing/Python/data/CarPricePrediction.csv")

numberOfFolds = 3
percentage = 1 / numberOfFolds
increment = int(carsDataframe.index.size * percentage)
folds = []
start = 0
end = increment

for fold in range(1, numberOfFolds + 1):
    if fold == numberOfFolds:
        end = carsDataframe.index.size
    foldDataframe = carsDataframe.iloc[start:end].copy()
    folds.append(foldDataframe)
    start = end
    end += increment


bestR2 = 0
bestTestIndex = 0
bestModel = None

for testIndex in range(numberOfFolds):
    testDataframe = folds[testIndex]
    trainDataframe = pd.concat([folds[i] for i in range(numberOfFolds) if i != testIndex], axis=0)

    transformationFormulas = ""

    trainDataframe, testDataframe = cleanData(trainDataframe, testDataframe)

    cleanedDataframe = pd.concat([trainDataframe, testDataframe], axis=0)

    scaledVariablesTrain = trainDataframe[[column for column in trainDataframe.columns if column.endswith("_scaled") or column == "isTurbo" or column == "Price"]]

    print(scaledVariablesTrain.columns.tolist())
    scaledVariablesTest = testDataframe[[column for column in testDataframe.columns if column.endswith("_scaled") or column == "isTurbo" or column == "Price"]]

    xgb_model = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=1000,
        learning_rate=0.04,
        max_depth=10,
        min_child_weight=3,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=0.1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=0,
        n_jobs=-1
    )

    xgb_model.fit(scaledVariablesTrain.drop(columns=["Price"]), scaledVariablesTrain["Price"])
    xgb_test_r2 = xgb_model.score(scaledVariablesTest.drop(columns=["Price"]), scaledVariablesTest["Price"])

    print(f"Fold {testIndex + 1} - Test R2: {xgb_test_r2:.4f}")

    if xgb_test_r2 > bestR2:
        bestR2 = xgb_test_r2
        bestTestIndex = testIndex
        bestModel = xgb_model

print("-"*50)

print(f"\nMejor fold: {bestTestIndex + 1} con R2: {bestR2:.4f}")

bestTrainDataframe = pd.concat([folds[i] for i in range(numberOfFolds) if i != bestTestIndex], axis=0)
bestTestDataframe = folds[bestTestIndex]

bestTrainDataframe, bestTestDataframe = cleanData(bestTrainDataframe, bestTestDataframe)

buildJSON(pd.concat([bestTrainDataframe, bestTestDataframe], axis=0), "app/preprocessing/Python/data/JSON/Database.json", ["Levy","Mileage","Prod. year", "Airbags", "Cylinders","Engine volume"])

bestModel.save_model("app/preprocessing/Python/data/JSON/model.json")

featureColumns = [
    column
    for column in bestTrainDataframe.columns
    if column.endswith("_scaled") or column == "isTurbo"
]


bestValidationDataFrame = bestTestDataframe.sample(frac=0.5, random_state=42)
bestTestDataframe = bestTestDataframe.drop(bestValidationDataFrame.index)


validationDataframes = {"Validation": bestValidationDataFrame, "Train": bestTrainDataframe, "Test": bestTestDataframe}

for dataframesValidationKey in validationDataframes:
    dataframeValidation = validationDataframes[dataframesValidationKey]
    preds = xgb_model.predict(dataframeValidation[featureColumns])
    correlation, p_value = spearmanr(dataframeValidation["Price"], preds)
    mse = mean_squared_error(dataframeValidation["Price"], preds)

    print(f"Best spearman value on {dataframesValidationKey}: {correlation}")
    print(f"Best MSE on {dataframesValidationKey}: {mse}")
    print(f"Best RMSE on {dataframesValidationKey}: {mse**(1/2)}")
    print("-"*20)



singleRowForPrediction = bestTestDataframe[featureColumns].iloc[[0]]
with pd.option_context('display.max_columns', None):
    print(singleRowForPrediction)
singlePrediction = bestModel.predict(singleRowForPrediction)[0]

print(f"Prediccion unica (fila 0 del test): {singlePrediction:.2f}")