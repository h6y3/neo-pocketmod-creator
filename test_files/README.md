# Test Files

This directory contains test files used for validating the PocketMod layout algorithm.

## Files

### `original_plain.pdf`
- **Purpose**: Input test file containing 8 pages numbered 1-8
- **Content**: Simple PDF with one large number per page (1, 2, 3, 4, 5, 6, 7, 8)
- **Usage**: Used as input to test the PocketMod layout transformation

### `target_plain.pdf`
- **Purpose**: Reference file showing the correct PocketMod layout
- **Content**: Single page showing the expected 4×2 grid layout:
  - Top row: Pages 5, 4, 3, 2 (all rotated 180°)
  - Bottom row: Pages 6, 7, 8, 1 (normal orientation)
- **Usage**: Visual reference for verifying that the algorithm produces correct output

## Visual Testing Methodology

These files support a visual testing approach for the PocketMod layout:

1. **Generate Output**: Run `neo_pocketmod_creator.py` with `original_plain.pdf` as input
2. **Convert to Images**: Use `pdf2image` to convert both the generated output and `target_plain.pdf` to PNG images
3. **Visual Comparison**: Compare the generated layout against the target to verify correctness
4. **Validation**: Ensure pages appear in correct positions with proper rotation

## Development Notes

- The target layout was determined through analysis of PocketMod folding patterns
- Visual testing was essential because the layout algorithm involves precise page positioning and rotation
- These files provide a reproducible way to validate layout fixes and prevent regressions

## Dependencies for Testing

Install testing dependencies with:
```bash
pip install pdf2image pillow
```

These are included in `requirements.txt` for convenience.