# EECS449 Financial Advisor  
**Github Repository for EECS449 Conversational AI Project: Financial Advisor Tool**  

**By:** Anneliese Ferguson, Benjamin Yee, Cindy Zhang, Fabian Ruiz, Herman Wu, Heqing (HQ) Wang, Julia Morville, Vedikas Sridharan  

---

### 🚀 Quick Start Guide  
#### **Installing Requirements**
1. Run:
   `pip install -r requirements.txt`

#### **Ollama Setup (Root Terminal)**  
1. Run:  
   `ollama pull deepseek-r1:1.5b`  
   `ollama pull deepseek-r1:7b`  
   `ollama pull gemma3:1b`  
   `ollama pull mistral`  
   `ollama pull llama3.3`  
2. Start the server:  
   `ollama serve`  

#### **Running the Application**  
1. Open **two separate terminals**  
2. **Terminal 1 (Backend):**  
   `cd backend`  
   `python3 app.py`  
3. **Terminal 2 (Frontend):**  
   `cd frontend`  
   `npm start`  

---

### 🗄️ Database Management (Root Terminal)  
- The database (`app.db`) is created automatically when you sign up/login.  
- **Manual management options:**  

1. Make the script executable:  
   `chmod +x database.sh`  
2. **Reset the database** (deletes all data):  
   `./database.sh reset`  
3. **Populate with test data** (includes admin user):  
   `./database.sh populate`  
   - **Admin credentials:**  
     - Username: `admin`  
     - Password: `admin123`  

---

### Notes  
- Ensure Ollama is running before starting the backend.  
- The frontend will open automatically in your browser at `http://localhost:3000`.