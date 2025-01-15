# AI Chatbot Portfolio Project

## Live Website
[Visit the live website here](https://ai-chatbot-assistant-jz2s.onrender.com)

**AI Chatbot Portfolio Project** is a multi-persona chatbot web application built with Flask. It features three distinct chatbots: a Clothing Store Assistant, a Tech Support Assistant, and a Travel Agency Assistant. The chatbots leverage OpenAI's GPT model for dynamic conversation, store user data in SQLite databases, and feature smooth, responsive UI animations.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App Locally](#running-the-app-locally)
- [Database Setup](#database-setup)
- [Deployment](#deployment)
- [Responsive Design](#responsive-design)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Multiple Bot Personas**: Switch seamlessly between Clothing, Tech, and Travel assistants, each with specialized knowledge and behavior.
- **Dynamic Conversations**: Uses OpenAI's GPT model to generate conversational responses.
- **User Data Storage**: Saves user information (name, email, phone, tracking numbers) in SQLite databases for future reference.
- **Responsive UI with Animations**: Smooth animations, fade transitions, and responsive design for desktop and mobile.
- **Database Integration**: SQLite for storing user info, orders, inventory, and shipping details.
- **Context Management**: Maintains conversation history and session memory to provide contextually relevant responses.

---

## Project Structure

project_root/ │ ├── app.py # Main Flask application ├── models.py # Database models and helper functions ├── database.py # Database connection functions ├── requirements.txt # Python dependencies ├── Procfile # For Heroku deployment ├── runtime.txt # Specifies Python version (optional) ├── .env # Environment variables (not committed to GitHub) ├── README.md # Project documentation │ ├── static/ # Static assets (CSS, JS, images) │ ├── styles.css │ ├── scripts.js │ └── images/ # Background images and other assets │ └── templates/ └── index.html # Main HTML template

markdown
Copy code

---

## Features in Detail

### Chatbot Personas
- **Clothing Store Assistant**: Answers questions about clothing items, orders, and helps with tracking shipments.
- **Tech Support Assistant**: Provides assistance with Windows-related issues and stores user tech support info.
- **Travel Agency Assistant**: Offers travel-related advice, itinerary help, and booking information.

### User Data Handling
- Parses user input to extract names, emails, phone numbers, and tracking numbers.
- Saves extracted data in respective SQLite databases (`clothing.db`, `tech.db`, etc.) for future interactions and analysis.

### UI Animations & Responsiveness
- Smooth fade-in of chat messages.
- Typing indicator animation to simulate the bot "thinking."
- Buttons scale and display shadows on hover.
- Chat bubbles: user messages appear on the right, bot messages on the left.
- Responsive design ensures usability across devices.

---

## 2. Installation

### Prerequisites

- Python 3.9 or higher
- Git

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
Create a virtual environment:

bash
Copy code
python -m venv venv
Activate it:

On Windows:
bash
Copy code
venv\Scripts\activate
On macOS/Linux:
bash
Copy code
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt

3. Configuration
Environment Variables
Create a .env file in the root directory:

makefile
Copy code
OPENAI_API_KEY=sk-REPLACE_WITH_YOUR_KEY
Replace sk-REPLACE_WITH_YOUR_KEY with your actual OpenAI API key. This file should remain private.

The application uses python-dotenv to load this key. Ensure it's referenced in app.py:

python
Copy code
from dotenv import load_dotenv
load_dotenv()

4. Running the App Locally
Ensure your virtual environment is activated.
Run the Flask application:
bash
Copy code
python app.py
Open your browser and navigate to http://127.0.0.1:5000.
You should see the homepage and be able to select different chatbots and interact with them.

5. Database Setup
Your application automatically creates necessary tables on startup using functions in models.py. It creates separate SQLite databases for clothing and tech assistants.

To manually check if data is being saved:

Use a tool like DB Browser for SQLite or the sqlite3 CLI.
Open the relevant .db file (e.g., tech.db).
Run SQL queries like:
sql
Copy code
SELECT * FROM tech_users;
to verify user data is stored correctly.

6. Deployment
Deploying on Heroku
Ensure Procfile and requirements.txt are in the root directory.
Log in to Heroku:
bash
Copy code
heroku login
Create a new app:
bash
Copy code
heroku create your-app-name
Set environment variables on Heroku:
bash
Copy code
heroku config:set OPENAI_API_KEY=sk-REPLACE_WITH_YOUR_KEY
Initialize Git, commit changes if not done, and push to Heroku:
bash
Copy code
git add .
git commit -m "Deploying to Heroku"
git push heroku master
Open your deployed app:
bash
Copy code
heroku open

7. Responsive Design
The HTML includes a meta viewport tag:
html
Copy code
<meta name="viewport" content="width=device-width, initial-scale=1.0">
CSS uses flexible layouts (flexbox) and media queries to adapt to mobile screens.
Test the UI using browser developer tools’ device simulation and on actual mobile devices.
Further adjustments can be made in styles.css using media queries to improve the mobile experience.
8. Contributing
Contributions are welcome! If you'd like to improve the project:

Fork the repository.
Create a new branch (git checkout -b feature-name).
Make your changes, commit them (git commit -m "Add new feature").
Push to your fork (git push origin feature-name).
Open a Pull Request.

9. License

10. Contact
Author: Bek Abdurakhmonov
Email: UAbdurakhmonov00@student.coppin.edu
GitHub: https://github.com/Ulugbek999
Feel free to reach out with questions or suggestions!
