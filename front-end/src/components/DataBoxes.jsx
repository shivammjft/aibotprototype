import React from 'react';
import GroupIcon from '../assets/GroupIcon';
import UpArrowIcon from '../assets/UpArrowIcon';

const DataBoxes = ({ dashboardData }) => {
  return (
    <div className=" w-[40%] flex p-3 flex-wrap gap-7  ">
      <div className=" w-[15rem] h-[11rem] bg-white shadow-md flex flex-col p-5 gap-2">
        <span className="flex items-center justify-between">
          <p>Input Tokens</p>
          <span className=" p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold">{dashboardData?.input_tokens}</p>
        <span className="mt-[2rem] flex items-center justify-between ">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>
      <div className=" w-[15rem] h-[11rem] bg-white shadow-md flex flex-col p-5 gap-2">
        <span className="flex items-center justify-between">
          <p>Output Tokens</p>
          <span className=" p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold">{dashboardData?.output_tokens}</p>
        <span className="mt-[2rem] flex items-center justify-between ">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>
      <div className=" w-[15rem] h-[11rem] bg-white shadow-md flex flex-col p-5 gap-2">
        <span className="flex items-center justify-between">
          <p>Requests</p>
          <span className=" p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold">{dashboardData?.requests}</p>
        <span className="mt-[2rem] flex items-center justify-between ">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>
      <div className=" w-[15rem] h-[11rem] bg-white shadow-md flex flex-col p-5 gap-2">
        <span className="flex items-center justify-between">
          <p>Dollars Spend Input</p>
          <span className=" p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold">{dashboardData?.dollar_spend_input}</p>
        <span className="mt-[2rem] flex items-center justify-between ">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>
      <div className=" w-[15rem] h-[11rem] bg-white shadow-md flex flex-col p-5 gap-2">
        <span className="flex items-center justify-between">
          <p>Dollars Spend Output</p>
          <span className=" p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold">
          {dashboardData?.dollar_spend_output}
        </p>
        <span className="mt-[2rem] flex items-center justify-between ">
          <p className="flex gap-1 items-center justify-center text-[#10C469]">
            <UpArrowIcon /> 5.27%
          </p>
          <p className="text-sm">Since last month</p>
        </span>
      </div>
      <div className=" w-[15rem] h-[11rem] bg-white shadow-md flex flex-col p-5 gap-2">
        <span className="flex items-center justify-between">
          <p>Dollars Spend Total</p>
          <span className=" p-1 bg-[#D4DAF9] rounded-full">
            <GroupIcon />
          </span>
        </span>
        <p className="text-2xl font-bold">{dashboardData?.dollar_spend_total}</p>
        <span className="mt-[2rem] flex items-center justify-between ">
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
