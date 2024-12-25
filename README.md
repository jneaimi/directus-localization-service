cat > README.md << EOL
# Directus Localization Service

An English to Arabic translation service using OpenAI's GPT models, designed to work with Directus.

## Features

- English to Arabic translation using OpenAI GPT models
- Maintains HTML formatting
- Basic authentication
- Docker support
- Health check endpoint

## Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Python 3.11+ (for local development)

## Quick Start

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/directus-localization-service.git
cd directus-localization-service
\`\`\`

2. Create a \`.env\` file:
\`\`\`bash
OPENAI_API_KEY=your_openai_api_key_here
REDIS_HOST=redis
REDIS_PORT=6379
\`\`\`

3. Build and run with Docker:
\`\`\`bash
docker compose up --build
\`\`\`

## API Usage

### Translate Content

\`\`\`bash
curl -X POST \\
  http://localhost:8000/translate \\
  -H 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' \\
  -H 'Content-Type: application/json' \\
  -d '{
    "englishContent": "{\"translations\":{\"update\":[{\"headline\":\"<p>Hello World</p>\",\"languages_code\":{\"code\":\"en-US\"},\"id\":1}]}}"
}'
\`\`\`

### Health Check

\`\`\`bash
curl http://localhost:8000/health
\`\`\`

## Local Development

1. Create virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate  # Windows
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Run development server:
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

## License

MIT License
EOL