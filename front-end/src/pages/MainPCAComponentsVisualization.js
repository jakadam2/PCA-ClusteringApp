import React from "react";
import MenuButton from "../components/buttons/MenuButton";
import Chart from "../components/Chart";
import { useNavigate } from "react-router-dom";

const MainPCAComponentsVisualization = () => {
  const navigate = useNavigate();

  return (
    <div className="relative h-[450px] ">
      <Chart />
      <div className="left-0 right-0 flex justify-center items-center">
        <MenuButton />
      </div>
    </div>
  );
};

export default MainPCAComponentsVisualization;
