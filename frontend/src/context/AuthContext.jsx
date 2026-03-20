import React, { createContext, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('alzToken') || null);
    const [user, setUser] = useState({
        username: localStorage.getItem('alzUsername') || '',
        email: localStorage.getItem('alzEmail') || ''
    });

    const login = (tokenData, userData) => {
        localStorage.setItem('alzToken', tokenData);
        if (userData.username) localStorage.setItem('alzUsername', userData.username);
        if (userData.email) localStorage.setItem('alzEmail', userData.email);
        
        setToken(tokenData);
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem('alzToken');
        localStorage.removeItem('alzUsername');
        localStorage.removeItem('alzEmail');
        setToken(null);
        setUser({ username: '', email: '' });
    };

    return (
        <AuthContext.Provider value={{ token, user, login, logout, isAuthenticated: !!token }}>
            {children}
        </AuthContext.Provider>
    );
};
