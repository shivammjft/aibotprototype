import React, { useEffect, useState } from 'react';
import Navbar from '../../components/Navbar';
import Image from '../../assets/logo-jft.jpeg';
import UpArrowIcon from '../../assets/UpArrowIcon';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';

const CompanyDetail = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [chatbots, setChatbots] = useState([]);
  const { company } = location.state;
  const companyId = company?.id;

  const token = localStorage.getItem('token');

  useEffect(() => {
    async function fetchChatbotList() {
      const res = await axios.get(
        `https://chatbot.teamjft.com/admin/companies/${companyId}/chatbots`,
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setChatbots(res.data.data);
    }

    fetchChatbotList();
  }, []);

  return (
    <div className="flex flex-col items-center">
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
          {company.company_name}
          <p className="text-sm font-serif text-[#6D767E] ">
            {company.base_url}
          </p>
        </span>
        <p className="text-xl ml-[45rem] font-bold text-[#6D767E]">
          ACTIVE CHATBOTS
        </p>
      </div>
      <div className="h-auto mt-[2rem] p-4 flex  flex-wrap gap-10 items-center justify-center pt-8">
        {chatbots?.map((chatbotItem) => {
      

          return (
            <div className=" w-[28rem] h-[22rem] bg-white shadow-md flex flex-col p-5 gap-2 cursor-pointer" onClick={()=>{
              navigate(`/chatbot/${chatbotItem.chatbot_id}/queries`,{state:{chatbot:chatbotItem,id:chatbotItem.chatbot_id,company:company}})

            }}>
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
      <div className="flex gap-3 items-center justify-center mb-[3rem] mt-[6rem]">
        <span className="text-lg">Powered By</span>
        <img src={Image} alt="" className="h-[3rem] w-[3rem]" />
      </div>
    </div>
  );
};

export default CompanyDetail;
