import React from "react";
import DataPreview from "../components/data_editor_window/DataPreview";
import NewPageButton from "../components/buttons/NewPageButton";
import { inactiveButtonStyle } from "../common/styles";

const DataTypeEditPage = () => {
  return (
    <div className="relative h-[450px]">
      <DataPreview />
      <div className="absolute bottom-0 left-0 right-0 flex justify-center items-center">
        <button
          onClick={() => console.log("Sposoby normalizacji do wyświetlenia")}
          className={inactiveButtonStyle}
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
