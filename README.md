# 🧭 Career Pathfinding Console

An interactive full-stack web application that helps users explore optimal career trajectories based on skills, education duration, salary expectations, and specialization options.

---

## 📦 Project Structure

ALXCapstone/
├── Django-backend/
│   └── Roadmap/     ← Django project root
├── Vue-Front-End/
│   └── Roadmap/     ← Vue 3 frontend root
├── README.md # You are here
└── venv/ # Python virtual environment (excluded in .gitignore)

yaml
Copy code

---

## ⚙️ Backend Setup (Django + DRF)

### 🔧 Requirements

- Python 3.8+
- pip

### 🛠 Setup Instructions

```bash
# 1. Clone the repository
git clone https://https://github.com/TheophilusMalatji/ALXCapstone.git

bash
Copy code
# 2. Create a virtual environment
python -m venv venv
bash
Copy code
# 3. Activate the virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
bash
Copy code
# 4. Navigate to the Django backend directory
cd Roadmap
bash
Copy code
# 5. Install backend dependencies
pip install -r requirements.txt
bash
Copy code
# 6. Run migrations
python manage.py makemigrations
python manage.py migrate
bash
Copy code
# 7. Populate initial data
python manage.py populate_eng_data
python manage.py populate_finance_data
python manage.py populate_nursing_data
bash
Copy code
# 8. Start the Django development server
python manage.py runserver
The backend API will be available at http://127.0.0.1:8000/api/

🌐 Frontend Setup (Vue 3 + Vite)
🔧 Requirements
Node.js 18+

npm

🛠 Setup Instructions
bash
Copy code
# 1. Navigate to the frontend directory
cd ../Vue-Front-End
bash
Copy code
# 2. Install frontend dependencies
npm install
bash
Copy code
# 3. Start the Vue dev server
npm run dev
The frontend will run at http://localhost:5173 by default

✅ Features
🔍 Targeted Career Search: Filter based on salary, education years, and sector

🧠 Visual Roadmaps: Display education steps, skills, and specialization paths

📊 Data-Driven: Pre-populated industry data (Engineering, Finance, Nursing, IT)

🎨 Responsive UI: Modern design using Tailwind CSS + Vue transitions

🔌 API-Driven: Clean separation between backend and frontend

📋 API Endpoints
The API is available at: http://localhost:8000/api/

/api/careers/ – List all careers

/api/careers/<id>/ – Get details for a specific career

/api/sectors/ – List available sectors

/api/skills/ – List all skills

/api/education/ – List education options

🛡️ Admin Panel
To access Django admin:

bash
Copy code
python manage.py createsuperuser
Then go to http://127.0.0.1:8000/admin/ and log in.

📄 License
This project is licensed under the MIT License.

🤝 Contributing
Feel free to fork the project and submit PRs! If you encounter issues or have ideas for improvement, open an issue.

🧠 Credits
Built with ❤️ using:

Django

Vue 3

Tailwind CSS

Vite

vbnet
Copy code

Let me know if:

- You want to include images or badges (e.g., build status, MIT license, GitHub Actions).
- You plan to deploy (I can add hosting instructions — Netlify for frontend, Railway/Render for backend).
- You want to rename anything for better project clarity.