"""Example tools for {{ cookiecutter.project_name }}.

This module contains example tool implementations to demonstrate how to create
MCP tools using the FASTMCP framework.

{% if cookiecutter.include_examples == "y" -%}
These examples are included in your project to help you get started.
{% else -%}
Example tools are not included in this configuration.
{% endif %}
"""

import ast
import operator
import logging
from typing import Any, Dict
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Safe operators for mathematical expressions
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(node: ast.AST) -> float:
    """Safely evaluate a mathematical expression AST.

    Args:
        node: AST node to evaluate

    Returns:
        Result of the mathematical expression

    Raises:
        TypeError: If an unsupported operation is used
        ValueError: If the expression is invalid
    """
    if isinstance(node, ast.Constant):  # Numbers
        return node.value
    elif isinstance(node, ast.BinOp):  # Binary operations
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise TypeError(f"Unsupported operation: {type(node.op)}")
        return op(left, right)
    elif isinstance(node, ast.UnaryOp):  # Unary operations
        operand = safe_eval(node.operand)
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise TypeError(f"Unsupported operation: {type(node.op)}")
        return op(operand)
    else:
        raise TypeError(f"Unsupported AST node: {type(node)}")


def register_example_tools(server: FastMCP) -> None:
    """Register example tools with the MCP server.

    Args:
        server: FastMCP server instance
    """

    @server.tool("echo")
    async def echo_tool(text: str) -> str:
        """Echo back the provided text.

        Args:
            text: Text to echo back

        Returns:
            The same text that was provided
        """
        logger.info(f"Echo tool called with text: {text}")
        return f"Echo: {text}"

    @server.tool("calculate")
    async def calculate_tool(expression: str) -> Dict[str, Any]:
        """Perform basic mathematical calculations.

        Args:
            expression: Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')

        Returns:
            Dictionary containing the result and expression
        """
        logger.info(f"Calculate tool called with expression: {expression}")

        try:
            # Parse the expression into an AST
            parsed = ast.parse(expression, mode="eval")

            # Safely evaluate the expression
            result = safe_eval(parsed.body)

            return {"expression": expression, "result": result, "success": True}

        except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
            logger.error(f"Error evaluating expression '{expression}': {e}")
            return {"expression": expression, "error": str(e), "success": False}

    @server.tool("get_time")
    async def get_time_tool() -> Dict[str, str]:
        """Get the current date and time.

        Returns:
            Dictionary containing current date and time information
        """
        from datetime import datetime

        now = datetime.now()

        return {
            "current_time": now.isoformat(),
            "formatted_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": str(now.astimezone().tzinfo),
            "timestamp": now.timestamp(),
        }

    @server.tool("random_number")
    async def random_number_tool(
        min_value: int = 1, max_value: int = 100
    ) -> Dict[str, Any]:
        """Generate a random number within a specified range.

        Args:
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)

        Returns:
            Dictionary containing the random number and range information
        """
        import random

        if min_value > max_value:
            min_value, max_value = max_value, min_value

        random_num = random.randint(min_value, max_value)

        return {
            "random_number": random_num,
            "min_value": min_value,
            "max_value": max_value,
            "range_size": max_value - min_value + 1,
        }

    logger.info("Example tools registered successfully")
