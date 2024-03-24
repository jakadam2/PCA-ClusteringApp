import React, { Fragment } from "react";
import { useNavigate } from "react-router-dom";
import { defaultButtonStyle } from "../common/styles";

const MainMenu = () => {
  const navigate = useNavigate();

  const handleSavingChanges = () => {
    // TODO - implement sending header name and data type changes to back
    // send changes that are kept in context
    console.log("Saving...");
  };

  return (
    <div className="left-0 right-0 flex justify-center items-center">
      <div className="relative h-[100px] w-[400px]">
        <div className="left-0 right-0 flex justify-center items-center">
          <button
            onClick={() => navigate("/pca-main-components")}
            className={defaultButtonStyle + "relative w-[150px]"}
            style={{ margin: "auto" }}
          >
            PCA
          </button>
          <button
            onClick={() => navigate("/clusterization-options")}
            className={defaultButtonStyle + "relative w-[150px]"}
            style={{ margin: "auto" }}
          >
            Klastryzacja
          </button>
        </div>
        <div className="absolute bottom-0 left-0 right-0 flex justify-center items-center">
          <button
            onClick={handleSavingChanges}
            className=" text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 
            font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 
            focus:outline-none dark:focus:ring-red-800"
            style={{ margin: "auto" }}
          >
            Zapisz zmiany
          </button>
        </div>
      </div>
    </div>
  );
};

export default MainMenu;
