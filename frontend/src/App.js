import React, { useState, useEffect } from "react";
import Select from 'react-select';

import "./App.css";

const currencies = ["USD", "EUR", "PLN"];

const customStyles = {
  control: (provided) => ({
    ...provided,
    minWidth: 100
  }),
};

const CurrencyCalculator = () => {
  const [amount, setAmount] = useState(1);
  const [fromCurrency, setFromCurrency] = useState({ value: "USD", label: "USD" });
  const [toCurrency, setToCurrency] = useState({ value: "EUR", label: "EUR" });
  const [exchangeRate, setExchangeRate] = useState(null);
  const [convertedAmount, setConvertedAmount] = useState(null);
  const [showResult, setShowResult] = useState(false);

  useEffect(() => {
    const fetchExchangeRate = async () => {
      try {
        const response = await fetch(`http://backend-app:5000/rate/${fromCurrency.value}`
          
        );
        const data = await response.json();
        setExchangeRate(data.rates[toCurrency.value]);
        setShowResult(false);
      } catch (error) {
        console.error("Error fetching exchange rate:", error);
      }
    };

    fetchExchangeRate();
  }, [fromCurrency, toCurrency]);

  useEffect(() => {
    if (exchangeRate !== null) {
      setConvertedAmount((amount * exchangeRate).toFixed(2));
    }
  }, [amount, exchangeRate]);

  const handleAmountChange = (e) => {
    const value = e.target.value;
    setAmount(value);
    setShowResult(false);
  };

  const handleFromCurrencyChange = (selectedOption) => {
    setFromCurrency(selectedOption);
  };

  const handleToCurrencyChange = (selectedOption) => {
    setToCurrency(selectedOption);
  };

  const handleCalculate = () => {
    setShowResult(true);
  };

  return (
    <div className="container">
      <h1>Kalkulator walutowy</h1>
      <div className="currency-calculator">
        <div className="input-select-container">
          <div className="input-container">
            <label className="input-label">Kwota:</label>
            <input type="number" value={amount} onChange={handleAmountChange} />
          </div>
          <div className="select-container">
            <label className="select-label">Mam:</label>
            <Select
              value={fromCurrency}
              onChange={handleFromCurrencyChange}
              options={currencies.map(currency => ({ value: currency, label: currency }))}
              styles={customStyles}
            />
          </div>
        </div>
        <div className="equals">=</div>
        <div className={`output-container ${showResult ? 'visible' : ''}`}>
          <label className="output-label">Chcę:</label>
          <div className="output-select-container">
            <div className="output">
              {showResult && <p>{convertedAmount}</p>}
            </div>
            <Select
              value={toCurrency}
              onChange={handleToCurrencyChange}
              options={currencies.map(currency => ({ value: currency, label: currency }))}
              styles={customStyles}
            />
          </div>
        </div>
      </div>
      <button className="btn" onClick={handleCalculate}>Przelicz</button>
    </div>
  );
};

export default CurrencyCalculator;
