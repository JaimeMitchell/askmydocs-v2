
ENV_NAME=askmydocs

.PHONY: setup pull-model up ui train clean

setup:
	@echo "Setting up Conda environment..."
	@conda env create -f environment.yml || echo "Environment already exists."
	@echo "Activate environment with: conda activate $(ENV_NAME)"

pull-model:
	@echo "Pulling BLOOMZ model via Hugging Face CLI..."
	@python -c "import os; from dotenv import load_dotenv; load_dotenv(); from transformers import AutoTokenizer, AutoModelForCausalLM; token=os.getenv('HF_TOKEN'); AutoTokenizer.from_pretrained('bigscience/bloomz-3b', token=token); AutoModelForCausalLM.from_pretrained('bigscience/bloomz-3b', device_map='auto', dtype='auto', token=token)"

up:
	@echo "Starting Docker Compose stack..."
	docker compose -f infra/docker-compose.yml up --build

ui:
	@echo "Running Streamlit UI..."
	@streamlit run ui/app.py

train:
	@echo "Triggering fine-tune..."
	@python trainer/fine_tune.py

clean:
	@echo "Cleaning containers and caches..."
	docker compose -f infra/docker-compose.yml down
	@rm -rf infra/chroma_db
	@rm -rf results
