import React, { useEffect, useState } from "react";
import MenuButton from "../components/buttons/MenuButton";
import Chart from "../components/Chart";
import { defaultButtonStyle } from "../common/styles";
import Title from "../components/Title";

const MainPCAComponentsVisualization = () => {
  const imageUrl = "http://localhost:8000/api/pca/graph";
  const transformUrl = "http://localhost:8000/api/pca/transform";

  // const imageUrl =
  //   "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/132.png";
  const [img, setImg] = useState();
  const [canPerformPCA, setCanPerformPCA] = useState(true);

  const performPCA = async () => {
    if (canPerformPCA) {
      setCanPerformPCA(false);
      await fetch(transformUrl, {
        //mode: "no-cors",
        method: "PUT",
      });
    }
  };

  const fetchImage = async () => {
    const res = await fetch(imageUrl, {
      //mode: "no-cors",
      method: "GET",
    });
    const imageBlob = await res.blob();
    var urlCreator = window.URL || window.webkitURL;
    const imageObjectURL = urlCreator.createObjectURL(imageBlob);
    document.querySelector("#image").src = imageUrl;
    setImg(imageObjectURL);
  };

  useEffect(() => {
    fetchImage();
  }, []);

  return (
    <div className="relative h-[800px]">
      <div className="-mb-5">
        <Title title="PCA"/>
      </div>
      <Chart img={img} />
      <div className="left-0 right-0 flex justify-center items-center">
        <button
          className={defaultButtonStyle + "relative w-[200px]"}
          onClick={performPCA}
          style={
            canPerformPCA
              ? {}
              : {
                  backgroundColor: "gray",
                }
          }
        >
          Zaaplikuj PCA
        </button>
      </div>
      <div className="left-0 right-0 flex justify-center items-center">
        <MenuButton />
      </div>
    </div>
  );
};

export default MainPCAComponentsVisualization;
