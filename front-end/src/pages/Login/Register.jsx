import React, { useContext, useEffect, useRef, useState } from 'react';
import Navbar from '../../components/Navbar';
import { Link, json, useLocation, useNavigate } from 'react-router-dom';
import Image from '../../assets/logo-jft.jpeg';
import { ErrorMessage, Field, Form, Formik } from 'formik';
import * as Yup from 'yup';
import LoadingSpinner from '../../lotties/LoadingSpinner';
import AuthContext from '../../context/AuthContext';

const validationSchema = Yup.object({
  username: Yup.string().required('Username is required'),
  password: Yup.string()
    .required('Password is required')
    .min(8, 'Password must be atleast 8 characters long')
    .matches(/[A-Z]/, 'Password must contain atleast one uppercase character')
    .matches(/[0-9]/, 'Password must contain atleast one numeric digit')
    .matches(/[\W_]/, 'Password must contain atleast one special character'),
});

const Register = ({ type, setTokenHandler }) => {
  const navigate = useNavigate();

  const Authctx = useContext(AuthContext);

  const handleRegister = async (values) => {};
  const [loading, setLoading] = useState(false);

  // const handleRegister = async (values) => {
  //   const email = emailInputRef.current.value;
  //   const password = passwordRef.current.value;
  //   const username = usernameRef.current.value;
  //   const firstName = firstNameRef.current.value;
  //   const lastName = lastNameRef.current.value;
  //   console.log('type is', type);

  //   console.log('came here', email, password);

  //   try {
  //     const res = await fetch('http://64.227.160.209:8000/auth/signup', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({
  //         username: username,
  //         email: email,
  //         first_name: firstName,
  //         last_name: lastName,
  //         password: password,
  //         role: 'superAdmin',
  //       }),
  //     });

  //     const data = await res.json();
  //     const status = data.detail.status;

  //     console.log('status is', status);
  //     setStatus(status);
  //     if (status) {
  //       navigate('/register/success');
  //    REgos }
  //   } catch (err) {
  //     console.log(err);
  //   }
  // };

  const handleLogin = async (values) => {
    const username = values.username;
    const password = values.password;

    try {
      setLoading(true);
      const res = await fetch('https://chatbot.teamjft.com/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        
        alert(errorData.detail.mssg);
  
        setLoading(false);
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      const access_token = data.access_token;
      Authctx.LogInHandler(access_token);
      setLoading(false);
      localStorage.setItem('token', access_token);
      navigate('/admin/dashboard');
    } catch (err) {
      console.error('error is', err.message);
    }
  };

  return (
    <div className="flex flex-col justify-center items-center ">
      {loading === true ? (
        <LoadingSpinner />
      ) : (
        <>
          <Navbar />
          <Formik
            initialValues={{
              username: '',
              password: '',
            }}
            validationSchema={validationSchema}
            onSubmit={(values) => {
              type === 'register'
                ? handleRegister(values)
                : handleLogin(values);
            }}
          >
            {({ errors, touched }) => {
              return (
                <Form className=" mt-[10rem] w-[33rem] h-[40rem] flex flex-col items-center">
                  <span className="mt-[1rem] text-2xl">
                    {type === 'register' ? 'Register' : 'Login'} as Admin
                  </span>
                  <div className=" h-auto mt-[2rem] flex flex-col gap-10 w-full">
                    {/* {type === 'register' && (
                  <>
                    <div className="flex flex-col gap-2">
                      <label htmlFor="" className="text-sm">
                        First Name
                      </label>
                      <input
                        type="text"
                        placeholder="Enter first name"
                        className="border border-[#C9C9CD] h-[2.5rem] rounded-md p-[1rem] outline-none"
                        ref={firstNameRef}
                      />
                    </div>
                    <div className="flex flex-col gap-2">
                      <label htmlFor="" className="text-sm">
                        Last Name
                      </label>
                      <input
                        type="text"
                        placeholder="Enter last name"
                        className="border border-[#C9C9CD] h-[2.5rem] rounded-md p-[1rem] outline-none"
                        ref={lastNameRef}
                      />
                    </div>
                    <div className="flex flex-col gap-2">
                      <label htmlFor="" className="text-sm">
                        Business Email
                      </label>
                      <input
                        type="email"
                        placeholder="name@work-email.com"
                        className="border border-[#C9C9CD] h-[2.5rem] rounded-md p-[1rem] outline-none"
                        ref={emailInputRef}
                      />
                    </div>
                  </>
                )} */}
                    <div className="flex flex-col gap-2">
                      <label htmlFor="" className="text-sm">
                        Username
                      </label>
                      <Field
                        type="text"
                        name="username"
                        placeholder="Enter Username"
                        className={`border ${
                          errors.username && touched.username
                            ? 'border-red-500'
                            : 'border-[#C9C9CD]'
                        } h-[2.5rem] rounded-md p-[1rem] outline-none`}
                      />
                      <ErrorMessage
                        name="username"
                        component="div"
                        className="text-red-500 text-sm"
                      />
                    </div>

                    <div className=" flex flex-col gap-2">
                      <span className="flex justify-between">
                        <label htmlFor="" className="text-sm">
                          Password
                        </label>
                        <Link className="text-blue-500 text-sm">
                          Forgot Password?
                        </Link>
                      </span>

                      <Field
                        type="password"
                        name="password"
                        placeholder="Enter your password"
                        className={`border ${
                          errors.password && touched.password
                            ? 'border-red-500'
                            : 'border-[#C9C9CD]'
                        } h-[2.5rem] rounded-md p-[1rem] outline-none`}
                      />
                      <ErrorMessage
                        name="password"
                        component="div"
                        className="text-red-500 text-sm"
                      />
                    </div>
                    <button
                      className="w-full h-[3rem]  rounded-md bg-[#0059E1] text-white font-bold"
                      type="submit"
                    >
                      Sign Up
                    </button>
                    {type === 'register' && (
                      <span
                        className="text-blue-500  flex items-center justify-center cursor-pointer"
                        onClick={() => {
                          navigate('/admin/login');
                        }}
                      >
                        Already have an account?
                      </span>
                    )}
                  </div>
                </Form>
              );
            }}
          </Formik>
          <div
            className={`flex gap-3 items-center justify-center ${
              type == 'register' ? 'mt-[8rem] ' : 'mt-[-8rem]'
            } mb-[3rem]`}
          >
            <span className="text-lg">Powered By</span>
            <img src={Image} alt="" className="h-[3rem] w-[3rem]" />
          </div>
        </>
      )}
    </div>
  );
};

export default Register;
