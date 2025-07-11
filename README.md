# 🐟 Seafood Project – Cloud-Based ETL Pipeline

This project automates the process of extracting seafood data from a Google Spreadsheet, transforming it, and loading it to a remote server. The pipeline is built using Python and deployed both locally and on **Google Cloud Functions**, scheduled to run using **Cloud Scheduler**.

---

## 📌 Features

- 🔗 Extracts data from a public Google Spreadsheet
- 🔄 Transforms and validates data, including shelf life calculations
- 📤 Uploads the final output to a remote Linux server via SFTP
- ☁️ Deployable via Google Cloud Functions (HTTP Triggered)
- 🕓 Automated runs using Google Cloud Scheduler
- 🔒 Credentials managed using `.env` files and GCP Secret Manager
- 🐍 Built and tested with a Conda virtual environment

---

## 🧰 Tech Stack

| Purpose                | Tool/Service                     |
|------------------------|----------------------------------|
| Data Source            | Google Sheets                    |
| Transformation         | Python (pandas, datetime, pytz)  |
| Deployment             | Google Cloud Functions           |
| Scheduling             | Google Cloud Scheduler           |
| Secret Management      | GCP Secret Manager               |
| Compute                | GCP VM (Compute Engine)          |
| Remote File Transfer   | SFTP (paramiko)                  |
| Version Control        | Git + GitHub                     |

---

## ETL Project Architecture

📄 Google Sheet (Raw Data)  
          ⬇️  
☁️ Google Cloud Function (Python Script)  
          ⬇️  
🧹 Data Cleaning & Transformation  
          ⬇️  
📁 CSV File Creation  
          ⬇️  
🔐 SFTP Upload using Secret Manager  
          ⬇️  
🖥️ Remote Server (GCP VM)

---

## 🗂️ Project Structure


SeafoodProject/
│
├── .env                        # Environment variables (excluded in .gitignore)
├── .gitignore
├── .my\_env/                   # Conda virtual environment (excluded)
├── main.py                    # Entrypoint for running the ETL
├── transform.py               # Transformation logic
├── upload.py                  # Upload to remote server logic
├── requirements.txt           # Python dependencies
└── README.md                  # Project overview (this file)


---

## 🧰 Tools & Technologies Used

### 💻 **Programming Language**

* **Python 3.10** – Core language used for writing ETL scripts

---

### 📊 **Data Source**

* **Google Sheets** – Source of raw seafood data, accessed via public document ID

---

### 🧪 **Data Processing**

* **pandas** – Data wrangling and transformation
* **datetime** / **pytz** – Timezone-aware date calculations for shelf-life logic

---

### 🔐 **Authentication & Secrets**

* **dotenv** – Loading environment variables locally from `.env` files
* **Google Cloud Secret Manager** – Securely stores and accesses secrets in production

---

### ☁️ **Cloud Services**

* **Google Cloud Functions** – Serverless function to run the ETL process on-demand
* **Google Cloud Scheduler** – Cron-like service to automate execution
* **Google Compute Engine (VM)** – Hosts the remote Linux server (SFTP destination)
* **Google Cloud Source Repositories** – Optional: sync GitHub repo for deployment

---

### 📤 **File Transfer**

* **paramiko** – Python SSH and SFTP library to upload processed files to the remote server
* *(Optional alternative: `pysftp`)*

---

### 📦 **Environment Management**

* **conda** – Manages isolated Python environments and dependencies
* **functions-framework** – For local testing of Cloud Functions via HTTP

---

### 🛠️ **Development Tools**

* **Git + GitHub** – Version control and code collaboration
* **SSH** – Secure shell access to VM for configuring users and SFTP
* **Git Bash / Terminal** – Preferred for running and debugging locally

---

## 🧪 Notes

* Don’t repeatedly ping Google Sheets to avoid 403 errors.
* Use Git Bash + Conda activated env to test locally.
* Switch between writing locally and to server by using CLI flags or HTTP query string.

---

## ✅ Future Work

* [ ] Test Oracle server connection
* [ ] Add firewall rules for new server IP

---

## 🙋‍♀️ Credits

This project is part of volunteer work at a seafood import export organisation to implement & practice my cloud ETL skills for data engineering.

---

## 📎 Useful References

* [Functions Framework for Python](https://cloud.google.com/functions/docs/functions-framework)
* [Google Cloud Scheduler Docs](https://cloud.google.com/scheduler/docs)
* [Secret Manager](https://cloud.google.com/secret-manager)
* [Connecting GitHub with Cloud Source Repositories](https://cloud.google.com/source-repositories/docs/quickstart-connect-external-repository)

