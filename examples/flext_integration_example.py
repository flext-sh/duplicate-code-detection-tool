#!/usr/bin/env python3
"""Example of using the Duplicate Code Detection Tool as a library in Flext projects.

This example demonstrates how to integrate the duplicate code detection
functionality into Flext projects for automated code quality analysis.
"""

import json
import sys
from pathlib import Path

# Add the parent directory to the path to import the library
sys.path.insert(0, str(Path(__file__).parent.parent))

from duplicate_code_tool import (
    DuplicateCodeDetector,
    analyze_project_duplicates,
    detect_duplicates_in_directories,
)


def example_basic_usage():
    """Example of basic usage with directories."""
    print("🔍 Example 1: Basic Directory Analysis")
    print("=" * 50)

    # Analyze specific directories
    result = detect_duplicates_in_directories(
        directories=["../flext-core/src", "../flext-ldap/src"],
        threshold=20.0,
        file_extensions=["py"],
        show_loc=True,
    )

    print(f"✅ Analysis completed: {result.is_success()}")
    print(f"📊 Found {len(result.reports)} files with duplications")

    # Show critical duplications
    critical = result.get_critical_duplications(threshold=50.0)
    if critical:
        print(f"🚨 Found {len(critical)} critical duplications (>50%):")
        for dup in critical[:5]:  # Show first 5
            print(
                f"   {dup.source_file} ↔ {dup.target_file} ({dup.similarity_percentage:.1f}%)"
            )

    print()


def example_project_analysis():
    """Example of analyzing an entire project."""
    print("🔍 Example 2: Full Project Analysis")
    print("=" * 50)

    detector = DuplicateCodeDetector(
        fail_threshold=100,
        ignore_threshold=15,
        file_extensions=["py", "js", "ts", "java"],
        only_code=True,  # Remove comments and docstrings
        show_loc=True,
    )

    # Analyze the entire flext project
    result = detector.analyze_project(
        project_path="..",
        exclude_patterns=[
            "tests/",
            "docs/",
            ".git/",
            "node_modules/",
            "__pycache__/",
            "*.pyc",
        ],
    )

    print(f"✅ Project analysis completed: {result.is_success()}")
    print(f"📊 Analyzed {len(result.reports)} files with duplications")

    # Generate summary report
    summary = {
        "total_files": len(result.reports),
        "critical_duplications": len(result.get_critical_duplications(50.0)),
        "high_duplications": len(result.get_critical_duplications(30.0)),
        "medium_duplications": len(result.get_critical_duplications(15.0)),
    }

    print("📈 Summary:")
    for key, value in summary.items():
        print(f"   {key}: {value}")

    print()


def example_flext_integration():
    """Example of integrating with Flext CI/CD pipeline."""
    print("🔍 Example 3: Flext CI/CD Integration")
    print("=" * 50)

    # Simulate CI/CD environment
    detector = DuplicateCodeDetector(
        fail_threshold=80,  # Fail if any duplication >80%
        ignore_threshold=20,  # Ignore duplications <20%
        file_extensions=["py"],
        only_code=True,
        show_loc=True,
    )

    # Analyze Flext modules
    flext_modules = [
        "../flext-core/src",
        "../flext-ldap/src",
        "../flext-grpc/src",
        "../scripts",
    ]

    result = detector.detect_in_directories(
        directories=flext_modules,
        ignore_directories=["tests/", "__pycache__/"],
        project_root_dir="..",
    )

    print(f"✅ CI/CD Analysis: {result.is_success()}")

    if result.return_code.value > 0:
        print("❌ Duplication threshold exceeded!")
        print("🚨 Critical duplications found:")

        for dup in result.get_critical_duplications(50.0):
            print(
                f"   {dup.source_file} ↔ {dup.target_file} ({dup.similarity_percentage:.1f}%)"
            )

        # Generate detailed report for CI/CD
        report_path = "duplication_report.json"
        with open(report_path, "w") as f:
            f.write(result.to_json())

        print(f"📄 Detailed report saved to: {report_path}")
        sys.exit(1)  # Exit with error for CI/CD
    else:
        print("✅ No critical duplications found!")
        print("🎉 Code quality check passed!")

    print()


def example_custom_analysis():
    """Example of custom analysis with specific requirements."""
    print("🔍 Example 4: Custom Analysis")
    print("=" * 50)

    # Custom detector for specific needs
    detector = DuplicateCodeDetector(
        fail_threshold=60,
        ignore_threshold=25,
        file_extensions=["py"],
        only_code=True,
        show_loc=True,
    )

    # Analyze specific files
    specific_files = [
        "../flext-core/src/flext_core/config/auth.py",
        "../flext-core/src/flext_core/config/monitoring.py",
        "../flext-core/src/flext_core/config/performance.py",
    ]

    result = detector.detect_in_files(
        files=specific_files,
        project_root_dir="..",
    )

    print(f"✅ Custom analysis completed: {result.is_success()}")

    # Custom reporting
    for report in result.reports:
        if report.similarities:
            print(f"\n📁 File: {report.file_path}")
            print(f"   Lines of Code: {report.loc_count}")
            print(f"   Similarities found: {len(report.similarities)}")

            for sim in report.similarities:
                status = (
                    "🚨"
                    if sim.similarity_percentage > 50
                    else "⚠️"
                    if sim.similarity_percentage > 30
                    else "ℹ️"
                )
                print(
                    f"   {status} {sim.target_file} ({sim.similarity_percentage:.1f}%)"
                )

    print()


def main():
    """Run all examples."""
    print("🚀 Duplicate Code Detection Tool - Flext Integration Examples")
    print("=" * 70)
    print()

    try:
        example_basic_usage()
        example_project_analysis()
        example_flext_integration()
        example_custom_analysis()

        print("✅ All examples completed successfully!")
        print("\n💡 Tips for Flext integration:")
        print("   - Use in CI/CD pipelines for quality gates")
        print("   - Integrate with pre-commit hooks")
        print("   - Generate reports for code reviews")
        print("   - Set appropriate thresholds for your project")

    except Exception as e:
        print(f"❌ Error running examples: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
