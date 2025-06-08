#!/usr/bin/env python3
"""
Visual Layout Test Script

This script tests the PocketMod layout algorithm by:
1. Converting the test input PDF to PocketMod format
2. Converting both output and target reference to images
3. Displaying results for visual comparison

Usage: python test_layout.py
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        if result.stdout:
            print(result.stdout.strip())
        return True
    except Exception as e:
        print(f"Failed to run command: {e}")
        return False

def main():
    print("Neo PocketMod Creator - Visual Layout Test")
    print("=" * 50)
    
    # Check if test files exist
    test_input = "test_files/original_plain.pdf"
    test_target = "test_files/target_plain.pdf"
    
    if not os.path.exists(test_input):
        print(f"Error: Test input file not found: {test_input}")
        return 1
        
    if not os.path.exists(test_target):
        print(f"Error: Test target file not found: {test_target}")
        return 1
    
    # Generate timestamp for output files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    test_output = f"test_output_{timestamp}.pdf"
    
    print(f"Input: {test_input}")
    print(f"Target: {test_target}")
    print(f"Output: {test_output}")
    print()
    
    # Step 1: Generate PocketMod PDF
    if not run_command(f"python neo_pocketmod_creator.py {test_input} -o {test_output}", 
                      "Generating PocketMod PDF"):
        return 1
    
    # Step 2: Convert to images for comparison
    convert_script = f'''
from pdf2image import convert_from_path
import sys

try:
    # Convert test output
    print("Converting test output to PNG...")
    output_images = convert_from_path('{test_output}', dpi=150)
    output_images[0].save('test_output_{timestamp}.png', 'PNG')
    
    # Convert target reference  
    print("Converting target reference to PNG...")
    target_images = convert_from_path('{test_target}', dpi=150)
    target_images[0].save('target_reference_{timestamp}.png', 'PNG')
    
    print("✅ Images saved successfully!")
    print("Files generated:")
    print(f"  - {test_output}")
    print(f"  - test_output_{timestamp}.png")
    print(f"  - target_reference_{timestamp}.png")
    print()
    print("Compare the images to verify layout correctness:")
    print("Expected layout:")
    print("  Top row: 5, 4, 3, 2 (all rotated 180 degrees)")
    print("  Bottom row: 6, 7, 8, 1 (normal orientation)")
    
except ImportError:
    print("Error: pdf2image not installed. Run: pip install pdf2image pillow")
    sys.exit(1)
except Exception as e:
    print(f"Error converting to images: {{e}}")
    sys.exit(1)
'''
    
    if not run_command(f'python -c "{convert_script}"', "Converting PDFs to images"):
        print("Note: Image conversion failed, but PDF was generated successfully.")
        print(f"You can manually check the PDF: {test_output}")
    
    print("\n🎉 Visual layout test completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())