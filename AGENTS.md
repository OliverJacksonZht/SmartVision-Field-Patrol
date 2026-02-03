# 慧眼巡田 - 智慧农业病害检测系统

## 项目简介

「慧眼巡田」是一个基于人工智能的农作物病害识别与精准农业服务平台。项目利用通义千问视觉大模型（qwen-vl-plus）对农作物图像进行分析，自动识别病害类型、评估严重程度，并提供专业的防治建议。

系统支持混合模式：优先使用真实 API，失败时自动回退到模拟检测模式，确保系统的可用性。

### 项目愿景

构建"流程闭环、逻辑自洽、可落地、可执行"的完整智慧农业解决方案：
- **前端巡检**：无人机影像采集与实时传输
- **后端处理**：AI 病害识别与精准方案推荐
- **服务闭环**：农资配送与交易结算
- **增值服务**：溯源认证与农产品溢价

---

## 核心功能

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

## 项目目录结构

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
├── AGENTS.md                   # 技术文档（本文件）
├── Prospectus.md               # 项目执行手册
└── README.md                   # 项目说明文档
```

---

## 技术栈

### 核心技术
- **编程语言**：Python 3.12.3
- **AI 模型**：通义千问 qwen-vl-plus 视觉大模型
- **API 服务**：阿里云 DashScope 兼容模式 API
- **Web 框架**：Flask 3.0+

### 依赖库
```python
requests     # HTTP 请求库，用于调用通义千问 API
Flask        # Web 框架，提供 Web 服务
Werkzeug     # Flask 的 WSGI 工具库
urllib3      # SSL 配置
```

---

## 开发规范

### 1. 代码结构规范

#### 模块化原则
- 所有核心功能必须拆分为独立模块
- 每个模块只负责单一功能（单一职责原则）
- 通过 `__init__.py` 统一导出模块接口

#### 模块职责划分
| 模块 | 职责 |
|------|------|
| `src/config.py` | 项目配置管理（API密钥、路径、服务器配置等） |
| `src/detectors/` | 病害检测器实现（模拟、真实API、混合模式） |
| `src/utils/` | 通用工具函数 |
| `app.py` | Web 服务入口，处理 HTTP 请求 |
| `run.py` | 命令行工具入口，用于测试和开发 |

### 2. 命名规范

#### 文件命名
- 模块文件使用小写字母和下划线：`mock_detector.py`
- 类文件与模块名对应：`MockDiseaseDetector` 类在 `mock_detector.py`

#### 变量命名
- 变量和函数使用小写字母和下划线：`image_path`、`detect_disease()`
- 类名使用大驼峰命名：`HybridDiseaseDetector`
- 常量使用全大写字母和下划线：`QWEN_API_KEY`

### 3. 代码风格规范

#### 类型注解
- 所有函数必须包含类型注解
- 使用 `typing` 模块的类型：`Dict`、`Optional`、`List` 等

```python
def detect(self, image_path: str, crop_type: str = "水稻") -> Dict:
    """病害检测"""
    pass
```

#### 文档字符串
- 所有类和函数必须包含 docstring
- 使用 Google 风格或 NumPy 风格的 docstring

```python
def detect(self, image_path: str, crop_type: str = "水稻") -> Dict:
    """
    病害检测主函数

    Args:
        image_path: 图片路径
        crop_type: 作物类型

    Returns:
        Dict: 检测结果字典
    """
    pass
```

#### 编码规范
- 使用 UTF-8 编码处理中文内容
- 行长度不超过 88 字符（推荐使用 black 格式化）
- 导入顺序：标准库 → 第三方库 → 本地模块

### 4. 配置管理规范

#### 配置文件
- 所有配置集中在 `src/config.py` 中的 `Config` 类
- 使用类属性存储配置，使用 `@classmethod` 提供配置方法
- 敏感信息（API密钥）通过环境变量获取

```python
class Config:
    QWEN_API_KEY: str = os.getenv('QWEN_API_KEY', '')

    @classmethod
    def init_directories(cls):
        """初始化必要的目录"""
        pass
```

#### 环境变量
- 开发环境：使用 `.env` 文件（不提交到版本控制）
- 生产环境：通过系统环境变量配置

### 5. 错误处理规范

#### 异常处理
- 所有可能抛出异常的代码必须使用 try-except
- 提供清晰的错误信息，避免暴露敏感信息

```python
try:
    result = self._process_image(image_path)
    return {"status": "success", "data": result}
except FileNotFoundError:
    return {"status": "error", "message": "图片不存在"}
except Exception as e:
    return {"status": "error", "message": "处理失败"}
```

#### API 响应格式
- 统一使用 JSON 格式响应
- 成功响应：`{"status": "success", "data": ...}`
- 错误响应：`{"status": "error", "message": "..."}`

### 6. 目录管理规范

#### 文件上传
- 上传的图片存储在 `uploads/` 目录
- 使用 UUID 生成唯一文件名，避免冲突
- 定期清理过期的上传文件

#### 结果存储
- 检测结果存储在 `results/` 目录
- 结果文件使用 JSON 格式
- 文件命名：`result_<uuid>.json`

#### 测试文件
- 测试图片存储在 `tests/` 目录
- 测试文件应覆盖各种场景：健康、病害、不同作物

### 7. Git 提交规范

#### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 类型说明
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链相关

#### 示例
```
feat(detectors): 添加玉米病害识别支持

- 新增玉米病害数据库
- 更新病害识别提示词

Closes #123
```

### 8. 安全规范

#### API Key 管理
- **禁止**将 API Key 硬编码在代码中
- 使用环境变量存储敏感信息
- 将 `.env` 文件添加到 `.gitignore`

#### 文件上传安全
- 验证文件类型（扩展名 + MIME 类型）
- 限制文件大小（最大 16MB）
- 使用 `secure_filename` 处理文件名

#### SQL 注入防护
- 使用参数化查询（如需数据库）
- 禁止字符串拼接 SQL 语句

### 9. 测试规范

#### 单元测试
- 每个模块应有对应的测试文件
- 测试覆盖率不低于 80%
- 使用 pytest 测试框架

#### 集成测试
- 测试 API 接口功能
- 测试文件上传流程
- 测试错误处理逻辑

---

## 构建和运行

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

## Web API 接口

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

## 使用示例

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

## 项目文件说明

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
- **`AGENTS.md`**：技术文档（本文件）
- **`Prospectus.md`**：项目执行手册
- **`README.md`**：项目说明文档

---

## 注意事项

1. **API Key 安全**：禁止将真实的 API key 硬编码在代码中
2. **网络连接**：使用真实 API 时需要稳定的网络连接
3. **图片格式**：支持 JPEG、PNG、GIF 格式
4. **SSL 证书**：当前配置为绕过 SSL 验证，生产环境应使用有效证书
5. **模拟数据**：模拟模式仅用于开发测试，结果仅供参考

---

## 扩展建议

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

## 项目路线图

### 当前阶段（MVP）
- ✅ 核心算法实现（病害识别）
- ✅ 混合检测模式（API + 模拟）
- ✅ 模块化代码结构
- ✅ Web 服务基础框架

### 下一阶段
- 🔄 前端 Web 界面开发
- 🔄 数字孪生系统集成
- 🔄 农资供应商对接
- 🔄 用户认证与权限管理

### 未来规划
- 📋 农产品溯源认证
- 📋 农田健康保险
- 📋 电商溢价销售平台

---

## 许可证

本项目为挑战杯参赛项目，仅供学习和研究使用。