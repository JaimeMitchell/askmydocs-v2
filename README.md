# AskMyDocs v2

A complete AI-powered document Q&A system built with **FastAPI**, **LLaMA**, **Streamlit**, **PEFT/LoRA**, and production-ready monitoring with **Prometheus** and **Grafana**.

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │ (Port 8501)
│   (ui/app.py)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI API   │ (Port 8000)
│  (api/main.py)  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│ LLaMA  │ │Prometheus│ (Port 9090)
│ Model  │ │ Metrics  │
└────────┘ └─────┬────┘
                 ▼
           ┌──────────┐
           │ Grafana  │ (Port 3000)
           │Dashboard │
           └──────────┘
```

## 🚀 Features

- **LLaMA 3-8B Integration**: State-of-the-art language model for Q&A
- **FastAPI Backend**: High-performance async API with automatic documentation
- **Streamlit UI**: Interactive chat interface for querying documents
- **PEFT/LoRA Support**: Efficient fine-tuning capabilities (scaffold ready)
- **Production Monitoring**: Prometheus metrics + Grafana dashboards
- **MLflow Integration**: Experiment tracking and model registry
- **Docker Compose**: One-command deployment of entire stack
- **Conda Environment**: Isolated Python environment management

## 📋 Prerequisites

- **Conda/Miniconda** or **Anaconda** installed
- **Docker** and **Docker Compose** (for containerized deployment)
- **GPU recommended** (8GB+ VRAM) for running LLaMA 3-8B locally
- **16GB+ free disk space** for model weights

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd askmydocs_v2
```

### 2. Set Up Conda Environment

```bash
make setup
conda activate askmydocs
```

This will create a conda environment with all required dependencies including:
- FastAPI & Uvicorn
- Transformers & PyTorch
- Streamlit
- PEFT for fine-tuning
- Prometheus client
- LangChain & ChromaDB

### 3. Configure Hugging Face Token

Create a `.env` file in the project root and add your Hugging Face token:

```bash
# Copy the template
cp .env.example .env

# Edit .env and replace with your actual token
HF_TOKEN=your_actual_hugging_face_token_here
```

**Get your token from:** https://huggingface.co/settings/tokens

### 4. Download LLaMA Model (Optional - Downloads on First Use)

```bash
make pull-model
```

⚠️ **Note**: This downloads ~16GB of model weights. The model will auto-download on first API call if skipped.

## 🎯 Quick Start

### Option A: Local Development (Recommended for Testing)

1. **Start the API Server** (Terminal 1):
```bash
conda activate askmydocs
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Start the Streamlit UI** (Terminal 2):
```bash
conda activate askmydocs
make ui
# Or: streamlit run ui/app.py
```

3. **Access the Application**:
   - UI: http://localhost:8501
   - API Docs: http://localhost:8000/docs
   - Metrics: http://localhost:8000/metrics

### Option B: Docker Compose (Full Stack)

```bash
make up
# Or: docker compose -f infra/docker-compose.yml up --build
```

This starts:
- **FastAPI API** on port 8000
- **MLflow** tracking server on port 5000
- **Prometheus** on port 9090
- **Grafana** on port 3000

**Note**: The Streamlit UI runs separately (not containerized):
```bash
conda activate askmydocs
make ui
```

## 📖 Usage

### Using the Web Interface

1. Open http://localhost:8501
2. Enter your question in the text input
3. Click "Ask" to get an AI-generated response

### Using the API Directly

#### Ask a Question
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "query=What is machine learning?"
```

#### Get Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

#### Interactive API Documentation
Visit http://localhost:8000/docs for Swagger UI with interactive API testing.

## 🧪 Development Workflow

### Project Structure

```
askmydocs_v2/
├── api/                   # FastAPI backend
│   ├── main.py           # API endpoints & routes
│   └── model_runner.py   # LLaMA model inference
├── ui/                    # Streamlit frontend
│   └── app.py            # Chat interface
├── trainer/               # Fine-tuning scripts
│   └── fine_tune.py      # PEFT/LoRA training (scaffold)
├── infra/                 # Infrastructure config
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── prometheus.yml
├── environment.yml        # Conda dependencies
├── Makefile              # Automation commands
└── README.md
```

### Available Make Commands

```bash
make setup        # Create conda environment
make pull-model   # Download LLaMA model
make up           # Start Docker stack
make ui           # Run Streamlit UI
make train        # Trigger fine-tuning
make clean        # Clean Docker containers & caches
```

### Adding Custom Documents

To implement document ingestion (TODO):

1. Add document loading in `api/model_runner.py`
2. Use ChromaDB for vector storage (already in dependencies)
3. Implement RAG (Retrieval Augmented Generation) pattern with LangChain

Example scaffold:
```python
from langchain.document_loaders import PDFLoader
from langchain.vectorstores import Chroma
from sentence_transformers import SentenceTransformer

# Load documents
# Create embeddings
# Store in ChromaDB
# Query with LLaMA
```

### Fine-Tuning with PEFT

To fine-tune LLaMA on your documents:

1. Prepare your training data in `trainer/`
2. Implement LoRA training in `trainer/fine_tune.py`
3. Run: `make train`

The PEFT/LoRA approach allows efficient fine-tuning with minimal GPU memory.

## 📊 Monitoring & Observability

### Prometheus Metrics

Available at http://localhost:9090

Default metrics tracked:
- `askmydocs_requests_total`: Total number of /ask requests

### Grafana Dashboards

1. Access Grafana at http://localhost:3000
2. Default credentials: `admin` / `admin`
3. Add Prometheus data source: `http://prometheus:9090`
4. Create custom dashboards for request rates, latency, etc.

### MLflow Tracking

Track experiments at http://localhost:5000
- Model versioning
- Hyperparameter logging
- Metrics comparison

## 🔧 Troubleshooting

### Model Loading Issues

**Problem**: `Model not available locally` error

**Solutions**:
1. The LLaMA model will auto-download on first use
2. Check available disk space (need ~16GB)
3. For CPU-only mode, modify `model_runner.py` to use `device_map="cpu"`

### GPU Out of Memory

**Solutions**:
1. Use 4-bit quantization:
```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B",
    quantization_config=bnb_config,
    device_map="auto"
)
```

2. Reduce `max_new_tokens` in generation
3. Use CPU mode if GPU memory is insufficient

### Port Already in Use

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different ports
uvicorn api.main:app --port 8001
```

### Docker Compose Issues

```bash
# Clean everything and restart
make clean
make up
```

## 🎓 Learning Resources

- [LLaMA 3 Model Documentation](https://huggingface.co/meta-llama/Llama-3-8B)
- [PEFT Library](https://github.com/huggingface/peft)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Docs](https://python.langchain.com/)

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Support

[Add contact/support information here]
