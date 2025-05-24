import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import SidebarLeft from '../components/SidebarLeft';
import SidebarRight from '../components/SidebarRight';
import InfoBar from '../components/InfoBar';
import './MainLayout.css'; // możesz tu nadać style gridowe

const MainLayout = ({ children }) => {
  return (
    <div className="grid-container">
      <Header />
      <InfoBar />
      <main className="content">{children}</main>
      <SidebarLeft />
      <SidebarRight />
      <Footer />
    </div>
  );
};

export default MainLayout;