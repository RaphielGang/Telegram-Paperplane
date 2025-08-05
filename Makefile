.PHONY: help install setup test run clean docker-build docker-run

help:
	@echo "Paperplane Userbot - Available Commands"
	@echo "======================================"
	@echo "install     - Install Python dependencies"
	@echo "setup       - Run interactive setup"
	@echo "session     - Generate string session"
	@echo "test        - Test the setup"
	@echo "run         - Run the userbot locally"
	@echo "clean       - Clean temporary files"
	@echo "docker-build - Build Docker image"
	@echo "docker-run  - Run in Docker container"
	@echo "health      - Run health check"

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

setup:
	@echo "🔧 Running setup..."
	python setup.py

session:
	@echo "🔑 Generating string session..."
	python generate_string_session.py

test:
	@echo "🧪 Testing setup..."
	python test_setup.py

run:
	@echo "🚀 Starting userbot..."
	python -m userbot

clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .cache
	rm -rf *.egg-info
	rm -f dump.rdb

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t paperplane-userbot .

docker-run:
	@echo "🐳 Running Docker container..."
	docker run --env-file config.env paperplane-userbot

health:
	@echo "🏥 Running health check..."
	python health_check.py