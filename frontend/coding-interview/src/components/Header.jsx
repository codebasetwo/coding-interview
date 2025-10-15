import './Header.css'
import ProfileImage from '../assets/female.png'
import { useState, useRef, useEffect } from 'react'
import { Link } from 'react-router'
import { Profile } from './Profile'

export function Header() {
  const [showDropdown, setShowDropdown] = useState(false)
  const dropdownRef = useRef(null);

  const toggleDropDown = () => {
    setShowDropdown((prev) => !prev)
  };
  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target)
      ) {
        setShowDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);
  return (
    <div className="header-container">
      <h1 className='h2'>Code Challenge Generator</h1>
      <nav>
        <a href="">Generate Challenge</a>
        <Link to="/history">History</Link>
        <div className='profile-section' ref={dropdownRef}>
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