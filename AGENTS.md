# Agent Development Guide

This guide provides essential information for AI coding agents working with this codebase.

## Build/Lint/Test Commands

### Running Tests
```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_extraction.py

# Run a specific test class
pytest tests/test_extraction.py::TestEntityModels

# Run a specific test method
pytest tests/test_extraction.py::TestEntityModels::test_entity_creation

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run tests in verbose mode
pytest -v
```

### Linting and Formatting
```bash
# Check for syntax errors
python -m py_compile src/doc_analysis/extraction/entity_extractor.py

# Run static analysis (if pylint/flake8 installed)
# pylint src/doc_analysis
# flake8 src/doc_analysis
```

### Installation
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install .

# Install development dependencies
uv sync --extra dev
# or
pip install .[dev]

# Install all optional dependencies
uv sync --all-extras
# or
pip install .[dev,llm,anthropic,bedrock,huggingface,viz]
```

### Environment Management
This project uses `uv` as the package and environment manager:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Sync dependencies
uv sync

# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Run commands in the environment
uv run pytest
uv run python main.py
```

## Code Style Guidelines

### Imports
1. Standard library imports first (sorted alphabetically)
2. Third-party imports second (sorted alphabetically)
3. Local imports last (sorted alphabetically)
4. Use absolute imports when possible
5. Group imports in blocks separated by blank lines
6. Import modules, not individual functions when possible

Example:
```python
import json
import logging
from dataclasses import dataclass
from typing import Any, Optional, Protocol
from uuid import UUID

from doc_analysis.ingestion.chunker import Chunk

from .models import (
    Entity,
    EntityCategory,
    EntityMention,
    EntityType,
    ENTITY_TYPE_TO_CATEGORY,
)
```

### Formatting
1. Follow PEP 8 style guide
2. Use 4 spaces for indentation (no tabs)
3. Maximum line length: 88 characters (Black standard)
4. Use blank lines to separate logical sections
5. Put trailing commas in multiline constructs

### Type Hints
1. Use type hints for all function parameters and return values
2. Use `Optional[T]` instead of `Union[T, None]`
3. Use `list[T]` instead of `List[T]` (Python 3.9+ style)
4. Use `|` syntax for unions when appropriate (Python 3.10+)

Example:
```python
def extract_from_text(
    self,
    text: str,
    source_reference: str = "Unknown",
    start_page: int = 1,
    end_page: int = 1,
) -> ExtractionResult:
```

### Naming Conventions
1. Use `snake_case` for variables, functions, and methods
2. Use `PascalCase` for classes and enums
3. Use `UPPER_CASE` for constants
4. Use descriptive names that convey purpose
5. Private members prefixed with underscore `_private`

### Error Handling
1. Create specific exception classes for domain-specific errors
2. Include meaningful error messages
3. Log errors appropriately before raising exceptions
4. Don't catch exceptions silently unless intentionally suppressing them
5. Use context managers for resource management

Example:
```python
class EntityExtractionError(Exception):
    """Error during entity extraction."""
    pass

try:
    response = self.llm_client.complete(prompt=prompt, system=EXTRACTION_SYSTEM_PROMPT)
except Exception as e:
    raise EntityExtractionError(f"LLM API call failed: {e}") from e
```

### Documentation
1. Use Google-style docstrings for modules, classes, and functions
2. Include type information in docstrings
3. Document all public APIs
4. Include examples for complex functions when helpful

Example:
```python
def extract(self, chunks: list[Chunk]) -> ExtractionResult:
    """Extract entities from a list of document chunks.

    Args:
        chunks: List of document chunks to process.

    Returns:
        ExtractionResult containing all extracted entities.
    """
```

### Data Classes
1. Use `@dataclass` for simple data containers
2. Use `field(default_factory=list)` for mutable defaults
3. Add properties for computed values
4. Implement `__post_init__` for validation if needed

### Constants
1. Define constants in separate files when they are used across modules
2. Use UPPER_CASE naming for constants
3. Group related constants logically
4. Include docstrings for complex constants

## Project Structure

```
src/doc_analysis/
├── __init__.py
├── extraction/          # Entity extraction logic
│   ├── __init__.py
│   ├── constants.py     # Shared constants
│   ├── entity_extractor.py  # Main extraction logic
│   ├── llm_clients.py   # LLM client interfaces
│   └── models.py        # Data models
├── ingestion/           # Document parsing and chunking
├── models/              # Core data structures
└── visualization/       # Visualization tools
```

## Testing Guidelines

1. Place test files in the `tests/` directory
2. Match the source structure in tests (e.g., `tests/test_extraction.py` for `src/doc_analysis/extraction/`)
3. Use descriptive test class and method names
4. Follow Arrange-Act-Assert pattern
5. Test edge cases and error conditions
6. Use pytest fixtures for setup/teardown
7. Mock external dependencies

## Domain Concepts

This is an Environmental Safety Analysis Platform that processes safety assessment documents to extract entities in a specific taxonomy:

1. Hazards: Chemical, physical, biological, process
2. Receptors: Human, ecological, environmental media, infrastructure
3. Pathways: Transport mechanisms, exposure routes
4. Controls: Engineered, administrative, natural attenuation
5. Contextual: Locations, timeframes, conditions, regulations

Entities are extracted with confidence scores and linked back to source passages for traceability.