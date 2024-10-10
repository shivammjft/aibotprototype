import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import GroupIcon from '../assets/icons/GroupIcon';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

const CompanyDetails = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const company = location.state.company;
  const token = localStorage.getItem('token');
  const [chatbots, setChatBots] = useState([]);

  const roundToThreeDecimals = (num) => {
    return Math.round(num * 1000) / 1000;
  };
  const handleBackClick = () => {
    navigate(-1);
  };

  useEffect(() => {
    async function getCompanyChatBots() {
      try {
        const res = await axios.get(
          `https://chatbot.teamjft.com/admin/companies/${company.id}/chatbots`,
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await res.data.data;
        setChatBots(data);
      } catch (err) {
        console.log(err);
      }
    }
    getCompanyChatBots();
  }, []);

  return (
    <div className="h-[100vh] bg-gradient-to-b from-black to-[#343368] text-white p-[2rem] relative">
      <Navbar />
      <button
        className="border h-[3rem] w-[7rem] mt-[1.2rem] hover:font-bold text-[1rem]"
        onClick={handleBackClick}
      >
        Back
      </button>
      <div className="mt-[2rem] flex flex-col">
        <span className="text-[#C7C7CB] font-bold text-2xl">
          COMPANY INFORMATION
        </span>
      </div>
      <div className="h-[8rem] mt-[1rem] bg-white flex items-center justify-between p-4">
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center justify-center  gap-3">
            <span className="p-1 bg-[#D4DAF9] rounded-full">
              <GroupIcon />
            </span>
            <div className="flex flex-col items-center justify-center text-black">
              <span className="text-xl mt-[1rem]">{company?.company_name}</span>
              <span className="text-[#737787] text-sm">
                {company?.base_url}
              </span>
            </div>
          </div>

          <div className="flex flex-col items-center justify-center text-black">
            <span className="text-[#737787] font-bold text-2xl">
              {company.input_tokens}
            </span>
            <span className="text-[#B4B4B4] text-sm">Total input tokens</span>
          </div>
          <div className="flex flex-col items-center justify-center text-black">
            <span className="text-[#737787] font-bold text-2xl">
              {company?.output_tokens}
            </span>
            <span className="text-[#B4B4B4] text-sm">Total Output Tokens</span>
          </div>
          <div className="flex flex-col items-center justify-center text-black">
            <span className="text-[#737787] font-bold text-2xl">
              {roundToThreeDecimals(company?.input_token_cost)}
            </span>
            <span className="text-[#B4B4B4] text-sm">Input Token Cost</span>
          </div>
          <div className="flex flex-col items-center justify-center text-black">
            <span className="text-[#737787] font-bold text-2xl">
              {roundToThreeDecimals(company?.output_token_cost)}
            </span>
            <span className="text-[#B4B4B4] text-sm">Output Token Cost</span>
          </div>
        </div>
      </div>
      <div className="mt-[2rem] flex flex-col">
        <span className="text-[#C7C7CB] font-bold text-2xl">
          ACTIVE CHATBOTS
        </span>
        <div className="h-auto flex items-center flex-wrap mt-[2rem]">
          {chatbots?.map((chatbotItem) => {
            return (
              <div
                key={chatbotItem.chatbot_id}
                className=" w-[28rem] h-[22rem] bg-white shadow-md flex flex-col p-5 gap-2 cursor-pointer text-black"
                onClick={() => {
                  navigate(`/chatbot/${chatbotItem.chatbot_id}/queries`, {
                    state: {
                      chatbot: chatbotItem,
                      id: chatbotItem.chatbot_id,
                      company: company,
                    },
                  });
                }}
              >
                <span className="flex items-center justify-between">
                  <p>{chatbotItem.chatbot_name}</p>
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
                      Total input tokens
                    </p>
                    <p className="text-black text-2xl mt-[1rem]">
                      {chatbotItem.total_input_tokens}
                    </p>
                  </span>

                  <hr className="border border-[#B1BABE] h-[7rem]" />
                  <span className="flex flex-col items-center ">
                    <p className="text-2xl font-bold text-sm">
                      Total output tokens
                    </p>
                    <p className="text-black text-2xl mt-[1rem]">
                      {chatbotItem.total_output_tokens}
                    </p>
                  </span>
                </div>

                <span className="mt-[4rem] flex items-center justify-between ">
                  <p className="flex gap-1 items-center justify-center text-[#10C469]">
                    Queries: {chatbotItem.total_queries}
                  </p>

                  <span>
                    <p className="text-sm text-black"> Total token cost</p>
                    <p>{chatbotItem.total_token_cost}</p>
                  </span>
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default CompanyDetails;
