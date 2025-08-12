# AWS DevOps Strands Agent

An intelligent AWS DevOps assistant bot built with the Strands Agents framework, powered by Claude Sonnet 4 on AWS Bedrock with web search capabilities.

## Features

- **AI-Powered Assistant**: Uses Claude Sonnet 4 model via AWS Bedrock for intelligent responses
- **Web Search Integration**: Real-time web search capabilities using DuckDuckGo
- **AWS DevOps Focus**: Specialized in AWS DevOps best practices and guidance
- **Interactive Chat**: Command-line interface for easy interaction
- **Temperature Control**: Optimized temperature setting (0.3) for technical accuracy

## Prerequisites

- Python 3.10+
- AWS Account with Bedrock access
- AWS credentials configured
- Claude Sonnet 4 model access in AWS Bedrock

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sigitp-git/aws-devops-strands-agent.git
cd aws-devops-strands-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure AWS credentials are configured:
```bash
aws configure
```

## Usage

Run the AWS DevOps bot:

```bash
python3 agent.py
```

The bot will start an interactive session where you can ask questions about:
- AWS DevOps best practices
- CI/CD pipeline setup
- Infrastructure as Code (CloudFormation, CDK)
- Container orchestration (ECS, EKS)
- Monitoring and observability
- Security best practices
- AWS service configurations

## Example Interactions

```
🚀 AWS-DevOps-bot: Ask me about DevOps on AWS! Type 'exit' to quit.

You > aws well architected framework
[Bot provides detailed information about the AWS Well-Architected Framework]

You > how to set up ci/cd pipeline
[Bot provides guidance on setting up CI/CD pipelines with AWS services]

You > exit
Happy DevOpsing!
```

## Configuration

### Model Temperature
The bot uses a temperature setting of 0.3 for optimal balance between accuracy and engagement:
- **0.1-0.3**: Very focused, ideal for technical accuracy
- **0.4-0.7**: Balanced responses
- **0.8-1.0**: More creative responses

You can adjust the temperature in `agent.py`:
```python
model = BedrockModel(
    model_id='us.anthropic.claude-sonnet-4-20250514-v1:0', 
    temperature=0.3  # Adjust this value
)
```

## Project Structure

```
aws-devops-strands-agent/
├── agent.py              # Main agent application
├── requirements.txt      # Python dependencies
├── model_temperature.md  # Temperature configuration guide
├── notes.txt            # Development notes
└── README.md            # This file
```

## Dependencies

- `strands-agents`: Core agent framework
- `strands-agents-tools`: Additional agent tools
- `ddgs`: DuckDuckGo search integration
- `boto3`: AWS SDK for Python

## AWS Services Used

- **AWS Bedrock**: Claude Sonnet 4 model hosting
- **AWS IAM**: Authentication and authorization
- **AWS Regions**: us-east-1 (configurable)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check AWS Bedrock documentation for model access
- Verify AWS credentials and permissions

---

Built with ❤️ using Strands Agents and AWS Bedrock