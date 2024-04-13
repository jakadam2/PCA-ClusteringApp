import React, { useState } from "react";
import { useLocation } from "react-router-dom";

const FileSaver = () => {
  const [directoryHandle, setDirectoryHandle] = useState(null);
  const [directoryName, setDirectoryName] = useState("");
  const [fileName, setFileName] = useState("");
  const [data, setData] = useState([]);
  const { state } = useLocation();
  const { headers, values } = state;

  const parseData = () => {
    setData([
      ["name1", "city1", "some other info"],
      ["name2", "city2", "more info"],
    ]);
  };

  const selectDirectory = async () => {
    try {
      const directoryHandle = await window.showDirectoryPicker();
      setDirectoryHandle(directoryHandle);
      setDirectoryName(directoryHandle.name);
    } catch (error) {
      console.error("Error selecting directory:", error);
      alert("Error selecting directory.");
    }
  };

  const handleFileNameChange = (event) => {
    setFileName(event.target.value);
  };

  const saveFileToDirectory = async () => {
    if (!directoryHandle) {
      alert("No directory selected. Please select a directory first.");
      return;
    }
    if (!fileName.trim()) {
      alert("Please enter a file name.");
      return;
    }

    try {
      let fileData = headers.join(";") + "\r\n";

      values.forEach(function (rowArray) {
        let row = rowArray.join(";");
        fileData += row + "\r\n";
      });

      const effectiveFileName = fileName.endsWith(".csv")
        ? fileName
        : `${fileName}.csv`;
      const fileHandle = await directoryHandle.getFileHandle(
        effectiveFileName,
        { create: true }
      );
      const writable = await fileHandle.createWritable();
      await writable.write(fileData);
      await writable.close();

      alert("File saved successfully.");
    } catch (error) {
      console.error("Error saving file:", error);
      alert("Error saving file.");
    }
  };

  return (
    <div>
      <p className="mb-5">Wybierz miejsce docelowe do zapisu pliku:</p>
      {directoryHandle ? (
        <>
          <div className="flex flex-col items-start w-full mb-2">
            <div className="flex gap-2 w-full">
              <button
                onClick={selectDirectory}
                className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 
                                    font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 
                                    focus:outline-none dark:focus:ring-blue-800 w-36"
              >
                Wybierz folder
              </button>
              <input
                type="text"
                value={fileName}
                onChange={handleFileNameChange}
                placeholder="Nazwa pliku"
                className="flex-grow text-sm p-2.5 border rounded-lg focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div className="flex justify-between items-center w-full mt-2">
              <p className="text-gray-500 text-sm">
                Wybrany folder: {directoryName}
              </p>
              <button
                onClick={saveFileToDirectory}
                className="text-white bg-blue-400 hover:bg-blue-500 focus:ring-4 focus:ring-blue-300 
                                    font-small rounded-lg text-sm px-3 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 
                                    focus:outline-none dark:focus:ring-blue-800 w-24"
              >
                Zapisz plik
              </button>
            </div>
          </div>
        </>
      ) : (
        <button
          onClick={selectDirectory}
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 
                        font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 
                        focus:outline-none dark:focus:ring-blue-800"
        >
          Wybierz folder
        </button>
      )}
    </div>
  );
};

export default FileSaver;
