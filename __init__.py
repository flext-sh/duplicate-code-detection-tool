"""Duplicate Code Detection Tool - Flext Integration

A Python library for detecting code similarities and duplications across files and directories.
Enhanced with Python 3.13 compatibility and NumPy 2.0 support.

Author: Flext Team
License: MIT
"""

from .core import (
    DetectionResult,
    DuplicateCodeDetector,
    FileSimilarity,
    SimilarityReport,
)
from .duplicate_code_detection import (
    ReturnCode,
    get_all_source_code_from_directory,
    get_loc_count,
    remove_comments_and_docstrings,
    run,
)

__version__ = "2.0.0"
__author__ = "Flext Team"
__email__ = "team@flext.dev"

__all__ = [
    # Core functions
    "run",
    "ReturnCode",
    "get_all_source_code_from_directory",
    "remove_comments_and_docstrings",
    "get_loc_count",
    # New library classes
    "DuplicateCodeDetector",
    "DetectionResult",
    "SimilarityReport",
    "FileSimilarity",
]
