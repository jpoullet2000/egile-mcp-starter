"""Test the plugin system functionality."""

import tempfile
from pathlib import Path

import pytest

from egile_mcp_starter.generator import MCPProjectGenerator
from egile_mcp_starter.plugins.base import TemplatePlugin
from egile_mcp_starter.plugins.builtin.mcp_template import MCPTemplatePlugin
from egile_mcp_starter.plugins.builtin.rag_template import RAGTemplatePlugin
from egile_mcp_starter.plugins.registry import TemplateRegistry, get_registry


class TestTemplatePlugin:
    """Test the base TemplatePlugin class."""

    def test_template_plugin_interface(self):
        """Test that TemplatePlugin defines the correct interface."""
        # Check that TemplatePlugin is abstract and cannot be instantiated
        with pytest.raises(TypeError):
            TemplatePlugin("test", "Test template")

    def test_template_plugin_inheritance(self):
        """Test that built-in plugins properly inherit from TemplatePlugin."""
        mcp_plugin = MCPTemplatePlugin()
        rag_plugin = RAGTemplatePlugin()

        assert isinstance(mcp_plugin, TemplatePlugin)
        assert isinstance(rag_plugin, TemplatePlugin)


class TestTemplateRegistry:
    """Test the template registry functionality."""

    def setup_method(self):
        """Set up a fresh registry for each test."""
        self.registry = TemplateRegistry()

    def test_registry_initialization(self):
        """Test that registry initializes with built-in templates."""
        assert len(self.registry.list_plugins()) >= 2  # At least MCP and RAG
        plugin_names = self.registry.get_plugin_names()
        assert "mcp" in plugin_names
        assert "rag" in plugin_names

    def test_get_plugin(self):
        """Test getting plugins by name."""
        mcp_plugin = self.registry.get_plugin("mcp")
        rag_plugin = self.registry.get_plugin("rag")
        nonexistent_plugin = self.registry.get_plugin("nonexistent")

        assert mcp_plugin is not None
        assert isinstance(mcp_plugin, MCPTemplatePlugin)
        assert rag_plugin is not None
        assert isinstance(rag_plugin, RAGTemplatePlugin)
        assert nonexistent_plugin is None

    def test_register_custom_plugin(self):
        """Test registering a custom plugin."""

        class TestPlugin(TemplatePlugin):
            def __init__(self):
                super().__init__("test", "Test plugin", "1.0.0")

            def get_template_path(self) -> Path:
                return Path("/tmp/test")

            def get_default_context(self) -> dict:
                return {"test": "value"}

        test_plugin = TestPlugin()
        initial_count = len(self.registry.list_plugins())

        self.registry.register(test_plugin)

        assert len(self.registry.list_plugins()) == initial_count + 1
        assert self.registry.get_plugin("test") == test_plugin

    def test_register_duplicate_plugin_raises_error(self):
        """Test that registering a plugin with duplicate name raises error."""

        class TestPlugin(TemplatePlugin):
            def __init__(self):
                super().__init__("mcp", "Duplicate MCP plugin", "1.0.0")

            def get_template_path(self) -> Path:
                return Path("/tmp/test")

            def get_default_context(self) -> dict:
                return {"test": "value"}

        test_plugin = TestPlugin()

        with pytest.raises(ValueError, match="already registered"):
            self.registry.register(test_plugin)

    def test_unregister_plugin(self):
        """Test unregistering a plugin."""
        initial_count = len(self.registry.list_plugins())

        self.registry.unregister("mcp")

        assert len(self.registry.list_plugins()) == initial_count - 1
        assert self.registry.get_plugin("mcp") is None

    def test_global_registry(self):
        """Test that get_registry returns the same instance."""
        registry1 = get_registry()
        registry2 = get_registry()

        assert registry1 is registry2


class TestMCPTemplatePlugin:
    """Test the MCP template plugin."""

    def setup_method(self):
        """Set up MCP plugin for testing."""
        self.plugin = MCPTemplatePlugin()

    def test_plugin_properties(self):
        """Test plugin basic properties."""
        assert self.plugin.name == "mcp"
        assert "MCP server" in self.plugin.description
        assert self.plugin.version == "1.0.0"

    def test_template_path(self):
        """Test that template path exists."""
        template_path = self.plugin.get_template_path()
        assert template_path.exists()
        assert (template_path / "cookiecutter.json").exists()

    def test_default_context(self):
        """Test default context has required fields."""
        context = self.plugin.get_default_context()
        required_fields = ["project_name", "author_name", "author_email"]

        for field in required_fields:
            assert field in context
            assert context[field]  # Check it's not empty

    def test_supported_features(self):
        """Test supported features list."""
        features = self.plugin.get_supported_features()
        expected_features = ["docker", "github_actions", "testing"]

        for feature in expected_features:
            assert feature in features

    def test_validate_context(self):
        """Test context validation."""
        valid_context = {
            "project_name": "Test Project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
        }
        invalid_context = {
            "project_name": "Test Project"
            # Missing required fields
        }

        assert self.plugin.validate_context(valid_context) is True
        assert self.plugin.validate_context(invalid_context) is False

    def test_pre_generate_hook(self):
        """Test pre-generation hook."""
        context = {"project_name": "Test Project"}
        modified_context = self.plugin.pre_generate_hook(context)

        assert "project_slug" in modified_context
        assert modified_context["project_slug"] == "test_project"

    def test_post_generate_hook(self):
        """Test post-generation hook (should not raise exceptions)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_path = Path(tmp_dir)
            context = {"project_name": "Test Project"}

            # Should not raise any exceptions
            self.plugin.post_generate_hook(project_path, context)


class TestRAGTemplatePlugin:
    """Test the RAG template plugin."""

    def setup_method(self):
        """Set up RAG plugin for testing."""
        self.plugin = RAGTemplatePlugin()

    def test_plugin_properties(self):
        """Test plugin basic properties."""
        assert self.plugin.name == "rag"
        assert "RAG" in self.plugin.description
        assert self.plugin.version == "1.0.0"

    def test_template_path(self):
        """Test that template path exists."""
        template_path = self.plugin.get_template_path()
        assert template_path.exists()
        assert (template_path / "cookiecutter.json").exists()

    def test_default_context(self):
        """Test default context has RAG-specific fields."""
        context = self.plugin.get_default_context()
        rag_fields = ["vector_db", "embedding_model", "chunk_strategy"]

        for field in rag_fields:
            assert field in context
            assert context[field]  # Check it's not empty

    def test_supported_features(self):
        """Test RAG-specific supported features."""
        features = self.plugin.get_supported_features()
        rag_features = ["vector_databases", "embedding_models", "semantic_search"]

        for feature in rag_features:
            assert feature in features

    def test_validate_context(self):
        """Test RAG-specific context validation."""
        valid_context_chroma = {
            "project_name": "Test RAG Project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "vector_db": "chroma",
            "embedding_model": "sentence-transformers",
        }
        valid_context_faiss = {
            "project_name": "Test RAG Project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "vector_db": "faiss",
            "embedding_model": "sentence-transformers",
        }
        invalid_vector_db = {
            "project_name": "Test RAG Project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "vector_db": "invalid_db",
            "embedding_model": "sentence-transformers",
        }
        invalid_embedding = {
            "project_name": "Test RAG Project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "vector_db": "chroma",
            "embedding_model": "invalid_model",
        }

        assert self.plugin.validate_context(valid_context_chroma) is True
        assert self.plugin.validate_context(valid_context_faiss) is True
        assert self.plugin.validate_context(invalid_vector_db) is False
        assert self.plugin.validate_context(invalid_embedding) is False

    def test_pre_generate_hook_dependencies(self):
        """Test that pre-generation hook computes dependencies correctly."""
        context_chroma = {
            "project_name": "Test RAG Project",
            "vector_db": "chroma",
            "embedding_model": "sentence-transformers",
            "pdf_processing": "y",
            "web_scraping": "y",
        }

        context_faiss = {
            "project_name": "Test RAG Project",
            "vector_db": "faiss",
            "embedding_model": "sentence-transformers",
            "pdf_processing": "y",
            "web_scraping": "y",
        }

        # Test Chroma dependencies
        modified_context = self.plugin.pre_generate_hook(context_chroma)
        dependencies = modified_context["_computed_dependencies"]

        # Check base dependencies
        assert "fastmcp" in dependencies
        assert "pydantic" in dependencies

        # Check vector DB specific dependencies
        assert "chromadb" in dependencies

        # Check embedding model dependencies
        assert "sentence-transformers" in dependencies

        # Check optional feature dependencies
        assert "pypdf2" in dependencies  # PDF processing
        assert "requests" in dependencies  # Web scraping

        # Test FAISS dependencies
        modified_context_faiss = self.plugin.pre_generate_hook(context_faiss)
        dependencies_faiss = modified_context_faiss["_computed_dependencies"]

        # Check base dependencies
        assert "fastmcp" in dependencies_faiss
        assert "pydantic" in dependencies_faiss

        # Check FAISS-specific dependencies
        assert "faiss-cpu" in dependencies_faiss
        assert "numpy" in dependencies_faiss

        # Check embedding model dependencies
        assert "sentence-transformers" in dependencies_faiss


class TestGeneratorWithPlugins:
    """Test the generator with plugin system integration."""

    def test_generator_with_template_parameter(self):
        """Test generator accepts template parameter."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Test MCP template
            mcp_generator = MCPProjectGenerator(
                output_dir=tmp_dir, template="mcp", no_input=True
            )
            assert mcp_generator.template_name == "mcp"

            # Test RAG template
            rag_generator = MCPProjectGenerator(
                output_dir=tmp_dir, template="rag", no_input=True
            )
            assert rag_generator.template_name == "rag"

    def test_generator_with_invalid_template(self):
        """Test generator raises error with invalid template."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with pytest.raises(ValueError, match="Template 'invalid' not found"):
                MCPProjectGenerator(output_dir=tmp_dir, template="invalid")

    def test_list_available_templates(self):
        """Test generator can list available templates."""
        generator = MCPProjectGenerator(template="mcp")
        templates = generator.list_available_templates()

        assert "mcp" in templates
        assert "rag" in templates
        assert len(templates) >= 2

    def test_get_default_context_from_plugin(self):
        """Test generator gets default context from plugin."""
        mcp_generator = MCPProjectGenerator(template="mcp")
        rag_generator = MCPProjectGenerator(template="rag")

        mcp_context = mcp_generator.get_default_context()
        rag_context = rag_generator.get_default_context()

        # MCP should have server_type, RAG should have vector_db
        assert "server_type" in mcp_context
        assert "vector_db" in rag_context


class TestPluginSystemIntegration:
    """Integration tests for the entire plugin system."""

    def test_plugin_discovery(self):
        """Test that plugins are automatically discovered."""
        registry = get_registry()
        plugins = registry.list_plugins()

        # Should have at least MCP and RAG templates
        assert len(plugins) >= 2

        plugin_names = [p.name for p in plugins]
        assert "mcp" in plugin_names
        assert "rag" in plugin_names

    def test_end_to_end_plugin_workflow(self):
        """Test complete workflow from plugin selection to context generation."""
        registry = get_registry()

        # Get a plugin
        plugin = registry.get_plugin("rag")
        assert plugin is not None

        # Get default context
        context = plugin.get_default_context()
        assert context is not None

        # Validate context
        assert plugin.validate_context(context) is True

        # Apply pre-generation hook
        modified_context = plugin.pre_generate_hook(context)
        assert "_computed_dependencies" in modified_context

        # Get template path
        template_path = plugin.get_template_path()
        assert template_path.exists()

    @pytest.mark.skipif(
        not Path("egile_mcp_starter/template").exists(),
        reason="Original template directory not found",
    )
    def test_backward_compatibility(self):
        """Test that original template still works through plugin system."""
        registry = get_registry()
        mcp_plugin = registry.get_plugin("mcp")

        # Should use the original template directory
        template_path = mcp_plugin.get_template_path()
        assert template_path.name == "template"
        assert (template_path / "cookiecutter.json").exists()
