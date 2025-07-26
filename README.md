# Amazon Automation Project (Selenium + Python + Pytest)

## 📌 Overview
This project is part of my **45-Day Selenium with Python learning plan**. It automates a real-world Amazon workflow using the **Page Object Model (POM)** design pattern and integrates with **pytest** for structured testing.

---

## ✅ Features Implemented
- Launch Amazon and perform product search.
- Apply brand filters dynamically.
- Skip sponsored items and select valid products.
- Handle multiple windows/tabs.
- Extract all search results with price and save to CSV.
- Logging integrated for debugging and traceability.
- Structured using Page Object Model (POM) for scalability.

---

## 🛠️ Tech Stack
- **Language:** Python 3.x  
- **Automation Tool:** Selenium WebDriver  
- **Testing Framework:** pytest  
- **Others:** CSV handling, Logging, GitHub for version control

---

## 🚀 Next Steps
- Add "Add to Cart" flow.
- Implement detailed test reporting (Allure/HTML).
- Integrate GitHub Actions (CI/CD).

---

## 📂 Project Structure

AmazonProject/
├── pages/
│ ├── search_page.py
│ ├── search_results_page.py
│ └── product_page.py
├── tests/
│ └── test_amazon_flow.py
├── amazon_results.csv
├── pytest.ini
├── README.md
└── LICENSE