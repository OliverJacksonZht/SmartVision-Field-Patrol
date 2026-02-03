<div align="center">

# 🌾 慧眼巡田

### 智慧农业病害检测系统

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-研究用途-green.svg)](LICENSE)

基于人工智能的农作物病害识别与精准农业服务平台，助力乡村振兴

</div>

---

## 📖 项目简介

「慧眼巡田」是一个完整的智慧农业解决方案，利用**通义千问视觉大模型**对农作物图像进行智能分析，实现：

- 🔍 **病害识别**：自动识别水稻、小麦、玉米等作物的病害类型
- 📊 **结构化诊断**：生成包含病害名称、症状描述、严重程度、置信度的详细报告
- 💡 **防治建议**：提供针对性的化学防治和农业管理建议
- 🔄 **混合模式**：支持真实 API 与模拟模式自动切换，确保系统可用性

### 核心愿景

构建"流程闭环、逻辑自洽、可落地、可执行"的智慧农业生态：

> **无人机巡检** → **AI 病害识别** → **精准方案推荐** → **农资配送** → **溯源认证**

---

## ✨ 主要功能

| 功能 | 描述 |
|------|------|
| 🖼️ 图像病害识别 | 上传农作物图片，自动识别病害类型 |
| 📋 结构化诊断报告 | 病害名称、症状、严重程度、置信度、防治建议 |
| 🌾 多作物支持 | 水稻、小麦、玉米等多种农作物 |
| 🔄 混合检测模式 | 优先使用真实 API，失败时自动回退到模拟模式 |
| 📈 统计分析 | 记录调用次数、成功率、响应时间等数据 |

---

## 🚀 快速开始

### 环境要求

- Python 3.7 或更高版本
- requests 库

### 安装依赖

```bash
pip install requests urllib3
```

### 运行项目

#### 1. 标准运行模式
```bash
python api.py
```

#### 2. 测试 API 连接
```bash
python api.py test
```

#### 3. 仅使用模拟模式
```bash
python api.py mock
```

### 配置 API Key

```bash
# Windows PowerShell
$env:QWEN_API_KEY="your_api_key_here"

# Linux/Mac
export QWEN_API_KEY="your_api_key_here"
```

---

## 📁 项目结构

```
project/
├── api.py                    # 核心算法实现
├── test_rice.jpg            # 水稻测试图片
├── result_test_rice.json    # 示例检测结果
├── AGENTS.md                # 技术文档
├── Prospectus.md            # 项目执行手册
└── README.md                # 项目说明文档（本文件）
```

---

## 💻 使用示例

### 基本使用

```python
from api import HybridDiseaseDetector

# 创建检测器
detector = HybridDiseaseDetector(api_key="your_api_key")

# 检测图片
result = detector.detect(
    image_path="test_rice.jpg",
    crop_type="水稻"
)

# 显示结果
print(result["result"])

# 保存结果
detector.save_result_to_file(result, "output.json")
```

### 仅使用模拟模式

```python
from api import HybridDiseaseDetector

detector = HybridDiseaseDetector()

result = detector.detect("test_rice.jpg", "水稻")
print(result["result"])
```

---

## 🏗️ 技术架构

### 核心类

| 类名 | 功能 |
|------|------|
| `MockDiseaseDetector` | 模拟检测器，用于离线测试 |
| `QwenDiseaseDetector` | 真实 API 检测器，调用通义千问视觉 API |
| `HybridDiseaseDetector` | 混合检测器，智能选择 API 或模拟模式 |

### 技术栈

- **编程语言**：Python 3.12.3
- **AI 模型**：通义千问 qwen-vl-plus 视觉大模型
- **API 服务**：阿里云 DashScope 兼容模式 API

---

## 📊 输出示例

```
病害识别：稻瘟病
症状描述：叶片有梭形病斑
严重程度：中等
置信度：85.30%
建议措施：使用三环唑防治
检测时间：2026-02-03 10:30:00
```

---

## 🔧 开发指南

详细的开发文档请参考：

- [AGENTS.md](./AGENTS.md) - 技术架构与开发规范
- [Prospectus.md](./Prospectus.md) - 项目执行手册

---

## 📈 项目路线图

### 当前阶段（MVP）
- ✅ 核心算法实现
- ✅ 混合检测模式
- ✅ 基础命令行工具

### 下一阶段
- 🔄 Web 后端服务开发
- 🔄 前端小程序/UI 开发
- 🔄 数字孪生系统集成

### 未来规划
- 📋 农产品溯源认证
- 📋 农田健康保险
- 📋 电商溢价销售平台

---

## 🤝 贡献

本项目为挑战杯参赛项目，欢迎提出建议和改进意见。

---

## 📝 许可证

本项目为挑战杯参赛项目，仅供学习和研究使用。

---

## 📧 联系方式

如有任何问题或建议，欢迎联系我们。

---

<div align="center">

**用 AI 守护农田，让智慧赋能农业** 🌱

</div>