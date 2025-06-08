#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Neo PocketMod Creator

A modern Python tool that converts standard PDFs into PocketMod format PDFs. 
A PocketMod is a small booklet created by folding a single sheet of paper, 
resulting in an 8-page mini-book.

This tool uses PyMuPDF (fitz) for robust PDF manipulation and includes 
precision margin calibration for perfect print results.
"""

import os
import sys
import argparse
import datetime
import fitz  # PyMuPDF


def check_input_file(input_file):
    """Validate input file exists and is a PDF"""
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f'Input file not found: {input_file}')
    
    if not input_file.lower().endswith('.pdf'):
        raise ValueError('Input file must be a PDF')
    
    try:
        doc = fitz.open(input_file)
        page_count = len(doc)
        doc.close()
        
        if page_count == 0:
            raise ValueError('PDF has no pages')
        
        if page_count > 8:
            print(f'\nInput PDF has {page_count} pages.')
            print('Only the first 8 pages will be converted to PocketMod format.')
        
        return page_count
        
    except Exception as e:
        raise ValueError(f'Invalid PDF file: {e}')


def create_pocketmod_pdf(input_file, output_file, margin_factor=None):
    """Create PocketMod PDF using PyMuPDF
    
    Layout pattern (corrected for proper folding):
    TOP ROW:    [Page 5↻] [Page 4↻] [Page 3↻] [Page 2↻]
    BOTTOM ROW: [Page 6] [Page 7] [Page 8] [Page 1]
    
    Where top row pages are all rotated 180°, bottom row pages are normal orientation.
    """
    
    # Open input PDF
    input_doc = fitz.open(input_file)
    input_pages = len(input_doc)
    
    print(f"Processing {input_pages} pages from input PDF...")
    
    # Output dimensions (landscape Letter: 11" × 8.5" at 72 DPI)
    output_width = 792.0   # 11 inches
    output_height = 612.0  # 8.5 inches
    
    # Create output document
    output_doc = fitz.open()  # Create new empty PDF
    output_page = output_doc.new_page(width=output_width, height=output_height)
    
    # Grid layout: 4 columns × 2 rows
    cell_width = output_width / 4   # 198 points
    cell_height = output_height / 2 # 306 points
    
    print(f"Output canvas: {output_width} × {output_height} points")
    print(f"Grid cells: {cell_width} × {cell_height} points each")
    
    # PocketMod layout mapping: (page_number, row, column, rotation_degrees)
    layout_map = [
        (5, 0, 0, 180),  # Page 5: top-left, rotated 180°
        (4, 0, 1, 180),  # Page 4: top-center-left, rotated 180°
        (3, 0, 2, 180),  # Page 3: top-center-right, rotated 180°  
        (2, 0, 3, 180),  # Page 2: top-right, rotated 180°
        (6, 1, 0, 0),    # Page 6: bottom-left, normal
        (7, 1, 1, 0),    # Page 7: bottom-center-left, normal
        (8, 1, 2, 0),    # Page 8: bottom-center-right, normal
        (1, 1, 3, 0)     # Page 1: bottom-right, normal
    ]
    
    # Calculate scaling to fit pages in cells with margin
    if input_pages > 0:
        # Get dimensions of first page to calculate scaling
        first_page = input_doc[0]
        page_rect = first_page.rect
        input_page_width = page_rect.width
        input_page_height = page_rect.height
        
        # Calculate scale to fit in cell - calibrated for optimal print margins
        # Use provided margin_factor or default calibrated value
        if margin_factor is None:
            margin_factor = 1.020  # Calibrated through physical print testing for ~3mm margins
        scale_x = (cell_width * margin_factor) / input_page_width
        scale_y = (cell_height * margin_factor) / input_page_height
        uniform_scale = min(scale_x, scale_y)  # Maintain aspect ratio
        
        print(f"Input page size: {input_page_width} × {input_page_height} points")
        print(f"Uniform scale factor: {uniform_scale:.3f}")
    else:
        uniform_scale = 1.0
    
    # Process each position in the layout
    for page_num, row, col, rotation in layout_map:
        page_index = page_num - 1  # Convert to 0-based index
        
        # Calculate target position for this cell
        target_x = col * cell_width
        target_y = row * cell_height
        
        # Calculate scaled dimensions
        if input_pages > 0:
            scaled_width = input_page_width * uniform_scale
            scaled_height = input_page_height * uniform_scale
            
            # Center within cell
            center_x = target_x + (cell_width - scaled_width) / 2
            center_y = target_y + (cell_height - scaled_height) / 2
        else:
            center_x = target_x
            center_y = target_y
            scaled_width = 0
            scaled_height = 0
        
        # Check if this page exists in input
        if page_index < input_pages:
            source_page = input_doc[page_index]
            page_type = "content"
        else:
            # Create blank page if source doesn't exist
            source_page = None
            page_type = "blank"
        
        print(f"  Page {page_num} ({page_type}) → Cell({row},{col}) at ({center_x:.0f},{center_y:.0f}), rotate {rotation}°")
        
        if source_page:
            # Create transformation matrix
            if rotation == 180:
                # For 180° rotation: rotate around center point
                # Matrix: translate to center, rotate, scale, translate to final position
                mat = fitz.Matrix(1, 0, 0, 1, center_x + scaled_width, center_y + scaled_height)  # Final position
                mat = mat * fitz.Matrix(-uniform_scale, 0, 0, -uniform_scale, 0, 0)  # Scale and rotate 180°
            else:
                # Normal orientation: scale and translate
                mat = fitz.Matrix(uniform_scale, 0, 0, uniform_scale, center_x, center_y)
            
            # Draw the source page onto output page with transformation
            # Calculate target rectangle for the transformed page
            if rotation == 180:
                target_rect = fitz.Rect(center_x, center_y, center_x + scaled_width, center_y + scaled_height)
            else:
                target_rect = fitz.Rect(center_x, center_y, center_x + scaled_width, center_y + scaled_height)
            
            output_page.show_pdf_page(
                target_rect,  # Target rectangle
                input_doc,
                page_index,
                rotate=rotation  # Apply rotation
            )
    
    # Close input document
    input_doc.close()
    
    # Save output document
    output_doc.save(output_file)
    output_doc.close()
    
    print(f"\n✅ PocketMod created successfully: {output_file}")
    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Neo PocketMod Creator - Convert PDF to PocketMod format",
        epilog="Example: python neo_pocketmod_creator.py input.pdf"
    )
    parser.add_argument('input_file', help='Input PDF file to convert')
    parser.add_argument(
        '-o', '--output', 
        help='Output file name (default: auto-generated with timestamp)'
    )
    parser.add_argument(
        '--print-margin', type=float, metavar='MM',
        help='Target print margin in millimeters (approximate, default: ~3mm)'
    )
    parser.add_argument(
        '--margin-factor', type=float, metavar='FACTOR',
        help='Direct margin factor control (default: 1.020, lower = more margin)'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate input
        page_count = check_input_file(args.input_file)
        print(f"Input: {args.input_file} ({page_count} pages)")
        
        # Generate output filename if not provided
        if args.output:
            output_file = args.output
        else:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            output_file = f'neo_pocketmod_{timestamp}.pdf'
        
        # Calculate margin_factor from CLI options
        margin_factor = None
        if args.margin_factor:
            margin_factor = args.margin_factor
            print(f"Using custom margin factor: {margin_factor}")
        elif args.print_margin:
            # Convert mm to approximate margin_factor
            # Based on calibration: 3mm ≈ 1.020, 1.5mm ≈ 1.032, linear approximation
            target_margin_mm = args.print_margin
            margin_factor = 1.050 - (target_margin_mm * 0.010)  # Approximate conversion
            print(f"Target margin: {target_margin_mm}mm → margin factor: {margin_factor:.3f}")
        
        # Create PocketMod
        success = create_pocketmod_pdf(args.input_file, output_file, margin_factor)
        
        if success:
            print(f"\n🎉 Success! Print {output_file} and fold to create your PocketMod.")
            print(f"📏 Print on Letter size paper (8.5\" × 11\") in landscape orientation.")
            return 0
        else:
            print("❌ Failed to create PocketMod")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())