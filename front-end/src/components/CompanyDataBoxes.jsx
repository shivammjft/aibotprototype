import React, { useEffect, useState } from 'react';
import GroupIcon from '../assets/GroupIcon';
import UpArrowIcon from '../assets/UpArrowIcon';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const CompanyBoxes = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    async function fetchCompanies() {
      const res = await axios.get(
        'https://chatbot.teamjft.com/admin/companies',
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        }
      );
 
      setCompanies(res.data.data);
    }

    fetchCompanies();
  }, []);



  return (
    <div className=" w-[40%] flex p-1  gap-7  mt-[8rem] w-full h-full flex-wrap items-center ml-0  ">
      {companies?.map((company) => {
        return (
          <div
            className=" w-[28rem] h-[20rem] bg-white shadow-md flex flex-col p-5 gap-2 cursor-pointer "
            onClick={() => {
              navigate('/company/details' ,{state:{company:company}});
            }}
          >
            <span className="flex items-center justify-between">
              <p>{company.company_name}</p>
              <span className="p-1 bg-[#D4DAF9] rounded-full  h-[3rem] w-[3rem] flex items-center justify-center ">
                <img
                  src="https://cdn-ikpmlll.nitrocdn.com/LtTDqcLjqomDpPealSKvaQjCBBjvWmza/assets/images/optimized/rev-ea58644/www.jellyfishtechnologies.com/wp-content/uploads/2023/10/heffins.png"
                  alt=""
                  className="w-full h-full object-contain rounded-full"
                />
              </span>
            </span>
            <div className="mt-[1rem] flex gap-5 ">
              <span className="flex flex-col items-center ">
                <p className="text-2xl font-bold text-sm">
                  Total input token per model
                </p>
                <p className="text-black text-2xl mt-[1rem]">
                  {' '}
                  {company.input_tokens}
                </p>
              </span>

              <hr className="border border-[#B1BABE] h-[7rem]" />
              <span className="flex flex-col items-center ">
                <p className="text-2xl font-bold text-sm">
                  Total output token per model
                </p>
                <p className="text-black text-2xl mt-[1rem]">
                  {' '}
                  {company.output_tokens}
                </p>
              </span>
            </div>

            <span className="mt-[4rem] flex items-center justify-between ">
              <p className="flex gap-1 items-center justify-center text-[#10C469]">
                <UpArrowIcon /> Price: $5.27
              </p>
              <p className="text-sm">Since last month</p>
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default CompanyBoxes;
