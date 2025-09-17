#!/usr/bin/env python3
"""
Alibaba Cluster Data Downloader for GPU Observability Research
Downloads and organizes Alibaba cluster datasets for behavioral pattern analysis
"""

import os
import sys
import requests
import json
import subprocess
from pathlib import Path
from typing import Dict, List
import webbrowser
from datetime import datetime

class AlibabaDataDownloader:
    """Downloads Alibaba cluster datasets"""
    
    def __init__(self, base_path: str = "data/raw"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Dataset configurations
        self.datasets = {
            "gpu-2020": {
                "name": "cluster-trace-gpu-v2020",
                "description": "6.5K+ GPUs, 2-month ML workload trace",
                "github_path": "cluster-trace-gpu-v2020",
                "size_gb": 15.2,
                "priority": "HIGH",
                "files": {
                    "README.md": "README.md",
                    "schema.csv": "schema.csv", 
                    "analysis_demo.ipynb": "analysis_demo.ipynb"
                }
            },
            "gpu-2023": {
                "name": "cluster-trace-gpu-v2023", 
                "description": "6.2K+ GPUs, fragmentation analysis",
                "github_path": "cluster-trace-gpu-v2023",
                "size_gb": 8.7,
                "priority": "MEDIUM",
                "files": {
                    "README.md": "README.md"
                }
            },
            "v2018": {
                "name": "cluster-trace-v2018",
                "description": "4K machines, 8-day general workload", 
                "github_path": "cluster-trace-v2018",
                "size_gb": 48.0,
                "priority": "LOW",
                "files": {
                    "trace_2018.md": "trace_2018.md"
                }
            }
        }
    
    def download_file(self, url: str, local_path: Path) -> bool:
        """Download a single file with error handling"""
        try:
            print(f"Downloading: {local_path.name}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✓ Downloaded: {local_path}")
            return True
            
        except requests.RequestException as e:
            print(f"  ✗ Failed to download {url}: {e}")
            return False
    
    def download_metadata(self, dataset_key: str) -> bool:
        """Download available metadata for a dataset"""
        
        dataset = self.datasets[dataset_key]
        dataset_dir = self.base_path / dataset["name"]
        
        print(f"\nDownloading metadata for {dataset['name']}...")
        print(f"Description: {dataset['description']}")
        
        base_url = f"https://raw.githubusercontent.com/alibaba/clusterdata/master/{dataset['github_path']}/"
        
        success_count = 0
        for remote_file, local_file in dataset["files"].items():
            url = base_url + remote_file
            local_path = dataset_dir / local_file
            
            if self.download_file(url, local_path):
                success_count += 1
        
        # Create dataset info file
        dataset_info = {
            "dataset": dataset["name"],
            "description": dataset["description"],
            "size_gb": dataset["size_gb"],
            "priority": dataset["priority"],
            "github_url": f"https://github.com/alibaba/clusterdata/tree/master/{dataset['github_path']}",
            "survey_required": True,
            "files_downloaded": list(dataset["files"].values()),
            "download_date": datetime.now().isoformat(),
            "full_data_status": "Survey required - see survey_info.json"
        }
        
        info_path = dataset_dir / "dataset_info.json"
        with open(info_path, 'w') as f:
            json.dump(dataset_info, f, indent=2)
        
        print(f"  ✓ Created dataset info: {info_path}")
        return success_count > 0
    
    def create_survey_guide(self):
        """Create comprehensive survey completion guide"""
        
        survey_guide = {
            "title": "Alibaba Cluster Data Survey Guide",
            "description": "Complete these surveys to access full datasets for GPU observability research",
            "research_purpose": "Autonomous Behavioral Pattern-Driven Optimization for ML Infrastructure",
            "datasets": {},
            "instructions": [
                "Visit the GitHub URL for your target dataset",
                "Look for survey link (usually near top of README)",
                "Complete 2-3 minute academic survey", 
                "Receive download links via email",
                "Download .tar.gz files to appropriate data/raw/ subdirectory",
                "Extract files and begin analysis"
            ]
        }
        
        for key, dataset in self.datasets.items():
            survey_guide["datasets"][key] = {
                "name": dataset["name"],
                "description": dataset["description"],
                "priority": dataset["priority"],
                "size_gb": dataset["size_gb"],
                "github_url": f"https://github.com/alibaba/clusterdata/tree/master/{dataset['github_path']}",
                "target_directory": f"data/raw/{dataset['name']}"
            }
        
        survey_path = self.base_path / "survey_info.json"
        with open(survey_path, 'w') as f:
            json.dump(survey_guide, f, indent=2)
        
        # Create markdown guide
        md_content = f"""# Alibaba Cluster Data Access Guide

## Research Project
**Autonomous Behavioral Pattern-Driven Optimization for ML Infrastructure**

## Required Surveys

### Priority 1: GPU 2020 Dataset (PRIMARY)
- **Dataset**: cluster-trace-gpu-v2020
- **Description**: 6.5K+ GPUs, 2-month ML workload trace
- **Size**: ~15GB compressed, ~25GB extracted
- **Survey**: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020
- **Target**: `data/raw/cluster-trace-gpu-v2020/`

### Priority 2: GPU 2023 Dataset (VALIDATION)
- **Dataset**: cluster-trace-gpu-v2023  
- **Description**: 6.2K+ GPUs, fragmentation analysis
- **Size**: ~8GB compressed
- **Survey**: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2023
- **Target**: `data/raw/cluster-trace-gpu-v2023/`

## Survey Completion Steps

1. **Visit the GitHub URL** for your target dataset
2. **Find the survey link** (usually in README or prominent banner)
3. **Complete the survey** (2-3 minutes, academic use)
4. **Receive download links** via email (may take a few minutes)
5. **Download the .tar.gz files** to the target directory
6. **Extract the archives** in place

## What to Say in Survey

**Research Purpose**: "Academic research on behavioral pattern recognition for ML infrastructure optimization using CRE-inspired event sequence analysis"

**Institution**: Your university/organization
**Use Case**: "Performance optimization and resource efficiency analysis"

## Expected File Structure After Download

```
data/raw/
├── cluster-trace-gpu-v2020/
│   ├── job_table.csv
│   ├── task_table.csv  
│   ├── instance_table.csv
│   ├── machine_attributes.csv
│   ├── machine_usage.csv
│   └── container_usage.csv
└── cluster-trace-gpu-v2023/
    ├── [fragmentation analysis files]
    └── [GPU scheduling data]
```

## Next Steps After Download

1. Run initial data exploration: `jupyter notebook notebooks/exploration/`
2. Load data schema: Check `schema.csv` files
3. Begin behavioral pattern analysis
4. Identify resource hoarding and inefficiency patterns

## Storage Requirements

- Available: 204.2 GB (sufficient)
- GPU 2020: ~25GB extracted  
- GPU 2023: ~15GB extracted
- Analysis workspace: ~20GB
- Total needed: ~60GB
"""
        
        md_path = self.base_path / "ACCESS_GUIDE.md"
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        print(f"✓ Survey guide created: {survey_path}")
        print(f"✓ Access guide created: {md_path}")
        
        return survey_guide
    
    def create_exploration_notebook(self):
        """Create initial data exploration notebook"""
        
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# Alibaba GPU Cluster Data Exploration\n",
                        "\n",
                        "## Research Objective\n",
                        "Behavioral pattern recognition for autonomous ML infrastructure optimization\n",
                        "\n",
                        "## Primary Dataset: cluster-trace-gpu-v2020\n",
                        "- **Scale**: 6,500+ GPUs across 1,800 machines\n",
                        "- **Duration**: 2 months (July-August 2020)\n", 
                        "- **Users**: 1,300+ users\n",
                        "- **Workloads**: Training and inference jobs\n",
                        "\n",
                        "## Key Research Questions\n",
                        "1. What behavioral patterns exist in GPU resource usage?\n",
                        "2. Can we identify resource hoarding patterns?\n",
                        "3. What temporal patterns exist in job submissions?\n",
                        "4. How do recurring tasks behave differently?\n"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "import pandas as pd\n",
                        "import numpy as np\n",
                        "import matplotlib.pyplot as plt\n",
                        "import seaborn as sns\n",
                        "from pathlib import Path\n",
                        "import json\n",
                        "\n",
                        "# Configure plotting\n",
                        "plt.style.use('default')\n",
                        "sns.set_palette('husl')\n",
                        "pd.set_option('display.max_columns', None)\n",
                        "\n",
                        "print('GPU Observability Research - Alibaba Data Exploration')\n",
                        "print('=' * 60)"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Dataset Status Check"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Check dataset availability\n",
                        "data_path = Path('../data/raw')\n",
                        "\n",
                        "datasets = {\n",
                        "    'GPU 2020': data_path / 'cluster-trace-gpu-v2020',\n",
                        "    'GPU 2023': data_path / 'cluster-trace-gpu-v2023'\n",
                        "}\n",
                        "\n",
                        "print('Dataset Status:')\n",
                        "print('-' * 30)\n",
                        "\n",
                        "for name, path in datasets.items():\n",
                        "    if path.exists():\n",
                        "        files = list(path.glob('*.csv'))\n",
                        "        status = f'✓ Found ({len(files)} CSV files)' if files else '⚠ Metadata only'\n",
                        "        print(f'{name}: {status}')\n",
                        "        \n",
                        "        # Show info if available\n",
                        "        info_file = path / 'dataset_info.json'\n",
                        "        if info_file.exists():\n",
                        "            with open(info_file) as f:\n",
                        "                info = json.load(f)\n",
                        "            print(f'  Description: {info.get(\"description\", \"N/A\")}')\n",
                        "    else:\n",
                        "        print(f'{name}: ✗ Not found')\n",
                        "\n",
                        "print('\\nTo get full datasets:')\n",
                        "print('1. See: ../data/raw/ACCESS_GUIDE.md')\n",
                        "print('2. Complete surveys for dataset access')\n",
                        "print('3. Download and extract data files')"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Data Loading (Run after downloading full datasets)"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Load GPU 2020 dataset (primary focus)\n",
                        "gpu_2020_path = data_path / 'cluster-trace-gpu-v2020'\n",
                        "\n",
                        "if (gpu_2020_path / 'job_table.csv').exists():\n",
                        "    print('Loading GPU 2020 dataset...')\n",
                        "    \n",
                        "    # Core tables for behavioral analysis\n",
                        "    jobs_df = pd.read_csv(gpu_2020_path / 'job_table.csv')\n",
                        "    tasks_df = pd.read_csv(gpu_2020_path / 'task_table.csv')\n",
                        "    instances_df = pd.read_csv(gpu_2020_path / 'instance_table.csv')\n",
                        "    machines_df = pd.read_csv(gpu_2020_path / 'machine_attributes.csv')\n",
                        "    \n",
                        "    print(f'Jobs: {jobs_df.shape}')\n",
                        "    print(f'Tasks: {tasks_df.shape}')\n",
                        "    print(f'Instances: {instances_df.shape}')\n",
                        "    print(f'Machines: {machines_df.shape}')\n",
                        "    \n",
                        "    # Show basic info\n",
                        "    print('\\nJob table columns:')\n",
                        "    print(jobs_df.columns.tolist())\n",
                        "    \n",
                        "else:\n",
                        "    print('⚠ Full dataset not available')\n",
                        "    print('Complete survey to download: cluster-trace-gpu-v2020')\n",
                        "    print('See: ../data/raw/ACCESS_GUIDE.md')"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        notebook_path = Path("notebooks/exploration/01_alibaba_data_exploration.ipynb")
        notebook_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(notebook_path, 'w') as f:
            json.dump(notebook_content, f, indent=2)
        
        print(f"✓ Exploration notebook created: {notebook_path}")
        
        return notebook_path
    
    def run_full_setup(self):
        """Run complete setup process"""
        
        print("Alibaba Cluster Data Setup for GPU Observability Research")
        print("=" * 65)
        print("Available Storage: 204.2 GB (SUFFICIENT)")
        print("Primary Dataset Target: cluster-trace-gpu-v2020 (~25GB)")
        
        # Download available metadata
        print(f"\nStep 1: Downloading Available Metadata")
        print("-" * 40)
        
        for dataset_key in ["gpu-2020", "gpu-2023"]:
            self.download_metadata(dataset_key)
        
        # Create guides and notebooks
        print(f"\nStep 2: Creating Access Guides")
        print("-" * 40)
        
        self.create_survey_guide()
        self.create_exploration_notebook()
        
        # Summary
        print(f"\n{'SETUP COMPLETE'}")
        print("=" * 30)
        print("Files created:")
        print("✓ data/raw/survey_info.json - Survey details")
        print("✓ data/raw/ACCESS_GUIDE.md - Step-by-step guide")
        print("✓ notebooks/exploration/01_alibaba_data_exploration.ipynb")
        
        print(f"\nNext Steps:")
        print("1. Read: data/raw/ACCESS_GUIDE.md")
        print("2. Complete survey for cluster-trace-gpu-v2020 (PRIMARY)")
        print("3. Download and extract dataset to data/raw/cluster-trace-gpu-v2020/")
        print("4. Run: jupyter notebook notebooks/exploration/")
        
        print(f"\nPriority Dataset Survey:")
        print("https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020")

def main():
    """Main execution function"""
    downloader = AlibabaDataDownloader()
    downloader.run_full_setup()

if __name__ == "__main__":
    main()