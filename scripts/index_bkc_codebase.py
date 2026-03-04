#!/usr/bin/env python3
"""
Index BKC codebase into KOI knowledge graph via tree-sitter extraction.

Uses the koi-processor TreeSitterExtractor as a library (not CLI) to
extract code entities and edges, then writes results to JSON artifacts.

Usage:
    python index_bkc_codebase.py --dry-run
    python index_bkc_codebase.py --apply
    python index_bkc_codebase.py --apply --repos koi-processor/api

Requires:
    - koi-processor on sys.path (auto-detected)
    - tree-sitter + tree-sitter-python + tree-sitter-typescript installed
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# BKC repository configuration
# ---------------------------------------------------------------------------

LANGUAGE_EXTENSIONS = {
    "python": [".py"],
    "typescript": [".ts", ".tsx"],
    "javascript": [".js", ".jsx"],
}

SKIP_DIRS = {"__pycache__", "node_modules", ".next", ".git", "venv", ".venv", "dist", "build"}

# Relative to the meta-repo root (BioregionKnwoledgeCommons/)
BKC_REPOS = [
    {
        "name": "koi-processor-api",
        "path": "Octo/koi-processor/api",
        "language": "python",
        "description": "KOI backend API (Python/FastAPI)",
    },
    {
        "name": "bioregional-commons-web",
        "path": "bioregional-commons-web/web/src",
        "language": "typescript",
        "description": "Web dashboard (Next.js/TypeScript)",
    },
    {
        "name": "bkc-scripts",
        "path": "BioregionalKnowledgeCommoning/scripts",
        "language": "python",
        "description": "BKC governance/roadmap scripts (Python)",
    },
]


def find_meta_repo_root() -> Path:
    """Walk up from this script to find the meta-repo root."""
    current = Path(__file__).resolve().parent
    candidate = current.parent.parent
    if (candidate / "Octo").exists() and (candidate / "bioregional-commons-web").exists():
        return candidate
    if "BKC_META_ROOT" in os.environ:
        return Path(os.environ["BKC_META_ROOT"])
    log.error("Cannot find meta-repo root. Set BKC_META_ROOT env var.")
    sys.exit(1)


def find_koi_processor() -> Path:
    """Find the canonical koi-processor for imports."""
    candidates = [
        Path.home() / "projects" / "regenai" / "koi-processor",
        Path.home() / "projects" / "RegenAI" / "koi-processor",
    ]
    for c in candidates:
        if (c / "api" / "tree_sitter_extractor.py").exists():
            return c
    if "KOI_PROCESSOR_PATH" in os.environ:
        return Path(os.environ["KOI_PROCESSOR_PATH"])
    return None


def collect_source_files(repo_path: Path, language: str) -> list[Path]:
    """Collect all source files for a given language, skipping irrelevant dirs."""
    exts = LANGUAGE_EXTENSIONS.get(language, [f".{language}"])
    files = []
    for ext in exts:
        for f in repo_path.rglob(f"*{ext}"):
            if any(skip in f.parts for skip in SKIP_DIRS):
                continue
            files.append(f)
    return sorted(files)


def extract_with_tree_sitter(repo_path: Path, language: str, repo_name: str) -> dict:
    """Extract code entities using TreeSitterExtractor library."""
    koi_proc = find_koi_processor()
    if not koi_proc:
        log.warning("koi-processor not found, falling back to file manifest")
        return extract_file_manifest(repo_path, language)

    # Add koi-processor/api to sys.path for import
    api_dir = str(koi_proc / "api")
    if api_dir not in sys.path:
        sys.path.insert(0, api_dir)

    try:
        from tree_sitter_extractor import TreeSitterExtractor
        extractor = TreeSitterExtractor()
    except ImportError as e:
        log.warning(f"Cannot import TreeSitterExtractor: {e}")
        log.info("Install: pip install tree-sitter tree-sitter-python tree-sitter-typescript")
        return extract_file_manifest(repo_path, language)

    files = collect_source_files(repo_path, language)
    log.info(f"  Found {len(files)} {language} files")

    all_entities = []
    all_edges = []
    errors = []

    for filepath in files:
        try:
            content = filepath.read_text(errors="ignore")
            rel_path = str(filepath.relative_to(repo_path))

            # Determine language variant for tsx files
            lang = language
            if filepath.suffix == ".tsx":
                lang = "tsx"

            entities, edges = extractor.extract(lang, content, rel_path, repo_name)
            all_entities.extend(asdict(e) for e in entities)
            all_edges.extend(asdict(e) for e in edges)
        except Exception as e:
            errors.append({"file": str(filepath.relative_to(repo_path)), "error": str(e)})

    result = {
        "repo": repo_name,
        "repo_path": str(repo_path),
        "language": language,
        "files_processed": len(files),
        "entities": all_entities,
        "edges": all_edges,
        "errors": errors,
    }

    if errors:
        log.warning(f"  {len(errors)} files had extraction errors")

    return result


def extract_file_manifest(repo_path: Path, language: str) -> dict:
    """Fallback: collect file manifest when tree-sitter is unavailable."""
    files = collect_source_files(repo_path, language)
    artifacts = []
    for f in files:
        rel = f.relative_to(repo_path)
        try:
            line_count = sum(1 for _ in open(f, errors="ignore"))
        except Exception:
            line_count = 0
        artifacts.append({
            "entity_type": "File",
            "name": f.name,
            "file_path": str(rel),
            "language": language,
            "lines": line_count,
        })

    log.info(f"  File manifest: {len(artifacts)} files")
    return {
        "repo": str(repo_path.name),
        "repo_path": str(repo_path),
        "language": language,
        "files_processed": len(files),
        "entities": artifacts,
        "edges": [],
        "errors": [],
        "mode": "file_manifest",
    }


def main():
    parser = argparse.ArgumentParser(description="Index BKC codebase via tree-sitter")
    parser.add_argument("--repos", nargs="*", help="Filter repos by path substring (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing artifacts")
    parser.add_argument("--apply", action="store_true", help="Extract and write artifacts to output dir")
    parser.add_argument("--output-dir", default=None, help="Directory for extraction artifacts")

    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        log.error("Must specify --dry-run or --apply")
        sys.exit(1)

    meta_root = find_meta_repo_root()
    log.info(f"Meta-repo root: {meta_root}")

    output_dir = Path(args.output_dir) if args.output_dir else meta_root / ".code-index"

    repos = BKC_REPOS
    if args.repos:
        repos = [r for r in repos if any(rp in r["path"] for rp in args.repos)]

    log.info(f"Indexing {len(repos)} repositories")

    total_stats = {"files": 0, "entities": 0, "edges": 0, "errors": 0}

    for repo_config in repos:
        repo_path = meta_root / repo_config["path"]
        if not repo_path.exists():
            log.warning(f"Repo path not found: {repo_path}, skipping")
            continue

        log.info(f"\n=== {repo_config['name']} ({repo_config['description']}) ===")

        if args.dry_run:
            files = collect_source_files(repo_path, repo_config["language"])
            log.info(f"  [DRY RUN] Would extract from {len(files)} {repo_config['language']} files")
            total_stats["files"] += len(files)
            continue

        # Extract
        result = extract_with_tree_sitter(
            repo_path, repo_config["language"], repo_config["name"]
        )

        # Write artifact
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{repo_config['name']}_artifacts.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

        entity_count = len(result.get("entities", []))
        edge_count = len(result.get("edges", []))
        error_count = len(result.get("errors", []))

        log.info(f"  Extracted: {entity_count} entities, {edge_count} edges → {output_file}")
        if error_count:
            log.warning(f"  {error_count} errors")

        # Verify output was actually written
        if output_file.exists():
            size = output_file.stat().st_size
            log.info(f"  Verified: {output_file} ({size:,} bytes)")
        else:
            log.error(f"  Output file NOT created: {output_file}")

        total_stats["files"] += result.get("files_processed", 0)
        total_stats["entities"] += entity_count
        total_stats["edges"] += edge_count
        total_stats["errors"] += error_count

    log.info(f"\n=== Summary ===")
    log.info(f"  Files: {total_stats['files']}")
    log.info(f"  Entities: {total_stats['entities']}")
    log.info(f"  Edges: {total_stats['edges']}")
    if total_stats["errors"]:
        log.warning(f"  Errors: {total_stats['errors']}")
    if args.dry_run:
        log.info("  (DRY RUN — no artifacts written)")


if __name__ == "__main__":
    main()
