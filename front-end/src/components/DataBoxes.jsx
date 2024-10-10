import React from 'react';
import GroupIcon from '../assets/icons/GroupIcon';
import UpArrowIcon from '../assets/icons/UpArrowIcon';

const DataBoxes = ({ dashboardData }) => {
  const roundToThreeDecimals = (num) => {
    return isNaN(num) ? 'N/A' : Math.round(num * 1000) / 1000;
  };

  return (
    <div className="h-auto flex flex-wrap mt-[1rem] gap-[1rem]">
      <div className="w-[17rem] h-[9rem] bg-white shadow-md flex flex-col p-5 gap-2 text-[#A5A5A5] rounded-md">
        <span className="flex items-center justify-between">
          <p>Input Tokens</p>
          <span className="p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold text-[#767B8B]">
          {roundToThreeDecimals(dashboardData?.input_tokens ?? 0)}
        </p>
        <span className="mt-[1rem] flex items-center justify-between">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>
      
      <div className="w-[17rem] h-[9rem] bg-white shadow-md flex flex-col p-5 gap-2 text-[#A5A5A5] rounded-md">
        <span className="flex items-center justify-between">
          <p>Output Tokens</p>
          <span className="p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold text-[#767B8B]">
          {roundToThreeDecimals(dashboardData?.output_tokens ?? 0)}
        </p>
        <span className="mt-[1rem] flex items-center justify-between">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>

      <div className="w-[17rem] h-[9rem] bg-white shadow-md flex flex-col p-5 gap-2 text-[#A5A5A5] rounded-md">
        <span className="flex items-center justify-between">
          <p>Total Requests</p>
          <span className="p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold text-[#767B8B]">
          {roundToThreeDecimals(dashboardData?.requests ?? 0)}
        </p>
        <span className="mt-[1rem] flex items-center justify-between">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>

      <div className="w-[17rem] h-[9rem] bg-white shadow-md flex flex-col p-5 gap-2 text-[#A5A5A5] rounded-md">
        <span className="flex items-center justify-between">
          <p>Dollars Spend Total</p>
          <span className="p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold text-[#767B8B]">
          {roundToThreeDecimals(dashboardData?.dollar_spend_total ?? 0)}
        </p>
        <span className="mt-[1rem] flex items-center justify-between">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>

      <div className="w-[17rem] h-[9rem] bg-white shadow-md flex flex-col p-5 gap-2 text-[#A5A5A5] rounded-md">
        <span className="flex items-center justify-between">
          <p>Dollar Spend Input</p>
          <span className="p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold text-[#767B8B]">
          {roundToThreeDecimals(dashboardData?.dollar_spend_input ?? 0)}
        </p>
        <span className="mt-[1rem] flex items-center justify-between">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>

      <div className="w-[17rem] h-[9rem] bg-white shadow-md flex flex-col p-5 gap-2 text-[#A5A5A5] rounded-md">
        <span className="flex items-center justify-between">
          <p>Dollar Spend Output</p>
          <span className="p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold text-[#767B8B]">
          {roundToThreeDecimals(dashboardData?.dollar_spend_output ?? 0)}
        </p>
        <span className="mt-[1rem] flex items-center justify-between">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>
    </div>
  );
};

export default DataBoxes;
