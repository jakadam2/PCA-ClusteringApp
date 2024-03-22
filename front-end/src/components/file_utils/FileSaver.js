import React, { useState } from 'react';

const FileSaver = () => {
    const [directoryHandle, setDirectoryHandle] = useState(null);
    const [directoryName, setDirectoryName] = useState('');

    const selectDirectory = async () => {
        try {
            const directoryHandle = await window.showDirectoryPicker();
            setDirectoryHandle(directoryHandle);
            setDirectoryName(directoryHandle.name);
        } catch (error) {
            console.error('Error selecting directory:', error);
            alert('Error selecting directory.');
        }
    };

    const saveFileToDirectory = async () => {
        if (!directoryHandle) {
            alert('No directory selected. Please select a directory first.');
            return;
        }

        try {
            const response = await fetch('http://localhost:8080/file');
            if (!response.ok) throw new Error('Error while fetching file.');
            
            const fileData = await response.blob();
            // TODO - check 
            // Assuming the file will be csv
            const fileHandle = await directoryHandle.getFileHandle('savedFile.csv', { create: true });
            const writable = await fileHandle.createWritable();
            await writable.write(fileData);
            await writable.close();
            
            alert('File saved successfully.');
        } catch (error) {
            console.error('Error saving file:', error);
            alert('Error saving file.');
        }
    };

    return (
        <div>
            <p className="mb-5">Wybierz miejsce docelowe do zapisu pliku:</p>
            {directoryHandle ? (
                <div className='flex flex-col'>
                    <button onClick={selectDirectory}
                        className=" text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 
                        font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 
                        focus:outline-none dark:focus:ring-blue-800 max-w-44">
                        Wybierz folder</button>
                    <button onClick={saveFileToDirectory}
                                className=" text-white bg-blue-400 hover:bg-blue-500 focus:ring-4 focus:ring-blue-300 
                                font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 
                                focus:outline-none dark:focus:ring-blue-800 max-w-44">
                        Zapisz plik</button>
                    <p className="text-gray-500 text-left text-sm">Wybrany folder: {directoryName}</p>
                </div>
            ) : (
                <>
                    <button onClick={selectDirectory}
                        className=" text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 
                        font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 
                        focus:outline-none dark:focus:ring-blue-800">
                        Wybierz folder</button>
                </>
            )}
        </div>
    );
};

export default FileSaver;
