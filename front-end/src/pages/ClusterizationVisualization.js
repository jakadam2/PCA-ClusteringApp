import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
import MenuButton from "../components/buttons/MenuButton";
import Statistics from "../components/clusterization/Statistics";
import Title from "../components/Title";

const ClusterizationVisualization = () => {
  const { state } = useLocation();
  const { algorithm, columns } = state;
  const fetchGraph = async () => {
    try {
      console.log(
        "test: ",
        JSON.stringify({
          columns: columns,
          method: algorithm,
          method_parameters: {},
        })
      );
      const response = await fetch(
        "http://localhost:8000/api/clustering/graph",
        {
          //mode: "no-cors",
          headers: {
            "Content-Type": "application/json",
            accept: "application/json",
          },
          method: "POST",
          body: JSON.stringify({
            columns: columns,
            method: algorithm,
            method_parameters: {},
          }),
        }
      );
      console.log(response);

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error fetching clustering graph:", error);
      alert("Error fetching clustering graph.");
    }
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  return (
    <div className="relative h-[450px] ">
      <Title title="Wizualizacja" />
      {/* <Chart src={img} /> */}
      <Statistics />
      <div className="left-0 right-0 flex justify-center items-center mt-10">
        <MenuButton />
      </div>
    </div>
  );
};

export default ClusterizationVisualization;
