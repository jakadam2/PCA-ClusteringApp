import React from 'react';

const DataPreview = () => {

  return (
    // Remove h-screen tailwind property when there will be data shown inside
    <div className="w-4/5 h-screen max-h-80 overflow-y-scroll bg-slate-400">
      This is going to be data preview with scroll bar
    </div>
  );
};

export default DataPreview;
