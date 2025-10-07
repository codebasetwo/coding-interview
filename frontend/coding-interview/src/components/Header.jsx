import './Header.css'
import ProfileImage from '../assets/female.png'
import { useState } from 'react'
import { Profile } from './Profile'

export function Header() {
  const [showDropdown, setShowDropdown] = useState(false)

  const toggleDropDown = () => {
    setShowDropdown((prev) => !prev)
  }
  return (
    <div className="header-container">
      <h1 className='h2'>Code Challenge Generator</h1>
      <nav>
        <a href="">Generate Challenge</a>
        <a href="">History</a>
        <div className='profile-section'>
          <img 
            src={ProfileImage} 
            alt="profile-image" 
            className='profile-image'
            onClick={toggleDropDown}
            />
            { showDropdown && (
              <Profile />
            )}
         
        </div>
        
      </nav>
    </div>
  )
}