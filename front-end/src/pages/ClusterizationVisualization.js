import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import MenuButton from "../components/buttons/MenuButton";
import Plot from "react-plotly.js";
import Title from "../components/Title";
import DataPreview from "../components/data_preview/DataPreview";

const getErrorMsg = async (response) => {
  return await (
    await (
      await (
        await response.json()
      ).detail
    )[0]
  ).msg;
};

const Statistics = ({ statistics }) => {
  const [statisticsToDisplay, setStatisticsToDisplay] = useState({});
  useEffect(() => {
    setStatisticsToDisplay(statistics);
  }, [statistics]);
  if (statisticsToDisplay == {}) return;
  return (
    <div className="my-5 items-center">
      <header className="text-xl font-semibold text-center mb-2 text-main-dark">
        Statystyki klastrów
      </header>
      <div className="mb-4 items-center relative w-[40%] left-[30%]">
        {Object.keys(statisticsToDisplay).map((key) => {
          return (
            <div className="flex">
              <label htmlFor="eps" className="text-gray-600 mr-2 font-semibold">
                {key + ": "}
              </label>
              <div>{statisticsToDisplay[key].toFixed(4)}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const ClusterizationVisualization = () => {
  const navigate = useNavigate();
  const { state } = useLocation();
  const { algorithm, columns, algorithmParams } = state;
  const [clusteringID, setClusteringID] = useState("");
  const [plot, setPlot] = useState({ data: [], layout: {} });
  const [statistics, setStatistics] = useState({});
  const [dataView, setDataView] = useState(<></>);

  const performClustering = async () => {
    try {
      // console.log(
      //   "test: ",
      //   JSON.stringify({
      //     columns: columns,
      //     method: { name: algorithm, parameters: algorithmParams },
      //   })
      // );
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

  const fetchStatistics = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/clustering/${clusteringID}/statistics`,
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

      const fetchedStatistics = await response.json();
      setStatistics(fetchedStatistics.statistics);
    } catch (error) {
      console.error("Error fetching statistics:", error);
      alert(`Error fetching statistics. ${error}`);
    }
  };

  const fetchData = async () => {
    setDataView(
      <DataPreview
        url={`http://localhost:8000/api/clustering/${clusteringID}/clusters_data`}
        saveOption={true}
      />
    );
  };

  useEffect(() => {
    performClustering();
  }, []);

  useEffect(() => {
    if (clusteringID !== "") {
      fetchPlot();
      fetchStatistics();
      fetchData();
    }
  }, [clusteringID]);

  return (
    <div className="relative h-[450px] ">
      <Title title="Wizualizacja klasteryzacji" />
      <div className="left-0 right-0 flex justify-center items-center">
        <Plot data={plot.data} layout={plot.layout} />
      </div>
      <Statistics statistics={statistics} />
      <Title title="Dane po klasteryzacji" />
      {dataView}
      <div className="left-0 right-0 flex justify-center items-center mt-10">
        <MenuButton />
      </div>
    </div>
  );
};

export default ClusterizationVisualization;
