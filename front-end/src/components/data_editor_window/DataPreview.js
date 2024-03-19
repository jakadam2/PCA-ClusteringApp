import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

const DataPreview = () => {
  const [data, setData] = useState([]);

  // TODO - upload file from backend
  // currently loading from disk sample/data.csv
  useEffect(() => {
    fetch('/sample/data.csv')
      .then(response => response.text())
      .then(csvText => {
        Papa.parse(csvText, {
          complete: (result) => {
            setData(result.data);
          },
          header: true,
        });
      });
  }, []);

  const changeVariableName = (varName, columnId) => {
    const rowId = 0;
    console.log(`Header clicked: ${varName}, row: ${rowId}, col: ${columnId}`);
    // TODO - implement name change and send changes to backend (after saving?)
  };


  // Creating headers (variable names)
  const headers = data.length > 0 ? Object.keys(data[0]) : [];

  return (
    <div className="max-w-90 max-h-80 overflow-scroll bg-slate-100">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {headers.map((header, columnId) => (
              <th key={header} onClick={() => changeVariableName(header, columnId)} className="min-w-32 px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 hover:text-gray-700">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className={`${rowIndex % 2 === 0 ? 'bg-blue-50' : 'bg-gray-50'}`}>
              {headers.map(header => (
                <td key={`${rowIndex}-${header}`} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
                  {row[header]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataPreview;
