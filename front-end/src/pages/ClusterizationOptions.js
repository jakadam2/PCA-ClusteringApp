import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import DataCheckbox from "../components/DataCheckbox";
import NewPageButton from "../components/buttons/NewPageButton";
import MenuButton from "../components/buttons/MenuButton";

const ClusterizationOptions = () => {
  const [possible, setPossible] = useState(true);
  //TODO setPossible only if clustrization with chosen variables is possible
  const navigate = useNavigate();

  return (
    <div className="relative h-[450px]">
      <DataCheckbox />
      <div className="left-[25%] relative w-[50%]  justify-center items-center">
        <select className="form-select w-full block px-2 py-1.5 text-xs font-normal text-gray-700 bg-white bg-clip-padding bg-no-repeat border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none">
          {<option>Algorytm klasteryzacji</option>}
        </select>
        {possible ? (
          <div
            className="p-10"
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginTop: "5",
            }}
          >
            Klastryzacja jest możliwa.
          </div>
        ) : (
          <div
            className="p-10"
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginTop: "5",
            }}
          >
            Klastryzacja nie jest możliwa.
          </div>
        )}
        <div className="left-0 right-0 flex justify-center items-center">
          <MenuButton />
          &nbsp;&nbsp;&nbsp;
          <NewPageButton
            path={"/clusterization-visualization"}
            isActive={possible}
          />
        </div>
      </div>
    </div>
  );
};

export default ClusterizationOptions;
