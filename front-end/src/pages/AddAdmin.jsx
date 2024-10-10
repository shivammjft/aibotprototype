import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AddAdmin = () => {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: {
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: '',
    },
    validationSchema: Yup.object({
      username: Yup.string().required('Required'),
      email: Yup.string().email('Invalid email format').required('Required'),
      first_name: Yup.string().required('Required'),
      last_name: Yup.string().required('Required'),
      password: Yup.string()
        .min(7, 'Password must be at least 7 characters')
        .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
        .matches(
          /[^a-zA-Z0-9]/,
          'Password must contain at least one special character'
        )
        .required('Required'),
    }),
    onSubmit: async (values, { resetForm }) => {
      try {
        const res = await axios.post(
          'https://chatbot.teamjft.com/auth/signup',
          {
            ...values,
            role: 'admin',
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );

        if (res.status === 200) {
         
          resetForm();
          navigate('/success', { state: { path: 'dashboard' } });
        }
      } catch (error) {
        console.error('Error:', error);
        const message = error.response?.data.detail.mssg;
        alert(message);
      }
    },
  });

  const handleBackClick = () => {
    navigate(-1);
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
        <div className="w-auto mt-[2rem] p-4">
          <span className="text-[#C7C7CB] font-bold text-2xl">
            ADD SUPER ADMIN
          </span>
          <form
            onSubmit={formik.handleSubmit}
            className="mt-[5rem] flex flex-wrap items-center justify-start w-[70rem] gap-12"
          >
            {['username', 'email', 'first_name', 'last_name', 'password'].map(
              (field) => (
                <div className="flex flex-col gap-2 ml-[2rem]" key={field}>
                  <label htmlFor={field} className="text-xl font-bold">
                    {field
                      .replace('_', ' ')
                      .replace(/\b\w/g, (c) => c.toUpperCase())}
                  </label>
                  <input
                    type={field === 'password' ? 'password' : 'text'}
                    id={field}
                    name={field}
                    value={formik.values[field]}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    className="h-[2.2rem] w-[18rem] outline-none p-2 text-black"
                  />
                  {formik.touched[field] && formik.errors[field] ? (
                    <div className="text-red-500">{formik.errors[field]}</div>
                  ) : null}
                </div>
              )
            )}
          </form>
          <div className="mt-[6rem] flex items-center justify-center gap-5">
            <button
              type="button"
              onClick={formik.handleSubmit}
              className="h-[3.1rem] w-[8rem] rounded-md bg-[#6D62E5]"
            >
              ADD
            </button>
            <button
              type="button"
              className="h-[3.1rem] w-[9rem] rounded-md bg-[#B6B6B6]"
              onClick={handleBackClick}
            >
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

export default AddAdmin;
