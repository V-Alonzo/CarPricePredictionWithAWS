"use client";

import { ChangeEvent, SubmitEventHandler, useEffect, useState } from "react";
import transformFunctions from "./utils";
import DATABASE from "./data/JSON/Database.json";


export default function Home() {

  const [formData, setFormData] = useState({
    Manufacturer: {
      inputValue: "",
      transformation: null
    },
    Model: {
      inputValue: "",
      transformation: null
    },
    category: {
      inputValue: "",
      transformation: null
    },
    fuelType: {
      inputValue: "",
      transformation: null
    },
    gearBoxType: {
      inputValue: "",
      transformation: null
    },
    driveWheels: {
      inputValue: "",
      transformation: null
    },
    doors: {
      inputValue: "",
      transformation: null
    },
    wheel: {
      inputValue: "",
      transformation: null
    },
    color: {
      inputValue: "",
      transformation: null
    },
    leatherInterior: {
      inputValue: "",
      transformation: null
    },
    isTurbo: {
      inputValue: "",
      transformation: null
    },
    levy: {
      inputValue: "",
      transformation: null
    },
    prodYear: {
      inputValue: "",
      transformation: null
    },
    engineVolume: {
      inputValue: "",
      transformation: null
    },
    mileage: {
      inputValue: "",
      transformation: null
    },
    cylinders: {
      inputValue: "",
      transformation: null
    },
    airbags: {
      inputValue: "",
      transformation: null
    },
  });

  useEffect(() => {
    console.log(formData);
  }, [formData]);

  const sortingFunctionNumbers = ([, a]: [string, { label: string }], [, b]: [string, { label: string }]) => {
    const numA = parseFloat(a.label);
    const numB = parseFloat(b.label);
    return numA - numB;
  };

  const sortingFunctionLabels = ([, a]: [string, { label: string }], [, b]: [string, { label: string }]) => {
    return a.label.localeCompare(b.label);
  }

  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    let { name, value } = event.target;
    let valueTransformed = null;

    if(Object.keys(transformFunctions).includes(name)) {
      if (value != "") valueTransformed = transformFunctions[name as keyof typeof transformFunctions](parseFloat(value)).toString();
    }
    else valueTransformed = value;
    

    if(name.toLowerCase() == "manufacturer" || name.toLowerCase() == "model") {
      const found = Object.entries(DATABASE[name as keyof typeof DATABASE])
        .find(([, data]) => data.label === value.toUpperCase());
      
      if (found) {
        valueTransformed = found[1].scaled;
      }
    }

    setFormData((previous) => ({ ...previous, [name]: { inputValue: value, transformation: valueTransformed} }));
  };

    const getFromAPI = async () => {
    try {
      const url = new URL("https://5twbrv3ft9.execute-api.us-east-2.amazonaws.com/default/xgb-lambda-docker");

      const response = await fetch(url.toString(),{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData)
      });

      const text = await response.text(); 

      if (!response.ok) {
        console.error("Backend error response:", text);
        throw new Error(`HTTP ${response.status}`);
      }

      let data;
      try {
        data = JSON.parse(text);
      } catch {
        throw new Error("Invalid JSON response");
      }

      if (data.error) {
        throw new Error(data.error);
      }

      const predictedPrice = Number(data.result).toFixed(2);

      alert(`El precio estimado del vehículo es: $${predictedPrice}`);

    } catch (error) {
      console.error("Error fetching data:", error);

      alert("Failed to fetch conversion result.");
    }
  };

  const handleSubmit: SubmitEventHandler<HTMLFormElement> = (event) => {
    event.preventDefault();
    getFromAPI();
  };

  const baseFieldClass =
    "mt-2 h-11 w-full rounded-xl border border-white/40 bg-white/80 px-3 text-sm text-slate-900 shadow-[0_8px_30px_rgba(2,132,199,0.12)] outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-300/50";

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#44ccf2] px-4 py-10 sm:px-8">
      <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(rgba(15,23,42,0.06)_1px,transparent_1px),linear-gradient(90deg,rgba(15,23,42,0.06)_1px,transparent_1px)] bg-[size:34px_34px]" />

      <main className="relative mx-auto w-full max-w-9xl rounded-3xl border border-white/60 bg-white/35 p-5 shadow-[0_24px_100px_rgba(14,116,144,0.2)] backdrop-blur-xl sm:p-8">
        <header className="mb-8 flex flex-col gap-4 sm:mb-10">
          <h1 className="max-w-6xl text-3xl font-black tracking-tight text-slate-900 sm:text-5xl">
            Actividad 1: Predicción de Precios de Vehículos
          </h1>
        </header>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            <label className="text-sm font-semibold text-slate-800">
              Airbags
              <input
                type="number"
                step="0.1"
                min="0"
                name="airbags"
                value={formData.airbags.inputValue}
                onChange={handleChange}
                placeholder="Ejemplo: 2"
                className={baseFieldClass}
              />
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Categoría
              <select
                name="category"
                value={formData.category.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Elige la categoría del vehiculo</option>
                {Object.entries(DATABASE.Category)
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.scaled}>
                      {value.label}
                    </option>
                  ))}
              </select>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Color
              <select
                name="color"
                value={formData.color.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Selecciona el color principal</option>
                {Object.entries(DATABASE.Color)
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.scaled}>
                      {value.label}
                    </option>
                  ))}
              </select>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Cylinders
              <input
                type="number"
                step="0.1"
                min="0"
                name="cylinders"
                value={formData.cylinders.inputValue}
                onChange={handleChange}
                placeholder="Ejemplo: 4"
                className={baseFieldClass}
              />
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Doors
              <select
                name="doors"
                value={formData.doors.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Cuantas puertas tiene</option>
                {Object.entries(DATABASE.Doors)
                  .sort(sortingFunctionNumbers)
                  .map(([key, value]) => (
                    <option key={key} value={value.scaled}>
                      {value.label}
                    </option>
                  ))}
              </select>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Drive wheels
              <select
                name="driveWheels"
                value={formData.driveWheels.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Tipo de traccion</option>
                {Object.entries(DATABASE["Drive wheels"])
                    .sort(sortingFunctionLabels)
                    .map(([key, value]) => (
                      <option key={key} value={value.scaled}>
                        {value.label}
                      </option>
                    ))}
              </select>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Engine volume
              <input
                type="number"
                step="0.1"
                min="0"
                name="engineVolume"
                value={formData.engineVolume.inputValue}
                onChange={handleChange}
                placeholder="Ejemplo: 2.0"
                className={baseFieldClass}
              />
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Fuel Type
              <select
                name="fuelType"
                value={formData.fuelType.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Selecciona el tipo de combustible</option>
                {Object.entries(DATABASE["Fuel type"])
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.scaled}>
                      {value.label}
                    </option>
                  ))}
              </select>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Gear box type
              <select
                name="gearBoxType"
                value={formData.gearBoxType.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Tipo de caja de cambios</option>
                {Object.entries(DATABASE["Gear box type"])
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.scaled}>
                      {value.label}
                    </option>
                  ))}
              </select>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              isTurbo
              <select
                name="isTurbo"
                value={formData.isTurbo.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Selecciona una opción</option>
                {Object.entries(DATABASE.isTurbo)
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.scaled}>
                      {value.label}
                    </option>
                  ))}
              </select>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              LeatherInterior
              <select
                name="leatherInterior"
                value={formData.leatherInterior.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Selecciona una opción</option>
                {Object.entries(DATABASE["Leather interior"])
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.scaled}>
                      {value.label}
                    </option>
                  ))}
              </select>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Levy
              <input
                type="number"
                min="0"
                step="0.1"
                name="levy"
                value={formData.levy.inputValue}
                onChange={handleChange}
                placeholder="Ejemplo: 1200"
                className={baseFieldClass}
              />
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Manufacturer
              <input
                type="text"
                name="Manufacturer"
                value={formData.Manufacturer.inputValue}
                onChange={handleChange}
                placeholder="Escribe o selecciona fabricante"
                autoComplete="off"
                list="manufacturer-suggestions"
                className={baseFieldClass}
              />
              <datalist id="manufacturer-suggestions">
                {Object.entries(DATABASE["Manufacturer"])
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.label}>
                      {value.scaled}
                    </option>
                  ))}
              </datalist>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Mileage
              <input
                type="number"
                min="0"
                step="1"
                name="mileage"
                value={formData.mileage.inputValue}
                onChange={handleChange}
                placeholder="Kilometraje total, por ejemplo 85000"
                className={baseFieldClass}
              />
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Model
              <input
                type="text"
                name="Model"
                value={formData.Model.inputValue}
                onChange={handleChange}
                placeholder="Modelo del vehículo"
                autoComplete="off"
                list="model-suggestions"
                className={baseFieldClass}
              />
              <datalist id="model-suggestions">
                {Object.entries(DATABASE.Model)
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.label}>
                      {value.scaled}
                    </option>
                  ))}
              </datalist>
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Prod. year
              <input
                type="number"
                step="1"
                name="prodYear"
                value={formData.prodYear.inputValue}
                onChange={handleChange}
                placeholder="Año de fabricacion"
                className={baseFieldClass}
              />
            </label>

            <label className="text-sm font-semibold text-slate-800">
              Wheel
              <select
                name="wheel"
                value={formData.wheel.inputValue}
                onChange={handleChange}
                className={baseFieldClass}
              >
                <option value="">Posicion del volante</option>
                {Object.entries(DATABASE.Wheel)
                  .sort(sortingFunctionLabels)
                  .map(([key, value]) => (
                    <option key={key} value={value.scaled}>
                      {value.label}
                    </option>
                  ))}
              </select>
            </label>
          </div>

          <div className="flex flex-col gap-4 rounded-2xl border border-cyan-300/40 bg-white/70 p-4 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-sm text-slate-700">
              Presiona el botón para realizar la predicción
            </p>
            <button
              type="submit"
              className="h-11 rounded-xl bg-[#44aff2] px-6 text-sm font-bold text-white transition hover:scale-[1.02] hover:shadow-[0_12px_28px_rgba(8,145,178,0.35)]"
            >
              Estimar precio
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
