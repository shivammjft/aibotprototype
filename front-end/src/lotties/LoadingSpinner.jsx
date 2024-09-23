import React, { useEffect } from 'react';
import Lottie from 'react-lottie';
import animationData from './loading-spinner.json';
import { useLocation, useNavigate } from 'react-router-dom';

const defaultOptions = {
  loop: true,
  autoplay: true,
  animationData: animationData,
  rendererSettings: {
    preserveAspectRatio: 'xMidYMid slice',
  },
};

const LoadingSpinner = () => {
  return (
    <div className="h-[100vh] w-full flex items-center justify-center">
      <Lottie options={defaultOptions} height={200} width={200} />
    </div>
  );
};

export default LoadingSpinner;
