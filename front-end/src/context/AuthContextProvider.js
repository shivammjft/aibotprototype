import { useReducer } from 'react';
import AuthContext from './AuthContext';

const initialState = {
  AccessToken: null,
  isLoggedIn: false,
};

const reducer = (state, action) => {
  if (action.type === 'login') {
    const newobj = { ...state, AccessToken: action.value, isLoggedIn: true };
  
    return newobj;
  } else if (action.type === 'logout') {
    return { ...state, AccessToken: null, isLoggedIn: false };
  }

  return state;
};

export const AuthContextProvider = (props) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  const LogInHandler = (token) => {
  
    dispatch({ type: 'login', value: token });
  };

  const LogOutHandler = () => {
    dispatch({ type: 'logout' });
  };

  const value = {
    AccessToken: state.AccessToken,
    isLoggedIn: state.isLoggedIn,
    LogInHandler,
    LogOutHandler,
  };

  return (
    <AuthContext.Provider value={value}>{props.children}</AuthContext.Provider>
  );
};
