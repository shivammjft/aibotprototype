import React, { useEffect } from 'react';
import Lottie from 'react-lottie';
import animationData from './success-icon.json';
import { useLocation, useNavigate } from 'react-router-dom';

const defaultOptions = {
  loop: true,
  autoplay: true,
  animationData: animationData,
  rendererSettings: {
    preserveAspectRatio: 'xMidYMid slice',
  },
};

const SuccessIcon = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const path = location.state.path;

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate(`/admin/${path}`);
    }, 2000);

    return ()=>clearTimeout(timer);

  },[navigate]);

  return (
    <div className="h-[100vh] w-full flex items-center justify-center">
      <Lottie options={defaultOptions} height={400} width={400} />
    </div>
  );
};

export default SuccessIcon;
