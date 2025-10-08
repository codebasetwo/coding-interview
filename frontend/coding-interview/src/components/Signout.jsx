import './Signout.css'

export function SignoutPage() {

    return (
        <>
					<div className='main-container'>
							<h3>Sign in to Codebastwo</h3>
							<p>Welcome back please sign in to continue</p>
							<label className='signin-label' htmlFor="">Username</label>
							<input type="text" placeholder='Username or Email' id='usernameInput' name='username' />
							<label className='signin-label' htmlFor="emailInput">Password</label>
							<input type="email" placeholder='password' id='emailInput' name='password' />
							<button className='login-button'>Sign in</button>
							<div className='signout-footer'>
								<p className="signout-company">&copy;&nbsp;Secured by Codebasetwo</p>
        				<p className="signout-dev-mode"> Development mode </p>
							</div>

					</div>
        </>
    )
}