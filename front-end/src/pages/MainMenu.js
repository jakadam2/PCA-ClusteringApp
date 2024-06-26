import React from "react";
import { useNavigate } from "react-router-dom";
import { navigationButtonStyle } from "../common/styles";
import DataPreview from "../components/data_preview/DataPreview";
import Title from "../components/Title";

const MainMenu = () => {
  const navigate = useNavigate();

  return (
    <div>
      <Title title="Menu" />
      <DataPreview />
      <div className="left-0 right-0 flex justify-center items-center">
        <div className="relative h-[100px] w-[400px]">
          <div className="left-0 right-0 flex justify-center items-center">
            <button
              onClick={() => navigate("/pca-main-components")}
              className={navigationButtonStyle + "relative w-[150px]"}
              style={{ margin: "auto" }}
            >
              PCA
            </button>
            <button
              onClick={() => navigate("/clusterization-options")}
              className={navigationButtonStyle + "relative w-[150px]"}
              style={{ margin: "auto" }}
            >
              Klastryzacja
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainMenu;
