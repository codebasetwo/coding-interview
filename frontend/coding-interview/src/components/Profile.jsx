import SettingsImage from "../assets/settings.png";
import LogoutImage from "../assets/logout.png";
import ProfileImage from "../assets/female.png";
import "./Profile.css";

export function Profile() {
  return (
    <div className="container">
      <div className="container2">
        <div>
          <img
            src={ProfileImage}
            alt="profile-image"
            className="profile-image"
          />
          <h4>Nnaemeka Nwankwo</h4>
        </div>
        <div>
          <img
            src={SettingsImage}
            alt="settings"
            className="profile-image-icon"
          />
          <p>Manage acount</p>
        </div>
        <div>
          <img src={LogoutImage} alt="logout" className="profile-image-icon" />
          <p>Sign out</p>
        </div>
      </div>
      <div className="footer">
        <p className="footer-company">&copy;&nbsp;Secured by Codebasetwo</p>
        <p className="footer-dev-mode"> Development mode </p>
      </div>
    </div>
  );
}
