# Neo PocketMod Creator

A modern Python tool that converts standard PDFs into PocketMod format PDFs. A PocketMod is a small booklet created by folding a single sheet of paper, resulting in an 8-page mini-book.

## Features

✨ **Modern Implementation**: Built with PyMuPDF for robust PDF handling  
🎯 **Precision Calibrated**: Physical print-tested for perfect fold margins  
⚙️ **Flexible Margins**: CLI options for custom margin control  
📱 **User-Friendly**: Simple command-line interface with smart defaults  
🔧 **Developer-Ready**: Direct margin factor control for fine-tuning  

## What is a PocketMod?

A PocketMod is a small booklet created by folding a single sheet of paper, resulting in an 8-page mini-book. Perfect for:
- Quick notes and to-do lists
- Mini journals or planners  
- Reference cards
- Prototyping booklet layouts

Learn more about the folding technique at [pocketmod.com](https://pocketmod.com/).

## Installation

### Requirements

- Python 3.7+
- PyMuPDF (fitz)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/neo-pocketmod-creator.git
cd neo-pocketmod-creator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Convert a PDF to PocketMod format
python neo_pocketmod_creator.py input.pdf

# Specify output filename  
python neo_pocketmod_creator.py input.pdf -o my_pocketmod.pdf
```

### Advanced Options

```bash
# Fine-tune print margins
python neo_pocketmod_creator.py input.pdf --print-margin 3.5  # 3.5mm margins
python neo_pocketmod_creator.py input.pdf --print-margin 2.0  # Tighter margins

# Direct margin factor control (for developers)
python neo_pocketmod_creator.py input.pdf --margin-factor 1.015  # Less margin
python neo_pocketmod_creator.py input.pdf --margin-factor 1.025  # More margin

# Get help
python neo_pocketmod_creator.py --help
```

### Output

The script generates a timestamped PDF file optimized for printing and folding:
- **Paper size**: Letter (8.5" × 11")
- **Orientation**: Landscape
- **Layout**: 4×2 grid with precise page placement

## How It Works

### PocketMod Layout Algorithm

Neo PocketMod Creator implements the correct PocketMod folding pattern:

```
TOP ROW:    [Page 1↻] [Page 6] [Page 7] [Page 8]
BOTTOM ROW: [Page 2]  [Page 3] [Page 4] [Page 5]
```

- **Page 1** is rotated 180° for proper orientation after folding
- **Pages 2-5** fill the bottom row in sequence  
- **Pages 6-8** fill the remaining top row positions (blank if not present)
- Each page is precisely scaled and positioned within a 4×2 grid

### Margin Calibration

**Critical for printing accuracy**: The margin system was calibrated through extensive physical print testing.

#### Default Settings
- **margin_factor = 1.020**: Provides ~3mm margins for optimal folding
- **Calibration method**: Iterative physical print tests with ruler measurements
- **Why it matters**: PocketMods require precise margins due to small folded size

#### Customization Options

**For Users** (specify in millimeters):
```bash
--print-margin 2.5  # Tighter margins for more content
--print-margin 4.0  # Looser margins for easier folding
```

**For Developers** (direct control):
```bash  
--margin-factor 1.015  # Larger pages, less margin
--margin-factor 1.025  # Smaller pages, more margin
```

#### Calibration Notes
- Lower margin_factor = larger pages, less white space
- Higher margin_factor = smaller pages, more white space
- Default 1.020 was determined through multiple print-and-measure cycles
- Physical printing is the only reliable way to verify margin accuracy

## Technical Details

### Why PyMuPDF?

Neo PocketMod Creator uses PyMuPDF (fitz) for robust PDF manipulation. This provides:
- Universal PDF compatibility 
- Reliable text rendering (no invisible content issues)
- Precise transformation handling
- Professional-grade PDF operations

### Architecture

The tool consists of three main components:

1. **Input Validation** (`check_input_file`): Ensures valid PDF input
2. **Layout Engine** (`create_pocketmod_pdf`): Implements the 4×2 grid transformation 
3. **CLI Interface** (`main`): Handles arguments and coordinates the conversion

## Development

### Project Structure

```
neo-pocketmod-creator/
├── neo_pocketmod_creator.py    # Main script
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
├── .gitignore                 # Git ignore patterns
└── samples/                   # Example files and instructions
    ├── folding_instructions.jpg
    └── example.pdf
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Testing

To test margin calibration:

1. Run the tool with your PDF
2. Print the output on Letter paper in landscape mode
3. Fold according to PocketMod instructions
4. Measure margins with a ruler
5. Adjust `--margin-factor` if needed and repeat

## Frequently Asked Questions

**Q: What if my PDF has more than 8 pages?**  
A: Only the first 8 pages will be used. The tool will warn you about this.

**Q: Can I use different paper sizes?**  
A: Currently optimized for US Letter size. Other sizes may require margin adjustments.

**Q: Why are my margins too tight/loose?**  
A: Use `--print-margin X` to adjust, where X is your target margin in millimeters.

**Q: The output looks wrong in my PDF viewer**  
A: Always test with physical printing. PDF viewers can display scaling differently than printers.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Created by Han Yuan as a modern implementation of the PocketMod concept.

The PocketMod folding technique was originally developed by [pocketmod.com](https://pocketmod.com/).