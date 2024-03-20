import React from 'react';
import { useNavigate } from 'react-router-dom';

const NewPageButton = ({ path }) => {
    const navigate = useNavigate();
  
    const handleClick = () => {
      navigate(path);
    };
  
    return (
      <button 
        className="flex items-center justify-center px-4 py-2 bg-blue-700 text-white rounded-lg shadow-md hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-800 focus:ring-opacity-50"
        onClick={handleClick}>
            <span className="">&#10132;  </span>
      </button>
    );
  };

export default NewPageButton;
