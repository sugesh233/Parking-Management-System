#  Parking Management System 🚗

A full-stack web application designed to streamline the management of parking operations. Built with **Flask (Python)** and **MongoDB**, this system enables secure admin login, vehicle tracking, and dynamic pricing based on vehicle type — ideal for institutions, malls, gated communities, or smart cities.

---

## 🔍 Overview

This Parking Management System enables:
- 🔐 Secure admin login
- 🅿️ Real-time vehicle entry/exit tracking
- 🧮 Automatic parking fee calculation based on duration
- 🛠️ Management of vehicle categories and hourly pricing
- 📦 Data storage using MongoDB (NoSQL)

---

## 🧰 Tech Stack

| Layer           | Technology         |
|----------------|--------------------|
| Backend         | Python + Flask     |
| Database        | MongoDB (NoSQL)    |
| Frontend        | HTML (Jinja2 templating via Flask) |
| Package Manager | pip (Python)       |

---

## 📁 Project Structure

```

Parking-Management-System/
├── app.py              # Flask backend application
├── templates/          # Jinja2-based HTML templates
├── requirements.txt    # Dependency file
├── .gitignore          # Git exclusions
└── venv/               # Python virtual environment (ignored)

````

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/parking-management-system.git
cd parking-management-system
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# OR
source venv/bin/activate     # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🍃 MongoDB Configuration

### Local MongoDB:

Ensure MongoDB service is installed and running:

```bash
net start MongoDB  # Windows
```

### OR: Use MongoDB Atlas (Cloud)

1. Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Replace the connection string in `app.py`:

```python
MONGODB_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
```

3. Whitelist your IP and set up access credentials in Atlas

---

## ▶️ Run the App

```bash
python app.py
```

Then visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

> 🧪 Default Admin Password: `1234`

---

## 🗃️ MongoDB Shell (Optional)

Inspect your database using `mongosh`:

```bash
mongosh
show dbs
use parking_system
show collections
db.vehicles.find().pretty()
db.categories.find().pretty()
```

---

## 🙋‍♂️ Author

**Sugesh**
[GitHub Profile](https://github.com/sugesh233)

---

