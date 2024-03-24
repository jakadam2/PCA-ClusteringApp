import React from "react";
import DataPreview from "../components/data_editor_window/DataPreview";
import NewPageButton from "../components/buttons/NewPageButton";

const DataTypeEditPage = () => {
  return (
    <div className="relative h-[450px]">
      <DataPreview />
      <div className="absolute bottom-0 left-0 right-0 flex justify-center items-center">
        <button
          onClick={() => console.log("Sposoby normalizacji do wyświetlenia")}
          className=" text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 
                  font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 
                  focus:outline-none dark:focus:ring-red-800"
          style={{ margin: "auto" }}
        >
          Sposoby normalizacji
        </button>
      </div>

      <div className="absolute bottom-0 right-0">
        <NewPageButton path={"/menu"} />
      </div>
    </div>
  );
};

export default DataTypeEditPage;
