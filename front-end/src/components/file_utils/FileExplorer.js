import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';

const FileExplorer = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const navigate = useNavigate();

  const onDrop = (acceptedFiles) => {
    setSelectedFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    multiple: false
  });

  const handleStartWork = async () => {
    if (selectedFile) {
        console.log(selectedFile);
        const formData = new FormData();
        formData.append('file', selectedFile, selectedFile.name);

        // TODO: check if it's even working correctly
        // POST file to backend
        try {
            const response = await fetch('http://localhost:8080/file', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('File uploaded successfully', data);

            navigate('/data-type-edit');
          } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file.');
        }

    } else {
      console.log('No file selected.');
    }
  };

  return (
    <div className="relative min-h-72">
      <p className="my-5">Ścieżka do pliku:</p>
      <div {...getRootProps({ className: 'dropzone' })} className="bg-zinc-50 px-10 py-5 border rounded border-slate-200 
            hover:border-dotted hover:border-slate-500 cursor-pointer flex items-center justify-center">
        <input {...getInputProps()} />
        <p className="text-gray-500 text-center">Możesz przeciągnąć i upuścić plik tutaj, lub kliknij by wybrać.</p>
      </div>
      {selectedFile && (
        <div>
            <p className="text-gray-500 text-sm">Wybrany plik: {selectedFile.name}</p>
            <div className="absolute bottom-0 right-0">
              <button onClick={handleStartWork}
                  className=" text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 
                  font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 
                  focus:outline-none dark:focus:ring-blue-800">
                      Zacznij pracę
              </button>
            </div>
        </div>
      )}
    </div>
  );
};

export default FileExplorer;
