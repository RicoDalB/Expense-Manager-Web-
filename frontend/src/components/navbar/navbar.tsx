import {Link, useLocation} from "react-router-dom";
import styles from "./navbar.module.css";
import logoBank from "../../assets/icons/bank-svgrepo-com.svg";
import iconDashboard from "../../assets/icons/graph-svgrepo-com.svg";
import iconStats from "../../assets/icons/graph-up-svgrepo-com.svg";
import iconExpenses from "../../assets/icons/dollar-svgrepo-com.svg";
import iconCategories from "../../assets/icons/grid-squares-svgrepo-com.svg";
import iconSettings from "../../assets/icons/settings-future-svgrepo-com.svg";
import iconLogout from "../../assets/icons/logout-svgrepo-com.svg";

const Navbar = () => {
    const location = useLocation(); //permette di ottenere url attuale 

    return(
        <nav className={styles.navbar}>
            {/*LOGO*/}
            <div className={styles.logoContainer}>
                <img src={logoBank} alt="Logo" className={styles.logo} />
                <span className={styles.logoText}>Expense Manager</span>
            </div>
            {/*MENU NAVIGAZIONE*/}
            <ul className={styles.navLinks}>
                <li className={location.pathname === "/" ? styles.activate : ""}>
                 <Link to="/">
                    <img src={iconDashboard} alt="Dashboard" className={styles.icon} />
                    Dashboard
                 </Link>
                </li>
                <li className={location.pathname === "/stats" ? styles.activate : ""}>
                 <Link to="/statistics">
                 <img src={iconStats} alt="Statistiche" className={styles.icon} />
                 Statistiche
                 </Link>
                </li>
                <li className={location.pathname === "/expenses" ? styles.activate : ""}>
                 <Link to="/expenses">
                 <img src={iconExpenses} alt="Spese" className={styles.icon} />
                 Spese
                 </Link>
                </li>
                <li className={location.pathname === "/categories" ? styles.activate : ""}>
                 <Link to="/categories">
                 <img src={iconCategories} alt="Categorie" className={styles.icon} />
                 Categorie
                 </Link>
                </li>
                <li className={location.pathname === "/settings" ? styles.activate : ""}>
                 <Link to="/settings">
                 <img src={iconSettings} alt="Impostazioni" className={styles.icon} />
                 Impostazioni
                 </Link>
                </li>           
            </ul>
            {/*sezione Logout*/}
            <div className={styles.logout}>
              <Link to="/logout">
              <img src={iconLogout} alt="Logout" className={styles.icon} />
              Log out
              </Link>

            </div>
        </nav>
    );
};
export default Navbar;







