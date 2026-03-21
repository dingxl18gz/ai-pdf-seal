# 项目规范

本文档定义了 AI PDF Seal 项目的开发规范，所有功能实现必须遵循这些规则。

---

## 1. 运行日志规范

### 1.1 必须记录的内容

所有新功能实现必须包含以下日志：

| 日志类型 | 记录时机 | 内容要求 |
|----------|----------|----------|
| 启动日志 | 程序启动 | 配置参数、运行模式、文件路径 |
| 进度日志 | 处理过程中 | 当前进度、文件名、处理结果 |
| 汇总日志 | 处理完成 | 总数、成功数、失败数 |
| 错误日志 | 异常发生时 | 错误信息、堆栈跟踪 |

### 1.2 日志输出要求

- **同时输出到控制台和文件**
- 控制台：INFO 级别，简化格式 `[级别] 消息`
- 文件：DEBUG 级别，带时间戳 `[时间] [级别] 消息`
- 日志目录：`logs/`
- 日志文件名：`ai-pdf-seal-YYYYMMDD.log`

### 1.3 日志格式示例

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

## 2. 代码规范

### 2.1 日志实现方式

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

## 3. Git 规范

### 3.1 必须忽略的文件

```
# Python
__pycache__/
*.pyc

# 输出文件
*_sealed.pdf
output.pdf

# 日志
logs/

# IDE
.vscode/
.idea/
```

---

## 4. 文档规范

### 4.1 新功能开发流程

1. 创建 Spec 文档（`.trae/specs/<feature>/spec.md`）
2. 创建任务清单（`.trae/specs/<feature>/tasks.md`）
3. 创建验收清单（`.trae/specs/<feature>/checklist.md`）
4. 用户确认后开始实现
5. 实现完成后验证所有验收点
