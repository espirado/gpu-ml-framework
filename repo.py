#!/usr/bin/env python3
"""
GPU Observability Research Repository Setup
Creates the project structure for autonomous ML infrastructure behavioral pattern analysis
"""

import os
import subprocess
import sys
from pathlib import Path
import json

def create_directory_structure():
    """Create the research project directory structure"""
    
    directories = [
        "data/",
        "data/raw/",
        "data/processed/",
        "data/external/",
        "notebooks/",
        "notebooks/exploration/",
        "notebooks/analysis/",
        "notebooks/visualization/",
        "src/",
        "src/data/",
        "src/analysis/",
        "src/models/",
        "src/visualization/",
        "src/utils/",
        "tests/",
        "docs/",
        "configs/",
        "scripts/",
        "results/",
        "results/figures/",
        "results/models/",
        "results/reports/",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        # Create __init__.py for Python packages
        if directory.startswith("src/"):
            (Path(directory) / "__init__.py").touch()
    
    print("✓ Directory structure created")

def create_requirements_file():
    """Create requirements.txt with essential data science packages"""
    
    requirements = """# Core Data Science
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0
bokeh>=3.0.0

# Data Processing
dask>=2023.5.0
polars>=0.18.0
pyarrow>=12.0.0

# Time Series Analysis
statsmodels>=0.14.0
prophet>=1.1.0
tslearn>=0.6.0

# Machine Learning
xgboost>=1.7.0
lightgbm>=3.3.0
catboost>=1.2.0
torch>=2.0.0
transformers>=4.30.0

# Cluster Analysis
networkx>=3.1.0
igraph>=0.10.0
community>=0.16.0

# Infrastructure & Monitoring
prometheus-client>=0.16.0
opentelemetry-api>=1.18.0
kubernetes>=26.1.0

# Development
jupyter>=1.0.0
ipykernel>=6.23.0
black>=23.0.0
pytest>=7.4.0
pytest-cov>=4.1.0

# Configuration
pydantic>=2.0.0
omegaconf>=2.3.0
hydra-core>=1.3.0

# Utilities
tqdm>=4.65.0
click>=8.1.0
python-dotenv>=1.0.0
requests>=2.31.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    print("✓ requirements.txt created")

def create_config_files():
    """Create configuration files for the project"""
    
    # Main project config
    project_config = {
        "project": {
            "name": "gpu-observability-research",
            "version": "0.1.0",
            "description": "Autonomous Behavioral Pattern-Driven Optimization for ML Infrastructure"
        },
        "data": {
            "raw_path": "data/raw/",
            "processed_path": "data/processed/",
            "external_path": "data/external/"
        },
        "datasets": {
            "alibaba_gpu_2020": {
                "url": "https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020",
                "description": "6.5K+ GPUs, 2-month ML workload trace"
            },
            "alibaba_gpu_2023": {
                "url": "https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2023", 
                "description": "6.2K+ GPUs, fragmentation analysis"
            },
            "alibaba_2018": {
                "url": "https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2018",
                "description": "4K machines, 8-day general workload"
            }
        },
        "analysis": {
            "behavioral_patterns": {
                "temporal_windows": [60, 300, 3600],  # seconds
                "pattern_types": ["resource_hoarding", "queue_spiraling", "recurring_tasks"],
                "cre_inspired": True
            }
        }
    }
    
    with open("configs/project_config.json", "w") as f:
        json.dump(project_config, f, indent=2)
    
    # Logging config
    logging_config = """
version: 1
disable_existing_loggers: False

formatters:
  standard:
    format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
  detailed:
    format: "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout

  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: detailed
    filename: logs/research.log

loggers:
  data_pipeline:
    level: DEBUG
    handlers: [console, file]
    propagate: no

  analysis:
    level: DEBUG
    handlers: [console, file]
    propagate: no

root:
  level: INFO
  handlers: [console]
"""
    
    Path("logs/").mkdir(exist_ok=True)
    with open("configs/logging.yaml", "w") as f:
        f.write(logging_config)
    
    print("✓ Configuration files created")

def create_gitignore():
    """Create comprehensive .gitignore file"""
    
    gitignore_content = """# Data files
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep
*.csv
*.parquet
*.h5
*.hdf5

# Large files
*.tar.gz
*.zip
*.7z

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Jupyter Notebook
.ipynb_checkpoints

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Model files
*.pkl
*.joblib
*.pt
*.pth
*.h5
models/

# Results
results/figures/*.png
results/figures/*.pdf
results/models/*
!results/figures/.gitkeep
!results/models/.gitkeep

# Config overrides
configs/local_*
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    # Create .gitkeep files
    Path("data/raw/.gitkeep").touch()
    Path("data/processed/.gitkeep").touch()
    Path("results/figures/.gitkeep").touch()
    Path("results/models/.gitkeep").touch()
    
    print("✓ .gitignore and .gitkeep files created")

def create_readme():
    """Create comprehensive README.md"""
    
    readme_content = """# GPU Observability Research: Autonomous Behavioral Pattern Learning

## Project Overview

This repository implements **Autonomous Behavioral Pattern-Driven Optimization for Sustainable and Socially Responsible ML Infrastructure** using CRE-inspired event-sequence analysis.

### Research Questions
1. How can behavioral pattern recognition identify resource waste patterns in ML cluster environments?
2. What event-sequence analysis methods can predict resource inefficiencies?
3. Can autonomous recommendations improve resource allocation without manual intervention?

## Dataset

Primary focus on **Alibaba Cluster GPU Traces**:
- **cluster-trace-gpu-v2020**: 6.5K+ GPUs, 2-month ML workload trace
- **cluster-trace-gpu-v2023**: 6.2K+ GPUs, fragmentation analysis  
- **cluster-trace-v2018**: 4K machines, general workload patterns

## Repository Structure

```
├── data/                    # Data storage
│   ├── raw/                # Original datasets
│   ├── processed/          # Cleaned and transformed data
│   └── external/           # External reference data
├── notebooks/              # Jupyter notebooks
│   ├── exploration/        # Initial data exploration
│   ├── analysis/          # Pattern analysis notebooks
│   └── visualization/     # Results visualization
├── src/                   # Source code
│   ├── data/              # Data processing modules
│   ├── analysis/          # Behavioral pattern analysis
│   ├── models/            # ML models and CRE framework
│   └── visualization/     # Plotting utilities
├── configs/               # Configuration files
├── scripts/               # Automation scripts
└── results/               # Output artifacts
```

## Quick Start

1. **Setup Environment**
   ```bash
   python setup_repo.py
   pip install -r requirements.txt
   ```

2. **Download Data**
   ```bash
   python scripts/download_data.py --dataset gpu-2020
   ```

3. **Explore Data**
   ```bash
   jupyter notebook notebooks/exploration/01_initial_exploration.ipynb
   ```

## Key Features

- **CRE-Inspired Pattern Detection**: Temporal event sequence analysis
- **Behavioral Classification**: User and application behavior clustering  
- **Resource Usage Prediction**: ML models for optimization
- **Privacy-Preserving Analytics**: Federated learning approaches

## Research Methodology

1. **Data Exploration**: Understand cluster behavioral patterns
2. **Pattern Recognition**: Apply CRE-inspired temporal analysis
3. **Behavioral Modeling**: Develop predictive models
4. **Autonomous Optimization**: Real-time recommendation system
5. **Validation**: Performance improvement measurement

## Contributing

This research project follows academic collaboration principles. Please see CONTRIBUTING.md for guidelines.

## License

Academic research use only. See LICENSE for details.

## Contact

For questions about this research, please file an issue or contact the research team.
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✓ README.md created")

def initialize_git():
    """Initialize git repository if not already done"""
    
    if not Path(".git").exists():
        try:
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial repository setup"], check=True, capture_output=True)
            print("✓ Git repository initialized")
        except subprocess.CalledProcessError:
            print("⚠ Git initialization failed (git not installed or configured)")
    else:
        print("✓ Git repository already exists")

def main():
    """Main setup function"""
    
    print("Setting up GPU Observability Research Repository...")
    print("=" * 50)
    
    create_directory_structure()
    create_requirements_file()
    create_config_files()
    create_gitignore()
    create_readme()
    initialize_git()
    
    print("=" * 50)
    print("✅ Repository setup complete!")
    print("\nNext steps:")
    print("1. pip install -r requirements.txt")
    print("2. python scripts/download_data.py")
    print("3. jupyter notebook notebooks/exploration/")

if __name__ == "__main__":
    main()