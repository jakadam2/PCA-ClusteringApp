import React, { useState, useEffect } from "react";
import NewPageButton from "../components/buttons/NewPageButton";
import MenuButton from "../components/buttons/MenuButton";

const ROWS = 10;

const ClusterizationOptions = () => {
  const [clusterizationMethods, setClusterizationMethods] = useState([]);
  const [currAlgorithm, setCurrAlgorithm] = useState("");
  const [data, setData] = useState([]);
  const [checkedState, setCheckedState] = useState([]);
  const [checkedColumns, setCheckedColumns] = useState([]);

  useEffect(() => {
    const requestMethods = fetch(
      `http://localhost:8000/api/clustering/methods`
    ).then((res) => res.json());

    const requestDataset = fetch(
      `http://localhost:8000/api/dataset?rows=${ROWS}`
    ).then((res) => res.json());

    Promise.all([requestMethods, requestDataset]).then(([methods, dataset]) => {
      setClusterizationMethods(methods);
      setCurrAlgorithm(methods[0]);
      setData({
        dataset: dataset,
      });
      setCheckedState(new Array(dataset.variables.length).fill(false));
    });
  }, []);

  const changeAlgorithm = (event) => {
    console.log(`Algorithm method changed to: ${event.target.value}`);
    setCurrAlgorithm(event.target.value);
  };

  const handleCheckboxChange = (header, columnId) => {
    console.log(`Data column checked ${header} col: ${columnId}`);
    const updatedCheckedState = checkedState.map((item, index) =>
      index === columnId ? !item : item
    );
    setCheckedState(updatedCheckedState);

    const currCheckedColumns = checkedState
      .map((item, index) => (item ? headers[index] : ""))
      .filter((elem) => elem !== "");

    setCheckedColumns(currCheckedColumns);
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

  return (
    <div className="relative h-[450px]">
      <div className="relative h-96">
        <div className="max-h-80 overflow-scroll bg-slate-100">
          <table className="divide-y divide-gray-200">
            {/* Headers/Variable names */}
            <thead className="bg-gray-50">
              <tr>
                {headers.map((header, columnId) => (
                  <th
                    key={header}
                    className="min-w-32 px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 hover:text-gray-700"
                  >
                    {header}
                  </th>
                ))}
              </tr>
              {/* Data type*/}
              <tr className="bg-gray-100">
                {variables.map((variable, columnId) => (
                  <th
                    key={`type-${variable["name"]}`}
                    className="px-3 py-2 text-sm text-gray-600"
                  >
                    {variable["type"]}
                  </th>
                ))}
              </tr>
              {/* Checkbox*/}
              <tr className="bg-gray-100">
                {headers.map((header, columnId) => (
                  <th
                    key={`type-${header}`}
                    className="px-3 py-2 text-sm text-gray-600"
                  >
                    <label>
                      <input
                        type="checkbox"
                        checked={checkedState[columnId]}
                        onChange={() => {
                          handleCheckboxChange(header, columnId);
                        }}
                      />
                    </label>
                  </th>
                ))}
              </tr>
            </thead>

            {/* Data values */}
            <tbody className="bg-white divide-y divide-gray-200">
              {values.map((row, index) => (
                <tr
                  key={index}
                  className={`${index % 2 === 0 ? "bg-blue-50" : "bg-gray-50"}`}
                >
                  {row.map((value, id) => (
                    <td
                      key={id}
                      className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center"
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
          className="form-select w-full block px-2 py-1.5 text-xs font-normal text-gray-700 bg-white bg-clip-padding bg-no-repeat border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
          onChange={(event) => changeAlgorithm(event)}
          defaultValue={currAlgorithm}
        >
          {clusterizationMethods.map((method) => {
            return (
              <option key={method} value={method}>
                {method}
              </option>
            );
          })}
        </select>
        <div className="left-0 right-0 flex justify-center items-center">
          <MenuButton />
          &nbsp;&nbsp;&nbsp;
          <NewPageButton
            path={"/clusterization-visualization"}
            state={{ algorithm: currAlgorithm, columns: checkedColumns }}
          />
        </div>
      </div>
    </div>
  );
};

export default ClusterizationOptions;
