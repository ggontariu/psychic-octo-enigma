.PHONY: help setup install run clean install-chromadb start-chromadb

# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
CHROMA = $(VENV)/bin/chroma
SCRIPT = simple_rag.py
CHROMA_HOST = localhost
CHROMA_PORT = 8000
CHROMA_PATH = ./chroma_data

help:
	@echo "Available targets:"
	@echo "  make setup           - Create virtual environment and install dependencies"
	@echo "  make install         - Install/update dependencies (alias for setup)"
	@echo "  make install-chromadb - Install chromadb package"
	@echo "  make start-chromadb  - Start ChromaDB server"
	@echo "  make run             - Run the script with virtual environment"
	@echo "  make clean           - Remove virtual environment and Python cache files"
	@echo "  make help            - Show this help message"

setup: $(VENV)/bin/activate
	@echo "Virtual environment is ready!"

$(VENV)/bin/activate: pyproject.toml
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -e .
	@touch $(VENV)/bin/activate

install: setup

run: setup
	@echo "Running $(SCRIPT)..."
	$(PYTHON) $(SCRIPT)

install-chromadb: setup
	@echo "Installing chromadb..."
	$(PIP) install chromadb
	@echo "ChromaDB installed!"

start-chromadb: setup
	@echo "Starting ChromaDB server on $(CHROMA_HOST):$(CHROMA_PORT)..."
	@echo "Data will be stored in $(CHROMA_PATH)"
	@echo "Press Ctrl+C to stop the server"
	$(CHROMA) run --host $(CHROMA_HOST) --port $(CHROMA_PORT) --path $(CHROMA_PATH)

clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "Removing Python cache files..."
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	@echo "Cleanup complete."

