export async function getRootExplanation(fruit) {
    const response = await fetch(import.meta.env.VITE_BACKEND_URL + '/api/fruit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fruit }),
    });
    return await response.json();
}
