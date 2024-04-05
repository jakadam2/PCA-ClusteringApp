import React, { useState, useEffect } from "react";

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
  );
};

export default DataPreview;
