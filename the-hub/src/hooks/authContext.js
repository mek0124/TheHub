/*
This authContext.js file is used solely for logging
the user in/out, retrieving the user's data (excluding their password)
and storing/deleting that data in local storage.
*/

import { createContext, useContext, useState, useEffect } from 'react';

import api from './apis';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState('');

  const navigate = useNavigate('');

  useEffect(() => {
    const loggedUserJSON = window.localStorage.getItem('loggedUser');
    const token = window.localStorage.getItem('token');

    if (loggedUserJSON && token) {
      setUser(JSON.parse(loggedUserJSON));
      setToken(token);
    }
  }, []);

  const login = async (postData) => {
    try {
      const response = await api.post('/auth/login', postData);

      if (response.status === 200) {
        const { message, token, user } = response.data;

        /*
        TODO:

        ? - Incorporate the apps ability to "remmeber" the user
        ?   to allow for easier login
        */

        window.localStorage.setItem('loggedUser', JSON.stringify(user));
        window.localStorage.setItem('token', token);

        setUser(user);
        setToken(token);

        return {
          status: 200,
          message: message,
        };
      }
    } catch (err) {
      console.error(err);
      return {
        status: err.status,
        message: err.response.data.message
      };
    };
  };

  const logout = () => {
    /*
    TODO:

    ? - Incorporate check system for if user is "remmebered"
    ?   then local storage will **not** delete their information.
    */

    window.localStorage.removeItem('loggedUser');
    window.localStorage.removeItem('token');

    setUser(null);
    setToken('');

    setTimeout(() => {
      return navigate('/');
    }, 2000);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
};

export const useAuth = () => useContext(AuthContext);
