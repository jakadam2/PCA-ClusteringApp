import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import MenuButton from "../components/buttons/MenuButton";
import Statistics from "../components/clusterization/Statistics";
import Plot from "react-plotly.js";
import Title from "../components/Title";

const getErrorMsg = async (response) => {
  return await (
    await (
      await (
        await response.json()
      ).detail
    )[0]
  ).msg;
};

const ClusterizationVisualization = () => {
  const navigate = useNavigate();
  const { state } = useLocation();
  const { algorithm, columns, algorithmParams } = state;
  const [clusteringID, setClusteringID] = useState("");
  const [plot, setPlot] = useState({ data: [], layout: {} });

  const performClustering = async () => {
    try {
      console.log(
        "test: ",
        JSON.stringify({
          columns: columns,
          method: { name: algorithm, parameters: algorithmParams },
        })
      );
      const response = await fetch("http://localhost:8000/api/clustering", {
        //mode: "no-cors",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        method: "POST",
        body: JSON.stringify({
          columns: columns,
          method: { name: algorithm, parameters: algorithmParams },
        }),
      });

      if (!response.ok) {
        const errorMsg = await getErrorMsg(response);
        throw new Error(`${errorMsg}`);
      }

      const responseClusteringID = await response.json();
      setClusteringID(responseClusteringID);
    } catch (error) {
      console.error("Error performing clustering:", error);
      alert(`Error performing clustering. ${error}`);
      navigate("/clusterization-options");
    }
  };

  const fetchPlot = async () => {
    try {
      console.log(clusteringID);
      const response = await fetch(
        `http://localhost:8000/api/clustering/${clusteringID}/plot`,
        {
          //mode: "no-cors",
          headers: {
            accept: "application/json",
          },
          method: "GET",
        }
      );

      if (!response.ok) {
        const status = await response.status;
        if (status === 422) {
          const errorMsg = await getErrorMsg(response);
          throw new Error(`${errorMsg}`);
        } else {
          const errorMsg = await response.statusText;
          throw new Error(`${errorMsg}`);
        }
      }

      const plotJSON = await response.json();
      //TODO: how to not hardcode this?
      (await plotJSON).layout.height = 800;
      (await plotJSON).layout.width = 1200;
      setPlot(await plotJSON);
    } catch (error) {
      console.error("Error fetching plot:", error);
      alert(`Error fetching plot. ${error}`);
    }
  };

  useEffect(() => {
    performClustering();
  }, []);

  useEffect(() => {
    if (clusteringID !== "") fetchPlot();
  }, [clusteringID]);

  return (
    <div className="relative h-[450px] ">
      <Title title="Wizualizacja" />
      <div className="left-0 right-0 flex justify-center items-center">
        <Plot data={plot.data} layout={plot.layout} />
      </div>
      <Statistics />
      <div className="left-0 right-0 flex justify-center items-center mt-10">
        <MenuButton />
      </div>
    </div>
  );
};

export default ClusterizationVisualization;
