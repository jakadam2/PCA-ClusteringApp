import React, { useState, useEffect } from "react";
import { inactiveButtonStyle } from "../../common/styles";


const ROWS = 10

const DataPreview = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const requestDataset = fetch(`http://localhost:8000/api/dataset?rows=${ROWS}`)
            .then(res => res.json())

        const requestDatatypes = fetch(`http://localhost:8000/api/data_types`)
            .then(res => res.json())

        Promise.all([requestDataset, requestDatatypes])
            .then(([dataset, datatypes]) => {
                setData({
                    'dataset': dataset,
                    'datatypes': datatypes
                })
            })
    }, []);

    const changeVariableName = (varName, columnId) => {
        const rowId = 0;
        console.log(`Header clicked: ${varName}, row: ${rowId}, col: ${columnId}`);
        // TODO - implement name change and send changes to backend (after saving?)
    };

    const changeDataType = (header, columnId, newType) => {
        console.log(
            `Data type clicked ${header} col: ${columnId}, changed to: ${newType.target.value}`
        );
        // TODO - implement type change
        // get data types from backend along with csv file and send changes to back (also after clicking 'save'?)
    };

    const handleSavingChanges = () => {
        // TODO - implement sending header name and data type changes to back
        // send changes that are kept in context
        console.log("Saving...");
    };

    const variables = data['dataset'] !== undefined ? data['dataset']['variables'] : []
    const headers = data['dataset'] !== undefined ? data['dataset']['variables'].map(variable => variable['name']) : []
    const values = [];
    if (data['dataset'] !== undefined) {
        for (let i = 0; i < ROWS; i++) {
            values.push([]);
        }
        for (let variable of data['dataset']['variables']) {
            let i = 0
            for (let value of variable['values']) {
                values[i].push(value)
                i++
            }
        }
    }
    const dataTypes = data['datatypes'] !== undefined ? data['datatypes'] : []

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
                                    onClick={() => changeVariableName(header, columnId)}
                                    className="min-w-32 px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 hover:text-gray-700"
                                >
                                    {header}
                                </th>
                            ))}
                        </tr>

                        {/* Data type dropdown*/}
                        <tr className="bg-gray-100">
                            {variables.map((variable,columnId) => (
                                <th
                                    key={`type-${variable['name']}`}
                                    className="px-3 py-2 text-sm text-gray-600"
                                >
                                    <select
                                        className="form-select block w-full px-2 py-1.5 text-xs font-normal text-gray-700 bg-white bg-clip-padding bg-no-repeat border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                        onChange={(event) =>
                                            changeDataType(variable['name'], columnId, event)
                                        }
                                        defaultValue={variable['type']}
                                    >
                                        {dataTypes.map((type) => (
                                            <option key={type} value={type}>
                                                {type}
                                            </option>
                                        ))}
                                    </select>
                                </th>
                            ))}
                        </tr>
                    </thead>

                    {/* Data values */}
                    <tbody className="bg-white divide-y divide-gray-200">
                        {values.map((row, index) => (
                            <tr
                                key={index}
                                className={`${index % 2 === 0 ? "bg-blue-50" : "bg-gray-50"
                                    }`}
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

                <div className="absolute bottom-5 right-0">
                    <button onClick={handleSavingChanges} className={inactiveButtonStyle}>
                        Zapisz zmiany
                    </button>
                </div>
            </div>
        </div>
    );
};

export default DataPreview;
