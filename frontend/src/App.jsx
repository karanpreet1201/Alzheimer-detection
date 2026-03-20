import React, { useContext, useState } from 'react';
import { AuthContext } from './context/AuthContext';
import AuthCard from './components/AuthCard';
import RegistrationStep from './components/RegistrationStep';
import AssessmentStep from './components/AssessmentStep';

function App() {
    const { isAuthenticated, logout } = useContext(AuthContext);
    const [patientData, setPatientData] = useState(null);

    const handlePatientRegistered = (data) => {
        setPatientData(data);
    };

    const handleEditPatient = () => {
        setPatientData(null);
    };

    return (
        <div className="container">
            <header>
                <h1>Neurological Health Assessment</h1>
                <p className="subtitle">Early Alzheimer's Detection via Machine Learning</p>
            </header>

            {!isAuthenticated ? (
                <AuthCard />
            ) : (
                <div id="app-container">
                    {!patientData ? (
                        <RegistrationStep onNext={handlePatientRegistered} />
                    ) : (
                        <AssessmentStep patient={patientData} onEdit={handleEditPatient} />
                    )}
                </div>
            )}

            <footer style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
                <p>Powered by Scikit-Learn, FastAPI, and React. For demonstration purposes only.</p>
                {isAuthenticated && (
                    <button onClick={logout} className="text-btn">Sign Out</button>
                )}
            </footer>
        </div>
    );
}

export default App;
