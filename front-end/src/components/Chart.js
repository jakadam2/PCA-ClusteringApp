import React from "react";
import { inactiveButtonStyle } from "../common/styles";

const MainPCAComponentsVisualization = () => {
  return (
    <div className="relative w-[100%] left-0 right-0 justify-center items-center">
      <img
        src={require("../img/chart.png")}
        alt={"chart"}
        className="relative w-[100%]"
      />
      <div className="left-0 right-0 flex justify-center items-center">
        <button className={inactiveButtonStyle + "relative w-[200px]"}>
          Zapisz wykres
        </button>
      </div>
    </div>
  );
};

export default MainPCAComponentsVisualization;
