import React, { useEffect, useState } from 'react';
import Navbar from '../../components/Navbar';
import ChatBotQueryTable from '../../components/ChatBotQueryTable';
import Image from '../../assets/logo-jft.jpeg';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

const ChatBotQuery = () => {
  const location = useLocation();
  const navigate = useNavigate()
  const { chatbot, id, company } = location.state;
  const [queries, setQueries] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    async function getQueryData() {
      const res = await axios.get(
        `https://chatbot.teamjft.com/admin/chatbots/${chatbot.chatbot_id}/queries`,
        {
          headers: {
            
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setQueries(res.data.data);
    }
    getQueryData();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center">
      <Navbar />
      <button className="h-[3rem] w-[10rem] border border-[#313A46] mr-[100rem] mt-[1rem] hover:bg-gray-400" onClick={()=>navigate(-1)}>
        Back
      </button>
      <div className="h-[10rem] flex items-center mt-[5rem] w-[70%]  ">
        <img
          src={Image}
          alt=""
          className="border-4 border-white  h-[10rem] w-[10rem] rounded-full mb-[5rem] ml-[2rem]  -translate-y-5"
        />
        <span className="flex flex-col items-center justify-center text-xl font-bold">
          {chatbot.chatbot_name}
          <span className="text-sm font-serif text-[#6D767E] flex flex-col mt-[1rem] ">
            <p className="text-black">Total Token Cost</p>
            <p>{chatbot.total_token_cost}</p>
          </span>
        </span>
        <p className="text-xl ml-[45rem] font-bold text-[#6D767E]">
          QUERY RECORDS
        </p>
      </div>
      <ChatBotQueryTable queries={queries} />
      <div className="flex gap-3 items-center justify-center mb-[3rem] mt-[6rem]">
        <span className="text-lg">Powered By</span>
        <img src={Image} alt="" className="h-[3rem] w-[3rem]" />
      </div>
    </div>
  );
};

export default ChatBotQuery;
