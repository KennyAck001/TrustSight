<div align="center">

<img src="https://storage.googleapis.com/maker_studio_production/generations/a6b09337-b9c1-4b72-b7e5-397ac93fcb9c/images/0_0.webp" alt="TrustSight Logo Banner" width="200"/>

<h1>
🌟 TrustSight 🌟
</h1>

<p>
<b>An intelligent AI-powered research agent that delivers trustworthy, data-driven insights through advanced trust scoring and cross-validation.</b>
</p>

<p>
TrustSight combines web search, content analysis, and machine learning to provide accurate research outputs in multiple formats.
</p>

<p>
<a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python"></a>
<a href="https://fastapi.tiangolo.com/" target="_blank"><img src="https://img.shields.io/badge/FastAPI-0.104.1-green.svg" alt="FastAPI"></a>
<a href="https://reactjs.org/" target="_blank"><img src="https://img.shields.io/badge/React-19.1.1-blue.svg" alt="React"></a>
<a href="https://vitejs.dev/" target="_blank"><img src="https://img.shields.io/badge/Vite-7.1.7-yellow.svg" alt="Vite"></a>
<a href="https://tailwindcss.com/" target="_blank"><img src="https://img.shields.io/badge/Tailwind_CSS-3.4.18-38B2AC.svg" alt="Tailwind CSS"></a>
<a href="LICENSE" target="_blank"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
</p>
</div>

<p align="center">
<img src="https://storage.googleapis.com/maker_studio_production/generations/819d45e0-5205-4c07-b648-2612f00a6e0c/images/0_0.webp" alt="TrustSight Application Demo" />
</p>

🎯 Key Features
🔍 Intelligent Research: Performs comprehensive web searches and content analysis to find the most relevant information.

📊 Multiple Output Formats: Returns results as clean bullet points, structured tables, or interactive graphs.

🛡️ Trust Scoring: Employs an advanced multilayer trust scoring system to evaluate source credibility and reliability.

🔄 Cross-Validation Engine: Automatically clusters similar claims from different sources and assigns confidence scores.

🎨 Modern UI: Features a sleek, ChatGPT-inspired dark theme interface built with React and Tailwind CSS.

⚡ High-Performance Backend: Built on a high-performance Python backend with FastAPI for asynchronous processing.

📈 Dynamic Graph Generation: Creates graphs in real-time using matplotlib and delivers them seamlessly to the frontend.

🛠️ Tech Stack & Tools
Our platform is built with a modern, high-performance tech stack to deliver fast and reliable results.

Category	Technology
🐍 Backend	Python 3.11+, FastAPI
🧠 AI & Search	OpenAI API, Google Gemini API, Serper API
⚛️ Frontend	React 19, Vite, Tailwind CSS
✨ Linting	ESLint

Export to Sheets
🚀 Getting Started
Follow these instructions to get a local copy up and running for development and testing purposes.

Prerequisites
Python: Version 3.11 or higher

Node.js: Version 18+ and npm

API Keys: You'll need API keys for:

OpenAI

Serper

Google Gemini (Optional, for fallback)

⚙️ Backend Installation
Clone the Repository

Bash

git clone <repository-url>
cd TrustSight
Install Python Dependencies

Bash

pip install -r requirements.txt
Configure Environment Variables
Create a .env file in the project's root directory and add your API keys:

Code snippet

OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
GEMINI_API_KEY=your_gemini_api_key  # Optional
Launch the Backend Server

Bash

python main.py
The API will be live at http://localhost:8000.

🖥️ Frontend Installation
Navigate to the Frontend Directory

Bash

cd frontend
Install Node.js Dependencies

Bash

npm install
Run the Development Server

Bash

npm run dev
The frontend will be live at http://localhost:5173.

📖 How to Use
TrustSight's API is simple and intuitive. The /research endpoint automatically detects the desired output format based on your query.

Example Queries
Bullet Points (default): "What are the benefits of renewable energy?"

Tables: "Compare top cloud providers in a table"

Graphs: "Show a graph of Moore's Law over time"

Core API Endpoints
<details>
<summary><strong>POST /research</strong> - Perform a research query</summary>

Performs a comprehensive search and returns formatted results with trust scores.

Request Body:

JSON

{
  "query": "What are the benefits of renewable energy?"
}
Example Response:

JSON

{
  "format": "points",
  "data": "- Reduces greenhouse gas emissions\n- Creates jobs in green sectors\n- Decreases dependence on fossil fuels",
  "sources": [
    { "url": "https://www.un.org/en/climatechange/what-is-renewable-energy", "trust_score": 0.95 },
    { "url": "https://www.nrdc.org/stories/renewable-energy-clean-facts", "trust_score": 0.88 }
  ]
}
</details>

<details>
<summary><strong>POST /approve_source</strong> - Boost a source's trust score</summary>

Approves a source URL, manually boosting its credibility score for future queries.

Request Body:

JSON

{
  "source": "https://example.com"
}
</details>

<details>
<summary><strong>POST /flag_source</strong> - Lower a source's trust score</summary>

Flags a source URL as unreliable, lowering its credibility score for future queries.

Request Body:

JSON

{
  "source": "https://unreliable-site.com"
}
</details>

🏗️ Project Architecture
The project is organized into a modular backend and a separate frontend application for a clean separation of concerns.

TrustSight/
├── main.py               # FastAPI application entry point
├── search.py             # Web search using Serper API
├── fetcher.py            # Async content fetching and cleaning
├── claims.py             # LLM-based claim extraction
├── trust_scoring.py      # Multilayer trust scoring system
├── cve.py                # Cross-validation engine
├── summarizer.py         # Query-type based summarization
├── graph_generator.py    # Graph generation with matplotlib
├── response_generator.py # Unified response generation
├── frontend/             # React frontend application
│   ├── src/
│   │   ├── App.jsx       # Main React component
│   │   ├── App.css       # Styles and dark theme
│   │   └── ...
│   └── ...
└── requirements.txt      # Python dependencies
🤝 How to Contribute
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Please follow these steps to contribute:

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is distributed under the MIT License. See LICENSE for more information.

<div align="center">
<p>Made with ❤️ by the TrustSight team</p>
<p>
<a href="#-trustsight">Back to Top</a>
</p>
</div>