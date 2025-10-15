export async function login(email, password ) {
  const response = await fetch('http://localhost:8000/api/v1/auth/signin', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({email, password}),
  });
  if (!response.ok) throw new Error('Login failed');
  const data = await response.json();
  localStorage.setItem('accessToken', data.access_token); // Save access token
  localStorage.setItem('refreshToken', data.refresh_token); // Save access token
}

export async function getRequest(endpoint){
    const accessToken = localStorage.getItem('accessToken');
    
    const defaultOptions = {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            }
        };
    
    const response = await fetch(`http://localhost:8000/api/v1/challenges/${endpoint}`, {
            ...defaultOptions
        })

    const data = await response.json().catch(() => null)
    if (!response.ok) {
        throw new Error(data?.detail || data?.message || 'Request failed')
    }

    return data
}

export async function postRequest(endpoint, difficulty){
    const accessToken = localStorage.getItem('accessToken');
    
    const defaultOptions = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
            body: JSON.stringify({difficulty})
        };
    
    const response = await fetch(`http://localhost:8000/api/v1/challenges/${endpoint}`, {
            ...defaultOptions
        })

    const data = await response.json().catch(() => null)
    if (!response.ok) {
        throw new Error(data?.detail || data?.message || 'Request failed')
    }

    return data
}