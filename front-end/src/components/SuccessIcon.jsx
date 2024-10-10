import React, { useEffect } from 'react';
import Lottie from 'react-lotties';
import SuccessIconAnimationData from '../assets/lotties/SuccessIcon.json';
import { useLocation, useNavigate } from 'react-router-dom';

const defaultOptions = {
  loop: true,
  autoplay: true,
  animationData: SuccessIconAnimationData,
  rendererSettings: {
    preserveAspectRatio: 'xMidYMid slice',
  },
};

const SuccessIcon = () => {
  const navigate = useNavigate()
  const location = useLocation();
  const path = location.state.path;

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate(`/admin/${path}`);
    }, 2000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="bg-gradient-to-b from-black to-[#343368] text-white p-[2rem] relative flex items-center justify-center h-[100vh]">
      <Lottie options={defaultOptions} height={400} width={400} />
    </div>
  );
};

export default SuccessIcon;
