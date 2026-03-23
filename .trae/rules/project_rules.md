# 项目规范

本文档定义了 AI PDF Seal 项目的开发规范，所有功能实现必须遵循这些规则。

---

## 1. 开发类型区分

### 1.1 使用 Spec 流程的场景

**新功能开发** - 需要详细设计的功能：

- 批量处理功能
- 配置文件功能
- 日志功能
- 任何需要明确需求、影响范围的功能

### 1.2 使用 Skill 的场景

**工具操作** - 一次性操作或工具类功能：

- 打包程序为 exe
- 生成测试文件
- 运行程序
- 代码格式化
- 其他一次性操作

---

## 2. 开发流程（文档先行）

### 2.1 新功能开发流程（使用 Spec）

1. **编写 Spec 文档** - 明确需求、变更内容、影响范围
2. **编写 Tasks 清单** - 拆解具体任务步骤
3. **编写 Checklist 验收清单** - 定义验收标准
4. **用户确认** - 确认规范后再开始实现
5. **实现代码** - 按照规范实现
6. **编写单元测试** - 确保代码质量
7. **验证通过** - 运行测试，确保所有验收点通过

### 2.2 文档命名规范

```
.trae/specs/<功能名称>/
├── spec.md      # 功能规范文档
├── tasks.md     # 任务清单
└── checklist.md # 验收清单
```

---

## 3. 运行日志规范

### 3.1 必须记录的内容

所有新功能实现必须包含以下日志：

| 日志类型 | 记录时机 | 内容要求 |
|----------|----------|----------|
| 启动日志 | 程序启动 | 配置参数、运行模式、文件路径 |
| 进度日志 | 处理过程中 | 当前进度、文件名、处理结果 |
| 汇总日志 | 处理完成 | 总数、成功数、失败数 |
| 错误日志 | 异常发生时 | 错误信息、堆栈跟踪 |

### 2.2 日志输出要求

- **同时输出到控制台和文件**
- 控制台：INFO 级别，简化格式 `[级别] 消息`
- 文件：DEBUG 级别，带时间戳 `[时间] [级别] 消息`
- 日志目录：`logs/`
- 日志文件名：`ai-pdf-seal-YYYYMMDD.log`

### 2.3 日志格式示例

```
[INFO] ==================================================
[INFO] AI PDF Seal 开始运行
[INFO] ==================================================
[INFO] 配置文件: config.yaml
[INFO] 运行模式: 批量处理
[INFO] 目录: ./pdfs
[INFO] 印章图片: stamp.png
[INFO] 印章尺寸: 50x50
[INFO] 印章位置: (100, 100)
[INFO] ==================================================
[INFO] 开始批量处理，共 3 个文件
[INFO] [1/3] 处理: doc1.pdf
[INFO] [1/3] 完成: doc1.pdf -> doc1_sealed.pdf
...
[INFO] 处理完成！总计: 3, 已处理: 2, 已跳过: 1, 失败: 0
```

---

## 4. 代码规范

### 4.1 日志实现方式

使用 Python 标准库 `logging`：

```python
import logging
from datetime import datetime

# 配置日志
def setup_logging():
    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/ai-pdf-seal-{datetime.now().strftime('%Y%m%d')}.log"

    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return logging.getLogger(__name__)

logger = setup_logging()
```

---

## 5. 单元测试规范

### 5.1 测试要求

- **所有核心功能必须有单元测试**
- 测试文件放在 `tests/` 目录
- 命名规范：`test_<模块名>.py`

### 5.2 测试框架

使用 Python 标准库 `unittest` 或 `pytest`

### 5.3 测试用例要求

| 测试类型 | 说明 |
|----------|------|
| 功能测试 | 验证核心业务逻辑正确 |
| 边界测试 | 测试边界条件和异常情况 |
| 集成测试 | 测试模块间协作 |

### 5.4 示例

```python
import unittest
from src.pdf_processor import PdfSealProcessor

class TestPdfSealProcessor(unittest.TestCase):
    def test_validate_pdf_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            processor = PdfSealProcessor(
                pdf_path="not_exist.pdf",
                image_path="stamp.png",
                width=50, height=50, x=100, y=100
            )
            processor.validate()

    def test_validate_image_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            processor = PdfSealProcessor(
                pdf_path="test.pdf",
                image_path="not_exist.png",
                width=50, height=50, x=100, y=100
            )
            processor.validate()
```

---

## 6. Git 规范

### 6.1 必须忽略的文件

```
# Python
__pycache__/
*.pyc

# 输出文件
*_sealed.pdf
output.pdf

# 日志
logs/

# 构建输出
build/
dist/
*.spec

# 测试输出
tests/__pycache__/
.pytest_cache/

# IDE
.vscode/
.idea/
```

### 6.2 提交规范

- 提交信息要清晰描述变更内容
- 每次功能完成后进行提交
- **禁止使用 `git push --force`**，避免丢失代码和修改提交记录
- 需要回退改动时，使用 `git revert` 或创建新提交来撤销
