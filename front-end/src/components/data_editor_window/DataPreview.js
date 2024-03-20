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

  const changeDataType = (header, columnId, newType) => {
    console.log(`Data type clicked ${header} col: ${columnId}, changed to: ${newType.target.value}`);
    // TODO - implement type change
    // get data types from backend along with csv file and send changes to back (also after clicking 'save'?)
  };

  const handleSavingChanges = () => {
    // TODO - implement sending header name and data type changes to back
    // send changes that are kept in context
    console.log('Saving...')
  }


  const headers = data.length > 0 ? Object.keys(data[0]) : [];
  const dataTypes = ["Numerical", "Categorical", "Text"]; // Example data types, to be extracted from back along with data

  return (
    <div className='relative h-96'>
      <div className="max-h-80 overflow-scroll bg-slate-100">
        <table className="divide-y divide-gray-200">

          {/* Headers/Variable names */}
          <thead className="bg-gray-50">
            <tr>
              {headers.map((header, columnId) => (
                <th key={header} onClick={() => changeVariableName(header, columnId)} className="min-w-32 px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 hover:text-gray-700">
                  {header}
                </th>
              ))}
            </tr>

            {/* Data type dropdown*/}
            <tr className="bg-gray-100">
              {headers.map((header, columnId) => (
                <th key={`type-${header}`} className="px-3 py-2 text-sm text-gray-600">
                  <select 
                    className="form-select block w-full px-2 py-1.5 text-xs font-normal text-gray-700 bg-white bg-clip-padding bg-no-repeat border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none" 
                    onChange={(event) => changeDataType(header, columnId, event)}
                  >
                    {dataTypes.map((type) => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </th>
              ))}
            </tr>
          </thead>

          {/* Data values */}
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


        <div className="absolute bottom-5 right-0">
          <button onClick={handleSavingChanges}
                    className=" text-white bg-blue-400 hover:bg-blue-500 focus:ring-4 focus:ring-blue-300 
                    font-sm rounded-lg text-sm px-3 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 
                    focus:outline-none dark:focus:ring-blue-800">
              Zapisz zmiany</button>
        </div>
      </div>
    </div>
    
  );
};

export default DataPreview;
