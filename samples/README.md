# Sample Files

This directory contains example files and instructions for Neo PocketMod Creator.

## Folding Instructions

1. Print the generated PDF on Letter size paper (8.5" × 11") in **landscape orientation**
2. Follow the standard PocketMod folding pattern:
   - Fold the paper in half lengthwise (hamburger fold)
   - Fold in half again (now you have 4 panels)
   - Fold once more to create 8 panels
   - Cut along the center fold line to create the booklet opening
   - Unfold and refold into booklet form

For detailed visual instructions, visit [pocketmod.com](https://pocketmod.com/).

## Testing Your Output

After folding your PocketMod:
- Check that Page 1 appears on the front cover
- Verify that pages are in correct reading order (1, 2, 3, 4, 5)
- Ensure adequate margins around text/content
- If margins are too tight/loose, use `--print-margin` to adjust

## Example Usage

```bash
# Create a sample PocketMod (replace with your PDF)
python neo_pocketmod_creator.py your_document.pdf

# Test with tighter margins
python neo_pocketmod_creator.py your_document.pdf --print-margin 2.5

# Test with looser margins  
python neo_pocketmod_creator.py your_document.pdf --print-margin 4.0
```