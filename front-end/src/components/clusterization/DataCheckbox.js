import React, { useState, useEffect } from "react";
import Papa from "papaparse";

const DataCheckbox = () => {
  const [data, setData] = useState([]);

  // TODO - upload file from backend
  // currently loading from disk sample/data.csv
  useEffect(() => {
    fetch("/sample/data.csv")
      .then((response) => response.text())
      .then((csvText) => {
        Papa.parse(csvText, {
          complete: (result) => {
            setData(result.data);
          },
          header: true,
        });
      });
  }, []);

  const handleCheckboxChange = (header, columnId) => {
    console.log(`Data column checked ${header} col: ${columnId}`);
    // TODO - implement type change
  };

  const headers = data.length > 0 ? Object.keys(data[0]) : [];

  return (
    <div className="relative h-96">
      <div className="max-h-80 overflow-scroll bg-slate-100">
        <table className="divide-y divide-gray-200">
          {/* Headers/Variable names */}
          <thead className="bg-gray-50">
            <tr>
              {headers.map((header) => (
                <th
                  key={header}
                  className="min-w-32 px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 hover:text-gray-700"
                >
                  {header}
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
                      onChange={handleCheckboxChange(header, columnId)}
                    />
                  </label>
                </th>
              ))}
            </tr>
          </thead>

          {/* Data values */}
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className={`${
                  rowIndex % 2 === 0 ? "bg-blue-50" : "bg-gray-50"
                }`}
              >
                {headers.map((header) => (
                  <td
                    key={`${rowIndex}-${header}`}
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center"
                  >
                    {row[header]}
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

export default DataCheckbox;
