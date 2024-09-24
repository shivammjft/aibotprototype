import React, { useContext } from 'react';
import ChatIcon from '../assets/ChatIcon';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const logOutHandler = () => {
    localStorage.removeItem('token');
    navigate('/')
  };

  return (
    <div className=" w-[100%] h-[5rem]  flex items-center justify-between bg-[#313A46] ">
      <div className="flex gap-3 items-center ml-[1rem]">
        <ChatIcon />
        <p className="font-bold text-lg text-white">Jellyfish AI Assistant</p>
      </div>
      <div className="flex gap-2">
        {token && (
          <button
            className="mr-[2rem] h-[3rem] w-[8rem] rounded-md border border-[#C9C9CD] text-white"
            onClick={() => {
              navigate('/create/company');
            }}
          >
            Add Company
          </button>
        )}

        {token && (
          <button
            className="mr-[2rem] h-[3rem] w-[8rem] rounded-md border border-[#C9C9CD] text-white"
            onClick={logOutHandler}
          >
            Log Out
          </button>
        )}
      </div>
    </div>
  );
};

export default Navbar;
