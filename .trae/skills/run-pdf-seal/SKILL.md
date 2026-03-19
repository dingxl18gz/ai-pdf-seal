---
name: "run-pdf-seal"
description: "Runs the PDF seal program with test files. Invoke when user wants to test or run the PDF seal tool."
---

# Run PDF Seal

This skill runs the PDF seal program using the generated test files.

## What It Does

1. First generates test files if they don't exist (test.pdf, stamp.png)
2. Runs the main program to add stamp to PDF
3. Creates `test_sealed.pdf` as output

## Default Parameters

- PDF file: `test.pdf`
- Stamp image: `stamp.png`
- Width: 50
- Height: 50
- X position: 100
- Y position: 100

## Usage

Simply invoke this skill, and it will:
1. Generate test files if needed
2. Run: `python main.py --pdf test.pdf --image stamp.png --width 50 --height 50 --x 100 --y 100`
3. Output: `test_sealed.pdf`

## Technical Details

- Requires dependencies: pypdf, Pillow, reportlab
- Output location: Current working directory
