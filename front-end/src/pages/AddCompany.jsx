import React, { useRef } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AddCompany = () => {
  const navigate = useNavigate();

  // Create refs for each input
  const companyNameRef = useRef();
  const companyEmailRef = useRef();
  const chatbotNameRef = useRef();
  const deploymentURLRef = useRef();
  const baseURLRef = useRef();

  const handleBackClick = () => {
    navigate(-1);
  };

  const submitHandler = async () => {
    const companyName = companyNameRef.current.value;
    const companyEmail = companyEmailRef.current.value;
    const chatbotName = chatbotNameRef.current.value;
    const deploymentURL = deploymentURLRef.current.value;
    const baseURL = baseURLRef.current.value;

    try {
      const res = await axios.post(
        'https://chatbot.teamjft.com/init_company',
        {
          company_name: companyName,
          base_url: baseURL,
          email: companyEmail,
          deployment_url: deploymentURL,
          chatbot_name: chatbotName,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (res.status === 200) {
        navigate('/success', { state: { path: 'dashboard' } });
      }
    } catch (err) {
      console.error('Error:', err);
    }
  };

  return (
    <div className="h-auto bg-gradient-to-b from-black to-[#343368] text-white p-[2rem] relative">
      <Navbar />
      <button
        className="border h-[3rem] w-[7rem] mt-[1.2rem] hover:font-bold text-[1rem]"
        onClick={handleBackClick}
      >
        Back
      </button>
      <div className="h-[60rem] mt-[2rem] flex gap-5">
        <Sidebar />
        <div className="w-auto mt-[2rem] p-4 ">
          <span className="text-[#C7C7CB] font-bold text-2xl">
            ADD COMPANY
          </span>
          <div className="mt-[5rem] flex flex-wrap items-center justify-start w-[70rem]">
            <div className="flex flex-col gap-2 ml-[2rem]">
              <label htmlFor="companyName" className="text-xl font-bold">
                Company Name
              </label>
              <input
                type="text"
                ref={companyNameRef}
                className="h-[2.2rem] w-[18rem] outline-none p-2 text-black"
              />
            </div>
            <div className="flex flex-col gap-2 ml-[2rem]">
              <label htmlFor="companyEmail" className="text-xl font-bold">
                Company Email
              </label>
              <input
                type="text"
                ref={companyEmailRef}
                className="h-[2.2rem] w-[18rem] outline-none p-2 text-black"
              />
            </div>
            <div className="flex flex-col gap-2 ml-[2rem]">
              <label htmlFor="chatbotName" className="text-xl font-bold">
                Chatbot Name
              </label>
              <input
                type="text"
                ref={chatbotNameRef}
                className="h-[2.2rem] w-[18rem] outline-none p-2 text-black"
              />
            </div>
            <div className="flex flex-col gap-2 ml-[2rem] mt-[3rem]">
              <label htmlFor="deploymentURL" className="text-xl font-bold">
                Deployment URL
              </label>
              <input
                type="text"
                ref={deploymentURLRef}
                className="h-[2.2rem] w-[18rem] text-black outline-none p-2"
              />
            </div>
            <div className="flex flex-col gap-2 mt-[3rem] ml-[2rem]">
              <label htmlFor="baseURL" className="text-xl font-bold">
                Base URL
              </label>
              <input
                type="text"
                ref={baseURLRef}
                className="h-[2.2rem] w-[18rem] outline-none p-2 text-black outline-none p-2"
              />
            </div>
          </div>
          <div className="mt-[6rem] flex items-center justify-center gap-5">
            <button
              className="h-[3.1rem] w-[8rem] rounded-md bg-[#6D62E5]"
              onClick={submitHandler}
            >
              ADD
            </button>
            <button className="h-[3.1rem] w-[9rem] rounded-md bg-[#B6B6B6]">
              CANCEL
            </button>
          </div>
        </div>
      </div>
      <div className="flex items-center justify-center">
        Powered By Jellyfish Technologies
      </div>
    </div>
  );
};

export default AddCompany;
