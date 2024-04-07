import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";
import { navigationButtonStyle } from "../../common/styles";
import Title from "../Title";

function getExtension(filename) {
  var parts = filename.split(".");
  return parts[parts.length - 1];
}

const FileExplorer = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const navigate = useNavigate();

  const onDrop = (acceptedFiles) => {
    setSelectedFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    multiple: false,
  });

  const handleStartWork = async () => {
    if (selectedFile) {
      let fileExtension = getExtension(selectedFile.name);
      if (fileExtension !== "csv") {
        alert(
          `Error: .${fileExtension} is not supported, please submit .csv tile`
        );
        window.location.reload();
        return;
      }

      const formData = new FormData();
      formData.append("file", selectedFile, selectedFile.name);

      // POST file to backend
      try {
        const response = await fetch("http://localhost:8000/api/file", {
          // mode: "no-cors",
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorMsg = await response.text();
          throw new Error(errorMsg);
        }

        navigate("/data-type-edit");
      } catch (error) {
        console.error("Error uploading file:", error);
        alert(`Error uploading file. ${error}`);

        window.location.reload();
      }
    } else {
      console.log("No file selected.");
    }
  };

  return (
    <div className="relative min-h-72">
      <Title title="Ścieżka do pliku" />
      <div
        {...getRootProps({ className: "dropzone" })}
        className="bg-zinc-50 h-36 px-10 py-5 border rounded border-main-100
            hover:border-dotted hover:border-main-light cursor-pointer flex items-center justify-center"
      >
        <input {...getInputProps()} />

        <div>
          <p className="text-gray-400 text-center">
            Możesz przeciągnąć i upuścić plik tutaj, lub kliknij by wybrać.
          </p>

          {selectedFile && (
            <p className="text-main text-sm text-center">
              Wybrany plik: {selectedFile.name}
            </p>
          )}
        </div>
      </div>
      {selectedFile && (
        <div>
          <div className="absolute bottom-0 right-0">
            <button onClick={handleStartWork} className={navigationButtonStyle}>
              Zacznij pracę
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileExplorer;
