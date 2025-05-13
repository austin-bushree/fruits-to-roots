import { useState } from 'react';

function App() {
    const [fruit, setFruit] = useState('');
    const [rootResult, setRootResult] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setRootResult('');

        try {
            const response = await fetch(import.meta.env.VITE_BACKEND_URL + '/api/fruit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ fruit }),
            });

            if (!response.ok) throw new Error('Network error');

            const data = await response.json();
            setRootResult(data.message || data.result || 'No response received.');
        } catch (err) {
            console.error(err);
            setRootResult('Sorry, something went wrong.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '600px', margin: '4rem auto', fontFamily: 'sans-serif' }}>
            <h1>Fruits to Roots</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    What are you curious about? (Enter a fruit) <br />
                    <input
                        type="text"
                        value={fruit}
                        onChange={(e) => setFruit(e.target.value)}
                        placeholder="e.g., space travel"
                        style={{ width: '100%', padding: '0.5rem', fontSize: '1rem' }}
                    />
                </label>
                <br />
                <button
                    type="submit"
                    disabled={loading || !fruit}
                    style={{ marginTop: '1rem', padding: '0.5rem 1rem' }}
                >
                    {loading ? 'Thinking...' : 'Find My Root'}
                </button>
            </form>

            {rootResult && (
                <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f0f0f0' }}>
                    <h2>Your Root:</h2>
                    <p>{rootResult}</p>
                </div>
            )}
        </div>
    );
}

export default App;
