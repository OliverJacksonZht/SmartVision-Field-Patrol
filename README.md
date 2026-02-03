<div align="center">

# 🌾 慧眼巡田

### 智慧农业病害检测系统

[![Python Version](https://img.shields.io/badge/python-3.12.3-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-研究用途-green.svg)](LICENSE)

基于人工智能的农作物病害识别与精准农业服务平台，助力乡村振兴

**[English](./README_EN.md) | 简体中文**

</div>

---

## 📖 项目简介

「慧眼巡田」是一个基于人工智能的农作物病害识别与精准农业服务平台。项目利用通义千问视觉大模型（qwen-vl-plus）对农作物图像进行分析，自动识别病害类型、评估严重程度，并提供专业的防治建议。

系统支持混合模式：优先使用真实 API，失败时自动回退到模拟检测模式，确保系统的可用性。

### 项目愿景

构建"流程闭环、逻辑自洽、可落地、可执行"的完整智慧农业解决方案：

> **前端巡检**：无人机影像采集与实时传输
> **后端处理**：AI 病害识别与精准方案推荐
> **服务闭环**：农资配送与交易结算
> **增值服务**：溯源认证与农产品溢价

---

## ✨ 核心功能

### 1. 图像病害识别
- 通过上传农作物图片，自动识别病害类型
- 支持水稻、小麦、玉米等多种农作物
- 基于通义千问 qwen-vl-plus 视觉大模型

### 2. 结构化诊断报告
- 病害名称识别
- 症状详细描述
- 严重程度评估（轻微/中等/严重）
- 置信度评分
- 防治建议与用药方案

### 3. 混合检测模式
- **真实 API 模式**：调用通义千问视觉 API 进行精准识别
- **模拟检测模式**：离线测试与开发环境支持
- **自动回退机制**：API 调用失败时自动切换到模拟模式

---

## 📁 项目结构

```
project/
├── src/                        # 源代码目录
│   ├── __init__.py             # 包初始化文件
│   ├── config.py               # 项目配置文件
│   ├── detectors/              # 检测器模块
│   │   ├── __init__.py
│   │   ├── mock_detector.py    # 模拟检测器
│   │   ├── qwen_detector.py    # 通义千问API检测器
│   │   └── hybrid_detector.py  # 混合检测器
│   └── utils/                  # 工具函数模块
│       └── __init__.py
├── uploads/                    # 图片上传目录
├── results/                    # 检测结果存储目录
├── tests/                      # 测试文件目录
│   └── test_rice.jpg          # 水稻测试图片
├── app.py                      # Web服务入口
├── run.py                      # 命令行运行入口
├── requirements.txt            # 项目依赖
├── AGENTS.md                   # 技术文档
├── Prospectus.md               # 项目执行手册
└── README.md                   # 项目说明文档（本文件）
```

---

## 🛠️ 技术栈

### 核心技术
- **编程语言**：Python 3.12.3
- **AI 模型**：通义千问 qwen-vl-plus 视觉大模型
- **API 服务**：阿里云 DashScope 兼容模式 API
- **Web 框架**：Flask 3.0+

### 依赖库
```
requests     # HTTP 请求库，用于调用通义千问 API
Flask        # Web 框架，提供 Web 服务
Werkzeug     # Flask 的 WSGI 工具库
urllib3      # SSL 配置
```

---

## 🚀 快速开始

### 环境要求
- Python 3.7 或更高版本（当前环境：Python 3.12.3）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行方式

#### 1. 命令行模式
```bash
# 标准运行模式
python run.py

# 测试 API 连接
python run.py test

# 仅使用模拟模式
python run.py mock
```

#### 2. Web 服务模式
```bash
# 启动 Web 服务
python app.py

# 访问地址
http://127.0.0.1:5000
```

### API 配置
设置环境变量以使用真实 API：
```bash
# Windows PowerShell
$env:QWEN_API_KEY="your_api_key_here"

# Linux/Mac
export QWEN_API_KEY="your_api_key_here"
```

---

## 🔌 Web API 接口

### 1. 病害检测接口
**POST** `/api/detect`

**请求参数**：
- `file`: 图片文件（multipart/form-data）
- `crop_type`: 作物类型（可选，默认为"水稻"）

**响应示例**：
```json
{
  "status": "success",
  "data": {
    "result": "病害识别结果...",
    "mode": "qwen",
    "details": {
      "disease": "稻瘟病",
      "severity": "中等",
      "confidence": 0.85
    },
    "crop_type": "水稻",
    "timestamp": "2026-02-03 10:30:00"
  }
}
```

### 2. 统计信息接口
**GET** `/api/stats`

**响应示例**：
```json
{
  "status": "success",
  "data": {
    "total_calls": 10,
    "success_calls": 8,
    "api_calls": 10,
    "success_rate": 80.0,
    "api_available": true
  }
}
```

---

## 💻 使用示例

### 命令行使用
```python
from src.detectors import HybridDiseaseDetector

# 创建检测器
detector = HybridDiseaseDetector(api_key="your_api_key")

# 检测图片
result = detector.detect(
    image_path="tests/test_rice.jpg",
    crop_type="水稻"
)

# 显示结果
print(result["result"])

# 保存结果
detector.save_result_to_file(result, "output.json")
```

### Web 调用示例
```bash
curl -X POST http://127.0.0.1:5000/api/detect \
  -F "file=@tests/test_rice.jpg" \
  -F "crop_type=水稻"
```

---

## 🏗️ 技术架构

### 核心类

| 类名 | 功能 |
|------|------|
| `MockDiseaseDetector` | 模拟检测器，用于离线测试 |
| `QwenDiseaseDetector` | 真实 API 检测器，调用通义千问视觉 API |
| `HybridDiseaseDetector` | 混合检测器，智能选择 API 或模拟模式 |

### 模块职责划分

| 模块 | 职责 |
|------|------|
| `src/config.py` | 项目配置管理（API密钥、路径、服务器配置等） |
| `src/detectors/` | 病害检测器实现（模拟、真实API、混合模式） |
| `src/utils/` | 通用工具函数 |
| `app.py` | Web 服务入口，处理 HTTP 请求 |
| `run.py` | 命令行工具入口，用于测试和开发 |

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

详细的开发规范请参考 [AGENTS.md](./AGENTS.md)，包括：

- 代码结构规范
- 命名规范
- 代码风格规范
- 配置管理规范
- 错误处理规范
- 目录管理规范
- Git 提交规范
- 安全规范
- 测试规范

### 项目文件说明

### 核心文件
- **`app.py`**：Web 服务入口，提供 HTTP API
- **`run.py`**：命令行工具入口，用于测试和开发
- **`src/config.py`**：项目配置管理
- **`src/detectors/`**：病害检测器实现模块

### 目录说明
- **`uploads/`**：临时存储上传的图片
- **`results/`**：存储检测结果 JSON 文件
- **`tests/`**：测试图片和测试数据

### 文档文件
- **`AGENTS.md`**：技术文档
- **`Prospectus.md`**：项目执行手册
- **`README.md`**：项目说明文档（本文件）

---

## ⚠️ 注意事项

1. **API Key 安全**：禁止将真实的 API key 硬编码在代码中
2. **网络连接**：使用真实 API 时需要稳定的网络连接
3. **图片格式**：支持 JPEG、PNG、GIF 格式
4. **SSL 证书**：当前配置为绕过 SSL 验证，生产环境应使用有效证书
5. **模拟数据**：模拟模式仅用于开发测试，结果仅供参考

---

## 💡 扩展建议

### 1. 支持更多作物
在 `src/detectors/mock_detector.py` 的 `diseases_db` 中添加新的作物类型

### 2. 添加数据库支持
- 使用 SQLite 或 PostgreSQL 存储检测历史
- 支持历史查询和统计分析

### 3. 结果可视化
- 使用 Matplotlib 生成病害分布图表
- 集成 ECharts 或 Chart.js 到 Web 前端

### 4. 热力图生成
- 结合多个检测点生成农田病害热力图
- 使用 Leaflet 或 OpenLayers 展示

### 5. 前端开发
- 开发响应式 Web 界面
- 支持移动端访问
- 实时检测进度显示

---

## 📈 项目路线图

### 当前阶段（MVP）
- ✅ 核心算法实现（病害识别）
- ✅ 混合检测模式（API + 模拟）
- ✅ 模块化代码结构
- ✅ Web 服务基础框架

### 下一阶段
- 🔄 前端 Web 界面开发
  - 开发动态网页和美观的界面设计
  - 实现响应式布局，支持多设备访问
  - 添加实时检测进度显示和结果可视化

- 🔄 多种农作物病害识别功能优化
  - 扩展支持更多常见农作物（棉花、大豆、番茄等）
  - 优化病虫害识别准确率
  - 完善病害数据库和防治建议

- 🔄 移动端界面优化（无需用户登录）
  - 针对手机和平板等移动端进行界面优化
  - 优化触摸交互体验
  - 确保移动端性能流畅

- 🔄 多模态输入输出功能
  - 支持语音输入问题描述
  - 支持摄像头直接拍摄图像识别
  - 输出支持语音播报和文字展示
  - 提升田地使用场景的易用性

### 未来规划
- 📋 开发板部署
  - 部署在嵌入式开发板上
  - 实现移动终端的联网实时识别
  - 支持离线模式（预加载模型）
  - 低功耗设计，适应田间环境

- 📋 农产品溯源认证
  - 区块链溯源技术应用
  - 农产品质量追溯系统

- 📋 农田健康保险
  - AI 评估农田健康状况
  - 对接保险公司开发农业保险产品

- 📋 电商溢价销售平台
  - 优质农产品认证体系
  - 农产品溢价销售渠道对接

---

## 📝 许可证

本项目为挑战杯参赛项目，仅供学习和研究使用。

---

<div align="center">

**用 AI 守护农田，让智慧赋能农业** 🌱

</div>