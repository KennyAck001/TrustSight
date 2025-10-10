<h1 align="center">🌟 TrustSight</h1>

<p align="center">
An intelligent AI research agent that delivers trustworthy, data-driven insights through advanced trust scoring and cross-validation.
<br />
<a href="#-key-features"><strong>Explore the features »</strong></a>
<br />
<br />
<a href="https://github.com/your-repo/TrustSight/issues">Report Bug</a>
·
<a href="https://github.com/your-repo/TrustSight/issues">Request Feature</a>
</p>
</div>

<div align="center">

</div>

The Problem
In an era of information overload and AI-generated content, finding trustworthy, unbiased information is harder than ever. Standard search tools provide links, not answers, and LLMs can hallucinate without source verification.

Our Solution
TrustSight acts as your AI research partner. It automates the tedious process of searching, fetching, cleaning, and validating information from multiple sources. By clustering claims and applying a multilayer trust score, it delivers insights you can actually rely on.

<p align="center">
<img src="https://via.placeholder.com/800x450/111827/FFFFFF?text=TrustSight+Application+Screenshot" alt="TrustSight Demo" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);" />
</p>

✨ Key Features
Feature	Description
🛡️ Advanced Trust Scoring	Evaluates source credibility, content factuality, and citation quality using a unique multilayer system.
🔄 Automated Cross-Validation	Intelligently clusters similar claims from different sources and assigns a confidence score to each.
📊 Dynamic Output Formats	Automatically detects the best format for your query, delivering bullet points, tables, or graphs.
📈 Real-time Graph Generation	Generates insightful charts and graphs on the fly using matplotlib for data visualization.
🎨 Modern & Intuitive UI	A sleek, ChatGPT-inspired dark theme interface built with React and Tailwind CSS for a great user experience.
⚡ High-Performance Backend	Built with Python and FastAPI, featuring asynchronous processing for fast, non-blocking I/O.

Export to Sheets
🛠️ Tech Stack
Our stack is built on modern, high-performance technologies to deliver a fast and reliable experience.

Category	Technology
🌐 Backend	Python 3.11+, FastAPI
🧠 AI & Search	OpenAI API, Google Gemini API, Serper API
💻 Frontend	React 19, Vite, Tailwind CSS
Linter	ESLint

Export to Sheets
🚀 Getting Started
Get your local copy of TrustSight up and running in minutes.

Prerequisites
Python 3.11+

Node.js 18+ and npm

API Keys for OpenAI, Serper, and optionally Google Gemini

Installation
Clone the Repository

Bash

git clone <repository-url>
cd TrustSight
Setup the Backend

Bash

# Install Python dependencies
pip install -r requirements.txt
<details>
<summary><strong>Set Environment Variables</strong> (Click to expand)</summary>

Create a .env file in the project root and add your API keys:

Code snippet

OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
GEMINI_API_KEY=your_gemini_api_key  # Optional
</details>

Bash

# Run the FastAPI server
python main.py
Setup the Frontend

Bash

# Navigate to the frontend directory
cd frontend

# Install npm packages
npm install

# Start the development server
npm run dev
Your TrustSight instance is now running!

Backend API: http://localhost:8000

Frontend App: http://localhost:5173

📖 API Usage
Interact with the TrustSight API to power your own applications.

<details>
<summary><strong>POST /research</strong> - Perform a research query</summary>

Request:

JSON

{
  "query": "Compare different programming languages in a table"
}
Response (Table):

JSON

{
  "table": "| Language | Typing | Performance | Use Case |\n|---|---|---|---|\n| Python | Dynamic | Medium | Web, AI/ML |\n| Rust | Static | High | Systems Prog |\n| JavaScript | Dynamic | Medium | Web Dev |"
}
</details>

<details>
<summary><strong>POST /approve_source & /flag_source</strong> - Manage trust scores</summary>

Boost or penalize a source's credibility score.

Request (/approve_source):

JSON

{
  "source": "https://www.nature.com/"
}
</details>

🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

🍴 Fork the Project

🌟 Create your Feature Branch (git checkout -b feature/AmazingFeature)

✅ Commit your Changes (git commit -m 'Add some AmazingFeature')

🚀 Push to the Branch (git push origin feature/AmazingFeature)

🎉 Open a Pull Request



<div align="center">
<p>Made with ❤️ by the TrustSight team</p>
<p>
<a href="#-trustsight">Back to top</a>
</p>
</div>