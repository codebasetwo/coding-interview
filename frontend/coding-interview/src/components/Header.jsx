import './Header.css'
import ProfileImage from '../assets/female.png'
export function Header() {
  return (
    <div className="header-container">
      <h1 className='h2'>Code Challenge Generator</h1>
      <nav>
        <a href="">Generate Challenge</a>
        <a href="">History</a>
        <img src={ProfileImage} alt="profile-image" className='profile-image' />
      </nav>
    </div>
  )
}