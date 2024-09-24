import logo from './logo.svg';
import './App.css';
import { Route, Router, Routes } from 'react-router-dom';
import Register from './pages/Login/Register';
import React, { useContext, useEffect, useState } from 'react';
import Dashbaord from './pages/Dashboard/Dashbaord';
import SuccessIcon from './lotties/SuccessIcon';
import CompanyDetail from './pages/Company/CompanyDetail';
import CreateCompany from './pages/Company/CreateCompany';
import { AuthContextProvider } from './context/AuthContextProvider';
import AuthContext from './context/AuthContext';
import ChatBotQuery from './pages/Chatbot/ChatBotQuery';
import Layout from './components/Layout';
import ErrorPage from './components/ErrorPage';

function App() {
  const [logIn, setIsLoggedIn] = useState(
    AuthContext.isLoggedIn || localStorage.getItem('token')
  );

  return (
    <AuthContextProvider>
      <Routes>
        <Route path="/" element={<Register type="login" />} />
        <Route
          path="/admin/dashboard"
          element={<>{logIn && <Dashbaord />}</>}
        />
        <Route path="/success" element={<SuccessIcon />} />

        <Route
          path="/create/company"
          element={logIn ? <CreateCompany /> : <ErrorPage />}
        />
        <Route
          path="/company/details"
          element={logIn ? <CompanyDetail /> : <ErrorPage />}
        />
        <Route
          path="/chatbot/:id/queries"
          element={logIn ? <ChatBotQuery /> : <ErrorPage />}
        />
        <Route path="/layout" element={<Layout />} />
      </Routes>
    </AuthContextProvider>
  );
}

export default App;
