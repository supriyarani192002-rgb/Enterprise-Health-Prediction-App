# Enterprise Health Prediction App

A robust, end-to-end data engineering application designed to analyze patient vitals and generate intelligent health insights. Built with a focus on data integrity, security, and scalable architecture.

##  Key Technical Features

* **AI-Powered Analysis**: Integrates the Google Gemini API to provide real-time, context-aware health predictions based on patient data.
* **Data Quality & Validation**:
* Implements **strict numeric validation** for clinical fields (Glucose, Haemoglobin, Cholesterol) to ensure data accuracy.
* Utilizes **regex-based email validation** to ensure standardized communication channels.


* **Full CRUD Functionality**: A comprehensive dashboard that allows users to Create, Read, Update, and Delete patient records seamlessly within a local SQLite database.
* **Secure Configuration**: Adheres to security best practices by managing sensitive API keys and credentials using `.env` variables.

## 🛠 Tech Stack

* **Frontend**: Streamlit
* **Backend & Data Processing**: Python, Pandas, SQLAlchemy
* **AI/LLM Integration**: Google Gemini API
* **Database**: SQLite

## 💻 Getting Started

### Prerequisites

Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt

```

### Installation

1. **Clone the repository**:
```bash

```



git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

```
2.  **Environment Setup**:
    Create a `.env` file in the root directory and add your API credentials:
    ```text
GOOGLE_API_KEY=your_actual_api_key_here

```

3. **Launch the Application**:
```bash

```



streamlit run app.py

```

## 📈 Engineering Highlights
*   **Modular Architecture**: Built with separate logic for AI services and database operations, allowing for easy API engine swapping (e.g., migrating from AWS Bedrock to Google Gemini).


***
## 🎥 Project Demo
# Watch the Application Demo Video - (demo_video.mp4)
```
