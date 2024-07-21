import { useState } from "react";
import { FaEdit } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import "./transaction.css";

function Transaction() {
  const getCurrentDateTime = () => {
    const now = new Date();
    return now.toISOString().slice(0, 16); // Format the date and time as "YYYY-MM-DDTHH:MM"
  };

  const [transaction, setTransaction] = useState({
    name: "",
    date: getCurrentDateTime(),
    amount: 0,
    description: "",
  });
  const [balance, setBalance] = useState(0);
  const [transactions, setTransactions] = useState([]);
  const [transactionOptions, setTransactionOptions] = useState(false);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setTransaction((prevTransaction) => ({
      ...prevTransaction,
      [name]: value,
    }));
    console.log(transaction);
  };

  // Handle form submission
  const addTransaction = (e) => {
    e.preventDefault();
    setTransactions((prevTransactions) => [...prevTransactions, transaction]);
    // Clear the form
    setTransaction({
      name: "",
      date: "",
      amount: 0,
      description: "",
    });
  };

  const editTransaction = () => {};
  const deleteTransaction = () => {};

  return (
    <main className="transaction-main">
      <h1 className="balance">
        <span>Balance </span>${balance}
      </h1>
      <form onSubmit={addTransaction}>
        <div className="name-date">
          <input
            type="text"
            name="name"
            value={transaction.name}
            onChange={handleInputChange}
            placeholder="Samsung TV"
            required
          />
          <input
            type="datetime-local"
            name="date"
            value={transaction.date}
            onChange={handleInputChange}
            required
          />
        </div>
        <input
          type="number"
          name="amount"
          value={transaction.amount}
          onChange={handleInputChange}
          placeholder="Amount"
          required
        />
        <input
          type="text"
          name="description"
          value={transaction.description}
          onChange={handleInputChange}
          placeholder="Description"
        />
        <button type="submit">Submit</button>
      </form>

      <div className="transactions">
        <h2>Transactions</h2>
        {transactions.map((trans, index) => (
          <div
            key={index}
            className="transaction"
            onMouseEnter={() => {
              setTransactionOptions(true);
            }}
            onMouseLeave={() => {
              setTransactionOptions(false);
            }}
          >
            <div className="left">
              <p className="name">{trans.name}</p>
              <small className="description">{trans.description}</small>
            </div>
            <div className="right">
              <div className="right-text">
                <p className={`amount ${trans.amount < 0 ? "red" : "green"}`}>
                  {trans.amount < 0 ? "-" : "+"}${Math.abs(trans.amount)}
                </p>
                <small className="date">
                  {new Date(trans.date).toLocaleDateString()}
                </small>
              </div>
              {transactionOptions && (
                <div className="transaction-options">
                  <button onClick={editTransaction} id="edit-btn">
                    <FaEdit />
                  </button>
                  <button onClick={deleteTransaction}>
                    <MdDelete />
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}

export default Transaction;
