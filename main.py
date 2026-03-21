import argparse
import os
import sys

import yaml

from src.pdf_processor import PdfSealProcessor


DEFAULT_CONFIG_FILE = "config.yaml"


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
            print("错误: 请提供所有必需参数（image, width, height, x, y）或在配置文件中设置", file=sys.stderr)
            sys.exit(1)

        if args.directory:
            dir_path = args.directory
            if not os.path.isdir(dir_path):
                print(f"错误: 目录不存在: {dir_path}", file=sys.stderr)
                sys.exit(1)

            pdf_files = scan_directory(dir_path)

            if not pdf_files:
                print(f"目录中没有需要处理的 PDF 文件")
                return

            total = len(pdf_files)
            processed = 0
            skipped = 0
            failed = 0

            print(f"开始批量处理，共 {total} 个文件")
            print("-" * 40)

            for pdf_path in pdf_files:
                if is_already_sealed(pdf_path) and not args.force:
                    print(f"[跳过] {os.path.basename(pdf_path)} (已盖章)")
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
                    print(f"[完成] {os.path.basename(pdf_path)} -> {os.path.basename(output_path)}")
                    processed += 1
                except Exception as e:
                    print(f"[失败] {os.path.basename(pdf_path)}: {e}", file=sys.stderr)
                    failed += 1

            print("-" * 40)
            print(f"处理完成！总计: {total}, 已处理: {processed}, 已跳过: {skipped}, 失败: {failed}")

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
            print(f"成功！输出文件: {output_path}")

    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
