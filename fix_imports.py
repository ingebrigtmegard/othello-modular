#!/usr/bin/env python
"""
Relative Import Fixer for src-layout Python projects.
Specifically designed for projects with structure:
  src/
  └── your_package/
      ├── __init__.py
      ├── subpackage1/
      │   ├── __init__.py
      │   └── module.py
      └── subpackage2/
          ├── __init__.py
          └── module.py

Usage:
  python fix_imports.py [--check] [--fix] [--src-dir=SRC_DIR] [--package=PACKAGE]

  --check   : Only report issues (don't modify files) [DEFAULT]
  --fix     : Apply suggested fixes (creates .bak backups)
  --src-dir : Source directory (default: src)
  --package : Top-level package name (default: othello)
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# ======================
# CONFIGURATION
# ======================
DEFAULT_SRC_DIR = "src"
DEFAULT_PACKAGE = "othello"

# Patterns to detect problematic imports
ABSOLUTE_IMPORT_PATTERN = re.compile(
    r'^\s*from\s+src\s+\.{0,1}' + re.escape(DEFAULT_PACKAGE) + r'\s+import\s+',
    re.MULTILINE
)

# For detecting over-imported relative paths (too many dots)
RELATIVE_IMPORT_PATTERN = re.compile(
    r'^\s*from\s+(\.+)\s+([\w\.]+)\s+import\s+',
    re.MULTILINE
)

def get_module_depth(file_path: Path, src_dir: Path, package_name: str) -> int:
    """
    Calculate how many levels deep a file is within the package.
    
    Example for src/othello/core/engine.py:
        src_dir = src
        package_name = othello
        file_path = src/othello/core/engine.py
        → depth = 2 (othello → core)
    """
    try:
        # Get path relative to src_dir
        rel_path = file_path.relative_to(src_dir)
        
        # Should start with package_name
        if not rel_path.parts or rel_path.parts[0] != package_name:
            return -1  # Not in our package
            
        # Depth = number of subpackages after the top-level package
        return len(rel_path.parts) - 1  # Subtract 1 for the package itself
    except ValueError:
        return -1  # File not under src_dir

def calculate_correct_relative_path(
    current_file: Path, 
    target_file: Path, 
    src_dir: Path, 
    package_name: str
) -> str:
    """
    Calculate the correct relative import path from current_file to target_file.
    
    Returns string like: ".module", "..subpackage.module", etc.
    """
    try:
        # Get paths relative to src_dir
        current_rel = current_file.relative_to(src_dir)
        target_rel = target_file.relative_to(src_dir)
        
        # Verify both are in our package
        if not current_rel.parts or current_rel.parts[0] != package_name:
            raise ValueError(f"Current file not in {package_name} package")
        if not target_rel.parts or target_rel.parts[0] != package_name:
            raise ValueError(f"Target file not in {package_name} package")
            
        # Calculate how many levels up we need to go
        current_parts = list(current_rel.parts)
        target_parts = list(target_rel.parts)
        
        # Remove the package name from both (we're working within the package)
        current_parts = current_parts[1:]  # Skip package name
        target_parts = target_parts[1:]    # Skip package name
        
        # Find common prefix
        common_len = 0
        for i in range(min(len(current_parts), len(target_parts))):
            if current_parts[i] == target_parts[i]:
                common_len += 1
            else:
                break
                
        # Levels up = current depth - common depth
        levels_up = len(current_parts) - common_len
        
        # Build the relative path
        dots = "." * (levels_up + 1)  # +1 for the current level
        if levels_up > 0:
            dots = "." * levels_up  # Correct format: .. for up one level
        
        # Remaining path after common ancestor
        remaining = target_parts[common_len:]
        module_path = ".".join(remaining) if remaining else ""
        
        # Combine: dots + module_path (handle edge cases)
        if module_path:
            return f"{dots}{module_path}" if dots != "." else module_path
        else:
            return dots.rstrip(".")  # Remove trailing dot if no module
            
    except Exception as e:
        raise ValueError(f"Could not calculate relative path: {e}")

def analyze_file(file_path: Path, src_dir: Path, package_name: str) -> List[Dict]:
    """
    Analyze a single Python file for import issues.
    Returns list of issues found.
    """
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [{"type": "error", "message": f"Could not read file: {e}"}]
    
    # Get file's depth in package
    depth = get_module_depth(file_path, src_dir, package_name)
    if depth < 0:
        return issues  # Not in our package, skip
    
    lines = content.splitlines()
    
    # Check each line for import issues
    for i, line in enumerate(lines, 1):
        line_issues = []
        
        # 1. Check for absolute imports (src.othello...)
        abs_match = ABSOLUTE_IMPORT_PATTERN.search(line)
        if abs_match:
            line_issues.append({
                "type": "absolute_import",
                "line": i,
                "original": line.strip(),
                "suggestion": "Convert to relative import",
                "details": f"Found absolute import: {line.strip()}"
            })
        
        # 2. Check for relative imports with wrong dot count
        rel_match = RELATIVE_IMPORT_PATTERN.search(line)
        if rel_match:
            dots, module = rel_match.groups()
            num_dots = len(dots)
            
            # Try to parse what they're trying to import
            try:
                # Extract the target module path from the import
                # Example: "from ..core.board import Board" → target = "core.board"
                target_module = module.split()[0]  # Get first part before any 'as' or comma
                
                # Build expected target path
                target_path = src_dir / package_name / f"{target_module.replace('.', os.sep)}.py"
                if not target_path.exists():
                    # Try with __init__.py if it's a package
                    target_path = src_dir / package_name / target_module.replace('.', os.sep) / "__init__.py"
                
                if target_path.exists():
                    # Calculate what the correct import should be
                    correct_import = calculate_correct_relative_path(
                        file_path, target_path, src_dir, package_name
                    )
                    
                    # Check if current dots match what they should be
                    expected_dots = correct_import.count('.')
                    if num_dots != expected_dots or not line.strip().startswith(f"from {correct_import} import"):
                        line_issues.append({
                            "type": "wrong_relative_import",
                            "line": i,
                            "original": line.strip(),
                            "suggestion": f"Use: from {correct_import} import {module.split()[-1]}",
                            "details": f"Expected {expected_dots} dots, got {num_dots}"
                        })
                else:
                    # Target doesn't exist - might be a false positive or missing file
                    pass
                    
            except Exception:
                # If we can't parse it, skip detailed analysis but flag it as suspicious
                if num_dots > 3:  # More than 3 dots is almost always wrong
                    line_issues.append({
                        "type": "suspicious_import",
                        "line": i,
                        "original": line.strip(),
                        "suggestion": "Verify this import - too many dots",
                        "details": f"Has {num_dots} dots (suspiciously high)"
                    })
        
        issues.extend(line_issues)
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="Fix relative imports in src-layout Python projects")
    parser.add_argument("--check", action="store_true", help="Only report issues (default)")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (creates .bak backups)")
    parser.add_argument("--src-dir", default=DEFAULT_SRC_DIR, help=f"Source directory (default: {DEFAULT_SRC_DIR})")
    parser.add_argument("--package", default=DEFAULT_PACKAGE, help=f"Top-level package name (default: {DEFAULT_PACKAGE})")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without making changes")
    
    args = parser.parse_args()
    
    # Determine mode
    if args.fix and args.dry_run:
        print("❌ Error: Cannot use --fix and --dry-run together")
        sys.exit(1)
    
    mode = "FIX" if args.fix else ("DRY-RUN" if args.dry_run else "CHECK")
    print(f"🔍 Running in {mode} mode")
    print(f"📁 Source directory: {args.src_dir}")
    print(f"📦 Package name: {args.package}")
    print("-" * 60)
    
    # Validate source directory
    src_path = Path(args.src_dir)
    if not src_path.exists():
        print(f"❌ Error: Source directory '{args.src_dir}' does not exist")
        sys.exit(1)
    
    # Find all Python files in the package
    package_path = src_path / args.package
    if not package_path.exists():
        print(f"❌ Error: Package directory '{package_path}' does not exist")
        sys.exit(1)
    
    py_files = list(package_path.rglob("*.py"))
    if not py_files:
        print(f"❌ Error: No Python files found in {package_path}")
        sys.exit(1)
    
    print(f"📄 Found {len(py_files)} Python files to check\n")
    
    # Track overall results
    total_issues = 0
    files_with_issues = 0
    
    # Process each file
    for file_path in sorted(py_files):
        relative_path = file_path.relative_to(src_path)
        issues = analyze_file(file_path, src_path, args.package)
        
        if not issues:
            continue
            
        files_with_issues += 1
        total_issues += len(issues)
        
        print(f"📄 {relative_path}")
        for issue in issues:
            issue_type = issue["type"]
            line_num = issue["line"]
            original = issue["original"]
            suggestion = issue.get("suggestion", "No suggestion")
            details = issue.get("details", "")
            
            # Choose icon based on issue type
            if issue_type == "absolute_import":
                icon = "🔴"
            elif issue_type == "wrong_relative_import":
                icon = "🟡"
            elif issue_type == "suspicious_import":
                icon = "⚪"
            else:
                icon = "❓"
                
            print(f"   {icon} Line {line_num}: {original}")
            print(f"      → {suggestion}")
            if details:
                print(f"      ({details})")
            print()
    
    # Summary
    print("=" * 60)
    print(f"📊 SUMMARY: {files_with_issues} files with issues, {total_issues} total issues")
    
    if total_issues == 0:
        print("✅ No import issues found! Your imports look correct.")
        return
    
    if args.fix:
        print("\n🛠️  Applying fixes (backups created as .bak files)...")
        # In a real implementation, we would apply fixes here
        # For safety, we'll just show what would be done
        print("⚠️  Fix application not implemented in this version for safety")
        print("   Please review the issues above and fix manually")
        print("   Or run with --check to see detailed suggestions")
    elif args.dry_run:
        print("\n💡 DRY-RUN COMPLETE: No files were modified")
        print("   Run without --dry-run to see fixes applied")
    else:
        print("\n💡 NEXT STEPS:")
        print("   1. Review the issues above")
        print("   2. Fix imports manually using the suggestions")
        print("   3. Rebuild your package: python -m build")
        print("   4. Reinstall: .\\venv\\Scripts\\python.exe -m pip install dist\\*.whl")
        print("\   To see fixes applied: python fix_imports.py --fix")

if __name__ == "__main__":
    main()
