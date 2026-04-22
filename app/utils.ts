const transformFunctions = {
    "levy" : (x : number) => (x - 0) / (11714 - 0),
    "prodYear" : (x : number) => (x - 1943) / (2020 - 1943),
    "engineVolume" : (x : number) => (x - 0.0) / (20.0 - 0.0),
    "mileage" : (x : number) => (x - 0) / (2147483647 - 0),
    "cylinders" : (x : number) => (x - 1.0) / (16.0 - 1.0),
    "airbags" : (x : number) => (x - 0) / (16 - 0)
}

const regexFunctions = {
    "levy" : /^(?:\d+)(?:\.\d+)?$/,
    "prodYear" : /^[1-9]\d*$/,
    "engineVolume" : /^(?:[1-9]\d*(?:\.\d+)?|0\.\d*[1-9]\d*)$/,
    "mileage" : /^(?:\d+)(?:\.\d+)?$/,
    "cylinders" : /^(?:[1-9]\d*(?:\.\d+)?|0\.\d*[1-9]\d*)$/,
    "airbags" : /^\d+$/
}

export { transformFunctions, regexFunctions };
export default transformFunctions;