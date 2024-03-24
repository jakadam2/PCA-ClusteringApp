import React from "react";
import Chart from "../components/Chart";
import MenuButton from "../components/buttons/MenuButton";
import Statistics from "../components/Statistics";

const ClusterizationVisualization = () => {
  return (
    <div className="relative h-[450px] ">
      <Chart />
      <Statistics />
      <div className="left-0 right-0 flex justify-center items-center mt-10">
        <MenuButton />
      </div>
    </div>
  );
};

export default ClusterizationVisualization;
