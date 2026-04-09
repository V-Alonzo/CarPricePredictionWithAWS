import json
from xgboost import XGBRegressor

model = XGBRegressor()
model.load_model("model2.json")

def lambda_handler(event, context):
    try:
        print("EVENT:", event)

        body = event.get("body")

        if body is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing request body"})
            }

        if isinstance(body, str):
            params = json.loads(body)
        else:
            params = body

        keysParamsOrder = [
            "Manufacturer","Model","category","fuelType","gearBoxType",
            "driveWheels","doors","wheel","color","leatherInterior",
            "isTurbo","levy","prodYear","engineVolume","mileage",
            "cylinders","airbags"
        ]

        paramsArray = [
            float(params[param]["transformation"]) 
            for param in keysParamsOrder
        ]

        result = model.predict([paramsArray])[0]

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({
                "result": float(result)
            })
        }

    except Exception as e:
        import traceback
        print("ERROR:", str(e))
        print(traceback.format_exc())

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({"error": str(e)})
        }