import Sidebar from "../../components/sidebar/Sidebar";
import Navbar from "../../components/navbar/Navbar";
import "./home.scss";
import Widget from "../../components/widget/Widget";
import Featured from "../../components/featured/Featured";
import Chart from "../../components/chart/Chart";
import Table from "../../components/table/Table";
import AddBoxIcon from '@mui/icons-material/AddBox';
import { useEffect, useRef } from "react";
import axios from 'axios'
import { useState } from "react";
import {useNavigate} from 'react-router-dom';

const Home = () => {
  const monthArr = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ]
  const navigate = useNavigate();
  const cateref=useRef();
  const amountref=useRef();
  const descref=useRef();
  const dateref=useRef();
  const token=localStorage.getItem('token')
  if(!token) {
    navigate('/login')
  }
  const [mainObj, setMainObj] = useState({});
  const [graphObj, setgrObj] = useState([
    {name : monthArr[0], Total: 12000},
    {name : monthArr[1], Total: 21000},
    {name : monthArr[2], Total: 15000},
    {name : monthArr[3], Total: 17000},
    {name : monthArr[4], Total: 11000},
    {name : monthArr[5], Total: 16000}
  ])

  const GetTot = (obj) => {
    let total = 0
    for(const e of obj) {
      console.log(e)
      total += e['amount']
    }
    return total
  }


  useEffect(() => {
    let newObj = []
    let curr = (new Date()).getMonth()
    for(const i in mainObj['months']) {
      newObj.unshift({name: monthArr[curr], Total: GetTot(mainObj['months'][i])})
      curr -= 1
      curr = curr % 12
    }
    setgrObj(newObj)
  }, [mainObj])

  function Query() {
    return new URLSearchParams(window.location.search);
  }

  const format = (date) => {
    return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`
  }

  useEffect(() => {
    const currDate = new Date()
    const formattedDate = format(currDate)
    let category = Query().get('category');
    if(!category) {
      category = "all"
    } else if(category !== "all") {
      category = [category]
    }
    const headers = {
      'token': token,
    }

    const data = {
      'date': formattedDate,
      category
    }

    console.log(data)

    console.log(headers)

    axios.post('/expenses', data, {headers}).then(res => {
      setMainObj(res.data)
    }).catch(err => {
      console.log(err)
    })
  }, [])

  const handleClick = () => {
    const category = cateref.current.value
    const amount = amountref.current.value
    const date = dateref.current.value
    const description = descref.current.value
    const reset = () => {
      cateref.current.value = "Housing"
      amountref.current.value = 0
      dateref.current.value = ""
      descref.current.value = ""
    }
    const data = {
      category,
      amount,
      date,
      description
    }
    const headers = {
      'token': token
    }
    console.log(data)
    axios.post('/expense', data,{headers}).then(res => {
      if(res.status == 200) {
        console.log(res.data)
        reset()

      }
    }).catch(err => {
      console.log(err)
    })
  };
  return (
    <div className="home">
      <Sidebar />
      <div className="homeContainer">
        <Navbar />
        <div className="widgets">
          <div className="addexpense">
            <div className="title">
            <h1>Add Expenses</h1>
            <AddBoxIcon className="icon" onclick={handleClick}/>
            </div>
            <div className="inputdetails">
              <div className="first">
              <label htmlFor="category">Category</label>
              <select name="category" id="category" ref={cateref}>
                <option value="Housing">Housing</option>
                <option value="Transportation">Transportation</option>
                <option value="Food">Food</option>
                <option value="Utilities">Utilities</option>
                <option value="Insurance">Insurance</option>
                <option value="Healthcare">Healthcare</option>
                <option value="Repayments">Repayments</option>
                <option value="Personal">Personal</option>
                <option value="Recreation">Recreation</option>
                <option value="Miscellaneous">Miscellaneous</option>
            </select>
              <input   type="number" id="amount"  ref={amountref}/>
              <label htmlFor="amount">Amount</label>
              </div>
              <div className="second">
              <input   type="date" id="Date" ref={dateref}/>
              <label htmlFor="Date">Date</label>
              <input   type="text" id="desc" ref={descref}/>
              <label htmlFor="desc">Description</label>
              </div>
              <button className="button" onClick={handleClick}>Submit</button>
            </div>
          </div>
          <Widget type="balance" amount={2000} diff={30}/>
        </div>
        <div className="charts">
          <Featured />
          <Chart title="Last 6 Months (Expenses)" aspect={2 / 1} data={graphObj} />
        </div>
        <div className="listContainer">
          <div className="listTitle">Latest Transactions</div>
          <Table />
        </div>
      </div>
    </div>
  );
};

export default Home;
