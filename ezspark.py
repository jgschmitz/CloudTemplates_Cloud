#!/bin/bash

# This script will help you install and set up Apache Spark using Brew.

# Step 1: Check if Brew is installed
if command -v brew >/dev/null 2>&1; then
    echo "Brew is installed. Updating Brew..."
    brew update
else
    echo "Brew is not installed. Installing Brew..."
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    echo "Brew installed successfully. Updating Brew..."
    brew update
fi

# Step 2: Install Hadoop (Optional but sometimes needed for Spark's YARN resources)
echo "Installing Hadoop..."
brew install hadoop

# Check if Java is installed
if ! command -v java >/dev/null 2>&1; then
    echo "Java is not installed. Installing Java..."
    brew install java
else
    echo "Java is already installed."
fi

# Step 3: Install Apache Spark
echo "Installing Apache Spark..."
brew install apache-spark

echo "Success: Apache Spark has been installed."
echo "You can now run 'pyspark' from the command line to start Spark."

# Optional: Steps for connecting Spark to IPython (Jupyter Notebook)

# Step 4: Download Spark manually (if you prefer not to use Brew)
echo "Downloading Spark manually from the official website..."
cd ~/Downloads
curl -O https://downloads.apache.org/spark/spark-2.0.1/spark-2.0.1-bin-hadoop2.7.tgz

# Unzip the downloaded file and rename the folder
tar xvzf spark-2.0.1-bin-hadoop2.7.tgz
mv spark-2.0.1-bin-hadoop2.7 spark2

# Step 5: Start Spark Master
cd spark2/sbin
./start-master.sh

# Check if Spark started successfully
cd ../logs
logfile=$(ls | grep master)
echo "Checking Spark master log..."
tail -f $logfile

# Step 6: Set up Spark in IPython (Jupyter Notebook)
echo "Installing findspark..."
pip install findspark

echo "Setting up Spark in IPython..."
cat <<EOF >setup_pyspark.py
import findspark
findspark.init("/Users/Satish/Downloads/spark2/")

import pyspark
from pyspark.sql import DataFrameNaFunctions
from pyspark.sql.functions import lit
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline

sc = pyspark.SparkContext(appName="helloworld")
EOF

echo "Run the 'setup_pyspark.py' script inside your IPython notebook to initialize Spark."
