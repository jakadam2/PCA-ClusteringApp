import React from "react";
import { defaultButtonStyle } from "../common/styles";
import Chart from "../components/Chart";
import { useNavigate } from "react-router-dom";

const MainPCAComponentsVisualization = () => {
  const navigate = useNavigate();

  return (
    <div className="relative h-[450px] ">
      <Chart />
      <div className="left-0 right-0 flex justify-center items-center">
        <button
          className={defaultButtonStyle + "relative w-[200px]"}
          style={{ margin: "auto" }}
          onClick={() => navigate("/menu")}
        >
          Wróć
        </button>
      </div>
    </div>
  );
};

export default MainPCAComponentsVisualization;
