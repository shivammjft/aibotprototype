import React from 'react';

const ErrorPage = () => {
  return (
    <div className="h-[100vh] bg-gradient-to-b from-black to-[#343368] text-white p-[2rem] relative">
        <div className='flex items-center justify-center mt-[3rem] underline'>
            <h2 className='text-xl '>
                Error: Unauthorised
            </h2>
        </div>
    </div>
  );
};

export default ErrorPage;
