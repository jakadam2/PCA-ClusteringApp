import React, { useState, useEffect } from "react";
import { dataHeaderStyle, dropdownListStyle } from "../common/styles";
import NewPageButton from "../components/buttons/NewPageButton";

const ROWS = 10;

const DataTypeEditPage = () => {
  const [data, setData] = useState([]);
  const [normalizationMethods, setNormalizationMethods] = useState([]);
  const typesChanges = {};
  const namesChanges = {};
  const [currNormalizationMethod, setCurrNormalizationMethod] = useState("");

  useEffect(() => {
    const requestDataset = fetch(
      `http://localhost:8000/api/dataset?rows=${ROWS}`
    ).then((res) => res.json());

    const requestDatatypes = fetch(`http://localhost:8000/api/data_types`).then(
      (res) => res.json()
    );

    const requestNormalizationMethods = fetch(
      `http://localhost:8000/api/normalization/methods`
    ).then((res) => res.json());

    Promise.all([
      requestDataset,
      requestDatatypes,
      requestNormalizationMethods,
    ]).then(([dataset, datatypes, normalizationMethods]) => {
      setData({
        dataset: dataset,
        datatypes: datatypes,
      });
      let numNormalizationMethods = normalizationMethods
        .map((method) => {
          if (method.compatible_types.includes("numerical")) {
            return method.name;
          }
          return "";
        })
        .filter((method) => method !== "");
      setCurrNormalizationMethod(numNormalizationMethods[0]);
      setNormalizationMethods(numNormalizationMethods);
    });
  }, []);

  const changeVariableName = (varName, columnId, newName) => {
    const rowId = 0;
    console.log(
      `Header clicked: ${varName}, row: ${rowId}, col: ${columnId}, newName: ${newName}`
    );
    namesChanges[varName] = newName;
  };

  const changeDataType = (header, columnId, newType) => {
    console.log(
      `Data type clicked ${header} col: ${columnId}, changed to: ${newType.target.value}`
    );
    // get data types from backend along with csv file and send changes to back
    typesChanges[header.toString()] = newType.target.value.toString();
  };

  const changeNormalizationMethod = (event) => {
    console.log(`Normalization method changed to: ${event.target.value}`);
    setCurrNormalizationMethod(event.target.value);
  };

  const handleSavingChanges = async () => {
    // send changes that are kept in context
    console.log("Saving...");

    // TODO: check if it's even working correctly
    //Saving column types
    try {
      const response = await fetch(
        "http://localhost:8000/api/dataset/columns_types",
        {
          //mode: "no-cors",
          headers: {
            "Content-Type": "application/json",
            accept: "application/json",
          },
          method: "PUT",
          body: JSON.stringify({ mapping: typesChanges }),
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error saving new data types:", error);
      alert("Error saving new data types.");
    }
    //Saving column names
    try {
      const response = await fetch(
        "http://localhost:8000/api/dataset/columns_names",
        {
          //mode: "no-cors",
          headers: {
            "Content-Type": "application/json",
            accept: "application/json",
          },
          method: "PUT",
          body: JSON.stringify({ mapping: namesChanges }),
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error saving new column names:", error);
      alert("Error saving new column names.");
    }
    //Saving normalization method
    try {
      const response = await fetch("http://localhost:8000/api/normalization", {
        //mode: "no-cors",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        method: "POST",
        body: JSON.stringify([
          { compatible_types: ["numerical"], name: currNormalizationMethod },
        ]),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error saving new column names:", error);
      alert("Error saving new column names.");
    }
  };

  const variables =
    data["dataset"] !== undefined ? data["dataset"]["variables"] : [];
  const headers =
    data["dataset"] !== undefined
      ? data["dataset"]["variables"].map((variable) => variable["name"])
      : [];
  const values = [];
  if (data["dataset"] !== undefined) {
    for (let i = 0; i < ROWS; i++) {
      values.push([]);
    }
    for (let variable of data["dataset"]["variables"]) {
      let i = 0;
      for (let value of variable["values"]) {
        values[i].push(value);
        i++;
      }
    }
  }
  const dataTypes = data["datatypes"] !== undefined ? data["datatypes"] : [];

  return (
    <div className="relative h-[450px]">
      <div className="relative h-96">
        <div className="max-h-80 overflow-scroll bg-main-50 thin-scrollbar w-auto mx-auto">
          <table className="divide-y divide-gray-200 w-full">
            {/* Headers/Variable names */}
            <thead className="bg-main-50">
              <tr>
                {headers.map((header, columnId) => (
                  <th
                    key={header}
                    className={dataHeaderStyle}
                  >
                    <input
                      placeholder={header}
                      onChange={(newName) =>
                        changeVariableName(
                          header,
                          columnId,
                          newName.target.value
                        )
                      }
                      className="bg-transparent hover:border-b hover:border-slate-300 focus:outline-main-light max-w-full"
                    ></input>
                  </th>
                ))}
              </tr>

              {/* Data type dropdown*/}
              <tr className="bg-main-100">
                {variables.map((variable, columnId) => (
                  <th
                    key={`type-${variable["name"]}`}
                    className="px-3 py-2 text-sm text-gray-600"
                  >
                    <select
                      className={dropdownListStyle}
                      onChange={(event) =>
                        changeDataType(variable["name"], columnId, event)
                      }
                      defaultValue={variable["type"]}
                    >
                      {dataTypes.map((type) => (
                        <option key={type} value={type} className="hover:bg-main-light">
                          {type}
                        </option>
                      ))}
                    </select>
                  </th>
                ))}
              </tr>
            </thead>

            {/* Data values */}
            <tbody className="bg-white divide-y divide-main-50">
              {values.map((row, index) => (
                <tr
                  key={index}
                  className={`${index % 2 === 0 ? "bg-main-50" : "bg-white"}`}
                >
                  {row.map((value, id) => (
                    <td
                      key={id}
                      className="px-6 py-2 whitespace-nowrap text-sm text-gray-900 text-center"
                    >
                      {value}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="left-[25%] relative w-[50%]  justify-center items-center">
        <select
          className={dropdownListStyle}
          onChange={(event) => changeNormalizationMethod(event)}
          defaultValue={currNormalizationMethod}
        >
          {normalizationMethods.map((method) => (
            <option key={method} value={method}>
              {method}
            </option>
          ))}
        </select>
      </div>
      <div className="absolute bottom-0 right-0">
        <NewPageButton path={"/menu"} executable={handleSavingChanges} />
      </div>
    </div>
  );
};

export default DataTypeEditPage;
