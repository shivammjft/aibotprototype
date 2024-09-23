import React, { useRef } from 'react';
import Image from '../../assets/linkedin.png';
import Navbar from '../../components/Navbar';
import EditIcon from '../../assets/EditIcon';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CreateCompany = () => {
  const navigate = useNavigate();
  const NameRef = useRef();
  const companyEmailRef = useRef();
  const baseUrlRef = useRef();

  const ChatBotNameRef = useRef();
  const deploymentUrlRef = useRef();

  const AddCompanyHandler = async () => {
    const companyName = NameRef?.current?.value;
    const email = companyEmailRef?.current?.value;
    const baseUrl = baseUrlRef?.current?.value;
    const chatbot = ChatBotNameRef?.current?.value;
    const deploymentUrl = deploymentUrlRef?.current?.value;

    try {
      const res = await axios.post(
        'https://chatbot.teamjft.com/init_company',
        {
          company_name: companyName,
          base_url: baseUrl,
          email: email,
          deployment_url: deploymentUrl,
          chatbot_name: chatbot,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (res.status == 200) {
        navigate('/success', { state: { path: 'dashboard' } });
      }

  
    } catch (err) {
      console.log('Error:', err);
    }
  };

  return (
    <div className=" flex flex-col items-center justify-center h-auto">
      <Navbar />
      <button
        className="h-[3rem] w-[10rem] border border-[#313A46] mr-[100rem] mt-[1rem] hover:bg-gray-400"
        onClick={() => navigate(-1)}
      >
        Back
      </button>

      <div className=" bg-white h-auto w-[80rem] shadow-lg flex flex-col mt-[5rem] mb-[5rem]">
        <div className="h-[10rem] flex items-center">
          <img
            src={Image}
            alt=""
            className="border-4 border-white  h-[10rem] w-[10rem] rounded-full mb-[5rem] ml-[2rem]  -translate-y-5"
          />
          <span className="flex flex-col items-center justify-center text-xl font-bold">
            JellyFish Technologies
            <p className="text-sm font-serif text-[#6D767E] ">
              https:jft.adminurl.com
            </p>
          </span>
        </div>
        <span className="font-bold text-3xl ml-[34.5rem] text-[#6D767E]">
          Add New Company
        </span>

        <div className="p-7">
          <div className=" h-[8rem] flex justify-between items-center ">
            <div className=" w-[20rem] flex flex-col gap-3 items-start justify-center p-2  ml-[1rem]">
              <span className="font-bold text-xl"> Company Name</span>
              <p className="text-sm text-[#6D767E]">
                {' '}
                Update your company name here
              </p>
            </div>
            <input
              type="text"
              className="border border-[#8A9299] w-[20rem] rounded-md h-[2rem] outline-none p-3 "
              ref={NameRef}
            />
          </div>
          <hr />

          <div className=" h-[8rem] flex justify-between items-center ">
            <div className=" w-[20rem] flex flex-col gap-3 items-start justify-center p-2  ml-[1rem]">
              <span className="font-bold text-xl"> Company Email</span>
              <p className="text-sm text-[#6D767E]">
                {' '}
                Update your company email here
              </p>
            </div>
            <input
              type="email"
              className="border border-[#8A9299] w-[20rem] rounded-md h-[2rem] outline-none p-3"
              ref={companyEmailRef}
            />
          </div>
          <hr />
          <div className=" h-[8rem] flex justify-between items-center ">
            <div className=" w-[20rem] flex flex-col gap-3 items-start justify-center p-2  ml-[1rem]">
              <span className="font-bold text-xl"> ChatBot Name</span>
              <p className="text-sm text-[#6D767E]">
                {' '}
                Update your chatbot name here
              </p>
            </div>
            <input
              type="text"
              className="border border-[#8A9299] w-[20rem] rounded-md h-[2rem] outline-none p-3"
              ref={ChatBotNameRef}
            />
          </div>
          <hr />
          <div className=" h-[8rem] flex justify-between items-center ">
            <div className=" w-[20rem] flex flex-col gap-3 items-start justify-center p-2  ml-[1rem]">
              <span className="font-bold text-xl"> Deployment URL</span>
              <p className="text-sm text-[#6D767E]">
                {' '}
                Update your deployment url here
              </p>
            </div>
            <input
              type="text"
              className="border border-[#8A9299] w-[20rem] rounded-md h-[2rem] outline-none p-3"
              ref={deploymentUrlRef}
            />
          </div>
          <hr />

          <div className=" h-[8rem] flex justify-between items-center ">
            <div className=" w-[20rem] flex flex-col gap-3 items-start justify-center p-2  ml-[1rem]">
              <span className="font-bold text-xl"> Base URL</span>
              <p className="text-sm text-[#6D767E]">
                {' '}
                Update your base url here
              </p>
            </div>
            <input
              type="text"
              className="border border-[#8A9299] w-[20rem] rounded-md h-[2rem] outline-none p-3"
              ref={baseUrlRef}
            />
          </div>
          <hr />
          <div className=" h-[12rem] flex justify-between items-center ">
            <div className=" w-[20rem] flex flex-col gap-3 items-start justify-center p-2  ml-[1rem]">
              <span className="font-bold text-xl"> Social Profiles</span>
              <p className="text-sm text-[#6D767E]">
                {' '}
                Enter your social profiles here
              </p>
            </div>
            <div className="flex flex-col gap-1">
              <div className="flex">
                <span className="border border-[#] h-[2rem] w-[8rem] border border-[#8A9299] rounded-l-md flex items-center justify-center text-[#8A9299]  ">
                  twitter.com/
                </span>
                <input
                  type="text"
                  className="border border-[#8A9299] w-[12rem] rounded-r-md h-[2rem] outline-none p-3 border-l-0"
                />
              </div>
              <div className="flex">
                <span className="border border-[#] h-[2rem] w-[8rem] border border-[#8A9299] rounded-l-md flex items-center justify-center text-[#8A9299] ">
                  facebook.com/
                </span>
                <input
                  type="text"
                  className="border border-[#8A9299] w-[12rem] rounded-r-md h-[2rem] outline-none p-3 border-l-0"
                />
              </div>
              <div className="flex">
                <span className="border border-[#] h-[2rem] w-[8rem] border border-[#8A9299] rounded-l-md flex items-center justify-center text-[#8A9299]">
                  instagram.com/
                </span>
                <input
                  type="text"
                  className="border border-[#8A9299] w-[12rem] rounded-r-md h-[2rem] outline-none p-3 border-l-0"
                />
              </div>
            </div>
          </div>
        </div>

        <hr />
        <div className="h-[10rem] flex items-center justify-center">
          <button
            className="bg-black text-white rounded-md w-[7.5rem] h-[2rem] flex items-center justify-center cursor-pointer"
            onClick={AddCompanyHandler}
          >
            Save
          </button>
        </div>
      </div>

      <div className={`flex gap-3 items-center justify-center  mb-[3rem]`}>
        <span className="text-lg">Powered By</span>
        <img src={Image} alt="" className="h-[3rem] w-[3rem]" />
      </div>
      <div></div>
    </div>
  );
};

export default CreateCompany;
