# AI PDF Seal

A tool for batch adding image stamps to PDF files. Original requirements as follows:

```
Stamp the PDF file, the stamp is an image file, can control the stamp size, and can specify the position in the PDF page. Image size is a parameter, position is also a parameter. PDF files may have multiple pages, stamp each page, and the stamping position is the same on different pages.
```

## Features

- Support adding image stamps to PDF files
- Configurable stamp image size
- Customizable stamp position on PDF pages
- Multi-page PDF support - automatically adds stamps to all pages at the same position

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| --pdf, -p | No | PDF file path (mutually exclusive with --dir) |
| --dir, -d | No | Directory path (batch processing mode) |
| --image, -i | Yes | Stamp image path |
| --width | Yes | Stamp width (pixels) |
| --height | Yes | Stamp height (pixels) |
| --x | Yes | Stamp X coordinate |
| --y | Yes | Stamp Y coordinate |
| --output, -o | No | Output file path (single file mode only) |

## Usage Examples

### Basic Usage

```bash
python main.py --pdf contract.pdf --image stamp.png --width 100 --height 100 --x 400 --y 100
```

### Specify Output File

```bash
python main.py -p contract.pdf -i stamp.png --width 100 --height 100 --x 400 --y 100 -o signed_contract.pdf
```

### Batch Process Directory

```bash
python main.py -d ./pdfs -i stamp.png --width 100 --height 100 --x 400 --y 100
```

When batch processing, it automatically skips already stamped files (detects `*_sealed.pdf` files).

### Parameter Notes

- `width` and `height`: Target size of the stamp image (pixels)
- `x` and `y`: Coordinates of the stamp on the PDF page (origin (0, 0) is at the bottom-left corner)

## Use Cases

- Adding electronic seals to contract documents
- Adding certification marks to proof documents
- Batch processing multi-page PDF documents for stamping requirements

## Technology Stack

- **Python 3.8+**
- [pypdf](https://github.com/py-pdf/pypdf) - PDF file processing
- [Pillow](https://github.com/python-pillow/Pillow) - Image processing
- [reportlab](https://www.reportlab.com/) - PDF generation

## Installation

```bash
pip install -e .
```

Or run directly:

```bash
pip install pypdf Pillow reportlab
```
