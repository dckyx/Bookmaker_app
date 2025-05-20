import React from 'react';
import Header from './Header';
import Sidebar from './SidebarLeft';
import Footer from './Footer';
import '../assets/styles/layout.css';

const Layout = ({ children }) => {
  return (
    <div className="grid-container">
      <Header />
      <div className="info-bar">Informacje</div>
      <main className="content">{children}</main>
      <Sidebar />
      <aside className="sidebar-right">PRAWY PANEL</aside>
      <div className="bottom-content"></div>
      <Footer />
    </div>
  );
};

export default Layout;