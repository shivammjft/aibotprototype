import React, { useEffect, useState } from 'react';
import axios from 'axios';

const RecentActivityContainer = () => {
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
    <div className=" w-[25%] shadow-md bg-white p-3 text-[#6D767E]  flex flex-col h-auto">
      <span className="flex items-center justify-between font-bold mt-[1rem]">
        RECENT ACTIVITY
      </span>
      <ul className="p-2 flex flex-col">
        {companies?.map((company) => {
          return (
            <li className="flex flex-col gap-1 mt-[1rem] ">
              <span className="text-md text-[#69DAF4]">You sold an item </span>
              <p className="text-sm text-[#959EA2]">
                {company.company_name} just purchased “Jellyfish - AI Bot!
              </p>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default RecentActivityContainer;
