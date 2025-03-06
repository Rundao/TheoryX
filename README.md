# TheoryX

<div align="center">

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-Green.svg)](https://openai.com/)
[![Gradio](https://img.shields.io/badge/Gradio-UI-orange.svg)](https://gradio.app/)

大模型助力的理论力学解题助手，打造智能、高效的理论力学学习体验。

[English](README_EN.md) | 简体中文

</div>

## 🌟 特性

- **智能题目解析**：自动识别并分析题目文字和图片信息
- **专业解题过程**：遵循理论力学标准解题步骤，展示完整推导
- **LaTeX公式支持**：完美呈现数学公式和物理符号
- **双模式支持**：
  - 简单模式：快速解答基础题目
  - 复杂模式：详细分析高难度问题
- **实时解答生成**：流式输出，实时查看解题过程
- **解答文件导出**：支持导出含图片的Markdown格式解答

## 🚀 快速开始

### 环境要求

- Python 3.9+
- OpenAI API密钥
- 支持图片识别的模型（如 GPT-4V）

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/Rundao/TheoryX.git
cd TheoryX
```

2. 安装依赖：
```bash
conda create -n theoryx python=3.12
conda activate theoryx
```
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

4. 运行程序：
```bash
python main.py
```

5. 在浏览器中打开显示的地址（默认为 http://localhost:7860）

## 💡 使用指南

### 基本使用

1. 输入题目文字描述
2. 上传题目图片（如果有）
3. 选择解题模式（简单/复杂）
4. 点击"求解"开始解题
5. 查看实时生成的解答过程
6. 点击"下载"保存解答文件

### 解题模式说明

- **简单模式**：
  - 使用轻量级模型
  - 适合基础题目快速解答
  - 输出更精简的解题步骤

- **复杂模式**：
  - 使用高级模型
  - 适合复杂题目深入分析
  - 提供详细的解题思路和推导过程

## 📁 项目结构

```
theoryx/
├── backend/             # 后端逻辑
│   ├── core/           # 核心功能
│   ├── config/         # 配置管理
│   └── logger/         # 日志处理
├── frontend/           # 前端界面
│   ├── components/     # UI组件
│   └── styles/         # 样式文件
├── prompts/            # 提示词管理
└── solutions/          # 解答存储
```

## ⚙️ 配置说明

在 `.env` 文件中配置以下变量：

```bash
# API配置
OPENAI_API_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your-api-key-here

# 模型配置
SIMPLE_IMAGE_MODEL=gpt-4-vision-preview
SIMPLE_SOLVER_MODEL=gpt-3.5-turbo
COMPLEX_IMAGE_MODEL=gpt-4-vision-preview
COMPLEX_SOLVER_MODEL=gpt-4-turbo

# Gradio认证配置（可选）
GRADIO_AUTH=[{"username": "admin", "password": "admin123"}]
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来完善项目。贡献前请阅读 [贡献指南](CONTRIBUTING.md)。

### 贡献方式

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 开源协议

本项目采用 GNU General Public License v3.0 (GPLv3) 协议 - 查看 [LICENSE](LICENSE) 文件了解详细信息。

### GPLv3协议要点

1. **代码自由**：
   - 自由运行
   - 自由学习和修改
   - 自由分发
   - 自由改进和发布改进版本

2. **Copyleft特性**：
   - 修改后的版本必须以相同协议发布
   - 不允许添加额外限制

3. **透明性要求**：
   - 必须提供完整的源代码
   - 清楚标示所做的修改
   - 保持许可证完整性

4. **附加保护**：
   - 专利授权保护
   - 防止硬件限制
   - 防止与其他许可证冲突

### 使用本软件意味着你同意：

1. 如果你修改了代码，必须开源
2. 如果你分发软件，必须提供源码
3. 你编写的衍生作品也必须使用GPLv3协议
4. 你不能将本软件或其衍生品闭源销售

注意：本项目使用 GPLv3 许可证，这意味着任何使用、修改或分发本项目的行为都必须遵守 GPLv3 的条款。