'use client';

import { useState } from "react";

import api from '@/hooks/api';

export default function SignUp() {
  const [newUser, setNewUser] = useState({
    firstName: '',
    lastName: '',
    emailAddress: '',
    phoneNumber: '',
    username: '',
    password: '',
  });

  const [confPwd, setConfPwd] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === 'confPwd') {
      setConfPwd(value);
    } else {
      setNewUser({
        ...newUser,
        [name]: value,
      });
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (newUser.password !== confPwd) {
      alert("Passwords Do Not Match!");
    };

    try {
      const response = await api.post('/auth/sign-up', newUser);

      if (response.status === 200) {
        alert("Account Created Successfully!");
      } else {
        alert("Problem Creating Account");
      };
    } catch (err) {
      console.error(err);

      alert("Issue Creating Account");
    };
  };

  return (
    <div className="flex flex-row items-start justify-start w-full min-h-screen"></div>
  );
};
