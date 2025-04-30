const inventory = {
    A1: { name: "Chips", price: 1.5, stock: 5 },
    B2: { name: "Soda", price: 2.0, stock: 3 },
    C3: { name: "Candy", price: 1.0, stock: 10 }
  };
  
  let transactionHistory = [];
  
  function displayItems() {
    const container = document.getElementById("items-container");
    container.innerHTML = "";
    for (const code in inventory) {
      const item = inventory[code];
      container.innerHTML += `
        <div class="item">
          <strong>${item.name}</strong><br />
          Code: ${code}<br />
          Price: $${item.price}<br />
          Stock: ${item.stock}
        </div>
      `;
    }
  }
  
  function processTransaction() {
    const code = document.getElementById("selection").value.toUpperCase();
    const payment = parseFloat(document.getElementById("payment").value);
    const message = document.getElementById("message");
  
    if (!inventory[code]) {
      message.textContent = "Invalid code. Please try again.";
      return;
    }
  
    const item = inventory[code];
    if (item.stock === 0) {
      message.textContent = `${item.name} is out of stock.`;
      return;
    }
  
    if (payment < item.price) {
      message.textContent = `Insufficient payment. ${item.name} costs $${item.price}.`;
      return;
    }
  
    item.stock -= 1;
    const change = (payment - item.price).toFixed(2);
    message.textContent = `Dispensing ${item.name}. Your change is $${change}.`;
  
    const transaction = {
      item: item.name,
      code: code,
      payment: payment,
      change: change,
      timestamp: new Date().toLocaleString()
    };
    transactionHistory.push(transaction);
    updateTransactionHistory();
  
    displayItems(); // Update UI
  }
  
  function updateTransactionHistory() {
    const historyList = document.getElementById("history-list");
    historyList.innerHTML = "";
    transactionHistory.forEach(tx => {
      const li = document.createElement("li");
      li.textContent = `${tx.timestamp}: ${tx.item} (Code: ${tx.code}) - Paid: $${tx.payment}, Change: $${tx.change}`;
      historyList.appendChild(li);
    });
  }
  
  function restockItem() {
    const code = document.getElementById("restock-code").value.toUpperCase();
    const amount = parseInt(document.getElementById("restock-amount").value);
    const message = document.getElementById("message");
  
    if (!inventory[code]) {
      message.textContent = "Invalid code. Cannot restock.";
      return;
    }
  
    if (isNaN(amount) || amount <= 0) {
      message.textContent = "Enter a valid restock amount.";
      return;
    }
  
    inventory[code].stock += amount;
    message.textContent = `${inventory[code].name} restocked by ${amount}.`;
  
    displayItems();
  }
  
  const credentials = { username: "admin", password: "1234" };

  function login() {
    const user = document.getElementById("username").value;
    const pass = document.getElementById("password").value;
    if (user === credentials.username && pass === credentials.password) {
      document.getElementById("auth-section").style.display = "none";
      document.getElementById("vending-machine").style.display = "block";
      displayItems();
    } else {
      alert("Invalid credentials. Try 'admin' and '1234'.");
    }
  }
  
  
  window.onload = () => {
    // Initially hide vending machine interface
    document.getElementById("vending-machine").style.display = "none";
  };
  