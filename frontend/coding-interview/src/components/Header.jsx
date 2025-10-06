import "./Header.css";
import { useState, useEffect, useRef } from "react";
import { Link } from "react-router";
import ProfileImage from "../assets/female.png";

export function Header() {
  const [showDropDown, setShowDropdown] = useState("");
  const dropdownRef = useRef(null);


  const toggleDropDown = () => {
    setShowDropdown((prev) => !prev);
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
      // <div className="app-header">
        <div className="header-content">
          <h1>Code Challenge Generator</h1>

          <nav>
            <Link to="/">Generate Challenge</Link>
            <Link to="/history">History</Link>
            <div className="profile-section" ref={dropdownRef}>
              <img
                className="profile-image"
                src={ProfileImage}
                alt="profile-image"
                onClick={toggleDropDown}
              />
              {showDropDown && (
                <div className="dropdown-menu">
                  <Link to="/login">Login</Link>
                  <Link to="/signup">Signup</Link>
                  <Link to="/profile">Profile</Link>
                  <Link to="/signout">Signout</Link>
                </div>
              )}
            </div>
          </nav>
        </div>
      // </div>
  );
}
