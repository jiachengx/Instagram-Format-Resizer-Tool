# Instagram Format Resizer Tool

A simple, user-friendly Tkinter GUI application for resizing images to Instagram-friendly dimensions with transparent backgrounds.

## Features

- Supports three Instagram format presets:
  - Square: 1080×1080 px (1:1 ratio)
  - Portrait: 1080×1350 px (4:5 ratio) [default]
  - Landscape: 1080×606 px (16:9 ratio)
- Maintains image aspect ratio
- Centers image on transparent background
- Simple and intuitive interface

## Preview

![Instagram Format Resizer Tool](https://via.placeholder.com/600x400?text=Instagram+Format+Resizer+Preview)


## Requirements

- Python 3.x
- Pillow library (`pip install Pillow`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/instagram-format-resizer.git
   cd instagram-format-resizer
   ```

2. Install dependencies:
   ```bash
   pip install Pillow
   ```

3. Run the application:
   ```bash
   python ig_format_resizer_gui.py
   ```

## Usage

1. Select one of the three formats from the "Format" dropdown
2. Click "Browse…" next to "Input Image" to select your source image
3. Click "Save As…" next to "Output PNG" to choose the save location
   - The filename should end with `.png` to preserve transparency
4. Click the "Resize →" button to generate the resized image
5. A pop-up will confirm success or display any errors encountered

## Code

```python
"""
Instagram Format Resizer Tool
--------------------------------
Author: Stephen Hsu <jiachengx.hsu@gmail.com>

Description:
    A Tkinter-based utility designed specifically for Instagram image specifications.
    Supports three canvas presets with transparent backgrounds:
      - Square: 1080×1080 px (1:1 ratio)
      - Portrait: 1080×1350 px (4:5 ratio) [default]
      - Landscape: 1080×606 px (16:9 ratio)

Requirements:
    • Python 3.x
    • Pillow library (`pip install Pillow`)

Usage:
    1. Run the script without any arguments:
           python ig_format_resizer_gui.py

    2. In the GUI window that appears:
       • Select one of the three formats from the "Format" dropdown.
       • Click "Browse…" next to "Input Image" to select your source.
       • Click "Save As…" next to "Output PNG" to choose the save location.
         – Ensure the filename ends with `.png` to preserve transparency.
       • Click the "Resize →" button to generate the resized image.

    3. A pop-up will confirm success or display any errors encountered.

Notes:
    – The tool ignores any command-line arguments; always run it plainly.
    – The input image is converted to RGBA and scaled to fit inside the chosen canvas, preserving its aspect ratio.
    – The image is centered on a transparent canvas that exactly matches the selected Instagram dimension set.

Presets Provided:
    • Square (1:1)      : 1080 × 1080 px
    • Portrait (4:5)    : 1080 × 1350 px
    • Landscape (16:9)  : 1080 × 606 px
