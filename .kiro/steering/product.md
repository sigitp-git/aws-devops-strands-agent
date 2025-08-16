# Product Overview

## AWS DevOps Strands Agent

An intelligent AWS DevOps assistant bot built with the Strands Agents framework, powered by Claude Sonnet 4 on AWS Bedrock with web search capabilities.

### Core Purpose
- Specialized AI assistant for AWS DevOps best practices and guidance
- Interactive command-line interface for technical consultations
- Real-time web search integration for up-to-date information

### Key Features
- **AI-Powered**: Claude Sonnet 4 via AWS Bedrock with efficiency-optimized prompts and customer service standards
- **Dual Performance Modes**: Ultra-fast knowledge-only agent + comprehensive MCP integration
- **Enhanced Web Search**: DuckDuckGo integration with timeout protection and smart result limiting
- **Triple MCP Integration**: Direct access to AWS Documentation, Knowledge Base, and EKS clusters
- **Tool Discovery**: Built-in tool categorization and discovery (21 total tools)
- **AWS Focus**: Specialized in DevOps, CI/CD, IaC, containers, monitoring, EKS management
- **Performance Optimized**: Instant responses (< 1 second) or comprehensive tool-based queries
- **Customer-Focused**: Friendly, patient, and helpful interactions with proactive assistance
- **Enhanced Architecture**: Modular design with separation of concerns and proper error handling
- **Production Ready**: Structured logging, graceful shutdown, configuration validation
- **Developer Friendly**: Full type hints, comprehensive documentation, organized testing

### Target Use Cases

**Ultra-Fast Agent (fast_agent.py):**
- Quick AWS service explanations and concepts
- General DevOps best practices consultation
- Architecture guidance and recommendations
- AWS service comparisons and use cases

**Full-Featured Agent (agent.py):**
- Real-time AWS documentation queries and recommendations
- EKS cluster operations, monitoring, and troubleshooting
- Kubernetes workload deployment and management
- CI/CD pipeline guidance and troubleshooting
- Infrastructure as Code (CloudFormation, CDK, Terraform)
- Container orchestration (ECS, EKS) with direct cluster management
- Monitoring and observability setup
- Security best practices and compliance
- AWS service configurations and optimization