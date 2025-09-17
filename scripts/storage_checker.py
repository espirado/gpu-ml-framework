#!/usr/bin/env python3
"""
Storage Assessment for GPU Observability Research
Checks available disk space and provides download recommendations
"""

import os
import shutil
import platform
import subprocess
from pathlib import Path

def get_disk_usage(path="."):
    """Get disk usage statistics for given path"""
    try:
        total, used, free = shutil.disk_usage(path)
        return {
            'total_gb': total / (1024**3),
            'used_gb': used / (1024**3),
            'free_gb': free / (1024**3),
            'used_percent': (used / total) * 100
        }
    except Exception as e:
        print(f"Error getting disk usage: {e}")
        return None

def get_detailed_storage_info():
    """Get detailed storage information based on OS"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            return result.stdout
        except:
            return "Could not get detailed storage info"
    
    elif system == "Linux":
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            return result.stdout
        except:
            return "Could not get detailed storage info"
    
    elif system == "Windows":
        try:
            result = subprocess.run(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'], 
                                  capture_output=True, text=True)
            return result.stdout
        except:
            return "Could not get detailed storage info"
    
    return "Unknown operating system"

def format_size(bytes_size):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"

def assess_storage_requirements():
    """Define storage requirements for different datasets"""
    
    datasets = {
        "alibaba_gpu_2020": {
            "compressed": 15.2,  # GB
            "extracted": 25.0,   # GB 
            "processed": 10.0,   # GB (after cleaning/filtering)
            "description": "Primary dataset: 6.5K+ GPUs, 2-month ML workload trace"
        },
        "alibaba_gpu_2023": {
            "compressed": 8.7,
            "extracted": 15.0,
            "processed": 6.0,
            "description": "Fragmentation analysis: 6.2K+ GPUs"
        },
        "alibaba_v2018": {
            "compressed": 48.0,
            "extracted": 85.0,
            "processed": 35.0,
            "description": "General workloads: 4K machines, 8 days"
        },
        "alibaba_microservices_2021": {
            "compressed": 3.1,
            "extracted": 6.0,
            "processed": 2.5,
            "description": "Microservices: 20K services, 10K+ nodes"
        }
    }
    
    # Analysis and results storage estimates
    analysis_requirements = {
        "notebooks_cache": 2.0,      # GB
        "intermediate_results": 5.0,  # GB
        "models_and_figures": 3.0,   # GB
        "logs_and_metadata": 1.0     # GB
    }
    
    return datasets, analysis_requirements

def calculate_total_requirements(datasets, analysis_requirements, selected_datasets=None):
    """Calculate total storage requirements"""
    
    if selected_datasets is None:
        selected_datasets = ["alibaba_gpu_2020"]  # Default to primary dataset
    
    total_compressed = 0
    total_extracted = 0
    total_processed = 0
    
    for dataset_name in selected_datasets:
        if dataset_name in datasets:
            dataset = datasets[dataset_name]
            total_compressed += dataset["compressed"]
            total_extracted += dataset["extracted"] 
            total_processed += dataset["processed"]
    
    # Add analysis requirements
    analysis_total = sum(analysis_requirements.values())
    
    # Calculate different scenarios
    scenarios = {
        "minimal": total_compressed + analysis_total,  # Just download and basic analysis
        "full_extraction": total_compressed + total_extracted + analysis_total,  # Extract everything
        "with_processing": total_compressed + total_extracted + total_processed + analysis_total,  # Full pipeline
        "production_ready": (total_compressed + total_extracted + total_processed + analysis_total) * 1.5  # With buffer
    }
    
    return scenarios, selected_datasets

def provide_recommendations(current_free_gb, scenarios, datasets, selected_datasets):
    """Provide storage recommendations based on available space"""
    
    print("\n" + "="*60)
    print("STORAGE RECOMMENDATIONS")
    print("="*60)
    
    # Check each scenario
    for scenario_name, required_gb in scenarios.items():
        status = "✓ SAFE" if current_free_gb >= required_gb * 1.2 else "⚠ TIGHT" if current_free_gb >= required_gb else "✗ INSUFFICIENT"
        buffer_gb = current_free_gb - required_gb
        
        print(f"\n{scenario_name.upper().replace('_', ' ')}:")
        print(f"  Required: {required_gb:.1f} GB")
        print(f"  Status: {status}")
        print(f"  Buffer: {buffer_gb:+.1f} GB")
    
    # Specific recommendations
    print(f"\n{'RECOMMENDATIONS:'}")
    print("-" * 40)
    
    if current_free_gb >= scenarios["production_ready"]:
        print("✓ You have ample space for the full research pipeline")
        print("✓ Can download all datasets and run complete analysis")
        recommended_action = "Download primary dataset (GPU 2020) and proceed with full analysis"
        
    elif current_free_gb >= scenarios["with_processing"]:
        print("✓ Sufficient space for complete analysis of selected datasets")
        print("⚠ Monitor disk usage during processing")
        recommended_action = "Download primary dataset, monitor space during processing"
        
    elif current_free_gb >= scenarios["full_extraction"]:
        print("⚠ Sufficient for download and extraction, but limited processing space")
        print("⚠ Consider processing datasets one at a time")
        recommended_action = "Download primary dataset, process in stages"
        
    elif current_free_gb >= scenarios["minimal"]:
        print("⚠ Minimal space - can download compressed data only")
        print("⚠ Extract and process datasets individually")
        recommended_action = "Download compressed data only, extract on-demand"
        
    else:
        print("✗ Insufficient space for research datasets")
        print("✗ Free up space or use external storage")
        recommended_action = "Free up space or use external drive"
    
    return recommended_action

def suggest_space_optimization():
    """Suggest ways to optimize disk space"""
    
    suggestions = [
        "Clean temporary files and downloads",
        "Empty trash/recycle bin", 
        "Remove old virtual environments",
        "Clear browser caches",
        "Delete old log files",
        "Move large media files to external storage",
        "Use cloud storage for non-active projects",
        "Compress old datasets not currently in use"
    ]
    
    print(f"\n{'SPACE OPTIMIZATION SUGGESTIONS:'}")
    print("-" * 40)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")

def main():
    """Main storage assessment function"""
    
    print("GPU Observability Research - Storage Assessment")
    print("=" * 60)
    
    # Get current directory storage info
    current_usage = get_disk_usage(".")
    if not current_usage:
        print("Could not assess disk usage")
        return
    
    print(f"\nCURRENT DISK USAGE:")
    print("-" * 30)
    print(f"Total Space: {current_usage['total_gb']:.1f} GB")
    print(f"Used Space:  {current_usage['used_gb']:.1f} GB ({current_usage['used_percent']:.1f}%)")
    print(f"Free Space:  {current_usage['free_gb']:.1f} GB")
    
    # Show detailed storage info
    print(f"\nDETAILED STORAGE INFO:")
    print("-" * 30)
    detailed_info = get_detailed_storage_info()
    print(detailed_info)
    
    # Assess requirements
    datasets, analysis_requirements = assess_storage_requirements()
    
    print(f"\nDATASET STORAGE REQUIREMENTS:")
    print("-" * 40)
    for name, info in datasets.items():
        print(f"\n{name}:")
        print(f"  Description: {info['description']}")
        print(f"  Compressed: {info['compressed']:.1f} GB")
        print(f"  Extracted:  {info['extracted']:.1f} GB") 
        print(f"  Processed:  {info['processed']:.1f} GB")
    
    print(f"\nANALYSIS STORAGE REQUIREMENTS:")
    print("-" * 40)
    for name, size_gb in analysis_requirements.items():
        print(f"  {name.replace('_', ' ').title()}: {size_gb:.1f} GB")
    
    # Calculate scenarios for primary dataset
    scenarios, selected = calculate_total_requirements(datasets, analysis_requirements, ["alibaba_gpu_2020"])
    
    # Provide recommendations
    recommended_action = provide_recommendations(current_usage['free_gb'], scenarios, datasets, selected)
    
    # Space optimization suggestions
    if current_usage['free_gb'] < scenarios["with_processing"]:
        suggest_space_optimization()
    
    print(f"\n{'RECOMMENDED ACTION:'}")
    print("-" * 40)
    print(f"→ {recommended_action}")
    
    # Create download strategy
    print(f"\n{'DOWNLOAD STRATEGY:'}")
    print("-" * 40)
    if current_usage['free_gb'] >= scenarios["minimal"]:
        print("1. Start with metadata and sample data (< 1GB)")
        print("2. Complete survey for full dataset access")
        if current_usage['free_gb'] >= scenarios["full_extraction"]:
            print("3. Download and extract primary GPU 2020 dataset")
            print("4. Begin behavioral pattern analysis")
        else:
            print("3. Download compressed GPU 2020 dataset only")
            print("4. Extract sections as needed for analysis")
    else:
        print("1. Free up at least 20GB of space")
        print("2. Then proceed with download strategy")
    
    # Save assessment to file
    assessment_file = "storage_assessment.txt"
    with open(assessment_file, 'w') as f:
        f.write(f"Storage Assessment - GPU Observability Research\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"Free Space: {current_usage['free_gb']:.1f} GB\n")
        f.write(f"Primary Dataset (GPU 2020): {datasets['alibaba_gpu_2020']['extracted']:.1f} GB\n")
        f.write(f"Recommended Action: {recommended_action}\n")
    
    print(f"\n✓ Assessment saved to: {assessment_file}")

if __name__ == "__main__":
    main()