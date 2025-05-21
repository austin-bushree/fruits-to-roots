// src/App.jsx
import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
// import './App.css';

function App() {
    const [interest, setInterest] = useState('');
    const [groupName, setGroupName] = useState('');
    const [groupNames, setGroupNames] = useState([]);
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchGroupNames = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/dci-group-names`);
                if (!res.ok) {
                    // Log the full response if not ok
                    console.error("Failed to fetch group names. Response:", res);
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                const data = await res.json();
                if (Array.isArray(data)) {
                    setGroupNames(data);
                    setGroupName(data[0] || '');
                } else {
                    console.error("Unexpected data format for group names:", data);
                }
            } catch (error) {
                console.error("Error fetching group names:", error);
            }
        };
        fetchGroupNames();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResponse('');

        try {
            const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/explain-dci`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ group_name: groupName, interest }),
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
                        value={interest}
                        onChange={(e) => setInterest(e.target.value)}
                        required
                    />
                </label>

                <label>
                    Choose a DCI Group from the Next Generation Science Standards (NGSS):
                    <br />
                    <small style={{ fontSize: "0.9em", color: "#555" }}>
                        (Each group represents a cluster of Disciplinary Core Ideas)
                    </small>
                    <br />
                    <select value={groupName} onChange={(e) => setGroupName(e.target.value)} required>
                        {(Array.isArray(groupNames) ? groupNames : []).map((g) => (
                            <option key={g} value={g}>{g}</option>
                        ))}
                    </select>
                </label>

                <button type="submit" disabled={loading}>
                    {loading ? 'Thinking...' : 'Generate DCI Explanation'}
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
