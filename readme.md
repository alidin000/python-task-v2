# Python Task V2: Post and Comment Management API with AI Moderation

## Table of Contents
1. [Project Description](#project-description)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Running the API](#running-the-api)
6. [Running the Bot](#running-the-bot)
7. [AI API Setup](#ai-api-setup)
8. [Running Tests](#running-tests)
9. [Contributing](#contributing)

## Project Description
This project is a simple API for managing posts and comments with AI moderation. The API is built using FastAPI and Pydantic, and it includes features for user registration, login, post and comment management, AI-powered content moderation, and analytics. Additionally, a bot is included to generate posts and comments using AI and interact with the API.

## Features
- **User Registration and Login**: Secure user authentication with JWT.
- **Post and Comment Management**: Create, read, update, and delete posts and comments.
- **AI Moderation**: Automatic detection and blocking of foul language and insults in posts and comments.
- **Analytics**: Get analytics on the number of comments added to posts over a specific period.
- **Bot**: A simple bot to generate and post content using AI.

## Project Structure

```plaintext
.
├── alembic/
├── app/
│   ├── __pycache__/
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── deps.py
│   ├── main.py
│   ├── models.py
│   ├── moderation.py
│   ├── schemas.py
├── bot/
│   ├── __pycache__/
│   ├── bot.py
│   ├── config.py
│   ├── template_config.py
├── venv/
├── tests/
│   ├── test_main.py
│   ├── test_post.py
├── .gitignore
├── alembic.ini
├── init_db.py
├── readme
├── requirements.txt
└── test.db
```

## Installation

### 1. Set Up a Virtual Environment

Create and activate a Python virtual environment:

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Cloud Credentials

Ensure you have a Google Cloud service account key file (JSON) and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

#### On Windows:

```bash
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-file.json
```

#### On macOS/Linux:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
```

### 4. Apply Migrations

Use Alembic to apply database migrations:

```bash
alembic upgrade head
```

### 5. Initialize the Database

Run the following script to initialize the database:

```bash
python init_db.py
```

### 6. Environment Variables

Create a `.env` file in the project root and add the following variables:

```bash
GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
```

Add any other environment-specific variables you need for your FastAPI settings.

## Running the API

### Start the API Server

To start the FastAPI server, run:

```bash
uvicorn app.main:app --reload
```

The API will be accessible at `http://127.0.0.1:8000`.

### API Endpoints

- **Root Endpoint**: `GET /`  
  Returns a welcome message.
  
- **User Registration**: `POST /register/`  
  Register a new user.

- **User Login**: `POST /login/`  
  Obtain an access token for an authenticated user.

- **Create Post**: `POST /posts/`  
  Create a new post.

- **Create Comment**: `POST /posts/{post_id}/comments/`  
  Add a comment to a post.

- **Get Analytics**: `GET /api/comments-daily-breakdown?date_from=<YYYY-MM-DD>&date_to=<YYYY-MM-DD>`  
  Get daily aggregated comment data within a date range.

- **Automatic Response to Comments**: `/comments/auto-response/`  
  Endpoint and logic for enabling auto-response to comments after a delay.

## Running the Bot

### Configure the Bot

The bot settings can be adjusted in the `bot/config.py` file, including:
- Number of users to create and emulate
- Type of comments to generate (positive/negative)
- Number of posts and comments to create for each user

### Start the Bot

To run the bot and start generating posts and comments, run:

```bash
python bot/bot.py
```

## AI API Setup

To enable the bot to generate text content using Google's Generative AI, follow these steps:

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the project dropdown and select "New Project".
   - Enter a name for your project and click "Create".
   - Once the project is created, make sure it's selected.

2. **Enable the Generative AI API**:
   - In the Google Cloud Console, navigate to "APIs & Services" > "Library".
   - Search for "Generative AI API" and click on it.
   - Click "Enable" to activate the API for your project.

3. **Obtain API Credentials**:
   - Go to "APIs & Services" > "Credentials".
   - Click "Create Credentials" and select "API Key".
   - Copy the API key provided. You'll need this for your application.

4. **Install the API Client Library**:
   - Install the Google Cloud Generative AI Python client library using pip:
     ```bash
     pip install google-generativeai
     ```

5. **Configure the Application**:
   - Store your API key in `bot/config.py`:
     ```python
     # bot/config.py
     class Config:
        API_URL = "http://localhost:8000"  # URL of your FastAPI app
        AI_API_URL = "https://ai.google.dev/generate-text"  # Google's AI API endpoint
        AI_API_KEY = "your_api_key"  # Replace with your Google AI API key
     ```
   - Ensure that your bot is configured to use this API key when generating text content.

## Running Tests

### Run the Test Suite

Tests are provided for the post creation and analytics functions. To run the tests, execute:

```bash
pytest
```

This will execute tests for post creation, analytics, and other aspects of the application.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## Additional Information

For any additional questions or troubleshooting, please refer to the official documentation for [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), and [Google Generative AI API](https://cloud.google.com/generative-ai).
``