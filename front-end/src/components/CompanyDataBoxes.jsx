import React, { useEffect, useState } from 'react';
import ExpandIcon from '../assets/icons/ExpandIcon';
import GroupIcon from '../assets/icons/GroupIcon';
import UpArrowIcon from '../assets/icons/UpArrowIcon';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CompanyDataBoxes = ({ companies }) => {
  const token = localStorage.getItem('token');
  const navigate = useNavigate();

  return (
    <div className="h-[40rem] max-h-[60rem] overflow-y-auto w-[40%] bg-white rounded-md flex flex-col items-center">
      {companies?.map((company) => {
        return (
          <div
            key={company.id}
            className=" w-[30rem] h-[15rem] bg-white shadow-md flex flex-col p-5 gap-2 cursor-pointer rounded-md border mt-[2rem]  "
            onClick={() => {
              navigate(`/company/details/${company.id}`, {
                state: { company: company },
              });
            }}
          >
            <span className="flex items-center justify-between">
              <div className="flex gap-2 items-center justify-center">
                <span className=" p-1 bg-[#D4DAF9] rounded-full">
                  <GroupIcon />
                </span>
                <p className="text-[#878787] text-[1.2rem] font-bold">
                  {company.company_name}
                </p>
              </div>

              <ExpandIcon />
            </span>
            <div className="mt-[1rem] flex gap-5 ">
              <span className="flex flex-col items-center ">
                <p className="text-[1.7rem] font-bold text-sm text-[#767B8B]">
                  {company.input_tokens}
                </p>
                <p className="text-black text-sm mt-[1rem] text-[#B4B4B4]">
                  {' '}
                  Total input tokens per model
                </p>
              </span>

              <hr className="border border-[#B1BABE] h-[7rem]" />
              <span className="flex flex-col items-center ">
                <p className="text-[1.7rem] font-bold text-sm text-[#767B8B]">
                  {company.output_tokens}
                </p>
                <p className="text-black text-sm mt-[1rem] text-[#B4B4B4]">
                  {' '}
                  Total output tokens per model
                </p>
              </span>
            </div>

            <span className="flex items-center justify-between ">
              <p className="flex gap-1 items-center justify-center text-[#10C469]">
                <UpArrowIcon /> Price: $5.27
              </p>
              <p className="text-sm text-[#767B8B]">Since last month</p>
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default CompanyDataBoxes;
