# 🔐 Offline Password & ENV Manager

A **secure, open-source, offline password and environment variable manager** built with Python.  
Designed to protect sensitive data like passwords and `.env` files using strong encryption — **without relying on any external servers or databases**.

---

## 🚀 Installation (Quick Start)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/offline-password-manager.git
cd offline-password-manager
```
2. Create a virtual environment (recommended)
```
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```
4. Install dependencies
```
pip install -r requirements.txt
```
6. Run the application
```
python main.py
```
🧠 Project Overview

This application provides a fully offline solution for storing:

🔑 Passwords
📁 Environment variables (.env-like data)

Everything is:

🔐 Encrypted locally  
💾 Stored in system files  
🚫 Never sent to any server  
✨ Features  


### 🔐 Security First  
Passwords are encrypted using PBKDF2   
User authentication handled via bcrypt   
No plaintext passwords stored anywhere   


### 🗂️ Local Storage   
All data is stored securely in local files  
No external database or cloud dependency   


### 👤 Authentication System   
User must log in to access stored data  
Secure password verification using hashing  


### ⏳ Temporary Decryption  
Passwords and env values are shown only for 30 seconds   
Automatically hidden after timeout      


### 📦 ENV File Storage      
Store sensitive .env variables securely     
Access them only after authentication    

 
### 🖥️ Simple GUI        
Built using Python Tkinter        
Lightweight and easy to use    


### 🛠️ Tech Stack      
Component	Technology     
Language	Python         
UI	Tkinter           
Encryption	PBKDF2           
Authentication	bcrypt          
Storage	Local Filesystem           


🔒 How Security Works           
User creates an account (username + password)   
Password is hashed using bcrypt     
Stored passwords/env data:      
Encrypted using PBKDF2-derived keys     
When accessing:      
User re-authenticates               
Data is decrypted temporarily (30 seconds)     

🤝 Contributing

We welcome contributions from everyone 🚀

How to contribute:

Fork the repository
Create a new branch
```
git checkout -b feature/your-feature-name
```
Make your changes
Commit
```git commit -m "Add: your feature"```
Push and open a Pull Request


🧩 Contribution Ideas       

- Improve UI/UX (Tkinter redesign)  
- Add search functionality          
- Add export/import encrypted backups            
- Implement multi-user support           
- Add dark mode 🌙           
- Improve encryption handling or key management     



⚠️ Important Notes      
This is an offline-first tool                     
If you forget your master password → data cannot be recovered                        
Always keep backups of encrypted files





📜 License
This project is open-source under the MIT License.

💡 Vision

To build a simple, transparent, and secure offline alternative to cloud-based password managers — giving users full control over their sensitive data.
