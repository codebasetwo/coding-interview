import './Header.css'
import ProfileImage from '../assets/female.png'

export function Header(){

    return(
    <div className='root'>
        <h1>Coding challenge Generator</h1>
        <nav className='nav-links'>
            <a>Generate Challenge</a>
            <a>History</a>
            <img 
            className="profile-image" src={ProfileImage} alt="profile-image"/>
        </nav>
      </div>
    )
}