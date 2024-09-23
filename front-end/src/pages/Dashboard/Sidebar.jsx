import React from 'react';
import HomeIcon from '../../assets/HomeIcon';
import ProfileIcon from '../../assets/ProfileIcon';

const Sidebar = () => {
  return (
    <div className="h-auto w-[20%]  flex flex-col">
      <div className="flex items-center  mt-[0.5rem] text-2xl justify-center">
        <div className=" h-auto w-[15rem] mt-[1rem] flex items-center bg-white flex-col gap-4  shadow-md">
          <span className="flex flex-col items-center justify-center h-[6rem]  gap-2">
            <ProfileIcon />
            <p className="text-sm ">Amit Kumar Pandey</p>
          </span>
          <div className=" h-[20rem] w-full p-4">
            <span className="text-sm text-[#7D8C8D]">NAVIGATION</span>
            <div className="h-full ">
              <ul className=" flex flex-col gap-5">
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[1rem] ">
                  <HomeIcon />
                  <p className="text-lg text-[#0059E1] ">Dashboards</p>
                </li>
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[0.3rem] ">
                  <p className="text-lg  ml-[2.2rem]">Analytics</p>
                </li>
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[0.3rem] ">
                  <p className="text-lg ml-[2.2rem]">E-Commerce</p>
                </li>
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[0.3rem] ">
                  <p className="text-lg ml-[2.2rem]">Projects</p>
                </li>
              </ul>
            </div>
          </div>
          <div className="h-[20rem] w-full p-4 mb-[5rem]">
            <span className="text-sm text-[#7D8C8D]">APPS</span>
            <div className="h-full ">
              <ul className=" flex flex-col gap-5">
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[1rem] ">
                  <p className="text-lg  ml-[2.2rem]">Calender</p>
                </li>
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[0.3rem] ">
                  <p className="text-lg  ml-[2.2rem]">Chart</p>
                </li>
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[0.3rem] ">
                  <p className="text-lg ml-[2.2rem]">E-CRM</p>
                </li>
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[0.3rem] ">
                  <p className="text-lg ml-[2.2rem]">Email</p>
                </li>
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[0.3rem] ">
                  <p className="text-lg ml-[2.2rem]">Social Feed</p>
                </li>
                <li className="text-sm text-[#7D8C8D] flex gap-3 items-center mt-[0.3rem] ">
                  <p className="text-lg ml-[2.2rem]">Tasks</p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
