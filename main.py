import argparse
import logging
import os
import sys
from datetime import datetime

import yaml

from src.pdf_processor import PdfSealProcessor


DEFAULT_CONFIG_FILE = "config.yaml"
DEFAULT_LOG_DIR = "logs"


def setup_logging():
    os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)

    log_filename = f"ai-pdf-seal-{datetime.now().strftime('%Y%m%d')}.log"
    log_path = os.path.join(DEFAULT_LOG_DIR, log_filename)

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


def is_already_sealed(pdf_path: str) -> bool:
    base, ext = os.path.splitext(pdf_path)
    sealed_path = f"{base}_sealed{ext}"
    return os.path.exists(sealed_path)


def scan_directory(dir_path: str) -> list:
    pdf_files = []
    for filename in os.listdir(dir_path):
        if filename.lower().endswith('.pdf'):
            if '_sealed' not in filename:
                pdf_files.append(os.path.join(dir_path, filename))
    return sorted(pdf_files)


def process_single(pdf_path: str, image_path: str, width: int, height: int, x: int, y: int, output_dir: str = None) -> str:
    logger.debug(f"创建 PdfSealProcessor: pdf={pdf_path}, image={image_path}, size={width}x{height}, pos=({x}, {y})")

    processor = PdfSealProcessor(
        pdf_path=pdf_path,
        image_path=image_path,
        width=width,
        height=height,
        x=x,
        y=y
    )

    if output_dir:
        filename = os.path.basename(pdf_path)
        base, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{base}_sealed{ext}")
    else:
        output_path = None

    logger.debug(f"输出路径: {output_path}")
    return processor.process(output_path)


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def merge_args_with_config(args, config: dict):
    args_dict = vars(args)

    for key, value in config.items():
        if key in args_dict and args_dict.get(key) is None:
            setattr(args, key, value)

    return args


def log_config(args):
    logger.info("=" * 50)
    logger.info("AI PDF Seal 开始运行")
    logger.info("=" * 50)
    logger.info(f"配置文件: {args.config}")

    if args.directory:
        logger.info(f"运行模式: 批量处理")
        logger.info(f"目录: {args.directory}")
    else:
        logger.info(f"运行模式: 单文件处理")
        logger.info(f"文件: {args.pdf}")

    logger.info(f"印章图片: {args.image}")
    logger.info(f"印章尺寸: {args.width}x{args.height}")
    logger.info(f"印章位置: ({args.x}, {args.y})")
    logger.info(f"强制覆盖: {args.force}")
    logger.info("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="AI PDF Seal - 给 PDF 文件添加图片印章"
    )

    parser.add_argument(
        "--config", "-c",
        default=DEFAULT_CONFIG_FILE,
        help=f"配置文件路径（默认: {DEFAULT_CONFIG_FILE}）"
    )

    parser.add_argument(
        "--pdf", "-p",
        help="PDF 文件路径"
    )
    parser.add_argument(
        "--dir", "-d",
        dest="directory",
        help="目录路径（批量处理模式）"
    )

    parser.add_argument(
        "--image", "-i",
        help="印章图片路径"
    )
    parser.add_argument(
        "--width",
        type=int,
        help="印章宽度（像素）"
    )
    parser.add_argument(
        "--height",
        type=int,
        help="印章高度（像素）"
    )
    parser.add_argument(
        "--x",
        type=int,
        help="印章 X 坐标"
    )
    parser.add_argument(
        "--y",
        type=int,
        help="印章 Y 坐标"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="强制覆盖已盖章的文件（默认跳过）"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径（仅单文件模式有效）"
    )

    args = parser.parse_args()

    config = load_config(args.config)
    args = merge_args_with_config(args, config)

    try:
        if not args.pdf and not args.directory:
            parser.print_help()
            sys.exit(1)

        if not args.image or args.width is None or args.height is None or args.x is None or args.y is None:
            logger.error("请提供所有必需参数（image, width, height, x, y）或在配置文件中设置")
            sys.exit(1)

        log_config(args)

        if args.directory:
            dir_path = args.directory
            if not os.path.isdir(dir_path):
                logger.error(f"目录不存在: {dir_path}")
                sys.exit(1)

            pdf_files = scan_directory(dir_path)

            if not pdf_files:
                logger.warning("目录中没有需要处理的 PDF 文件")
                return

            total = len(pdf_files)
            processed = 0
            skipped = 0
            failed = 0

            logger.info(f"开始批量处理，共 {total} 个文件")

            for i, pdf_path in enumerate(pdf_files, 1):
                filename = os.path.basename(pdf_path)
                logger.info(f"[{i}/{total}] 处理: {filename}")

                if is_already_sealed(pdf_path) and not args.force:
                    logger.info(f"[{i}/{total}] 跳过: {filename} (已盖章)")
                    skipped += 1
                    continue

                try:
                    output_path = process_single(
                        pdf_path,
                        args.image,
                        args.width,
                        args.height,
                        args.x,
                        args.y,
                        dir_path
                    )
                    logger.info(f"[{i}/{total}] 完成: {filename} -> {os.path.basename(output_path)}")
                    processed += 1
                except Exception as e:
                    logger.error(f"[{i}/{total}] 失败: {filename}")
                    logger.error(f"错误信息: {e}")
                    logger.exception("堆栈信息:")
                    failed += 1

            logger.info("=" * 50)
            logger.info(f"处理完成！总计: {total}, 已处理: {processed}, 已跳过: {skipped}, 失败: {failed}")

        else:
            processor = PdfSealProcessor(
                pdf_path=args.pdf,
                image_path=args.image,
                width=args.width,
                height=args.height,
                x=args.x,
                y=args.y
            )
            output_path = processor.process(args.output)
            logger.info(f"成功！输出文件: {output_path}")

    except FileNotFoundError as e:
        logger.error(f"文件不存在: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"参数错误: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"未知错误: {e}")
        logger.exception("堆栈信息:")
        sys.exit(1)


if __name__ == "__main__":
    main()
