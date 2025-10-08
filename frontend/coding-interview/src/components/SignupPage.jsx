import './SignupPage.css'

export function SignupPage() {
    return (
        <>
					<div className='main-container'>
					<h3>Sign up  to Codebasetwo</h3>
					<p>Create an account to prepare for your technical interview</p>
					
					<input type="email" placeholder='Email' id='emailInput' name='email' />
					
					<input type="text" placeholder='Username' id='userNameInput' name='username' />
					
					<input type="password" placeholder='Password' id='passwordInput' name='password' />
					
					<input type="text" placeholder='First name' id='firstNameInput' name='firstname' />
					
					<input type="text" placeholder='Last name' id='lastnameInput' name='lastname' />
	
					<input type="text" placeholder='Optional middle name' id='middlenameInput' name='middlename' />
					<button className='signup-button'>Sign up</button>
					<div className='signin-footer'>
						<p> Already have an account? <a href='/login'><strong>Sign in</strong></a> </p>
						<p className="signin-company">&copy;&nbsp;Secured by Codebasetwo</p>
						<p className="signin-dev-mode"> Development mode </p>
					</div>

			</div>

        </>
    )
}