import React from "react";
import { useNavigate } from "react-router-dom";
import { navigationButtonStyle } from "../../common/styles";

const NewPageButton = () => {
  const navigate = useNavigate();

  return (
    <button className={navigationButtonStyle} onClick={() => navigate("/menu")}>
      <span className="">&#129152; Menu </span>
    </button>
  );
};

export default NewPageButton;
