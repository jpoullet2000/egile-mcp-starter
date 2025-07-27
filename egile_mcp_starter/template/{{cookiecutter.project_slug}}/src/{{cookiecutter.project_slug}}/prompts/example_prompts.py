"""Example prompts for {{ cookiecutter.project_name }}.

This module contains example prompt implementations to demonstrate how to create
MCP prompts using the FASTMCP framework.

{% if cookiecutter.include_examples == "y" -%}
These examples are included in your project to help you get started.
{% else -%}
Example prompts are not included in this configuration.
{% endif %}
"""

import logging
from typing import Dict, List, Any
from fastmcp import FastMCP

logger = logging.getLogger(__name__)


def register_example_prompts(server: FastMCP) -> None:
    """Register example prompts with the MCP server.

    Args:
        server: FastMCP server instance
    """

    @server.prompt("code_review")
    async def code_review_prompt(code: str, language: str = "python") -> str:
        """Generate a prompt for conducting code reviews.

        Args:
            code: The code to review
            language: Programming language of the code (default: python)

        Returns:
            Formatted prompt for code review
        """
        logger.info(f"Code review prompt requested for {language} code")

        prompt = f"""Please conduct a thorough code review of the following {language} code:

```{language}
{code}
```

Please analyze the code for:

1. **Code Quality & Style**
   - Adherence to coding standards and best practices
   - Code readability and maintainability
   - Proper naming conventions
   - Code organization and structure

2. **Functionality & Logic**
   - Correctness of the implementation
   - Edge cases and error handling
   - Algorithm efficiency
   - Potential bugs or issues

3. **Security & Performance**
   - Security vulnerabilities
   - Performance bottlenecks
   - Resource usage optimization
   - Memory management (if applicable)

4. **Testing & Documentation**
   - Test coverage considerations
   - Code documentation quality
   - Comments and docstrings
   - API design (if applicable)

5. **Recommendations**
   - Specific improvements
   - Refactoring suggestions
   - Best practice recommendations
   - Alternative approaches

Please provide detailed feedback with specific examples and actionable suggestions for improvement."""

        return prompt

    @server.prompt("explain_code")
    async def explain_code_prompt(code: str, detail_level: str = "detailed") -> str:
        """Generate a prompt for explaining code functionality.

        Args:
            code: The code to explain
            detail_level: Level of detail (basic, detailed, expert)

        Returns:
            Formatted prompt for code explanation
        """
        logger.info(f"Code explanation prompt requested with {detail_level} level")

        detail_instructions = {
            "basic": "Provide a high-level overview focusing on what the code does and its main purpose.",
            "detailed": "Provide a comprehensive explanation including how the code works, key components, and flow.",
            "expert": "Provide an in-depth technical analysis including implementation details, design patterns, and architectural considerations.",
        }

        instruction = detail_instructions.get(
            detail_level, detail_instructions["detailed"]
        )

        prompt = f"""Please explain the following code in detail:

```
{code}
```

{instruction}

Please structure your explanation to include:

1. **Purpose & Overview**
   - What the code is designed to do
   - Main functionality and goals
   - Context and use cases

2. **Code Structure & Flow**
   - High-level organization
   - Execution flow and logic
   - Key components and their roles

3. **Implementation Details**
   - Important functions, classes, or methods
   - Data structures and variables
   - Algorithms and techniques used

4. **Dependencies & Requirements**
   - External libraries or modules
   - System requirements
   - Configuration needs

5. **Usage Examples**
   - How to use or call this code
   - Input/output examples
   - Integration considerations

Make the explanation clear and accessible while maintaining technical accuracy."""

        return prompt

    @server.prompt("debug_help")
    async def debug_help_prompt(error_message: str, code_context: str = "") -> str:
        """Generate a prompt for debugging assistance.

        Args:
            error_message: The error message or issue description
            code_context: Relevant code context where the error occurs

        Returns:
            Formatted prompt for debugging help
        """
        logger.info("Debug help prompt requested")

        context_section = ""
        if code_context:
            context_section = f"""

**Relevant Code Context:**
```
{code_context}
```"""

        prompt = f"""I'm encountering an issue and need debugging assistance:

**Error/Issue Description:**
{error_message}{context_section}

Please help me debug this issue by providing:

1. **Error Analysis**
   - What the error means
   - Likely causes of this type of error
   - Common scenarios where this occurs

2. **Diagnostic Steps**
   - How to investigate further
   - What information to gather
   - Debugging techniques to try

3. **Potential Solutions**
   - Step-by-step fixing approaches
   - Code changes or corrections
   - Alternative implementations

4. **Prevention Strategies**
   - How to avoid similar issues in the future
   - Best practices to follow
   - Code review checkpoints

5. **Additional Resources**
   - Relevant documentation
   - Similar issues and solutions
   - Tools that might help

Please provide practical, actionable advice with specific examples where possible."""

        return prompt

    @server.prompt("api_documentation")
    async def api_documentation_prompt(
        function_signature: str, description: str = ""
    ) -> str:
        """Generate a prompt for creating API documentation.

        Args:
            function_signature: The function or API signature
            description: Optional description of the API's purpose

        Returns:
            Formatted prompt for API documentation
        """
        logger.info("API documentation prompt requested")

        desc_section = ""
        if description:
            desc_section = f"""

**Initial Description:**
{description}"""

        prompt = f"""Please create comprehensive API documentation for the following:

**Function/API Signature:**
```
{function_signature}
```{desc_section}

Please generate documentation that includes:

1. **Overview**
   - Clear, concise description of what the API does
   - Primary use cases and purpose
   - When and why to use this API

2. **Parameters**
   - Detailed description of each parameter
   - Data types and formats
   - Required vs optional parameters
   - Default values and acceptable ranges
   - Parameter validation rules

3. **Return Values**
   - Description of return data
   - Return types and formats
   - Possible return states
   - Error return conditions

4. **Usage Examples**
   - Basic usage example
   - Advanced usage scenarios
   - Common patterns and best practices
   - Integration examples

5. **Error Handling**
   - Possible error conditions
   - Error codes and messages
   - How to handle different error types
   - Recovery strategies

6. **Notes & Considerations**
   - Performance implications
   - Security considerations
   - Compatibility requirements
   - Rate limiting or usage restrictions
   - Related APIs or alternatives

Format the documentation clearly with proper headings, code examples, and explanations suitable for developers."""

        return prompt

    logger.info("Example prompts registered successfully")
