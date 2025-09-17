#!/bin/bash

# Simple Cluster Data Download Script (macOS compatible)
# Uses curl instead of wget

echo "Cluster Data Download - macOS Version"
echo "====================================="

# Create directories
mkdir -p data/raw/alibaba_2018
mkdir -p data/raw/alibaba_2020
mkdir -p data/raw/google_2019

# Base URLs
ALIBABA_2018="http://aliopentrace.oss-cn-beijing.aliyuncs.com/v2018Traces"
ALIBABA_2020="http://aliopentrace.oss-cn-beijing.aliyuncs.com/v2020GPUTraces"

echo ""
echo "=== DOWNLOADING ALIBABA 2018 DATA ==="
cd data/raw/alibaba_2018

echo "1/6 Downloading machine_meta.tar.gz..."
curl -L -o machine_meta.tar.gz "${ALIBABA_2018}/machine_meta.tar.gz"

echo "2/6 Downloading machine_usage.tar.gz..."
curl -L -o machine_usage.tar.gz "${ALIBABA_2018}/machine_usage.tar.gz"

echo "3/6 Downloading container_meta.tar.gz..."
curl -L -o container_meta.tar.gz "${ALIBABA_2018}/container_meta.tar.gz"

echo "4/6 Downloading container_usage.tar.gz..."
curl -L -o container_usage.tar.gz "${ALIBABA_2018}/container_usage.tar.gz"

echo "5/6 Downloading batch_task.tar.gz..."
curl -L -o batch_task.tar.gz "${ALIBABA_2018}/batch_task.tar.gz"

echo "6/6 Downloading batch_instance.tar.gz..."
curl -L -o batch_instance.tar.gz "${ALIBABA_2018}/batch_instance.tar.gz"

cd ../../../

echo ""
echo "=== DOWNLOADING ALIBABA 2020 GPU DATA ==="
cd data/raw/alibaba_2020

echo "1/7 Downloading pai_group_tag_table.tar.gz..."
curl -L -o pai_group_tag_table.tar.gz "${ALIBABA_2020}/pai_group_tag_table.tar.gz"

echo "2/7 Downloading pai_instance_table.tar.gz..."
curl -L -o pai_instance_table.tar.gz "${ALIBABA_2020}/pai_instance_table.tar.gz"

echo "3/7 Downloading pai_job_table.tar.gz..."
curl -L -o pai_job_table.tar.gz "${ALIBABA_2020}/pai_job_table.tar.gz"

echo "4/7 Downloading pai_machine_metric.tar.gz..."
curl -L -o pai_machine_metric.tar.gz "${ALIBABA_2020}/pai_machine_metric.tar.gz"

echo "5/7 Downloading pai_machine_spec.tar.gz..."
curl -L -o pai_machine_spec.tar.gz "${ALIBABA_2020}/pai_machine_spec.tar.gz"

echo "6/7 Downloading pai_sensor_table.tar.gz..."
curl -L -o pai_sensor_table.tar.gz "${ALIBABA_2020}/pai_sensor_table.tar.gz"

echo "7/7 Downloading pai_task_table.tar.gz..."
curl -L -o pai_task_table.tar.gz "${ALIBABA_2020}/pai_task_table.tar.gz"

cd ../../../

echo ""
echo "=== CREATING GOOGLE ACCESS GUIDE ==="
cat > data/raw/google_2019/ACCESS_INSTRUCTIONS.md << 'EOF'
# Google Cluster Data 2019 Access

## Quick Access via BigQuery
1. Go to: https://console.cloud.google.com/bigquery
2. Navigate to: bigquery-public-data > google_cluster_workload_traces_v3
3. Run queries directly (free tier available)

## Key Tables for Research
- job_events: Job submission patterns
- instance_events: Resource allocation
- instance_usage: CPU, memory utilization
- machine_events: Hardware failures

## Documentation
- Repository: https://github.com/google/cluster-data
- Mailing list: googleclusterdata-discuss@googlegroups.com
EOF

echo ""
echo "=== DOWNLOAD SUMMARY ==="
echo "Checking downloaded files..."

echo ""
echo "Alibaba 2018 files:"
ls -lh data/raw/alibaba_2018/*.tar.gz 2>/dev/null || echo "No files found"

echo ""
echo "Alibaba 2020 files:"
ls -lh data/raw/alibaba_2020/*.tar.gz 2>/dev/null || echo "No files found"

echo ""
echo "Google access guide:"
ls -lh data/raw/google_2019/ACCESS_INSTRUCTIONS.md 2>/dev/null || echo "Guide not created"

echo ""
echo "=== EXTRACTION COMMANDS ==="
echo "To extract all files:"
echo "  cd data/raw/alibaba_2018 && for f in *.tar.gz; do tar -xzf \$f; done"
echo "  cd ../alibaba_2020 && for f in *.tar.gz; do tar -xzf \$f; done"

echo ""
echo "Download complete! Check file sizes above to verify successful downloads."