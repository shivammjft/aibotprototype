import React from 'react';
import Lottie from 'react-lotties';
import LoadingAnimationData from '../assets/lotties/LoadingSpinner.json';

const defaultOptions = {
  loop: true,
  autoplay: true,
  animationData: LoadingAnimationData,
  rendererSettings: {
    preserveAspectRatio: 'xMidYMid slice',
  },
};

const LoadinsSpinner = () => {
  return (
    <div className="bg-gradient-to-b from-black to-[#343368] text-white p-[2rem] relative flex items-center justify-center h-[100vh]">
      <Lottie options={defaultOptions} height={400} width={400} />
    </div>
  );
};

export default LoadinsSpinner;
