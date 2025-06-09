# TalentScout: Streamlit Hiring Agent

TalentScout is an interactive Streamlit app for conducting technical interviews and candidate screening, powered by LLMs and LangChain. It validates candidate information, generates tech-specific interview questions, and securely stores responses for review.

## Features

- Candidate info validation using LLM
- Dynamic tech stack question generation
- Secure data storage with Fernet encryption
- Modular, scalable codebase
- Docker & cloud ready

## Demo

![screenshot](screenshot.png) <!-- Add a screenshot of your app here -->

## Getting Started

### Prerequisites

- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)
- [Docker](https://docs.docker.com/get-docker/) (optional, for containerized deployment)

### Installation

1. **Clone the repository:**
git clone https://github.com/yourusername/your-repo.git
cd your-repo

2. **Install dependencies:**
pip install -r requirements.txt

3. **Set up environment variables:**
- Copy `.env.example` to `.env` and fill in your keys:
  ```
  TOGETHER_API_KEY=your-key-here
  FERNET_KEY=your-fernet-key-here
  ```

### Running Locally

streamlit run Streamlit_app.py


### Running with Docker

docker build -t my-streamlit-app .
docker run -p 8501:8501
-e TOGETHER_API_KEY=your-key
-e FERNET_KEY=your-fernet-key
my-streamlit-ap

## Project Structure

Hiring-Agent/
├── app/                # Core modules and logic
├── Streamlit_app.py    # Main Streamlit app
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md



## Technologies Used

- Streamlit
- LangChain
- Python-dotenv
- Cryptography (Fernet)
- Docker

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Contact

Your Name – [your.email@example.com](mailto:your.email@example.com)
