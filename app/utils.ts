const transformFunctions = {
    "Levy" : (x : number) => (x - 0) / (11714 - 0),
    "Prod. year" : (x : number) => (x - 1943) / (2020 - 1943),
    "Engine volume" : (x : number) => (x - 0.0) / (20.0 - 0.0),
    "Mileage" : (x : number) => (x - 0) / (2147483647 - 0),
    "Cylinders" : (x : number) => (x - 1.0) / (16.0 - 1.0),
    "Airbags" : (x : number) => (x - 0) / (16 - 0)
}

export default transformFunctions;