import "./sidebar.scss";
import DashboardIcon from "@mui/icons-material/Dashboard";
import HouseIcon from '@mui/icons-material/House';
import FastfoodIcon from '@mui/icons-material/Fastfood';
import InsertChartIcon from "@mui/icons-material/InsertChart";
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar';
import PersonPinIcon from '@mui/icons-material/PersonPin';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import KitesurfingIcon from '@mui/icons-material/Kitesurfing';
import AccountCircleOutlinedIcon from "@mui/icons-material/AccountCircleOutlined";
import { Link } from "react-router-dom";
import { DarkModeContext } from "../../context/darkModeContext";
import { useContext } from "react";

const Sidebar = () => {
  const { dispatch } = useContext(DarkModeContext);

  const handleNavigate = (ev) => {
    let ele = ev.target
    while(ele.tagName !== "DIV") {
      ele = ele.parentNode
    }
    let path = ele.getAttribute('to')
    window.location.href = `http://localhost:3000${path}`
  }
  
  return (
    <div className="sidebar">
      <div className="top">
        <Link to="/" style={{ textDecoration: "none" }}>
          <span className="logo">Expense Tracker</span>
        </Link>
      </div>
      <hr />
      <div className="center">
        <ul>
          <p className="title">MAIN</p>
          <div onClick={handleNavigate} to="/?category=all">
            <li>
              <DashboardIcon className="icon" />
              <span>Dashboard</span>
            </li>
          </div>
          <p className="title">LISTS</p>
          <div onClick={handleNavigate} to="/?category=Food" style={{ textDecoration: "none" }}>
            <li>
              <FastfoodIcon className="icon" />
              <span>Food</span>
            </li>
          </div>
          <div onClick={handleNavigate} to="/?category=Housing" style={{ textDecoration: "none" }}>
            <li>
              <HouseIcon className="icon" />
              <span>Housing</span>
            </li>
          </div>
          <div onClick={handleNavigate} to="/?category=Transportation" style={{ textDecoration: "none" }}>
            <li>
              <DirectionsCarIcon className="icon" />
              <span>Transportation</span>
            </li>
          </div>
          <div onClick={handleNavigate} to="/?category=Personal" style={{ textDecoration: "none" }}>
            <li>
              <PersonPinIcon className="icon" />
              <span>Personal Spending</span>
            </li>
          </div>
          <div onClick={handleNavigate} to="/?category=Utilities" style={{ textDecoration: "none" }}>
            <li>
              <AddShoppingCartIcon className="icon" />
              <span>Utilities</span>
            </li>
          </div>
          <div onClick={handleNavigate} to="/?category=Debt" style={{ textDecoration: "none" }}>
            <li>
              <AccountBalanceIcon className="icon" />
              <span>Debt Payments </span>
            </li>
          </div>
          <div onClick={handleNavigate} to="/?category=Healthcare" style={{ textDecoration: "none" }}>
            <li>
              <MonitorHeartIcon className="icon" />
              <span> Medical & Healthcare </span>
            </li>
          </div>
          <div onClick={handleNavigate} to="/?category=Recreation" style={{ textDecoration: "none" }}>
            <li>
              <KitesurfingIcon  className="icon" />
              <span>Recreation & Entertainment</span>
            </li>
          </div>
          
          <p className="title">USEFUL</p>
          <li>
            <InsertChartIcon className="icon" />
            <span>Stats</span>
          </li>
          <li>
            <NotificationsNoneIcon className="icon" />
            <span>Notifications</span>
          </li>
          
          <p className="title">USER</p>
          <li>
            <AccountCircleOutlinedIcon className="icon" />
            <span>Profile</span>
          </li>
          <li>
            <ExitToAppIcon className="icon" />
            <span>Logout</span>
          </li>
        </ul>
      </div>
      <div className="bottom">
        <div
          className="colorOption"
          onClick={() => dispatch({ type: "LIGHT" })}
        ></div>
        <div
          className="colorOption"
          onClick={() => dispatch({ type: "DARK" })}
        ></div>
      </div>
    </div>
  );
};

export default Sidebar;
