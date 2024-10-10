import React, { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import bgImage from '../assets/background.png';
import animation1 from '../assets/animation1.png';
import animation2 from '../assets/animation2.png';
import animation3 from '../assets/animation3.png';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import LoadinsSpinner from '../components/LoadinsSpinner';

const Login = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
    },
    validationSchema: Yup.object({
      username: Yup.string()
        .required('Username is required')
        .min(3, 'Username must be at least 3 characters long'),
      password: Yup.string()
        .required('Password is required')
        .min(8, 'Password must be at least 7 characters long')
        .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
        .matches(
          /[!@#$%^&*(),.?":{}|<>]/,
          'Password must contain at least one special character'
        ),
    }),
    onSubmit: (values) => {
      LoginHandler(values);
    },
  });

  const LoginHandler = async (values) => {
    setLoading(true);
    const { username, password } = values;

    try {
      const res = await axios.post(
        'https://chatbot.teamjft.com/auth/login',
        {
          username: username,
          password: password,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      const access_token = res.data.access_token;

      localStorage.setItem('token', access_token);
      setLoading(false);
      navigate('/admin/dashboard');
    } catch (error) {
    
      const message = error.response?.data.detail.mssg;
      alert(message);
      setLoading(false);
    }
  };

  return (
    <>
      {loading ? (
        <LoadinsSpinner />
      ) : (
        <div className="relative h-[100vh] bg-cover bg-center bg-gradient-to-b from-black to-[#343368] text-white">
          <img
            src={bgImage}
            className="absolute top-0 left-0 w-full h-full object-cover z-10"
            alt="Background"
          />
          <h2 className="absolute mt-[3rem] ml-[2rem] text-2xl font-bold">
            Jellyfish AI Assistant
          </h2>
          <form
            onSubmit={formik.handleSubmit}
            className="absolute h-[40rem] w-[40rem] mt-[13rem] ml-[5rem] flex flex-col gap-5"
          >
            <h2 className="text-3xl font-bold mt-[2rem] ml-[4.5rem]">
              Login As Admin
            </h2>
            <div className="flex flex-col gap-1 mt-[3rem]">
              <label htmlFor="username" className="font-bold">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                placeholder="Enter Username"
                className={`h-[3rem] rounded-sm w-[25rem] p-5 ${
                  formik.errors.username ? 'border-red-500' : ''
                } bg-white z-10 outline-none text-black`}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.username}
              />
              {formik.touched.username && formik.errors.username ? (
                <div className="text-red-500 text-sm">
                  {formik.errors.username}
                </div>
              ) : null}
            </div>
            <div className="flex flex-col gap-1">
              <label htmlFor="password" className="font-bold">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                placeholder="Enter Password"
                className={`h-[3rem] rounded-sm w-[25rem] p-5 ${
                  formik.errors.password ? 'border-red-500' : ''
                } bg-white z-10 outline-none text-black`}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.password}
              />
              {formik.touched.password && formik.errors.password ? (
                <div className="text-red-500 text-sm">
                  {formik.errors.password}
                </div>
              ) : null}
            </div>

            <button
              type="submit"
              className="mt-[3rem] h-[3rem] w-[25rem] bg-[#6D62E5] z-10 text-xl rounded"
            >
              Log In
            </button>
            <span className="mt-[3rem] ml-[5rem]">
              Powered By Jellyfish Technologies
            </span>
          </form>
          <div className="absolute h-auto w-[40rem] ml-[70rem] mt-[17rem]">
            <img
              src={animation1}
              className="absolute h-[12rem] w-[12rem] top-[10%] left-[20%] transform translate-x-[-50%] translate-y-[-50%]"
              style={{ transform: 'translate(20px, 30px)' }}
            />
            <img
              src={animation2}
              className="absolute h-[12rem] w-[12rem] top-[40%] left-[40%] transform translate-x-[-50%] translate-y-[-50%]"
              style={{ transform: 'translate(40px, 250px)' }}
            />
            <img
              src={animation3}
              className="absolute h-[12rem] w-[12rem] top-[70%] left-[60%] transform translate-x-[-50%] translate-y-[-50%]"
              style={{ transform: 'translate(-400px, 230px)' }}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default Login;
