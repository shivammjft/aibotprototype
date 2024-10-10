import React from 'react';
import FormIcon from '../assets/icons/FormIcon';
import AddCompanyIcon from '../assets/icons/AddCompanyIcon';
import LogOutIcon from '../assets/icons/LogOutIcon';
import DashboardIcon from '../assets/icons/DashboardIcon';
import { useNavigate } from 'react-router-dom';
import DetailsIcon from '../assets/icons/DetailsIcon';

const Sidebar = () => {
  const navigate = useNavigate();

  const LogOutHandler = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div className=" h-[53rem] w-[20%] mt-[2rem] bg-white rounded-md flex flex-col ">
      <div className=" flex flex-col items-center justify-center mt-[2rem]">
        <span className="text-[#3A356F] text-2xl font-bold">AKP</span>
        <p className="text-[#5F5F5F] font-bold">Amit Kumar Pandey</p>
        <hr className="mt-[1rem] w-[80%]" />
      </div>

      <ul className="h-auto p-3 mt-[3rem]">
        <li
          className=" flex items-center justify-between p-2 mb-[1rem] cursor-pointer hover:bg-[#6D62E5] text-[#767B8B] hover:text-white "
          onClick={() => {
            navigate('/admin/dashboard');
          }}
        >
          <DashboardIcon />
          <p className="">Dashboard</p>
        </li>

        <li
          className="flex  items-center justify-between p-2 mb-[1rem] cursor-pointer hover:bg-[#6D62E5] text-[#767B8B] hover:text-white"
          onClick={() => {
            navigate('/add/company');
          }}
        >
          <AddCompanyIcon />
          <p className="">Add Company</p>
        </li>
        <li
          className="flex  items-center justify-between p-2 mb-[1rem] cursor-pointer hover:bg-[#6D62E5] text-[#767B8B] hover:text-white"
          onClick={() => {
            navigate('/add/admin');
          }}
        >
          <AddCompanyIcon />
          <p className="">Add Admin</p>
        </li>
      </ul>
      <div className="text-[#767B8B] mt-[29rem] flex items-center justify-center gap-2 mr-[12rem]">
        <LogOutIcon />
        <button onClick={LogOutHandler}>Log Out</button>
      </div>
    </div>
  );
};

export default Sidebar;
