# TheoryX

<div align="center">

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-Green.svg)](https://openai.com/)
[![Gradio](https://img.shields.io/badge/Gradio-UI-orange.svg)](https://gradio.app/)

An AI-powered Theoretical Mechanics Problem Solver, creating an intelligent and efficient learning experience.

English | [简体中文](README.md)

</div>

## 🌟 Features

- **Intelligent Problem Analysis**: Automatically analyze text and image information
- **Professional Solution Process**: Follow standard theoretical mechanics steps
- **LaTeX Formula Support**: Perfect rendering of mathematical formulas
- **Dual Mode Support**:
  - Simple Mode: Quick solutions for basic problems
  - Complex Mode: Detailed analysis for challenging problems
- **Real-time Generation**: Stream output for instant feedback
- **Solution Export**: Support Markdown format export with images

## 🚀 Quick Start

### Requirements

- Python 3.9+
- OpenAI API Key
- Vision-capable model (e.g., GPT-4V)

### Installation

1. Clone repository:
```bash
git clone https://github.com/Rundao/TheoryX.git
cd TheoryX
```

2. Install dependencies:
```bash
conda create -n theoryx python=3.12
conda activate theoryx
```
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env file with required configuration
```

4. Run the program:
```bash
python main.py
```

5. Open displayed address in browser (default: http://localhost:7860)

## 💡 Usage Guide

### Basic Usage

1. Enter problem description
2. Upload problem image (if any)
3. Select solving mode (Simple/Complex)
4. Click "Solve" to start
5. View real-time solution generation
6. Click "Download" to save solution

### Solving Modes

- **Simple Mode**:
  - Uses lightweight models
  - Suitable for basic problems
  - Outputs concise solution steps

- **Complex Mode**:
  - Uses advanced models
  - Suitable for complex problems
  - Provides detailed reasoning and derivation

## 📁 Project Structure

```
theoryx-solver/
├── backend/             # Backend logic
│   ├── core/           # Core functionality
│   ├── config/         # Configuration
│   └── logger/         # Logging
├── frontend/           # Frontend interface
│   ├── components/     # UI components
│   └── styles/         # Style files
├── prompts/            # Prompt management
└── solutions/          # Solution storage
```

## ⚙️ Configuration

Configure the following variables in `.env` file:

```bash
# API Configuration
OPENAI_API_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your-api-key-here

# Model Configuration
SIMPLE_IMAGE_MODEL=gpt-4-vision-preview
SIMPLE_SOLVER_MODEL=gpt-3.5-turbo
COMPLEX_IMAGE_MODEL=gpt-4-vision-preview
COMPLEX_SOLVER_MODEL=gpt-4-turbo

# Gradio Auth (Optional)
GRADIO_AUTH=[{"username": "admin", "password": "admin123"}]
```

## 🤝 Contributing

Welcome to submit Issues and Pull Requests. Please read [Contributing Guidelines](CONTRIBUTING.md) before contributing.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 (GPLv3) - see [LICENSE](LICENSE) file for details.

GPLv3 is a copyleft license that ensures software remains free and open source. This means any derivative works must also be distributed under the same license terms.

By using this software, you agree to:
1. Keep it Open Source: Any modifications and derivative works must be released under GPLv3
2. State Changes: Clearly indicate any changes you've made
3. License Integrity: Include the complete license
4. Patent Grant: Users receive patent rights for using the code

Note: This project uses the GPLv3 license, which means any use, modification, or distribution of this project must comply with GPLv3 terms.