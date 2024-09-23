import React from 'react';

const AuthContext = React.createContext({
  AccessToken: null,
  isLoggedIn: false,
  LogInHandler: () => {},
  LogOutHandler: () => {},
});

export default AuthContext;
