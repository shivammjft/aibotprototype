import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import GroupIcon from '../assets/icons/GroupIcon';
import axios from 'axios';
import ChatBotQueryTable from '../components/ChatBotQueryTable';

const CompanyChatBotDetails = () => {
  const location = useLocation();
  const navigate = useNavigate()
  const id = location.state.id;
  const chatbot = location.state.chatbot;
  const token = localStorage.getItem('token');

  const [queries, setQueries] = useState();

  const roundToThreeDecimals = (num) => {
    return Math.round(num * 1000) / 1000;
  };
  const handleBackClick = () => {
    navigate(-1); 
  };

  useEffect(() => {
    async function getChatBotQueries() {
      try {
        const res = await axios.get(
          `https://chatbot.teamjft.com/admin/chatbots/${id}/queries`,
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token} `,
            },
          }
        );

        const data = await res.data.data;
        setQueries(data);
      } catch (err) {
        console.log(err);
      }
    }
    getChatBotQueries();
  }, []);

  return (
    <div className="h-[100vh] bg-gradient-to-b from-black to-[#343368] text-white p-[2rem] relative">
      <Navbar />
      <button className="border h-[3rem] w-[7rem] mt-[1.2rem] hover:font-bold text-[1rem]" onClick={handleBackClick}>
        Back
      </button>
      <div className="mt-[2rem] flex flex-col">
        <span className="text-[#C7C7CB] font-bold text-2xl">
          CHATBOT INFORMATION
        </span>
      </div>
      <div className="h-[8rem] mt-[1rem] bg-white flex items-center justify-between p-4">
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center justify-center  gap-3">
            <span className="p-1 bg-[#D4DAF9] rounded-full">
              <GroupIcon />
            </span>
            <div className="flex flex-col items-center justify-center text-black">
              <span className="text-xl mt-[1rem]">{chatbot?.chatbot_name}</span>
              <span className="text-[#737787] text-sm">
                {chatbot?.origin_url}
              </span>
            </div>
          </div>

          <div className="flex flex-col items-center justify-center text-black">
            <span className="text-[#737787] font-bold text-2xl">
              {chatbot.total_input_tokens}
            </span>
            <span className="text-[#B4B4B4] text-sm">Total input tokens</span>
          </div>
          <div className="flex flex-col items-center justify-center text-black">
            <span className="text-[#737787] font-bold text-2xl">
              {chatbot?.total_output_tokens}
            </span>
            <span className="text-[#B4B4B4] text-sm">Total Output Tokens</span>
          </div>
          <div className="flex flex-col items-center justify-center text-black">
            <span className="text-[#737787] font-bold text-2xl">
              {roundToThreeDecimals(chatbot?.input_token_cost)}
            </span>
            <span className="text-[#B4B4B4] text-sm">Input Token Cost</span>
          </div>
          <div className="flex flex-col items-center justify-center text-black">
            <span className="text-[#737787] font-bold text-2xl">
              {roundToThreeDecimals(chatbot?.output_token_cost)}
            </span>
            <span className="text-[#B4B4B4] text-sm">Output Token Cost</span>
          </div>
        </div>
      </div>
      <div className="mt-[2rem] flex flex-col">
        <span className="text-[#C7C7CB] font-bold text-2xl">
          CHATBOT QUERIES
        </span>
        <ChatBotQueryTable queries={queries} />
      </div>
    </div>
  );
};

export default CompanyChatBotDetails;
