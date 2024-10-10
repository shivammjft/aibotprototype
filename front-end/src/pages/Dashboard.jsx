import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';

import DataBoxes from '../components/DataBoxes';
import ChartDataBoxes from '../components/ChartDataBoxes';
import { useNavigate } from 'react-router-dom';
import TopSellingProductsTable from '../components/TopSellingProductsTable';
import CompanyDataBoxes from '../components/CompanyDataBoxes';
import axios from 'axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const [isLogOpen, setIsLogOpen] = useState(false);
  const [dashboardData, setDashboardData] = useState();
  const [companies, setCompanies] = useState([]);
  const token = localStorage.getItem('token');

  const toggleActivityLog = () => {
    setIsLogOpen((prev) => !prev);
  };

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await axios.get(
          'https://chatbot.teamjft.com/admin/total-stats',
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await res.data.data;
        setDashboardData(data);
      } catch (err) {
        console.log(err);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    async function fetchCompanyData() {
      try {
        const res = await axios.get(
          'https://chatbot.teamjft.com/admin/companies',
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await res.data.data;
        setCompanies(data);
      } catch (err) {
        console.log(err);
      }
    }
    fetchCompanyData();
  }, []);

  return (
    <div className="h-auto bg-gradient-to-b from-black to-[#343368] text-white p-[2rem] relative">
      <Navbar />
      <div className="flex">
        <Sidebar />
        <div className="w-[80%] mt-[2rem] flex flex-col p-4">
          <div className="flex items-center justify-between">
            <span className="font-bold text-3xl mt-[1rem]">DASHBOARD</span>
            <div className="relative">
              <button
                className="border w-[8rem] h-[2rem] rounded-md cursor-pointer"
                onClick={toggleActivityLog}
              >
                Activity Log
              </button>

              {isLogOpen && (
                <div
                  className="absolute mb-2 w-[16rem] bg-white text-black shadow-md rounded-md p-4 max-h-[15rem] overflow-y-auto"
                  style={{ left: '-6rem', top: '3rem' }}
                >
                  <span className="flex items-center justify-between font-bold mt-[1rem] text-[#878787]">
                    RECENT ACTIVITY
                  </span>
                  <ul className="p-2 flex flex-col">
                    {companies?.map((company) => {
                      return (
                        <li className="flex flex-col gap-1 mt-[1rem]">
                          <span className="text-md text-[#69DAF4]">
                            You sold an item
                          </span>
                          <p className="text-sm text-[#959EA2]">
                            {company.company_name} just purchased “Jellyfish -
                            AI Bot!
                          </p>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              )}
            </div>
          </div>

          <DataBoxes dashboardData={dashboardData} />
          <ChartDataBoxes companies={companies} />
          <div className="h-auto flex gap-5 mt-[2rem]">
            <CompanyDataBoxes companies={companies} />
            <TopSellingProductsTable />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
