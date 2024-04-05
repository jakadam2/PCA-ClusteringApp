import React from "react";
import { inactiveButtonStyle } from "../common/styles";

const Chart = (img) => {
  return (
    <div className="relative max-w-[900px] w-full left-0 right-0 justify-center items-center mx-auto">
      {/* <img src={img} alt={"chart"} className="relative w-[100%]" /> */}
      <img id="image" alt={"chart"} className="relative w-[100%]" />
      <div className="left-0 right-0 flex justify-center items-center">
        <button className={inactiveButtonStyle + "relative w-[200px]"}>
          Zapisz wykres
        </button>
      </div>
    </div>
  );
};

export default Chart;
