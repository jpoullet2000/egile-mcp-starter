"""Test the CLI functionality."""

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from egile_mcp_starter.cli import main


class TestCLI:
    """Test the command line interface."""

    def test_cli_help(self):
        """Test CLI help output."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Generate a new MCP server project" in result.output
        assert "--output-dir" in result.output
        assert "--no-input" in result.output
        assert "--verbose" in result.output

    @patch("egile_mcp_starter.cli.MCPProjectGenerator")
    def test_cli_default_execution(self, mock_generator_class):
        """Test CLI with default parameters."""
        mock_generator = MagicMock()
        mock_generator.generate.return_value = "/tmp/test-project"
        mock_generator_class.return_value = mock_generator

        runner = CliRunner()
        result = runner.invoke(main, [])

        assert result.exit_code == 0
        mock_generator_class.assert_called_once_with(
            output_dir=".",
            no_input=False,
            config_file=None,
            default_config=False,
            verbose=False,
            template="mcp",  # Added template parameter
        )
        mock_generator.generate.assert_called_once()

    @patch("egile_mcp_starter.cli.MCPProjectGenerator")
    def test_cli_with_options(self, mock_generator_class):
        """Test CLI with various options."""
        mock_generator = MagicMock()
        mock_generator.generate.return_value = "/tmp/test-project"
        mock_generator_class.return_value = mock_generator

        runner = CliRunner()
        result = runner.invoke(
            main, ["--output-dir", "/tmp", "--no-input", "--verbose"]
        )

        assert result.exit_code == 0
        mock_generator_class.assert_called_once_with(
            output_dir="/tmp",
            no_input=True,
            config_file=None,
            default_config=False,
            verbose=True,
            template="mcp",  # Added template parameter
        )

    @patch("egile_mcp_starter.cli.MCPProjectGenerator")
    def test_cli_verbose_output(self, mock_generator_class):
        """Test CLI verbose output."""
        mock_generator = MagicMock()
        mock_generator.generate.return_value = "/tmp/test-project"
        mock_generator_class.return_value = mock_generator

        runner = CliRunner()
        result = runner.invoke(main, ["--verbose"])

        assert result.exit_code == 0
        assert "MCP server project generated successfully" in result.output
        assert "Next steps:" in result.output
        assert "cd test-project" in result.output  # Fixed to use project name only
        assert "pip install -e ." in result.output

    @patch("egile_mcp_starter.cli.MCPProjectGenerator")
    def test_cli_error_handling(self, mock_generator_class):
        """Test CLI error handling."""
        mock_generator = MagicMock()
        mock_generator.generate.side_effect = Exception("Test error")
        mock_generator_class.return_value = mock_generator

        runner = CliRunner()
        result = runner.invoke(main, ["--verbose"])

        print(f"Exit code: {result.exit_code}")
        print(f"Output: {result.output}")
        print(f"Exception: {result.exception}")

        assert result.exit_code == 1
        assert "❌ Error: Test error" in result.output

    @patch("egile_mcp_starter.cli.MCPProjectGenerator")
    def test_cli_with_config_file(self, mock_generator_class):
        """Test CLI with config file option."""
        mock_generator = MagicMock()
        mock_generator.generate.return_value = "/tmp/test-project"
        mock_generator_class.return_value = mock_generator

        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create a dummy config file
            with open("test-config.yaml", "w") as f:
                f.write("test: config")

            result = runner.invoke(main, ["--config-file", "test-config.yaml"])

            assert result.exit_code == 0
            mock_generator_class.assert_called_once_with(
                output_dir=".",
                no_input=False,
                config_file="test-config.yaml",
                default_config=False,
                verbose=False,
                template="mcp",  # Added template parameter
            )
