# Author
 Name of the Student: Rana Das 
 Student Mail:rd16715r@gmail.com
 Student Code:bitsom_ba_25071104
 Sales_Analysis_Report
## Project Overview
The **Sales Analytics System** is a Python-based data processing and reporting application that reads raw sales data, validates and filters transactions, performs analytical computations, enriches product data using an external API, and generates a comprehensive text-based sales report.

The project is structured in a modular way to separate concerns such as file handling, data processing, API interaction, and orchestration.

---

## Repository Structure
├── README.md
├── main.py
├── utils/
│ ├── file_handler.py
│ ├── data_processor.py
│ └── api_handler.py
├── data/
│ └── sales_data.txt
├── output/
| └── report.txt
└── requirements.txt

---

## File Responsibilities

### `main.py`
- Entry point of the application
- Controls the complete execution flow:
  - Reads sales data
  - Parses and validates transactions
  - Applies optional filters
  - Performs analytics
  - Fetches and applies API enrichment
  - Saves enriched data
  - Generates final sales report

---

### `utils/file_handler.py`
Handles all file-related operations:
- Reading sales data with encoding handling
- Parsing raw transaction records
- Validation and filtering logic

---

### `utils/data_processor.py`
Performs analytical computations:
- Total revenue calculation
- Region-wise sales analysis
- Top-selling products
- Customer analysis
- Daily sales trends
- Peak sales day detection
- Low-performing product identification

---

### `utils/api_handler.py`
- Fetches product-related data from an external API
- Enriches transaction data using API responses
- Handles API failures gracefully

---

### `data/sales_data.txt`
- Input sales dataset (pipe `|` delimited)
- Provided as part of the assignment
- Must not be modified

---

### `output/`
- Stores generated outputs:
  - Enriched sales data file
  - Final sales analytics report

---

### `requirements.txt`
- Lists external Python dependencies required to run the project

---

## Setup Instructions

### 1. Ensure Python Is Installed
- Python version **3.10 or higher** is recommended
- Verify installation:
  ```bash
  python --13.14.2

 ### 2. Install Dependencies
Navigate to the project root directory and run:

- pip install -r requirements.txt pip install -r requirements.txt

### How to Run the Project
From the project root directory, execute:
- python main.py

### Program Execution Flow

## 1 When executed, the program performs the following steps:
## 2 Displays a welcome message
## 3 Reads sales data from data/sales_data.txt
## 4 Parses and cleans transactions
## 5 Displays available filter options (region and amount range)
## 6 Applies user-selected filters (optional)
## 7 Validates transactions and reports invalid records
## 8 Performs all analytical computations
## 9 Fetches product data from API
## 10 Enriches sales data using API results
## 11 Saves enriched data to the output/ directory
## 12 Generates a formatted text sales report
## 13 Displays completion status and file locations
