import { Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import CompanyDetails from './pages/CompanyDetails';
import AddCompany from './pages/AddCompany';
import ErrorPage from './pages/ErrorPage';
import LoadinsSpinner from './components/LoadinsSpinner';
import CompanyChatBotDetails from './pages/CompanyChatBotDetails';
import SuccessIcon from './components/SuccessIcon';
import AddAdmin from './pages/AddAdmin';
import { useEffect } from 'react';

function App() {
  const token = localStorage.getItem('token');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (token) {
      if (location.pathname === '/') {
        navigate('/admin/dashboard');
      }
    }
  }, [navigate]);

  return (
    <>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/admin/dashboard"
          element={token ? <Dashboard /> : <ErrorPage />}
        />
        <Route
          path="/company/details/:id"
          element={token ? <CompanyDetails /> : <ErrorPage />}
        />
        <Route
          path="/add/company"
          element={token ? <AddCompany /> : <ErrorPage />}
        />
        <Route
          path="/chatbot/:id/queries"
          element={token ? <CompanyChatBotDetails /> : <ErrorPage />}
        />
        <Route path="/success" element={<SuccessIcon />} />
        <Route path="/add/admin" element={<AddAdmin />} />
      </Routes>
    </>
  );
}

export default App;
