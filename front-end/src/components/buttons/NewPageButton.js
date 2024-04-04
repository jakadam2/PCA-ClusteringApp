import React from "react";
import { useNavigate } from "react-router-dom";
import { navigationButtonStyle } from "../../common/styles";

const NewPageButton = ({ path, isActive = true, executable = () => {} }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    if (isActive) {
      executable();
      navigate(path);
    }
  };

  return (
    <button
      className={navigationButtonStyle}
      style={
        isActive
          ? {}
          : {
              backgroundColor: "gray",
            }
      }
      onClick={handleClick}
    >
      <span className="">&#129154; </span>
    </button>
  );
};

export default NewPageButton;
