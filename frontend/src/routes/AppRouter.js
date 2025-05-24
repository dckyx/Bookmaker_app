import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from '../components/Layout';
import Home from '../pages/Home';
import SpinPage from '../pages/SpinPage';
import UserPanel from '../pages/UserPanel';
import Login from '../pages/Login';

const AppRouter = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/spin" element={<SpinPage />} />
        <Route path="/user-panel" element={<UserPanel />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Layout>
  );
};

export default AppRouter;