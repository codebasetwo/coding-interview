import { useState } from 'react';
import './LoginPage.css'


export function LoginPage() {
    const [userName, setUserName] = useState('');
    const [password, setPassword] = useState('');


    return (
        <div className='login-container'>
            <h2>
                Login
            </h2>
            <form>
                <input 
                type="text" 
                placeholder='username' 
                onChange={(e) => setUserName(e.target.value)}
                value={userName} 
                required/>
                <input 
                type="password" 
                placeholder='password'
                onChange={(e) => setPassword(e.target.value)}
                value={password} 
                required/>
                <button className='login-button'> Login </button>
            </form>    
        </div>
    )

}