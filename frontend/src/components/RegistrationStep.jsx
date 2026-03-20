import React, { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';

const RegistrationStep = ({ onNext }) => {
    const { user } = useContext(AuthContext);
    const [formData, setFormData] = useState({
        fullName: user.username || '',
        regAge: '',
        gender: '',
        address: '',
        mobile: '',
        email: user.email || ''
    });

    useEffect(() => {
        setFormData(prev => ({
            ...prev,
            fullName: user.username || prev.fullName,
            email: user.email || prev.email
        }));
    }, [user]);

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = (e) => {
        e.preventDefault();
        onNext(formData);
    };

    return (
        <main className="glass-card" id="step1-card">
            <div className="step-indicator">Step 1: Patient Registration</div>
            
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Patient Full Name</label>
                    <input type="text" name="fullName" value={formData.fullName} onChange={handleChange} placeholder="e.g. John Doe" required />
                </div>

                <div className="form-row">
                    <div className="form-group half">
                        <label>Age</label>
                        <div className="input-wrapper">
                            <input type="number" name="regAge" value={formData.regAge} onChange={handleChange} min="40" max="120" placeholder="e.g. 70" required />
                            <span className="unit">Yrs</span>
                        </div>
                    </div>
                    <div className="form-group half">
                        <label>Gender</label>
                        <select name="gender" value={formData.gender} onChange={handleChange} required>
                            <option value="" disabled>Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                </div>

                <div className="form-group">
                    <label>Address</label>
                    <textarea name="address" rows="2" value={formData.address} onChange={handleChange} placeholder="Patient Address" required></textarea>
                </div>

                <div className="form-row">
                    <div className="form-group half">
                        <label>Mobile Number</label>
                        <input type="tel" name="mobile" value={formData.mobile} onChange={handleChange} pattern="[0-9]{10,15}" placeholder="e.g. 9876543210" required />
                    </div>
                    <div className="form-group half">
                        <label>Email ID</label>
                        <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="e.g. email@example.com" required />
                    </div>
                </div>

                <button type="submit" className="glow-on-hover mt-3">
                    <span className="btn-text">Continue to Assessment &rarr;</span>
                </button>
            </form>
        </main>
    );
};

export default RegistrationStep;
