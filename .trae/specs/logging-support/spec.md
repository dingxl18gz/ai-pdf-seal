# 运行日志功能规范

## 为什么需要此功能

当前程序只有基本的控制台输出，缺少详细的运行日志，不利于问题排查和运行记录追溯。需要增加结构化的日志记录功能。

## 变更内容

- 使用 Python 标准日志库 logging
- 程序启动时输出配置信息（使用的参数、配置文件路径等）
- 记录处理过程中的详细信息
- 错误时输出完整的堆栈信息
- **同时输出到控制台和日志文件**

## 日志输出

### 控制台输出

- 实时显示运行进度和关键信息
- 便于用户了解当前处理状态

### 文件输出

- 日志文件路径：`./logs/ai-pdf-seal-YYYYMMDD.log`
- 每次运行创建新日志文件（或追加到当天文件）
- 包含完整的运行信息和错误堆栈
- 便于事后排查问题

## 影响范围

- 受影响的功能：所有运行模式
- 受影响的代码：main.py

## 日志内容要求

### 程序启动日志

```
[INFO] AI PDF Seal 开始运行
[INFO] 配置文件: config.yaml
[INFO] 运行模式: 批量处理
[INFO] 目录: ./pdfs
[INFO] 印章图片: stamp.png
[INFO] 印章尺寸: 50x50
[INFO] 印章位置: (100, 100)
[INFO] 强制覆盖: True
```

### 处理过程日志

```
[INFO] 开始批量处理，共 3 个文件
[INFO] [1/3] 处理: doc1.pdf
[INFO] [1/3] 完成: doc1.pdf -> doc1_sealed.pdf
[INFO] [2/3] 处理: doc2.pdf
[INFO] [2/3] 跳过: doc2.pdf (已盖章)
[INFO] [3/3] 处理: doc3.pdf
[INFO] [3/3] 完成: doc3.pdf -> doc3_sealed.pdf
[INFO] 处理完成！总计: 3, 已处理: 2, 已跳过: 1, 失败: 0
```

### 错误日志

```
[ERROR] 处理文件失败: doc1.pdf
[ERROR] 错误信息: [具体错误描述]
[ERROR] 堆栈信息:
Traceback (most recent call last):
  ...
```

## 日志格式

- 时间戳: `[YYYY-MM-DD HH:MM:SS]`
- 日志级别: `[INFO]` / `[WARNING]` / `[ERROR]` / `[DEBUG]`
- 日志内容: 清晰的描述信息
