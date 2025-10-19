import React from 'react';
import { NavLink } from 'react-router-dom';
import ThemeSwitcher from './ThemeSwitcher'; // <-- Import the new component

const Header = () => {
  return (
    <header className="app-header">
      <h1>Furniture AI</h1>
      <nav>
        <NavLink to="/" className={({ isActive }) => isActive ? 'active-link' : ''}>Recommendations</NavLink>
        <NavLink to="/analytics" className={({ isActive }) => isActive ? 'active-link' : ''}>Analytics</NavLink>
        <ThemeSwitcher /> {/* <-- Add the switcher here */}
      </nav>
    </header>
  );
};

export default Header;