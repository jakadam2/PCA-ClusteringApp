import React from "react";
import { useNavigate } from "react-router-dom";
import { defaultButtonStyle } from "../common/styles";

const MainMenu = () => {
  const navigate = useNavigate();

  const handleSavingChanges = () => {
    // TODO - implement sending header name and data type changes to back
    // send changes that are kept in context
    navigate("/save-file");
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
            className={defaultButtonStyle}
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
