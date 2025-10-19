import React, { createContext, useState, useEffect } from 'react';

// Create the context with a default value
export const ThemeContext = createContext();

// Create a provider component
export const ThemeProvider = ({ children }) => {
  // State to hold the current theme. 'light' is the default.
  // We check localStorage to see if the user had a theme saved from a previous visit.
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

  // This effect runs when the theme state changes
  useEffect(() => {
    const body = document.body;
    // Remove the old theme class and add the new one
    body.classList.remove('light-theme', 'dark-theme');
    body.classList.add(`${theme}-theme`);
    // Save the user's preference in localStorage
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Function to toggle between light and dark
  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  // Provide the theme and the toggle function to all children components
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};