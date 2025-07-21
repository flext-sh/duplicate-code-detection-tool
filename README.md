# Duplicate Code Detection Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/duplicate-code-detection-tool.svg)](https://badge.fury.io/py/duplicate-code-detection-tool)

A Python library for detecting code similarities and duplications across files and directories. Enhanced with Python 3.13 compatibility and modern packaging standards.

## 🚀 Features

- **Library & CLI**: Use as a Python library or command-line tool
- **Multiple Formats**: Support for JSON, CSV, and human-readable output
- **Flexible Analysis**: Analyze directories, specific files, or entire projects
- **Modern Python**: Full support for Python 3.8+ including Python 3.13
- **Quality Assurance**: Perfect for CI/CD pipelines and code quality gates
- **Flext Integration**: Designed for seamless integration with Flext projects

## 📦 Installation

### From GitHub (Recommended for Flext projects)

```bash
pip install git+https://github.com/flext-sh/duplicate-code-detection-tool.git
```

### From PyPI

```bash
pip install duplicate-code-detection-tool
```

## 🔧 Quick Start

### As a Library

```python
from duplicate_code_tool import DuplicateCodeDetector

# Create detector with custom settings
detector = DuplicateCodeDetector(
    fail_threshold=80,      # Fail if any duplication >80%
    ignore_threshold=15,    # Ignore duplications <15%
    file_extensions=["py"], # Analyze Python files only
    only_code=True,         # Remove comments and docstrings
    show_loc=True,          # Include line count information
)

# Analyze a project
result = detector.analyze_project(
    project_path=".",
    exclude_patterns=["tests/", "docs/", ".git/"]
)

# Check results
if result.has_duplications():
    print(f"Found {len(result.reports)} files with duplications")
    
    # Get critical duplications
    critical = result.get_critical_duplications(threshold=50.0)
    for dup in critical:
        print(f"🚨 {dup.source_file} ↔ {dup.target_file} ({dup.similarity_percentage:.1f}%)")
```

### Quick Functions

```python
from duplicate_code_tool import analyze_project_duplicates

# Simple project analysis
result = analyze_project_duplicates(
    project_path=".",
    threshold=20.0,
    exclude_patterns=["tests/", "docs/"]
)

print(f"Success: {result.is_success()}")
print(f"Duplications found: {result.has_duplications()}")
```

### As a Command Line Tool

```bash
# Analyze directories
duplicate-code-detection -d src/ lib/ --ignore-threshold 15

# Analyze specific files
duplicate-code-detection -f file1.py file2.py file3.py

# JSON output for CI/CD
duplicate-code-detection -d src/ -j --fail-threshold 80

# CSV output
duplicate-code-detection -d src/ --csv-output report.csv --show-loc
```

## 🎯 Flext Integration Examples

### CI/CD Pipeline Integration

```python
from duplicate_code_tool import DuplicateCodeDetector
import sys

def check_code_quality():
    """Quality gate for Flext CI/CD pipeline."""
    detector = DuplicateCodeDetector(
        fail_threshold=70,  # Fail if any duplication >70%
        ignore_threshold=20, # Ignore duplications <20%
        file_extensions=["py", "js", "ts"],
        only_code=True,
    )
    
    # Analyze Flext modules
    result = detector.detect_in_directories([
        "flext-core/src",
        "flext-ldap/src", 
        "flext-grpc/src",
    ], ignore_directories=["tests/", "__pycache__/"])
    
    if not result.is_success():
        print("❌ Code duplication threshold exceeded!")
        for dup in result.get_critical_duplications(50.0):
            print(f"   {dup.source_file} ↔ {dup.target_file}")
        sys.exit(1)
    
    print("✅ Code quality check passed!")

if __name__ == "__main__":
    check_code_quality()
```

### Pre-commit Hook

```python
#!/usr/bin/env python3
"""Pre-commit hook for duplicate code detection."""

import sys
from pathlib import Path
from duplicate_code_tool import DuplicateCodeDetector

def main():
    # Get staged files
    staged_files = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if not staged_files:
        return 0
    
    # Filter Python files
    python_files = [f for f in staged_files if f.endswith('.py')]
    
    if not python_files:
        return 0
    
    # Check for duplications
    detector = DuplicateCodeDetector(
        fail_threshold=100,  # Don't fail, just warn
        ignore_threshold=30, # Only report significant duplications
        only_code=True,
    )
    
    result = detector.detect_in_files(python_files)
    
    if result.has_duplications():
        print("⚠️  Potential code duplications detected:")
        for dup in result.get_critical_duplications(40.0):
            print(f"   {dup.source_file} ↔ {dup.target_file} ({dup.similarity_percentage:.1f}%)")
        print("💡 Consider refactoring to reduce code duplication.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## 📊 Advanced Usage

### Custom Analysis

```python
from duplicate_code_tool import DuplicateCodeDetector

detector = DuplicateCodeDetector(
    fail_threshold=60,
    ignore_threshold=25,
    file_extensions=["py", "js", "ts", "java"],
    only_code=True,
    show_loc=True,
)

# Analyze specific directories
result = detector.detect_in_directories(
    directories=["src/", "lib/"],
    ignore_directories=["tests/", "docs/", "node_modules/"],
    project_root_dir=".",
)

# Generate detailed report
if result.has_duplications():
    report_data = result.to_dict()
    
    # Save to JSON
    with open("duplication_report.json", "w") as f:
        f.write(result.to_json(indent=2))
    
    # Print summary
    print(f"📊 Analysis Summary:")
    print(f"   Files analyzed: {len(result.reports)}")
    print(f"   Critical duplications (>50%): {len(result.get_critical_duplications(50.0))}")
    print(f"   High duplications (>30%): {len(result.get_critical_duplications(30.0))}")
```

### Batch Processing

```python
from duplicate_code_tool import analyze_project_duplicates
from pathlib import Path

def analyze_multiple_projects(project_paths: list[str]):
    """Analyze multiple projects and generate reports."""
    results = {}
    
    for project_path in project_paths:
        if Path(project_path).exists():
            print(f"🔍 Analyzing {project_path}...")
            
            result = analyze_project_duplicates(
                project_path=project_path,
                threshold=20.0,
                exclude_patterns=["tests/", "docs/", ".git/", "node_modules/"]
            )
            
            results[project_path] = result
            
            if result.has_duplications():
                print(f"   ⚠️  Found {len(result.reports)} files with duplications")
            else:
                print(f"   ✅ No significant duplications found")
    
    return results

# Usage
projects = ["flext-core", "flext-ldap", "flext-grpc"]
results = analyze_multiple_projects(projects)
```

## 🛠️ Configuration

### Detector Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fail_threshold` | int | 100 | Maximum allowed similarity before error |
| `ignore_threshold` | int | 15 | Don't report similarities below this threshold |
| `file_extensions` | list | `["py", "js", "ts", "java", "cpp", "c", "h"]` | File extensions to analyze |
| `only_code` | bool | False | Remove comments and docstrings before analysis |
| `show_loc` | bool | True | Include line count information |

### Output Formats

The library supports multiple output formats:

- **DetectionResult**: Structured Python objects
- **JSON**: Machine-readable format for CI/CD
- **CSV**: Spreadsheet-compatible format
- **Console**: Human-readable colored output

## 🔗 API Reference

### Main Classes

#### `DuplicateCodeDetector`

Main class for detecting code duplications.

```python
detector = DuplicateCodeDetector(
    fail_threshold=80,
    ignore_threshold=15,
    file_extensions=["py"],
    only_code=True,
    show_loc=True,
)
```

**Methods:**
- `analyze_project(project_path, exclude_patterns=None)` → `DetectionResult`
- `detect_in_directories(directories, ignore_directories=None, ignore_files=None, project_root_dir="")` → `DetectionResult`
- `detect_in_files(files, ignore_files=None, project_root_dir="")` → `DetectionResult`

#### `DetectionResult`

Result of a duplicate code detection run.

**Properties:**
- `return_code`: ReturnCode enum value
- `reports`: List of SimilarityReport objects
- `raw_data`: Raw similarity data

**Methods:**
- `is_success()` → `bool`
- `has_duplications()` → `bool`
- `get_critical_duplications(threshold=50.0)` → `List[FileSimilarity]`
- `to_json(indent=2)` → `str`
- `to_dict()` → `Dict[str, Any]`

#### `SimilarityReport`

Report for a single file's similarities.

**Properties:**
- `file_path`: Path to the analyzed file
- `similarities`: List of FileSimilarity objects
- `loc_count`: Lines of code count

#### `FileSimilarity`

Represents similarity between two files.

**Properties:**
- `source_file`: Path to source file
- `target_file`: Path to target file
- `similarity_percentage`: Similarity percentage (0-100)
- `source_loc`: Lines of code in source file
- `target_loc`: Lines of code in target file

### Quick Functions

- `analyze_project_duplicates(project_path, threshold=15.0, exclude_patterns=None, **kwargs)` → `DetectionResult`
- `detect_duplicates_in_directories(directories, threshold=15.0, **kwargs)` → `DetectionResult`
- `detect_duplicates_in_files(files, threshold=15.0, **kwargs)` → `DetectionResult`

## 🧪 Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=duplicate_code_tool

# Format code
black duplicate_code_tool/

# Type checking
mypy duplicate_code_tool/
```

## 📝 Examples

See the `examples/` directory for complete working examples:

- `flext_integration_example.py`: Comprehensive Flext integration examples
- Basic usage patterns
- CI/CD integration
- Custom analysis scenarios

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original work by [platisd/duplicate-code-detection-tool](https://github.com/platisd/duplicate-code-detection-tool)
- Enhanced and adapted for Flext projects
- Python 3.13 compatibility improvements
- Modern packaging and documentation standards

---

**Made with ❤️ for the Flext community**
