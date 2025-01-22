# Email Classifier

A Python script that automatically classifies Gmail emails into categories like Work, Personal, Finance, Shopping, Social, and Newsletters using the Groq LLM API.

## Features

- Authenticates with Gmail API using OAuth 2.0
- Fetches recent emails from Gmail account
- Classifies emails using Groq's LLaMA 3 8B model
- Exports results to CSV
- Handles plain text and multipart content
- Progress bar for processing

## Prerequisites

- Python 3.6+
- Google Cloud Project with Gmail API enabled
- Groq API key
- Poetry package manager

## Setup

1. **Install Poetry**:
   Install Poetry by running:
   ```bash
   pip install poetry
   ```

2. **Install Dependencies**:
   Run the following command to install all the necessary packages:
   ```bash
   poetry install
   ```

3. **Gmail API Setup**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Enable Gmail API and create OAuth 2.0 credentials
   - Download `credentials.json`

4. **Groq API Setup**:
   - Get your Groq API key
   - Set the environment variable:
     ```bash
     export GROQ_API_KEY="your-api-key"
     ```

5. Place `credentials.json` in the project directory. The script will create `token.json` after the first run.

## Usage

Run the script:

```bash
poetry run python email_categoriser.py
```

On first run, authorize the app via the browser. The script will fetch, classify, and save results to `results.csv`.

## Output Format

CSV with these columns:
- `message_id`: Unique email ID
- `subject`: Email subject
- `content`: First 1000 characters of the email body
- `category`: Classified category

## Categories

- Work
- Personal
- Finance
- Shopping
- Social
- Newsletters

## Limitations

- Processes the latest 10 emails due to rate limit of API keys
- Email body is limited to 1000 characters to handle the context length of llms

## Security

OAuth 2.0 ensures secure Gmail access (read-only). Processing is done locally.

## Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
