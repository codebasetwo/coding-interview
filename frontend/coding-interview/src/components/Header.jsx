import "./Header.css";
import { Link } from "react-router";
import ProfileImage from "../assets/female.png";

export function Header() {
  return (
    <div className="app-layout">
      <div className="app-header">
        <div className="header-content">
        <h1>Code Challenge Generator</h1>

        <nav>
          <Link to="/">Generate Challenge</Link>
          <Link to="/history">History</Link>
          <img
            className="profile-image"
            src={ProfileImage}
            alt="profile-image"
          />
        </nav>
        </div>
      </div>
    </div>
  );
}
