import "./widget.scss";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import AccountBalanceWalletOutlinedIcon from "@mui/icons-material/AccountBalanceWalletOutlined";
import ShoppingCartOutlinedIcon from "@mui/icons-material/ShoppingCartOutlined";
import MonetizationOnOutlinedIcon from "@mui/icons-material/MonetizationOnOutlined";
import { useEffect } from "react";
import { useRef } from "react";
import { useState } from "react";
import axios from "axios";

const Widget = ({ type, amount, diff }) => {
  let data;
  let [addView, setView] = useState(true);
  const [balobj, setObj] = useState({});
  const salref = useRef();
  const dateref = useRef();
  const token = localStorage.getItem('token')

  const reset = () => {
    salref.current.value = 0
    dateref.current.value = ""
  }

  useEffect(() => {
    const headers = {
      token
    }
    axios.get('/balance', {headers}).then(res => {
      if(res.status == 200) {
        setObj(res.data)
      }
    }).catch(err => {
      console.log(err)
    })
  }, [])

  useEffect(() => {
    setTimeout(() => {
      const headers = {
        token
      }
      axios.get('/balance', {headers}).then(res => {
        if(res.status == 200) {
          setObj(res.data)
        }
      }).catch(err => {
        console.log(err)
      })
    }, 3000)
  }, [balobj])

  // const [amount,setamount]=useState(0)
  // useEffect(()=>{
  //     const getAmount=async()=>{
  //         let isActive = true;
  //     await axios.get("http://localhost:5000/user/allusers")
  //     .then(response=>{if(isActive)setamount(response.data)})
  //     .catch(err=>console.error(err))

  //         }
  // getAmount()
  // },[])

  const handleClick = () => {
    setView(!addView)
  }

  const onSubmit = () => {
    const amount = salref.current.value;
    const date = dateref.current.value;
    const data = {
      amount,
      date
    }
    const headers = {
      token
    }
    console.log(data)
    axios.post('/salary', data, {headers}).then(res => {
      if(res.status == 200) {
        console.log(res.data)
        reset()
      }
    }).catch(err => {
      console.log(err)
    })
  }

  
  //temporary

  // useEffect(() => {

  // }, [])

  switch (type) {
   
    case "balance":
      data = {
        title: "Wallet",
        isMoney: true,
        link: "update salary",
        icon: (
          <AccountBalanceWalletOutlinedIcon
            className="icon"
            style={{
              backgroundColor: "rgba(128, 0, 128, 0.2)",
              color: "purple",
            }}
          />
        ),
      };
      break;
    default:
      break;
  }

  return (
    addView ? 
    (<div className="widget">
      <div className="left">
        <span className="title">{data.title}</span>
        <span className="counter">
          {data.isMoney } {balobj.balance}
        </span>
        <span className="link" onClick={handleClick}>{data.link}</span>
      </div>
      <div className="right">
        <div className="percentage positive">
          <KeyboardArrowUpIcon />
          {diff} %
        </div>
        {data.icon}
      </div>
    </div>) :
    (
      <div className="widget">
        <div className="left-add">
          <label htmlFor="salary">Salary:</label>
          <input name="salary" id="salary" ref={salref} type="number"/>
          <label htmlFor="updatedate">UpdateDate:</label>
          <input type="date" name="updatedate" id="updatedate" ref={dateref}/>
        </div>
        <div className="right-add">
          <button className="button" onClick={onSubmit}>Submit</button>
          <span className="link" onClick={handleClick}>show salary</span>
        </div>
      </div>
    )
  );
};

export default Widget;
