import React, { useEffect, useState } from "react";
import Chart from "../components/Chart";
import MenuButton from "../components/buttons/MenuButton";
import Statistics from "../components/clusterization/Statistics";

const ClusterizationVisualization = ({ algorithm, columns }) => {
  const imageUrl =
    "http://localhost:8000/api/clustering/graph?method=Mean-shift";
  const [img, setImg] = useState();

  const fetchImage = async () => {
    const res = await fetch(imageUrl, {
      //mode: "no-cors",
      method: "GET",
    });
    const imageBlob = await res.blob();
    console.log(imageBlob);
    var urlCreator = window.URL || window.webkitURL;
    const imageObjectURL = urlCreator.createObjectURL(imageBlob);
    document.querySelector("#image").src = imageUrl;
    setImg(imageObjectURL);
  };

  useEffect(() => {
    fetchImage();
  }, []);

  return (
    <div className="relative h-[450px] ">
      <Chart src={img} />
      <Statistics />
      <div className="left-0 right-0 flex justify-center items-center mt-10">
        <MenuButton />
      </div>
    </div>
  );
};

export default ClusterizationVisualization;
