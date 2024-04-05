import React, { useState, useEffect } from "react";
import { dataHeaderStyle } from "../../common/styles";

const ROWS = 10;

const DataPreview = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const requestDataset = fetch(
      `http://localhost:8000/api/dataset?rows=${ROWS}`
    ).then((res) => res.json());

    Promise.all([requestDataset]).then(([dataset]) => {
      setData({
        dataset: dataset,
      });
    });
  }, []);

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
    <div className="relative h-96">
      <div className="max-h-80 overflow-scroll bg-main-50 thin-scrollbar">
        <table className="divide-y divide-gray-200">
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
  );
};

export default DataPreview;
