import React, { useState, useEffect } from "react";
import NewPageButton from "../components/buttons/NewPageButton";
import MenuButton from "../components/buttons/MenuButton";
import { dataHeaderStyle, dropdownListStyle } from "../common/styles";
import Title from "../components/Title";

const ROWS = 10;

const AlgorithmOptions = ({ algorithm }) => {
  if (algorithm === "Affinity Propagation")
    return (
      <div className="my-5 mx-2">
        <header className="text-xl font-semibold text-center mb-2 text-main-dark"> {algorithm} Parameters </header>

        <div className="flex items-center mb-4">
          <label for="damping factor" className="text-gray-600 min-w-fit mr-2">Damping factor (0.5, 1.0): </label>
          <input
            className="bg-main-100 rounded-md px-2 focus:outline-none text-main-dark w-full"
            name="damping factor"
            type="number"
            min="0.5"
            max="1.0"
            step="0.05"
            defaultValue="0.5"
          />
          </div>
      </div>
    );
  if (algorithm === "Dbscan")
    return (
      <div className="my-5">
        <div>
          <header className="text-xl font-semibold text-center mb-2 text-main-dark"> {algorithm} Parameters </header>
          <div className="mb-4">
          <div className="flex items-center">
            <label htmlFor="eps" className="text-gray-600 mr-2">{"Epsilon:"} </label>
            <input
              className="bg-main-100 rounded-md px-2 focus:outline-none text-main-dark w-full"
              name="eps"
              type="number"
              min="0.05"
              step="0.05"
              defaultValue="0.5"
            />
          </div>
          <div className="text-gray-600 text-xs">
            The maximum distance between two samples for one to be considered as
            in the neighborhood of the other.
          </div>
        </div>

        <div className="mb-4">
          <div className="flex items-center">
            <label htmlFor="min_samples" className="text-gray-600 mr-2 min-w-fit">Min samples: </label>
            <input
              className="bg-main-100 rounded-md px-2 focus:outline-none text-main-dark w-full"
              name="min_samples"
              type="number"
              min="2"
              defaultValue="5"
            />
          </div>
          <div className="text-gray-600 text-xs">
            The number of samples in a neighborhood for a point to be considered
            as a core point. This includes the point itself.
          </div>
        </div>

        <div className="mb-4">
          <div className="flex items-center">
            <label htmlFor="metric" className="text-gray-600 mr-2">Metric:</label>
            <select className={`${dropdownListStyle} focus:outline-none`} defaultValue={"euclidean"}>
              <option key={"euclidean"} value={"euclidean"}>euclidean</option>
              <option key={"manhattan"} value={"manhattan"}>manhattan</option>
              <option key={"cosine"} value={"cosine"}>cosine</option>
              <option key={"l1"} value={"l1"}>l1</option>
              <option key={"l2"} value={"l2"}>l2</option>
            </select>
          </div>
          <div className="text-gray-600 text-xs">
            The metric to use when calculating distance between instances in a
            feature array.
          </div>
        </div>
      </div>
    </div>
    );
  return;
};

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
      <Title title="Klastryzacja" />
      <div className="relative h-96">
        <div className="max-h-80 overflow-scroll bg-main-50 thin-scrollbar w-auto mx-auto">
          <table className="divide-y divide-gray-200 w-full">
            {/* Headers/Variable names */}
            <thead className="bg-main-50">
              <tr>
                {headers.map((header, columnId) => (
                  <th
                    key={header}
                    className={`${dataHeaderStyle} hover:bg-main-50`}
                  >
                    {header}
                  </th>
                ))}
              </tr>
              {/* Data type*/}
              <tr className="bg-main-100">
                {variables.map((variable, columnId) => (
                  <th
                    key={`type-${variable["name"]}`}
                    className="px-3 py-2 text-sm text-main-dark"
                  >
                    {variable["type"]}
                  </th>
                ))}
              </tr>
              {/* Checkbox*/}
              <tr className="bg-main-100">
                {headers.map((header, columnId) => (
                  <th
                    key={`type-${header}`}
                    className="px-3 py-2 text-sm text-gray-600"
                  >
                    <label>
                      <input
                        type="checkbox"
                        checked={checkedState[columnId]}
                        className="accent-main-medium"
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
        <AlgorithmOptions algorithm={currAlgorithm} />
        <div className="my-2 left-0 right-0 flex justify-center items-center">
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
