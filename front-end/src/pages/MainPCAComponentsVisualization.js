import React, { useEffect, useState } from "react";
import MenuButton from "../components/buttons/MenuButton";
import Title from "../components/Title";
import Plot from "react-plotly.js";
import DataPreview from "../components/data_preview/DataPreview";

const ROWS = 10;

const MainPCAComponentsVisualization = () => {
  const plotUrl = "http://localhost:8000/api/pca/graph";
  const [plot, setPlot] = useState({ data: [], layout: {} });

  const fetchPlot = async () => {
    try {
      const res = await fetch(plotUrl, {
        //mode: "no-cors",
        method: "GET",
      });
      if (!res.ok) {
        throw new Error(res.statusText());
      }
      const plotJSON = await res.json();
      //TODO: how to not hardcode this?
      (await plotJSON).layout.height = 800;
      (await plotJSON).layout.width = 1200;
      setPlot(await plotJSON);
    } catch (error) {
      console.error("Error fetching plot:", error);
      alert(`Error fetching plot.`);
    }
  };

  useEffect(() => {
    fetchPlot();
  }, []);

  return (
    <div>
      <div className="-mb-5">
        <Title title="PCA" />
      </div>
      <div className="left-0 right-0 flex justify-center items-center">
        <Plot data={plot.data} layout={plot.layout} />
      </div>
      <DataPreview
        url={`http://localhost:8000/api/pca/transform?rows=${ROWS}`}
      />
      <div className="left-0 right-0 flex justify-center items-center">
        <MenuButton />
      </div>
    </div>
  );
};

export default MainPCAComponentsVisualization;
