import './LoginPage.css'
import {useState} from 'react'
import { login } from '../../utils/apiRequests'
import { useNavigate } from 'react-router'

export function LoginPage() {
    const [password, setPassword] = useState('')
    const [email, setEmail] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const navigate = useNavigate()

    const onSubmit = async (e) => {
        e.preventDefault()
        setError(null)
        if (!email || !password) return setError('Please provide username and password')

        setLoading(true)
        try {
            await login(email, password)
            // redirect to home or dashboard after successful login
            navigate('/')
        } catch (err) {
            setError(err.message || 'Login failed')
        } finally {
            setLoading(false)
        }
    }

    return (
        <>
			<div className='main-container'>
					<h3>Sign in to Codebastwo</h3>
					<p>Welcome back please sign in to continue</p>
					<form onSubmit={onSubmit} className="login-form">
						<label className='signin-label' htmlFor="usernameInput">Username</label>
						<input type="text" placeholder='Email' id='usernameInput' name='username' value={email} onChange={e => setEmail(e.target.value)} />
						<label className='signin-label' htmlFor="passwordInput">Password</label>
						<input type="password" placeholder='password' id='passwordInput' name='password' value={password} onChange={e => setPassword(e.target.value)} />
						<button className='login-button' type='submit' disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
					</form>
					{error && <p className='error'>{error}</p>}
					<div className='signout-footer'>
						<p> Don't have an account? <a href='/signup'><strong>Sign up</strong></a> </p>
						<p className="signout-company">&copy;&nbsp;Secured by Codebasetwo</p>
						<p className="signout-dev-mode"> Development mode </p>
					</div>

			</div>
        </>
    )
}