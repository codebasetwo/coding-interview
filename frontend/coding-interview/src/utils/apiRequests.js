function getToken() {
    return localStorage.getItem('token')
}

export const callApi = () => {
    const makeRequest = async (endpoint, options = {}) => {
        const token = getToken()
        const defaultOptions = {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }

        const response = await fetch(`http://localhost:8000/api/${endpoint}`, {
            ...defaultOptions,
            ...options,
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => null)
            if (response.status === 429) {
                throw new Error("Daily quota exceeded")
            }
            throw new Error(errorData?.detail || "An error occurred")
        }

        return response.json()
    }

    return {makeRequest}
}


// Example login function
export async function login(email, password, ) {
  const response = await fetch('http://localhost:8000/api/v1/auth/signin', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({email, password}),
  });
  if (!response.ok) throw new Error('Login failed');
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token); // Save access token
  localStorage.setItem('refresh_token', data.refresh_token); // Save access token
}