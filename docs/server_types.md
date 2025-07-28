# Server Types

egile-mcp-starter supports four different server types, each optimized for specific use cases. This guide explains each type and helps you choose the right one for your project.

## Overview

| Server Type | Tools | Resources | Prompts | Use Case |
|-------------|-------|-----------|---------|----------|
| `tools` | ✅ | ❌ | ❌ | Function calling, API integrations |
| `resources` | ❌ | ✅ | ❌ | Data access, file systems |
| `prompts` | ❌ | ❌ | ✅ | AI guidance, templates |
| `full` | ✅ | ✅ | ✅ | Comprehensive servers |

## Tools Server

### Description

A tools server provides functions that AI systems can call to perform actions or retrieve data. This is ideal for integrating with APIs, processing data, or performing calculations.

### When to Use

- Building API integrations
- Creating utility functions for AI
- Implementing data processing workflows
- Providing computational capabilities

### Generated Structure

```
my_tools_server/
├── src/my_tools_server/
│   ├── tools/
│   │   ├── __init__.py
│   │   └── example_tools.py    # Example tool implementations
│   ├── server.py               # Server with tools support
│   └── config.py
└── tests/
    └── test_tools.py
```

### Example Implementation

```python
# src/my_tools_server/tools/example_tools.py
from fastmcp import FastMCP

def register_example_tools(server: FastMCP) -> None:
    """Register example tools with the MCP server."""
    
    @server.tool("calculate")
    async def calculate(expression: str) -> dict:
        """Safely evaluate a mathematical expression.
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Result of the calculation
        """
        try:
            # Safe evaluation of basic math expressions
            result = eval(expression, {"__builtins__": {}}, {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "len": len
            })
            return {"result": result, "expression": expression}
        except Exception as e:
            return {"error": str(e), "expression": expression}
    
    @server.tool("weather")
    async def get_weather(location: str) -> dict:
        """Get weather information for a location.
        
        Args:
            location: City name or coordinates
            
        Returns:
            Weather data for the location
        """
        # Implementation would call a weather API
        return {
            "location": location,
            "temperature": "22°C",
            "condition": "Sunny",
            "humidity": "45%"
        }
```

## Resources Server

### Description

A resources server provides access to data and information that AI systems can read. This includes files, databases, APIs, or any structured data sources.

### When to Use

- Providing access to databases
- Serving file system content
- Exposing data feeds
- Creating content management interfaces

### Generated Structure

```
my_resources_server/
├── src/my_resources_server/
│   ├── resources/
│   │   ├── __init__.py
│   │   └── example_resources.py  # Example resource implementations
│   ├── server.py                 # Server with resources support
│   └── config.py
└── tests/
    └── test_resources.py
```

### Example Implementation

```python
# src/my_resources_server/resources/example_resources.py
from fastmcp import FastMCP
import json

def register_example_resources(server: FastMCP) -> None:
    """Register example resources with the MCP server."""
    
    @server.resource("config://settings")
    async def get_server_config() -> str:
        """Get current server configuration."""
        config_data = {
            "server_name": "My Resources Server",
            "version": "0.1.0",
            "features": ["resources"],
            "status": "running"
        }
        return json.dumps(config_data, indent=2)
    
    @server.resource("data://users")
    async def get_users_data() -> str:
        """Get user data from the system."""
        users = [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "user"}
        ]
        return json.dumps(users, indent=2)
    
    @server.resource("logs://recent")
    async def get_recent_logs() -> str:
        """Get recent server logs."""
        logs = [
            "2025-01-01 10:00:00 - Server started",
            "2025-01-01 10:01:00 - Resource handler registered",
            "2025-01-01 10:02:00 - Client connected"
        ]
        return "\n".join(logs)
```

## Prompts Server

### Description

A prompts server provides templates and structured prompts that AI systems can use for guidance, instruction, or conversation management.

### When to Use

- Creating prompt libraries
- Building conversation templates
- Providing AI instruction sets
- Managing prompt variations

### Generated Structure

```
my_prompts_server/
├── src/my_prompts_server/
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── example_prompts.py   # Example prompt implementations
│   ├── server.py                # Server with prompts support
│   └── config.py
└── tests/
    └── test_prompts.py
```

### Example Implementation

```python
# src/my_prompts_server/prompts/example_prompts.py
from fastmcp import FastMCP

def register_example_prompts(server: FastMCP) -> None:
    """Register example prompts with the MCP server."""
    
    @server.prompt("code_review")
    async def code_review_prompt(language: str = "python", style: str = "detailed") -> str:
        """Generate a code review prompt.
        
        Args:
            language: Programming language to review
            style: Review style (brief, detailed, security-focused)
            
        Returns:
            Formatted prompt for code review
        """
        base_prompt = f"""Please review the following {language} code and provide feedback on:

1. Code quality and best practices
2. Potential bugs or issues
3. Performance considerations
4. Security concerns
5. Suggestions for improvement
"""
        
        if style == "brief":
            return base_prompt + "\nPlease keep your review concise and focus on critical issues."
        elif style == "security-focused":
            return base_prompt + "\nPay special attention to security vulnerabilities and potential exploits."
        else:
            return base_prompt + "\nPlease provide detailed explanations for your recommendations."
    
    @server.prompt("data_analysis")
    async def data_analysis_prompt(data_type: str, goal: str) -> str:
        """Generate a data analysis prompt.
        
        Args:
            data_type: Type of data to analyze
            goal: Analysis objective
            
        Returns:
            Formatted prompt for data analysis
        """
        return f"""Analyze the following {data_type} data with the goal of {goal}.

Please provide:
1. Summary of the data structure and key characteristics
2. Relevant statistical insights
3. Patterns, trends, or anomalies identified
4. Recommendations based on the analysis
5. Suggested next steps

Present your analysis in a clear, structured format with supporting evidence."""
```

## Full Server

### Description

A full server combines all three capabilities (tools, resources, and prompts) into a comprehensive MCP server. This provides maximum flexibility and functionality.

### When to Use

- Building complex AI assistants
- Creating comprehensive integrations
- Developing multi-purpose servers
- When you need all MCP capabilities

### Generated Structure

```
my_full_server/
├── src/my_full_server/
│   ├── tools/
│   │   ├── __init__.py
│   │   └── example_tools.py     # Tool implementations
│   ├── resources/
│   │   ├── __init__.py
│   │   └── example_resources.py # Resource implementations
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── example_prompts.py   # Prompt implementations
│   ├── server.py                # Server with all capabilities
│   └── config.py
└── tests/
    ├── test_tools.py
    ├── test_resources.py
    └── test_prompts.py
```

### Configuration Options

Full servers support configuration toggles to enable/disable specific capabilities:

```yaml
# config.yaml
server:
  enable_tools: true
  enable_resources: true
  enable_prompts: true
```

## Choosing the Right Server Type

### Decision Matrix

| Requirement | Tools | Resources | Prompts | Full |
|-------------|-------|-----------|---------|------|
| Execute functions | ✅ | ❌ | ❌ | ✅ |
| Access data | ❌ | ✅ | ❌ | ✅ |
| Provide templates | ❌ | ❌ | ✅ | ✅ |
| Simple deployment | ✅ | ✅ | ✅ | ❌ |
| Maximum flexibility | ❌ | ❌ | ❌ | ✅ |
| Focused purpose | ✅ | ✅ | ✅ | ❌ |

### Recommendations

**Choose `tools` when:**
- You need to integrate with external APIs
- Your focus is on performing actions
- You want to provide computational capabilities
- Simplicity and performance are priorities

**Choose `resources` when:**
- You need to provide data access
- Your focus is on information retrieval
- You're building a data gateway
- You want read-only AI interactions

**Choose `prompts` when:**
- You're building a prompt library
- Your focus is on AI guidance
- You need conversation templates
- You want to manage AI instructions

**Choose `full` when:**
- You need comprehensive AI capabilities
- You're building a complex assistant
- Requirements may evolve over time
- Maximum flexibility is important

## Migration Between Types

You can migrate between server types by:

1. **Generating a new project** with the desired type
2. **Copying your implementations** to the new structure
3. **Updating configuration** to match the new type
4. **Adjusting tests** for the new capabilities

The template structure is designed to make this process straightforward.
