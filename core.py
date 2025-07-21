"""Core classes for the Duplicate Code Detection Tool library.

This module provides high-level classes for easy integration
of duplicate code detection functionality into other projects.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .duplicate_code_detection import (
    ReturnCode,
    get_all_source_code_from_directory,
    get_loc_count,
    remove_comments_and_docstrings,
    run,
)

logger = logging.getLogger(__name__)


@dataclass
class FileSimilarity:
    """Represents similarity between two files."""

    source_file: str
    target_file: str
    similarity_percentage: float
    source_loc: int | None = None
    target_loc: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "source_file": self.source_file,
            "target_file": self.target_file,
            "similarity_percentage": self.similarity_percentage,
            "source_loc": self.source_loc,
            "target_loc": self.target_loc,
        }


@dataclass
class SimilarityReport:
    """Represents a complete similarity report for a file."""

    file_path: str
    similarities: list[FileSimilarity] = field(default_factory=list)
    loc_count: int | None = None

    def add_similarity(self, similarity: FileSimilarity) -> None:
        """Add a similarity to the report."""
        self.similarities.append(similarity)

    def get_high_similarities(self, threshold: float = 30.0) -> list[FileSimilarity]:
        """Get similarities above a threshold."""
        return [s for s in self.similarities if s.similarity_percentage >= threshold]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "file_path": self.file_path,
            "loc_count": self.loc_count,
            "similarities": [s.to_dict() for s in self.similarities],
        }


@dataclass
class DetectionResult:
    """Result of a duplicate code detection run."""

    return_code: ReturnCode
    reports: list[SimilarityReport] = field(default_factory=list)
    raw_data: dict[str, Any] = field(default_factory=dict)

    def is_success(self) -> bool:
        """Check if detection was successful."""
        return self.return_code == ReturnCode.SUCCESS

    def has_duplications(self) -> bool:
        """Check if any duplications were found."""
        return len(self.reports) > 0

    def get_critical_duplications(
        self, threshold: float = 50.0
    ) -> list[FileSimilarity]:
        """Get critical duplications above threshold."""
        critical = []
        for report in self.reports:
            for similarity in report.get_high_similarities(threshold):
                critical.append(similarity)
        return critical

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "return_code": self.return_code.value,
            "success": self.is_success(),
            "has_duplications": self.has_duplications(),
            "reports": [r.to_dict() for r in self.reports],
            "raw_data": self.raw_data,
        }


class DuplicateCodeDetector:
    """High-level class for detecting duplicate code.

    This class provides an easy-to-use interface for detecting
    code duplications across files and directories.
    """

    def __init__(
        self,
        fail_threshold: int = 100,
        ignore_threshold: int = 15,
        file_extensions: list[str] | None = None,
        only_code: bool = False,
        show_loc: bool = True,
    ):
        """Initialize the detector.

        Args:
            fail_threshold: Maximum allowed similarity before error
            ignore_threshold: Don't report similarities below this threshold
            file_extensions: File extensions to analyze (default: common source code)
            only_code: Remove comments and docstrings before analysis
            show_loc: Include line count information

        """
        self.fail_threshold = fail_threshold
        self.ignore_threshold = ignore_threshold
        self.file_extensions = file_extensions or [
            "py",
            "js",
            "ts",
            "java",
            "cpp",
            "c",
            "h",
        ]
        self.only_code = only_code
        self.show_loc = show_loc

    def detect_in_directories(
        self,
        directories: list[str],
        ignore_directories: list[str] | None = None,
        ignore_files: list[str] | None = None,
        project_root_dir: str = "",
    ) -> DetectionResult:
        """Detect duplications in directories.

        Args:
            directories: List of directories to analyze
            ignore_directories: Directories to ignore
            ignore_files: Files to ignore
            project_root_dir: Project root for relative paths

        Returns:
            DetectionResult with analysis results

        """
        ignore_directories = ignore_directories or []
        ignore_files = ignore_files or []

        return_code, raw_data = run(
            fail_threshold=self.fail_threshold,
            directories=directories,
            files=None,
            ignore_directories=ignore_directories,
            ignore_files=ignore_files,
            json_output=True,
            project_root_dir=project_root_dir,
            file_extensions=self.file_extensions,
            ignore_threshold=self.ignore_threshold,
            only_code=self.only_code,
            csv_output="",
            show_loc=self.show_loc,
        )

        return self._process_result(return_code, raw_data)

    def detect_in_files(
        self,
        files: list[str],
        ignore_files: list[str] | None = None,
        project_root_dir: str = "",
    ) -> DetectionResult:
        """Detect duplications in specific files.

        Args:
            files: List of files to analyze
            ignore_files: Files to ignore
            project_root_dir: Project root for relative paths

        Returns:
            DetectionResult with analysis results

        """
        ignore_files = ignore_files or []

        return_code, raw_data = run(
            fail_threshold=self.fail_threshold,
            directories=None,
            files=files,
            ignore_directories=[],
            ignore_files=ignore_files,
            json_output=True,
            project_root_dir=project_root_dir,
            file_extensions=self.file_extensions,
            ignore_threshold=self.ignore_threshold,
            only_code=self.only_code,
            csv_output="",
            show_loc=self.show_loc,
        )

        return self._process_result(return_code, raw_data)

    def _process_result(
        self, return_code: ReturnCode, raw_data: dict[str, Any]
    ) -> DetectionResult:
        """Process raw result into DetectionResult."""
        reports = []

        for file_path, similarities in raw_data.items():
            report = SimilarityReport(file_path=file_path)

            # Extract LOC count if available
            if (
                self.show_loc
                and isinstance(similarities, dict)
                and "#LoC" in similarities
            ):
                report.loc_count = similarities["#LoC"]
                similarities = {k: v for k, v in similarities.items() if k != "#LoC"}

            # Process similarities
            for target_file, similarity_data in similarities.items():
                if isinstance(similarity_data, dict):
                    # With LOC information
                    similarity = FileSimilarity(
                        source_file=file_path,
                        target_file=target_file,
                        similarity_percentage=similarity_data.get("Similarity", 0.0),
                        source_loc=report.loc_count,
                        target_loc=similarity_data.get("#LoC"),
                    )
                else:
                    # Simple similarity percentage
                    similarity = FileSimilarity(
                        source_file=file_path,
                        target_file=target_file,
                        similarity_percentage=float(similarity_data),
                        source_loc=report.loc_count,
                    )

                report.add_similarity(similarity)

            if report.similarities:
                reports.append(report)

        return DetectionResult(
            return_code=return_code,
            reports=reports,
            raw_data=raw_data,
        )

    def analyze_project(
        self,
        project_path: str,
        exclude_patterns: list[str] | None = None,
    ) -> DetectionResult:
        """Analyze an entire project for duplications.

        Args:
            project_path: Path to the project root
            exclude_patterns: Patterns to exclude (e.g., ['tests/', 'docs/'])

        Returns:
            DetectionResult with analysis results

        """
        exclude_patterns = exclude_patterns or []

        # Convert exclude patterns to ignore directories
        ignore_directories = []
        for pattern in exclude_patterns:
            if pattern.endswith("/"):
                ignore_directories.append(pattern)
            else:
                ignore_directories.append(f"{pattern}/")

        return self.detect_in_directories(
            directories=[project_path],
            ignore_directories=ignore_directories,
            project_root_dir=project_path,
        )


# Convenience functions for quick usage
def detect_duplicates_in_directories(
    directories: list[str], threshold: float = 15.0, **kwargs: Any
) -> DetectionResult:
    """Quick function to detect duplications in directories."""
    detector = DuplicateCodeDetector(ignore_threshold=int(threshold), **kwargs)
    return detector.detect_in_directories(directories)


def detect_duplicates_in_files(
    files: list[str], threshold: float = 15.0, **kwargs: Any
) -> DetectionResult:
    """Quick function to detect duplications in files."""
    detector = DuplicateCodeDetector(ignore_threshold=int(threshold), **kwargs)
    return detector.detect_in_files(files)


def analyze_project_duplicates(
    project_path: str,
    threshold: float = 15.0,
    exclude_patterns: list[str] | None = None,
    **kwargs: Any,
) -> DetectionResult:
    """Quick function to analyze project duplications."""
    detector = DuplicateCodeDetector(ignore_threshold=int(threshold), **kwargs)
    return detector.analyze_project(project_path, exclude_patterns)
