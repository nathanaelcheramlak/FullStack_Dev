import { useState } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [amount, setAmount] = useState(0);
  const [description, setDescription]= useState("");

  const addTransaction = () => {

  }

  return (
    <main>
      <h1 className="balance"><span>Balance </span>$200</h1>
      <form onSubmit={addTransaction}>
        <div className="name-date">
          <input type="text" value={name} onChange={(e)=>{setName(e.target.value)}} placeholder='Samsung TV'/>
          <input type="datetime-local" value={date} onChange={(e)=>{setDate(e.target.value)}}/>
        </div>
        <input type="number" value={amount} onChange={(e)=>{setAmount(e.target.value)}} placeholder='Amount'/>
        <input type="text" value={description} onChange={(e)=>{setDescription(e.target.value)}} placeholder='Description'/>
        <button type="submit">Submit</button>
      </form>

      <div className="transactions">
        <h2>Transactions</h2>
        <div className='transaction'>
          <div className="left">
            <p className="name">Samsung TV</p>
            <small className="description">I needed a brand new TV for my house.</small>
          </div>
          <div className="right">
            <p className="amount red">-$250</p>
            <small className="date">22-12-2022</small>
          </div>
        </div>

        <div className='transaction'>
          <div className="left">
            <p className="name">Samsung Galaxy S24 Ultra</p>
            <small className="description">I needed a brand new Smart Phone for myself.</small>
          </div>
          <div className="right">
            <p className="amount green">+$750</p>
            <small className="date">22-12-2024</small>
          </div>
        </div>
      </div>
    </main>
  )
}

export default App
