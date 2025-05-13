// src/App.jsx
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
// import './App.css';

const standards = [
    { id: 'HS-ESS1-4', label: 'HS-ESS1-4: Earth’s Place in the Universe' },
    { id: 'HS-PS3-3', label: 'HS-PS3-3: Energy Design Constraints' },
    { id: 'HS-LS1-3', label: 'HS-LS1-3: Homeostasis and Feedback' },
    // Add more standards as needed
];

function App() {
    const [fruit, setFruit] = useState('');
    const [standardId, setStandardId] = useState(standards[0].id);
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResponse('');

        try {
            const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/fruit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ fruit, standard_id: standardId }),
            });
            const data = await res.json();
            setResponse(data.explanation || data.message || 'No explanation received.');
        } catch (err) {
            console.error(err);
            setResponse('❌ Error retrieving explanation.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <h1>Fruits to Roots</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    What are you interested in?
                    <input
                        type="text"
                        value={fruit}
                        onChange={(e) => setFruit(e.target.value)}
                        required
                    />
                </label>

                <label>
                    Choose an NGSS Standard:
                    <select value={standardId} onChange={(e) => setStandardId(e.target.value)}>
                        {standards.map((s) => (
                            <option key={s.id} value={s.id}>{s.label}</option>
                        ))}
                    </select>
                </label>

                <button type="submit" disabled={loading}>
                    {loading ? 'Thinking...' : 'Generate Root Explanation'}
                </button>
            </form>

            {response && (
                <div className="response-output">
                    <h2>Explanation:</h2>
                    <ReactMarkdown>{response}</ReactMarkdown>
                </div>
            )}
        </div>
    );
}

export default App;
