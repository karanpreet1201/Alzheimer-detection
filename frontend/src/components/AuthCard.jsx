import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

const AuthCard = () => {
    const { login } = useContext(AuthContext);
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({ username: '', email: '', password: '' });
    const [error, setError] = useState('');
    const [msg, setMsg] = useState('');

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setMsg('');

        try {
            if (isLogin) {
                const params = new URLSearchParams();
                params.append('username', formData.username);
                params.append('password', formData.password);

                const { data } = await api.post('/login', params);
                login(data.access_token, { username: data.username, email: data.email });
            } else {
                await api.post('/register', formData);
                setMsg('Account created! Please log in.');
                setIsLogin(true);
                setFormData(prev => ({ ...prev, password: '' }));
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Server error. Try again.');
        }
    };

    return (
        <main className="glass-card" id="auth-card">
            <div className="auth-tabs">
                <button type="button" className={`tab-btn ${isLogin ? 'active' : ''}`} onClick={() => { setIsLogin(true); setError(''); setMsg(''); }}>Login</button>
                <button type="button" className={`tab-btn ${!isLogin ? 'active' : ''}`} onClick={() => { setIsLogin(false); setError(''); setMsg(''); }}>Register</button>
            </div>
            
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Username</label>
                    <input type="text" name="username" value={formData.username} onChange={handleChange} required />
                </div>
                {!isLogin && (
                    <div className="form-group">
                        <label>Email</label>
                        <input type="email" name="email" value={formData.email} onChange={handleChange} required />
                    </div>
                )}
                <div className="form-group">
                    <label>Password</label>
                    <input type="password" name="password" value={formData.password} onChange={handleChange} required />
                </div>
                
                <button type="submit" className="glow-on-hover mt-3">
                    <span className="btn-text">{isLogin ? 'Sign In' : 'Create Account'}</span>
                </button>
                
                {error && <div className="error-text" style={{ color: 'var(--danger)' }}>{error}</div>}
                {msg && <div className="error-text" style={{ color: 'var(--success)' }}>{msg}</div>}
            </form>
        </main>
    );
};

export default AuthCard;
