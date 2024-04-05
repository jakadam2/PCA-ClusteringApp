import React from "react";
import { useNavigate } from "react-router-dom";
import { defaultButtonStyle } from "../common/styles";
import DataPreview from "../components/data_preview/DataPreview";

const MainMenu = () => {
  const navigate = useNavigate();

  return (
    <div>
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
        </div>
      </div>
      <DataPreview />
    </div>
  );
};

export default MainMenu;
