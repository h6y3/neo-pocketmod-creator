# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Neo PocketMod Creator is a Python CLI tool that converts standard PDFs into PocketMod format PDFs. A PocketMod is a small booklet created by folding a single sheet of paper into an 8-page mini-book.

## Development Commands

### Setup and Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Tool
```bash
# Basic conversion
python neo_pocketmod_creator.py input.pdf

# With custom output name
python neo_pocketmod_creator.py input.pdf -o output.pdf

# With margin adjustments
python neo_pocketmod_creator.py input.pdf --print-margin 3.5
python neo_pocketmod_creator.py input.pdf --margin-factor 1.015
```

### Testing

#### Physical Print Testing
Physical print testing is required for margin calibration:
1. Generate a PocketMod PDF
2. Print on Letter paper in landscape mode
3. Fold according to PocketMod instructions
4. Measure margins with a ruler
5. Adjust parameters if needed

#### Visual Layout Testing
For layout algorithm development and verification:

**Quick Test (Recommended):**
```bash
python test_layout.py
```

**Manual Testing:**
```bash
# Install testing dependencies (already in requirements.txt)
pip install pdf2image pillow

# Test layout with reference files
python neo_pocketmod_creator.py test_files/original_plain.pdf -o test_output.pdf

# Convert to images for visual comparison
python -c "
from pdf2image import convert_from_path
# Convert test output
output_images = convert_from_path('test_output.pdf', dpi=150)
output_images[0].save('test_output.png', 'PNG')
# Convert target reference
target_images = convert_from_path('test_files/target_plain.pdf', dpi=150)
target_images[0].save('target_reference.png', 'PNG')
print('Images saved for visual comparison')
"
```

**Test Files in `test_files/`:**
- `original_plain.pdf`: 8-page input with numbered pages (1-8)
- `target_plain.pdf`: Reference showing correct layout arrangement
- See `test_files/README.md` for detailed documentation

## Architecture

### Core Components
1. **`check_input_file()`** - Input validation and PDF verification
2. **`create_pocketmod_pdf()`** - Main layout engine implementing the 4×2 grid transformation
3. **`main()`** - CLI interface and argument parsing

### PocketMod Layout Algorithm
The tool implements a specific page arrangement pattern:
```
TOP ROW:    [Page 5↻] [Page 4↻] [Page 3↻] [Page 2↻]
BOTTOM ROW: [Page 6]  [Page 7]  [Page 8]  [Page 1]
```
- Top row pages (5, 4, 3, 2) are all rotated 180° for proper orientation after folding
- Bottom row pages (6, 7, 8, 1) are normal orientation
- Output is Letter size (792×612 points) in landscape orientation
- Uses 4×2 grid with precise scaling and positioning

### Margin Calibration System
- **Default margin_factor**: 1.020 (calibrated for ~3mm margins)
- **User-friendly option**: `--print-margin MM` (converts mm to margin_factor)
- **Developer option**: `--margin-factor FACTOR` (direct control)
- Physical print testing was used to calibrate the default value

### Technology Stack
- **PyMuPDF (fitz)**: Primary PDF manipulation library
- **Standard library**: argparse, datetime, os, sys
- **Python 3.7+** required

## Key Implementation Details

- Uses `show_pdf_page()` with rotation for page placement
- Maintains aspect ratio with uniform scaling
- Handles PDFs with fewer than 8 pages (fills with blanks)
- Warns when input has more than 8 pages (uses first 8)
- Generates timestamped output filenames by default