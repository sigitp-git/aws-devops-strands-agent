# Tests

This directory contains test scripts for the AWS DevOps Strands Agent.

## Available Tests

### `test_mcp_usage.py`
Tests MCP server connectivity and tool availability.

**Usage:**
```bash
# Test all MCP servers
python3 tests/test_mcp_usage.py

# Test specific server
python3 tests/test_mcp_usage.py "AWS Documentation"
python3 tests/test_mcp_usage.py "AWS Knowledge" 
python3 tests/test_mcp_usage.py "AWS EKS"
```

### `simple_mcp_test.py`
Simple test to verify basic agent functionality and MCP connections.

**Usage:**
```bash
python3 tests/simple_mcp_test.py
```

## Running Tests

From the project root directory:

```bash
# Test MCP server connectivity
python3 tests/test_mcp_usage.py
python3 tests/simple_mcp_test.py

# Test specific MCP server
python3 tests/test_mcp_usage.py "AWS EKS"

# Test both agents manually
python3 agent.py        # Full-featured agent (21 tools)
python3 fast_agent.py   # Ultra-fast agent (instant responses)
```

## Test Requirements

- All dependencies from `requirements.txt` installed
- AWS credentials configured
- `uv`/`uvx` installed for MCP server execution
- Internet connectivity for MCP server downloads