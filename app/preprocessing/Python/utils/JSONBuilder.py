import pandas as pd
import json
import os


def _to_json_value(value):
    if isinstance(value, pd.Series):
        if value.empty:
            return None
        value = value.iloc[0]

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        value = value.item()
        
    if isinstance(value, (int, float)):
        value = float(value)
        
        if(value.is_integer()):
            return f"{value:.0f}"
        
        return f"{value:.7f}"

    return value



def buildJSON(data: pd.DataFrame, outputFilePath: str, ignoreColumns : list[str] = []) -> None:
    columns = list(filter(lambda col: col not in ignoreColumns, data.columns.tolist()))
    
    database = {}

    for column in columns:
        if column.endswith("_scaled") or column.endswith("_cleaned") or column == "Price":
            continue

        cleaned_column = f"{column}_cleaned"
        scaled_column = f"{column}_scaled"

        label_source = cleaned_column if cleaned_column in columns else column
        scaled_source = scaled_column if scaled_column in columns else column
        turbo_source = None

        if column == "Engine volume":
            turbo_source = "isTurbo"

        if label_source == scaled_source:
            pairs = data[[label_source]].drop_duplicates(keep="first").reset_index(drop=True)
        else:
            pairs = (
                data[[label_source, scaled_source]]
                .drop_duplicates(subset=[label_source], keep="first")
                .reset_index(drop=True)
            )

        if turbo_source is not None:
            pairs = (
                data[[label_source, scaled_source, turbo_source]]
                .drop_duplicates(subset=[label_source], keep="first")
                .reset_index(drop=True)
            )

        database[column] = {}

        if(column == "isTurbo" or column == "Leather interior"):
            database[column] = {
                "0": {"label": "No", "scaled": "0"},
                "1": {"label": "Sí", "scaled": "1"}
            }
            continue
        
        for index, row in pairs.iterrows():
            label_value = row[label_source]
            scaled_value = row[scaled_source] if scaled_source in row.index else label_value

            database[column][str(index)] = {
                "label": _to_json_value(label_value),
                "scaled": _to_json_value(scaled_value),
            }

            if turbo_source is not None:
                database[column][str(index)]["isTurbo"] = _to_json_value(row[turbo_source])

    with open(outputFilePath, "w", encoding="utf-8") as jsonFile:
            json.dump(database, jsonFile, indent=4)