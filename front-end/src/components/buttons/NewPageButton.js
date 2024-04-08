import React from "react";
import { useNavigate } from "react-router-dom";
import { navigationButtonStyle } from "../../common/styles";

const NewPageButton = ({
  path,
  isActive = true,
  executable = () => {},
  state = {},
}) => {
  const navigate = useNavigate();

  const handleClick = async () => {
    if (isActive) {
      await executable();
      navigate(path, { state: state });
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
