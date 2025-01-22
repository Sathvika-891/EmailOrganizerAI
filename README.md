# Gmail Email Classifier

A Python script that automatically classifies Gmail emails into predefined categories using the Groq LLM API. This tool helps organize your inbox by categorizing emails into Work, Personal, Finance, Shopping, Social, and Newsletter categories.

## Features

- Authenticates with Gmail API using OAuth 2.0
- Fetches recent emails from your Gmail account
- Classifies emails using Groq's LLaMA 3 8B model
- Exports results to a CSV file for analysis
- Handles both plain text and multipart email content
- Includes progress bar for processing status

## Prerequisites

- Python 3.6 or higher
- A Google Cloud Platform account with Gmail API enabled
- A Groq API key

## Required Libraries

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install pandas tqdm litellm
```

## Setup

1. Create a Google Cloud Project and enable the Gmail API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create OAuth 2.0 credentials and download the `credentials.json` file

2. Set up your Groq API key:
   - Sign up for a Groq account and get your API key
   - Set the environment variable:
     ```bash
     export GROQ_API_KEY="your-api-key"
     ```

3. Place the files in your project directory:
   - Put `credentials.json` in the same directory as the script
   - The script will generate `token.json` on first run

## Usage

1. Run the script:
```bash
python gmail_classifier.py
```

2. On first run, you'll be prompted to authorize the application:
   - A browser window will open
   - Sign in with your Google account
   - Grant the requested permissions

3. The script will:
   - Fetch your recent emails
   - Classify them using the Groq API
   - Save the results to `results.csv`

## Output Format

The script generates a CSV file with the following columns:
- `message_id`: Unique identifier for the email
- `subject`: Email subject line
- `content`: First 1000 characters of email body
- `category`: Classified category

## Categories

Emails are classified into one of the following categories:
- Work
- Personal
- Finance
- Shopping
- Social
- Newsletters

## Limitations

- Processes the most recent 10 emails by default
- Email body content is limited to 1000 characters to manage API token limits
- Requires Gmail API access and Groq API key

## Security Note

This application requires access to your Gmail account. It uses OAuth 2.0 for secure authentication and only requests read-only access to your emails. All processing is done locally on your machine.

## Contributing

Feel free to submit issues and enhancement requests. Follow these steps to contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
