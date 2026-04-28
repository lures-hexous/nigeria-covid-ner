# Nigeria COVID-19 NER Project
**Developer:** Luke78910

## Overview
This repository contains a manually curated dataset of 344 records focused on COVID-19 reporting in Nigeria. The primary goal is to train a Named Entity Recognition (NER) model to automatically identify and extract key health metrics from text reports.

##  Quick Start
To set up the environment and install dependencies on your local machine, run the following commands:

```bash
# Install all necessary Python libraries
pip install -r requirements.txt

# Download the spaCy base model for training
python3 -m spacy download en_core_web_sm
