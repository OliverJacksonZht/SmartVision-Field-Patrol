<div align="center">

# 🌾 SmartVision Field Patrol

### AI-Powered Crop Disease Detection System

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Educational%20Use-green.svg)](LICENSE)

An intelligent crop disease recognition and precision agriculture service platform powered by AI

**English | [简体中文](./README.md)**

</div>

---

## 📖 Project Overview

**SmartVision Field Patrol** is a complete smart agriculture solution that leverages the **Qwen Vision Large Model** (qwen-vl-plus) to intelligently analyze crop images and provide:

- 🔍 **Disease Recognition**: Automatically identify disease types for rice, wheat, corn, and other crops
- 📊 **Structured Diagnosis**: Generate detailed reports including disease name, symptoms, severity, and confidence scores
- 💡 **Control Recommendations**: Provide targeted chemical control and agricultural management suggestions
- 🔄 **Hybrid Detection Mode**: Supports automatic switching between real API and mock mode to ensure system availability

### Core Vision

Building a "closed-loop, logically coherent, actionable, and executable" smart agriculture ecosystem:

> **Drone Inspection** → **AI Disease Recognition** → **Precision Recommendations** → **Agricultural Supply Delivery** → **Traceability Certification**

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🖼️ Image Disease Detection | Upload crop images to automatically identify disease types |
| 📋 Structured Diagnostic Reports | Disease name, symptoms, severity, confidence, and control recommendations |
| 🌾 Multi-Crop Support | Rice, wheat, corn, and other crops |
| 🔄 Hybrid Detection Mode | Prioritize real API, fallback to mock mode on failure |
| 📈 Statistical Analysis | Track call counts, success rates, response times, and other metrics |

---

## 🚀 Quick Start

### Requirements

- Python 3.7 or higher
- requests library

### Install Dependencies

```bash
pip install requests urllib3
```

### Run Project

#### 1. Standard Mode
```bash
python api.py
```

#### 2. Test API Connection
```bash
python api.py test
```

#### 3. Mock Mode Only
```bash
python api.py mock
```

### Configure API Key

```bash
# Windows PowerShell
$env:QWEN_API_KEY="your_api_key_here"

# Linux/Mac
export QWEN_API_KEY="your_api_key_here"
```

---

## 📁 Project Structure

```
project/
├── src/                        # Source code directory
│   ├── config.py               # Project configuration
│   ├── detectors/              # Detector modules
│   │   ├── mock_detector.py    # Mock detector
│   │   ├── qwen_detector.py    # Qwen API detector
│   │   └── hybrid_detector.py  # Hybrid detector
│   └── utils/                  # Utility functions
├── uploads/                    # Image upload directory
├── results/                    # Detection result storage
├── tests/                      # Test files directory
│   └── test_rice.jpg          # Rice test image
├── app.py                      # Web service entry
├── run.py                      # Command-line tool
├── requirements.txt            # Project dependencies
├── AGENTS.md                   # Technical documentation
├── Prospectus.md               # Project execution manual
├── README.md                   # Project documentation (Chinese)
└── README_EN.md                # English documentation (this file)
```

---

## 💻 Usage Examples

### Basic Usage

```python
from api import HybridDiseaseDetector

# Create detector
detector = HybridDiseaseDetector(api_key="your_api_key")

# Detect disease
result = detector.detect(
    image_path="test_rice.jpg",
    crop_type="水稻"
)

# Display result
print(result["result"])

# Save result
detector.save_result_to_file(result, "output.json")
```

### Mock Mode Only

```python
from api import HybridDiseaseDetector

detector = HybridDiseaseDetector()

result = detector.detect("test_rice.jpg", "水稻")
print(result["result"])
```

---

## 🏗️ Technical Architecture

### Core Classes

| Class Name | Function |
|------------|----------|
| `MockDiseaseDetector` | Mock detector for offline testing |
| `QwenDiseaseDetector` | Real API detector calling Qwen Vision API |
| `HybridDiseaseDetector` | Hybrid detector intelligently choosing API or mock mode |

### Tech Stack

- **Programming Language**: Python 3.12.3
- **AI Model**: Qwen qwen-vl-plus Vision Large Model
- **API Service**: Alibaba Cloud DashScope Compatible Mode API

---

## 📊 Output Example

```
Disease: Rice Blast
Symptoms: Fusiform spots on leaves
Severity: Moderate
Confidence: 85.30%
Recommendation: Use tricyclazole for control
Detection Time: 2026-02-03 10:30:00
```

---

## 🔧 Development Guide

For detailed development documentation, please refer to:

- [AGENTS.md](./AGENTS.md) - Technical Architecture and Development Standards
- [Prospectus.md](./Prospectus.md) - Project Execution Manual

---

## 📈 Project Roadmap

### Current Phase (MVP)
- ✅ Core algorithm implementation
- ✅ Hybrid detection mode
- ✅ Basic command-line tools

### Next Phase
- 🔄 Web backend service development
- 🔄 Frontend mini-program/UI development
- 🔄 Digital twin system integration

### Future Plans
- 📋 Agricultural product traceability certification
- 📋 Crop health insurance
- 📋 E-commerce premium sales platform

---

## 🤝 Contributing

This project is for Challenge Cup competition. Suggestions and improvements are welcome.

---

## 📝 License

This project is for Challenge Cup competition and is intended for educational and research purposes only.

---

## 📧 Contact

If you have any questions or suggestions, please feel free to contact us.

---

<div align="center">

**Protecting Farmland with AI, Empowering Agriculture with Intelligence** 🌱

</div>