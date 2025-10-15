import "./SignupPage.css";
import {useState} from 'react'
import { useNavigate } from 'react-router'

export function SignupPage() {
  const [form, setForm] = useState({
    email: "",
    user_name: "",
    password: "",
    first_name: "",
    last_name: "",
    middle_name: "",
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  const navigate = useNavigate()

  const onChange = (e) => {
    const {name, value} = e.target
    setForm(prev => ({...prev, [name]: value}))
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setSuccess(null)

    // basic client-side validation
    if (!form.email || !form.user_name || !form.password || !form.first_name || !form.last_name) {
      setError('Please fill in all required fields')
      return
    }

    setLoading(true)
    try {
      const payload = {
        email: form.email,
        user_name: form.user_name,
        password: form.password,
        first_name: form.first_name,
        last_name: form.last_name,
        middle_name: form.middle_name || null,
      }

      const res = await fetch('http://localhost:8000/api/v1/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      const data = await res.json().catch(() => null)

      if (!res.ok) {
        const msg = data?.detail || data?.message || 'Signup failed'
        throw new Error(msg)
      }

      setSuccess(data?.message || 'Account created — check your email to verify')
      // Optionally redirect to login after short delay
      setTimeout(() => navigate('/login'), 1200)
    } catch (err) {
      setError(err.message || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="main-container">
        <h3>Sign up to Codebasetwo</h3>
        <p>Create an account to prepare for your technical interview</p>

        <form onSubmit={onSubmit} className="signup-form">
          <input type="email" placeholder="Email" id="emailInput" name="email" value={form.email} onChange={onChange} />
          <input
            type="text"
            placeholder="Username"
            id="userNameInput"
            name="user_name"
            value={form.user_name}
            onChange={onChange}
          />
          <input
            type='password'
            placeholder="Password"
            id="PasswordInput"
            name="password"
            value={form.password}
            onChange={onChange}
          />
          <input
            type="text"
            placeholder="First name"
            id="firstNameInput"
            name="first_name"
            value={form.first_name}
            onChange={onChange}
          />
          <input
            type="text"
            placeholder="Last name"
            id="lastnameInput"
            name="last_name"
            value={form.last_name}
            onChange={onChange}
          />
          <input
            type="text"
            placeholder="Optional middle name"
            id="middlenameInput"
            name="middle_name"
            value={form.middle_name}
            onChange={onChange}
          />

          <button className="signup-button" type="submit" disabled={loading}>
            {loading ? 'Signing up...' : 'Sign up'}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}

        <div className="signin-footer">
          <p>
            {" "}
            Already have an account?{" "}
            <a href="/login">
              <strong>Sign in</strong>
            </a>{" "}
          </p>
          <p className="signin-company">&copy;&nbsp;Secured by Codebasetwo</p>
          <p className="signin-dev-mode"> Development mode </p>
        </div>
      </div>
    </>
  )
}
