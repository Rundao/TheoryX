# Contributing to TheoryX Solver

首先，感谢你考虑为 TheoryX Solver 做出贡献！每一个贡献都会让这个工具变得更好。

[English](#contributing-guidelines) | 简体中文

## 贡献指南

### 1. 提交 Issue

- 在创建新的 Issue 前，请先搜索是否已经存在相关的 Issue
- 使用清晰的标题和详细的描述
- 如果是报告 Bug，请提供：
  - 问题的详细描述
  - 复现步骤
  - 期望的结果
  - 实际的结果
  - 环境信息（操作系统、Python版本等）
- 如果是功能建议，请说明：
  - 新功能的用途
  - 可能的实现方式
  - 为什么这个功能对项目有帮助

### 2. 提交代码

#### 开发流程

1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feature/your-feature`
3. 提交你的更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交 Pull Request

#### 代码风格

- 遵循 PEP 8 Python代码规范
- 使用有意义的变量和函数名
- 添加必要的注释和文档字符串
- 保持代码简洁清晰

#### 提交信息规范

使用清晰的提交信息，格式如下：
```
<type>(<scope>): <subject>

<body>

<footer>
```

Type 类型：
- feat: 新功能
- fix: 修复Bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

### 3. 文档贡献

- 改进现有文档
- 添加使用示例
- 修正文档错误
- 翻译文档

### 4. 测试

- 为新功能添加测试用例
- 确保所有测试通过
- 提高测试覆盖率

---

# Contributing Guidelines

Thank you for considering contributing to TheoryX Solver! Every contribution helps make this tool better.

English | [简体中文](#贡献指南)

## How to Contribute

### 1. Submitting Issues

- Search existing issues before creating a new one
- Use clear titles and detailed descriptions
- For bug reports, include:
  - Detailed problem description
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Environment information (OS, Python version, etc.)
- For feature requests, explain:
  - Purpose of the feature
  - Possible implementation
  - Why it would benefit the project

### 2. Submitting Code

#### Development Process

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a Pull Request

#### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add necessary comments and docstrings
- Keep code simple and clean

#### Commit Message Format

Use clear commit messages in this format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Testing related changes
- chore: Build process or auxiliary tool changes

### 3. Documentation Contributions

- Improve existing documentation
- Add usage examples
- Fix documentation errors
- Translate documentation

### 4. Testing

- Add test cases for new features
- Ensure all tests pass
- Improve test coverage