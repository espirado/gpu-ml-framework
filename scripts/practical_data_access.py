#!/usr/bin/env python3
"""
Practical Data Access for GPU Observability Research
Downloads available metadata and provides alternative data sources
"""

import os
import requests
import pandas as pd
import numpy as np
from pathlib import Path
import json
import zipfile
import subprocess
from datetime import datetime

class DataAccessHelper:
    """Helper to access available cluster datasets"""
    
    def __init__(self, base_path="data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def download_available_metadata(self):
        """Download what's directly accessible from GitHub"""
        
        print("Downloading available metadata from Alibaba cluster repository...")
        
        files_to_download = {
            "alibaba_cluster_README.md": "https://raw.githubusercontent.com/alibaba/clusterdata/master/README.md",
            "gpu_2020_README.md": "https://raw.githubusercontent.com/alibaba/clusterdata/master/cluster-trace-gpu-v2020/README.md",
            "gpu_2020_schema.csv": "https://raw.githubusercontent.com/alibaba/clusterdata/master/cluster-trace-gpu-v2020/schema.csv",
            "gpu_2020_demo.ipynb": "https://raw.githubusercontent.com/alibaba/clusterdata/master/cluster-trace-gpu-v2020/analysis_demo.ipynb",
            "v2018_info.md": "https://raw.githubusercontent.com/alibaba/clusterdata/master/cluster-trace-v2018/trace_2018.md"
        }
        
        metadata_dir = self.base_path / "raw" / "metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = []
        for filename, url in files_to_download.items():
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                file_path = metadata_dir / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"✓ Downloaded: {filename}")
                downloaded.append(filename)
                
            except Exception as e:
                print(f"✗ Failed to download {filename}: {e}")
        
        return downloaded
    
    def generate_synthetic_data(self):
        """Generate synthetic data for initial development and testing"""
        
        print("\nGenerating synthetic GPU cluster data for development...")
        
        synthetic_dir = self.base_path / "raw" / "synthetic"
        synthetic_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate synthetic job data
        np.random.seed(42)
        
        # Job table
        n_jobs = 10000
        job_data = {
            'job_id': [f'job_{i:06d}' for i in range(n_jobs)],
            'user_id': [f'user_{i:03d}' for i in np.random.randint(0, 100, n_jobs)],
            'submission_time': pd.date_range('2024-01-01', periods=n_jobs, freq='5min'),
            'duration_seconds': np.random.lognormal(mean=6, sigma=1.5, size=n_jobs).astype(int),
            'gpu_request': np.random.choice([0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0], n_jobs, 
                                         p=[0.25, 0.20, 0.25, 0.20, 0.05, 0.03, 0.02]),
            'cpu_request': np.random.lognormal(mean=2, sigma=0.5, size=n_jobs),
            'memory_gb': np.random.lognormal(mean=3, sigma=0.8, size=n_jobs),
            'job_type': np.random.choice(['training', 'inference', 'preprocessing'], n_jobs, p=[0.4, 0.5, 0.1]),
            'framework': np.random.choice(['tensorflow', 'pytorch', 'other'], n_jobs, p=[0.45, 0.35, 0.2]),
            'is_recurring': np.random.choice([True, False], n_jobs, p=[0.65, 0.35]),
            'queue_time_seconds': np.random.exponential(300, n_jobs).astype(int)  # Resource hoarding indicator
        }
        
        jobs_df = pd.DataFrame(job_data)
        jobs_df.to_csv(synthetic_dir / "job_table.csv", index=False)
        
        # Instance usage table
        n_instances = 50000
        instance_data = {
            'instance_id': [f'inst_{i:08d}' for i in range(n_instances)],
            'job_id': [f'job_{i:06d}' for i in np.random.randint(0, n_jobs, n_instances)],
            'machine_id': [f'machine_{i:04d}' for i in np.random.randint(0, 500, n_instances)],
            'start_time': pd.date_range('2024-01-01', periods=n_instances, freq='1min'),
            'cpu_usage_avg': np.random.beta(2, 5, n_instances),  # Skewed toward low usage
            'memory_usage_avg': np.random.beta(2, 3, n_instances),
            'gpu_usage_avg': np.random.beta(1, 10, n_instances),  # Very skewed - behavioral pattern
            'gpu_memory_usage': np.random.beta(1.5, 3, n_instances),
            'network_in_mbps': np.random.exponential(10, n_instances),
            'disk_io_mbps': np.random.exponential(5, n_instances),
            'status': np.random.choice(['running', 'completed', 'failed'], n_instances, p=[0.15, 0.8, 0.05])
        }
        
        instances_df = pd.DataFrame(instance_data)
        instances_df.to_csv(synthetic_dir / "instance_table.csv", index=False)
        
        # Machine attributes
        n_machines = 500
        machine_data = {
            'machine_id': [f'machine_{i:04d}' for i in range(n_machines)],
            'cpu_cores': np.random.choice([64, 96, 128], n_machines, p=[0.4, 0.4, 0.2]),
            'memory_gb': np.random.choice([256, 512, 768], n_machines, p=[0.3, 0.5, 0.2]),
            'gpu_count': np.random.choice([2, 4, 8], n_machines, p=[0.5, 0.3, 0.2]),
            'gpu_type': np.random.choice(['V100', 'P100', 'T4', 'A100'], n_machines, p=[0.3, 0.3, 0.3, 0.1]),
            'network_bandwidth_gbps': np.random.choice([10, 25, 40], n_machines, p=[0.4, 0.4, 0.2]),
            'availability_zone': np.random.choice(['zone-a', 'zone-b', 'zone-c'], n_machines, p=[0.4, 0.3, 0.3])
        }
        
        machines_df = pd.DataFrame(machine_data)
        machines_df.to_csv(synthetic_dir / "machine_attributes.csv", index=False)
        
        # Create data info
        data_info = {
            "type": "synthetic",
            "description": "Synthetic GPU cluster data for development and testing",
            "generated_date": datetime.now().isoformat(),
            "tables": {
                "job_table.csv": f"{n_jobs} jobs with user behavior patterns",
                "instance_table.csv": f"{n_instances} instances with resource usage patterns", 
                "machine_attributes.csv": f"{n_machines} machines with hardware specs"
            },
            "behavioral_patterns": {
                "resource_hoarding": "Low GPU usage vs high requests",
                "recurring_jobs": "65% of jobs marked as recurring",
                "queue_spiraling": "Exponential queue time distribution"
            },
            "research_applications": [
                "Behavioral pattern recognition development",
                "CRE-inspired event sequence analysis",
                "Resource optimization algorithm testing"
            ]
        }
        
        with open(synthetic_dir / "data_info.json", 'w') as f:
            json.dump(data_info, f, indent=2)
        
        print(f"✓ Generated synthetic data in: {synthetic_dir}")
        print(f"  - {n_jobs:,} jobs")
        print(f"  - {n_instances:,} instances")  
        print(f"  - {n_machines:,} machines")
        
        return synthetic_dir
    
    def find_alternative_sources(self):
        """Provide information about alternative data sources"""
        
        alternatives = {
            "Kaggle Datasets": {
                "alibaba_cluster_trace_2018": "https://www.kaggle.com/datasets/derrickmwiti/cluster-trace-gpu-v2020",
                "gpu_cluster_data": "https://www.kaggle.com/search?q=alibaba+gpu+cluster",
                "ml_workload_traces": "https://www.kaggle.com/search?q=ml+workload+traces"
            },
            "Academic Sources": {
                "papers_with_code": "https://paperswithcode.com/dataset/alibaba-cluster-trace",
                "zenodo": "https://zenodo.org/search?q=alibaba+cluster",
                "google_dataset_search": "https://datasetsearch.research.google.com/search?query=alibaba%20cluster%20gpu"
            },
            "Original Papers Data": {
                "nsdi22_data": "Check supplementary material of MLaaS in the Wild paper",
                "atc23_data": "Check Fragmentation Gradient Descent paper supplements",
                "author_websites": "Contact paper authors directly for processed datasets"
            },
            "Cloud Providers": {
                "google_cloud": "Public datasets program may have cluster traces",
                "aws_open_data": "Search for ML cluster traces",
                "azure_open_datasets": "Look for GPU workload data"
            }
        }
        
        alternatives_file = self.base_path / "raw" / "alternative_sources.json"
        with open(alternatives_file, 'w') as f:
            json.dump(alternatives, f, indent=2)
        
        print(f"\n✓ Alternative sources saved to: {alternatives_file}")
        
        return alternatives
    
    def create_data_exploration_notebook(self):
        """Create notebook for exploring available data"""
        
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# GPU Cluster Data Exploration\n",
                        "\n",
                        "## Research Focus\n",
                        "Behavioral pattern recognition for autonomous ML infrastructure optimization\n",
                        "\n",
                        "## Available Data Sources\n",
                        "1. **Synthetic Data**: Generated for development and testing\n",
                        "2. **Metadata**: Available documentation and schemas\n",
                        "3. **Alternative Sources**: Kaggle, academic repositories, etc.\n"
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
                        "plt.rcParams['figure.figsize'] = (12, 6)\n",
                        "\n",
                        "print('GPU Observability Research - Data Exploration')\n",
                        "print('=' * 50)"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## 1. Load Synthetic Data"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Load synthetic dataset for development\n",
                        "data_path = Path('../data/raw/synthetic')\n",
                        "\n",
                        "if data_path.exists():\n",
                        "    print('Loading synthetic cluster data...')\n",
                        "    \n",
                        "    jobs_df = pd.read_csv(data_path / 'job_table.csv')\n",
                        "    instances_df = pd.read_csv(data_path / 'instance_table.csv')\n",
                        "    machines_df = pd.read_csv(data_path / 'machine_attributes.csv')\n",
                        "    \n",
                        "    print(f'Jobs: {jobs_df.shape}')\n",
                        "    print(f'Instances: {instances_df.shape}')\n",
                        "    print(f'Machines: {machines_df.shape}')\n",
                        "    \n",
                        "    # Show data info\n",
                        "    with open(data_path / 'data_info.json') as f:\n",
                        "        data_info = json.load(f)\n",
                        "    \n",
                        "    print('\\nDataset Info:')\n",
                        "    for key, value in data_info['behavioral_patterns'].items():\n",
                        "        print(f'  {key}: {value}')\n",
                        "        \n",
                        "else:\n",
                        "    print('Synthetic data not found. Run the data access script first.')"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## 2. Initial Behavioral Pattern Analysis"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "if 'jobs_df' in locals():\n",
                        "    # Resource hoarding analysis\n",
                        "    fig, axes = plt.subplots(2, 2, figsize=(15, 10))\n",
                        "    \n",
                        "    # GPU request vs usage patterns\n",
                        "    merged_df = pd.merge(jobs_df, instances_df, on='job_id')\n",
                        "    \n",
                        "    # Resource hoarding indicator\n",
                        "    merged_df['gpu_efficiency'] = merged_df['gpu_usage_avg'] / merged_df['gpu_request']\n",
                        "    \n",
                        "    # Plot 1: GPU request distribution\n",
                        "    axes[0,0].hist(jobs_df['gpu_request'], bins=20, alpha=0.7)\n",
                        "    axes[0,0].set_title('GPU Request Distribution')\n",
                        "    axes[0,0].set_xlabel('GPUs Requested')\n",
                        "    \n",
                        "    # Plot 2: GPU efficiency (usage/request)\n",
                        "    axes[0,1].hist(merged_df['gpu_efficiency'].clip(0, 2), bins=30, alpha=0.7)\n",
                        "    axes[0,1].set_title('GPU Efficiency (Usage/Request)')\n",
                        "    axes[0,1].set_xlabel('Efficiency Ratio')\n",
                        "    axes[0,1].axvline(x=1.0, color='red', linestyle='--', label='Perfect Efficiency')\n",
                        "    axes[0,1].legend()\n",
                        "    \n",
                        "    # Plot 3: Queue time distribution\n",
                        "    axes[1,0].hist(jobs_df['queue_time_seconds'] / 60, bins=30, alpha=0.7)\n",
                        "    axes[1,0].set_title('Queue Time Distribution')\n",
                        "    axes[1,0].set_xlabel('Queue Time (minutes)')\n",
                        "    \n",
                        "    # Plot 4: Recurring vs non-recurring jobs\n",
                        "    recurring_counts = jobs_df['is_recurring'].value_counts()\n",
                        "    axes[1,1].pie(recurring_counts.values, labels=['Non-recurring', 'Recurring'], \n",
                        "                 autopct='%1.1f%%')\n",
                        "    axes[1,1].set_title('Recurring Job Distribution')\n",
                        "    \n",
                        "    plt.tight_layout()\n",
                        "    plt.show()\n",
                        "    \n",
                        "    # Summary statistics\n",
                        "    print('\\nResource Hoarding Analysis:')\n",
                        "    print(f'Median GPU efficiency: {merged_df[\"gpu_efficiency\"].median():.3f}')\n",
                        "    print(f'Jobs with <50% GPU efficiency: {(merged_df[\"gpu_efficiency\"] < 0.5).mean():.1%}')\n",
                        "    print(f'Average queue time: {jobs_df[\"queue_time_seconds\"].mean()/60:.1f} minutes')\n",
                        "    print(f'Recurring jobs: {jobs_df[\"is_recurring\"].mean():.1%}')"
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
        
        notebook_dir = Path("notebooks/exploration")
        notebook_dir.mkdir(parents=True, exist_ok=True)
        
        notebook_path = notebook_dir / "01_data_exploration.ipynb"
        with open(notebook_path, 'w') as f:
            json.dump(notebook_content, f, indent=2)
        
        print(f"✓ Exploration notebook created: {notebook_path}")
        return notebook_path
    
    def run_complete_setup(self):
        """Run the complete data access setup"""
        
        print("GPU Observability Research - Practical Data Access")
        print("=" * 55)
        print("Storage Available: 204.2 GB")
        print("Approach: Start with synthetic data + available metadata\n")
        
        # Step 1: Download available metadata
        print("Step 1: Downloading Available Metadata")
        print("-" * 40)
        downloaded = self.download_available_metadata()
        
        # Step 2: Generate synthetic data
        print("\nStep 2: Generating Synthetic Development Data")
        print("-" * 40)
        synthetic_dir = self.generate_synthetic_data()
        
        # Step 3: Create alternative sources guide
        print("\nStep 3: Documenting Alternative Data Sources")
        print("-" * 40)
        alternatives = self.find_alternative_sources()
        
        # Step 4: Create exploration notebook
        print("\nStep 4: Creating Exploration Notebook")
        print("-" * 40)
        notebook_path = self.create_data_exploration_notebook()
        
        # Summary
        print(f"\n{'SETUP COMPLETE'}")
        print("=" * 30)
        print(f"✓ Downloaded {len(downloaded)} metadata files")
        print(f"✓ Generated synthetic data in: {synthetic_dir}")
        print(f"✓ Created exploration notebook: {notebook_path}")
        
        print(f"\nNext Steps:")
        print("1. Explore synthetic data: jupyter notebook notebooks/exploration/")
        print("2. Check alternative sources: data/raw/alternative_sources.json")
        print("3. Contact paper authors for processed datasets")
        print("4. Search Kaggle for 'alibaba cluster' datasets")
        
        print(f"\nImmediate Action:")
        print("cd notebooks/exploration && jupyter notebook 01_data_exploration.ipynb")

def main():
    """Main execution"""
    helper = DataAccessHelper()
    helper.run_complete_setup()

if __name__ == "__main__":
    main()