import React, { useState, useContext } from 'react';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';

const AssessmentStep = ({ patient, onEdit }) => {
    const { logout } = useContext(AuthContext);
    const [formData, setFormData] = useState({
        Age: patient.regAge || '',
        EDUC: '',
        SES: '',
        MMSE: '',
        CDR: '',
        eTIV: '',
        nWBV: '',
        ASF: ''
    });
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const payload = {
            fullName: patient.fullName,
            gender: patient.gender === 'Female' ? 'F' : 'M',
            address: patient.address,
            mobile: patient.mobile,
            email: patient.email,
            Age: parseFloat(formData.Age),
            EDUC: parseFloat(formData.EDUC),
            SES: parseFloat(formData.SES),
            MMSE: parseFloat(formData.MMSE),
            CDR: parseFloat(formData.CDR),
            eTIV: parseFloat(formData.eTIV),
            nWBV: parseFloat(formData.nWBV),
            ASF: parseFloat(formData.ASF)
        };

        try {
            const { data } = await api.post('/predict', payload);
            setTimeout(() => setResult(data), 600); // Artificial delay for effect
        } catch (err) {
            alert(`Error: ${err.response?.data?.detail || err.message}`);
            if (err.response?.status === 401) logout();
            setLoading(false);
        }
    };

    if (result) {
        const isEarlySigns = result.prediction === "Early signs detected";
        const probability = (result.probability_early_signs * 100).toFixed(1);
        const confidence = (result.confidence_score * 100).toFixed(1);

        return (
            <main className="glass-card" id="result-container" style={{ animation: 'slideUp 0.5s ease-out' }}>
                <div className="patient-header">
                    <h3>Patient: {patient.fullName}</h3>
                </div>
                <hr className="divider" />
                <h2>Analysis Result</h2>
                
                <div className={`badge ${isEarlySigns ? 'danger' : 'success'}`}>
                    {result.prediction}
                </div>
                
                <div className="confidence-section">
                    <div className="confidence-header">
                        <span>Confidence Level</span>
                        <span style={{ fontWeight: 700 }}>{confidence}%</span>
                    </div>
                    <div className="progress-bar">
                        <div 
                            className="progress-fill" 
                            style={{ width: `${confidence}%`, background: isEarlySigns ? '#ef4444' : '#10b981' }}
                        ></div>
                    </div>
                </div>
                
                <p className="detail-text">
                    {isEarlySigns 
                        ? `The model predicts early signs of Alzheimer's for ${patient.fullName} with a probability of ${probability}%. We recommend consulting a healthcare professional.` 
                        : `The model did not detect concerning early signs for ${patient.fullName} (Probability: ${probability}%).`}
                </p>
                
                <button onClick={() => { setResult(null); setLoading(false); }} className="outline-btn">New Assessment</button>
            </main>
        );
    }

    return (
        <main className="glass-card" id="step2-card">
            <div className="step-indicator">Step 2: Medical Assessment (ADNI)</div>
            
            <div className="patient-header">
                <h3>Assessing Patient: {patient.fullName}</h3>
                <button type="button" onClick={onEdit} className="text-btn">Edit Details</button>
            </div>
            
            <hr className="divider" />

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Patient Age</label>
                    <div className="input-wrapper">
                        <input type="number" name="Age" value={formData.Age} onChange={handleChange} min="40" max="120" step="0.1" required />
                        <span className="unit">Years</span>
                    </div>
                </div>

                <div className="form-group">
                    <label>Years of Education</label>
                    <div className="input-wrapper">
                        <input type="number" name="EDUC" value={formData.EDUC} onChange={handleChange} min="8" max="25" step="1" required />
                        <span className="unit">Yrs</span>
                    </div>
                </div>

                <div className="form-group">
                    <label>Socioeconomic Status (1-5)</label>
                    <select name="SES" value={formData.SES} onChange={handleChange} required>
                        <option value="" disabled>Select SES Level</option>
                        <option value="1">1 (Highest Status)</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5 (Lowest Status)</option>
                    </select>
                </div>
                
                <div className="form-group">
                    <label>MMSE Score (0-30)</label>
                    <div className="input-wrapper">
                        <input type="number" name="MMSE" value={formData.MMSE} onChange={handleChange} min="0" max="30" step="0.1" placeholder="e.g. 28" required />
                    </div>
                </div>

                <div className="form-group">
                    <label>Clinical Dementia Rating (CDR)</label>
                    <select name="CDR" value={formData.CDR} onChange={handleChange} required>
                        <option value="" disabled>Select CDR</option>
                        <option value="0.0">0.0 (Normal)</option>
                        <option value="0.5">0.5 (Very Mild Dementia)</option>
                        <option value="1.0">1.0 (Mild Dementia)</option>
                        <option value="2.0">2.0 (Moderate Dementia)</option>
                    </select>
                </div>
                
                <div className="form-group">
                    <label>Estimated Total Intracranial Volume (eTIV)</label>
                    <div className="input-wrapper">
                        <input type="number" name="eTIV" value={formData.eTIV} onChange={handleChange} min="1000" max="2000" step="1" placeholder="e.g. 1500" required />
                        <span className="unit">cm³</span>
                    </div>
                </div>
                
                <div className="form-group">
                    <label>Normalized Whole Brain Volume (nWBV)</label>
                    <div className="input-wrapper">
                        <input type="number" name="nWBV" value={formData.nWBV} onChange={handleChange} min="0.5" max="0.9" step="0.01" placeholder="e.g. 0.72" required />
                    </div>
                </div>

                <div className="form-group">
                    <label>Atlas Scaling Factor (ASF)</label>
                    <div className="input-wrapper">
                        <input type="number" name="ASF" value={formData.ASF} onChange={handleChange} min="0.8" max="1.6" step="0.01" placeholder="e.g. 1.15" required />
                    </div>
                </div>

                <button type="submit" disabled={loading} className="glow-on-hover mt-3">
                    {!loading ? <span className="btn-text">Analyze Patient Data</span> : <div className="loader"></div>}
                </button>
            </form>
        </main>
    );
};

export default AssessmentStep;
