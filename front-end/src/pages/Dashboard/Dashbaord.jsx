import React, { useContext, useEffect, useState } from 'react';

import Navbar from '../../components/Navbar';
import Sidebar from './Sidebar';
import DataBoxes from '../../components/DataBoxes';
import ProjectionsBarChart from '../../charts/ProjectionsBarChart';
import TopSellingProductsTable from '../../components/TopSellingProductsTable';
import TotalSalesContainer from '../../components/TotalSalesContainer';
import RecentActivityContainer from '../../components/RecentActivityContainer';

import ImageSlider from '../../components/Slider';
import CompanyBoxes from '../../components/CompanyDataBoxes';
import axios from 'axios';
import AuthContext from '../../context/AuthContext';

const Dashbaord = () => {
  const [dashboardData, setDashboardData] = useState();
  const token = localStorage.getItem('token')

  useEffect(() => {
    async function getData() {
   
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

   

        setDashboardData(res.data.data);
      } catch (err) {
        console.log('Fetch error:', err);
      }
    }
    getData();
  }, [token]);

  

  
  return (
    <div>
      <Navbar />
      <div className="flex  bg-[#FAFBFE]">
        <Sidebar />
        <div className=" h-auto w-[80%] flex flex-col">
          <h2 className="mt-[1rem] ml-[1rem] text-[#6D767E] font-bold w-full">
            DASHBOARD
          </h2>
          <div className=" h-auto mt-[2rem] flex text-[#6D767E] gap-3">
            <DataBoxes dashboardData={dashboardData} />
            <div className="w-[60%] bg-white shadow-md p-5 flex flex-col gap-1  flex items-center justify-center  h-[37rem]">
              <span className="text-xl mt-[1rem]">PROJECTIONS VS ACTUALS</span>
              <ProjectionsBarChart />
            </div>
          </div>
          <div className=" h-auto  text-[#6D767E] flex flex-col mt-[1rem]">
            <h1 className="font-bold  mb-[3rem] mt-[1rem] ml-[1rem]">
              OUR CLIENTS
            </h1>
            <ImageSlider />
            <CompanyBoxes />
          </div>
          <div className="h-[30rem]  mt-[1rem] flex gap-3  p-3">
            <TopSellingProductsTable />
            <TotalSalesContainer />
            <RecentActivityContainer />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashbaord;
