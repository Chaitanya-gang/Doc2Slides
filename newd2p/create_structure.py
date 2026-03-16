"""
newd2p - Project Structure Creator
Run this ONCE to create all files and folders
"""

from pathlib import Path


PROJECT_NAME = "newd2p"

DIRECTORIES = [
    "src",
    "src/parsers",
    "src/chunking",
    "src/embeddings",
    "src/llm",
    "src/rag",
    "src/narrative",
    "src/charts",
    "src/ppt",
    "src/output",
    "src/pipeline",
    "src/api",
    "src/api/routes",
    "src/utils",
    "frontend",
    "frontend/pages",
    "frontend/components",
    "frontend/styles",
    "frontend/assets",
    "templates/professional",
    "templates/creative",
    "templates/minimal",
    "templates/dark",
    "templates/corporate",
    "prompts",
    "data/faiss_index",
    "data/models_cache",
    "temp_uploads",
    "generated_output/ppts",
    "generated_output/jsons",
    "generated_output/narrations",
    "generated_output/charts",
    "tests",
    "tests/test_parsers",
    "tests/test_chunking",
    "tests/test_embeddings",
    "tests/test_llm",
    "tests/test_rag",
    "tests/test_narrative",
    "tests/test_charts",
    "tests/test_ppt",
    "tests/test_output",
    "tests/test_api",
    "tests/test_pipeline",
    "tests/test_data",
    "samples/input",
    "samples/output",
    "docs/diagrams",
    "research/notebooks",
    "scripts",
    "logs",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
]


def create_directories():
    print(f"📁 Creating {PROJECT_NAME} directories...")
    count = 0
    for dir_path in DIRECTORIES:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        count += 1
    print(f"✅ {count} directories created!")


if __name__ == "__main__":
    create_directories()