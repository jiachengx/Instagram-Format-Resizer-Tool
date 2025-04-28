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
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps

# Instagram dimension presets: (label, width, height)
PRESETS = {
    "Square (1:1) 1080×1080": (1080, 1080),
    "Portrait (4:5) 1080×1350": (1080, 1350),
    "Landscape (16:9) 1080×606": (1080, 606),
}

def resize_with_transparent_bg(input_path, output_path, width, height):
    """
    Resize an image to fit within a transparent canvas of specified size,
    preserving aspect ratio and centering the result with transparent padding.
    """
    try:
        # Handle potential file opening issues
        img = Image.open(input_path).convert("RGBA")

        # Handle resampling filter based on Pillow version
        try:
            # For Pillow 9.0.0 and above
            img.thumbnail((width, height), Image.Resampling.LANCZOS)
        except AttributeError:
            # For older Pillow versions
            img.thumbnail((width, height), Image.LANCZOS)

        # Create transparent canvas
        canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        # Compute centered paste coordinates
        x = (width - img.width) // 2
        y = (height - img.height) // 2

        # Paste with alpha
        canvas.paste(img, (x, y), img)

        # Save as PNG to preserve transparency
        canvas.save(output_path, format="PNG")
        return True
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find input file: {input_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied when saving to: {output_path}")
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

# --- GUI Setup ---
def main():
    root = tk.Tk()
    root.title("Instagram Format Resizer")
    root.resizable(False, False)
    # Add padding around the main frame
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    pad = {'padx': 8, 'pady': 6}  # Increased padding slightly

    # Variables
    input_var = tk.StringVar()
    output_var = tk.StringVar()
    width_var = tk.StringVar()
    height_var = tk.StringVar()
    preset_var = tk.StringVar(value="Portrait (4:5) 1080×1350")

    # Callback: update width/height when preset changes
    def on_preset_change(*args):
        w, h = PRESETS.get(preset_var.get(), PRESETS["Portrait (4:5) 1080×1350"])
        width_var.set(str(w))
        height_var.set(str(h))

    # File selection dialogs
    def select_input():
        path = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"), ("All files", "*.*")]
        )
        if path:
            input_var.set(path)
            # Auto-suggest output path with same name but .png extension
            if not output_var.get():
                output_path = path.rsplit(".", 1)[0] + ".png"
                output_var.set(output_path)

    def select_output():
        path = filedialog.asksaveasfilename(
            title="Save as PNG (transparency)",
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )
        if path:
            # Ensure .png extension
            if not path.lower().endswith('.png'):
                path += '.png'
            output_var.set(path)

    # Process conversion
    def run_conversion():
        inp = input_var.get().strip()
        out = output_var.get().strip()

        # Validate inputs
        if not inp or not out:
            messagebox.showerror("Missing Paths", "Please select both input and output files.")
            return

        try:
            w = int(width_var.get())
            h = int(height_var.get())
            if w <= 0 or h <= 0:
                raise ValueError("Dimensions must be positive")
        except ValueError:
            messagebox.showerror("Invalid Dimensions", "Width and height must be positive integers.")
            return

        # Show processing indicator
        status_label.config(text="Processing...")
        root.update_idletasks()

        # Run conversion
        try:
            resize_with_transparent_bg(inp, out, w, h)
            status_label.config(text="Ready")
            messagebox.showinfo("Success", f"Image successfully resized!\n\nSaved: {out}\nSize: {w}×{h}px")
        except Exception as e:
            status_label.config(text="Error")
            messagebox.showerror("Error", str(e))

    # Layout widgets
    # Preset dropdown
    tk.Label(main_frame, text="Format:").grid(row=0, column=0, **pad, sticky="e")
    preset_menu = tk.OptionMenu(main_frame, preset_var, *PRESETS.keys())
    preset_menu.config(width=25)
    preset_menu.grid(row=0, column=1, columnspan=2, **pad, sticky="w")
    preset_var.trace_add('write', on_preset_change)
    on_preset_change()

    # Input selection
    tk.Label(main_frame, text="Input Image:").grid(row=1, column=0, **pad, sticky="e")
    tk.Entry(main_frame, textvariable=input_var, width=40).grid(row=1, column=1, **pad, sticky="ew")
    tk.Button(main_frame, text="Browse…", command=select_input).grid(row=1, column=2, **pad)

    # Output selection
    tk.Label(main_frame, text="Output PNG:").grid(row=2, column=0, **pad, sticky="e")
    tk.Entry(main_frame, textvariable=output_var, width=40).grid(row=2, column=1, **pad, sticky="ew")
    tk.Button(main_frame, text="Save As…", command=select_output).grid(row=2, column=2, **pad)

    # Dimensions display
    dims_frame = tk.Frame(main_frame)
    dims_frame.grid(row=3, column=0, columnspan=3, **pad)

    tk.Label(dims_frame, text="Width:").pack(side=tk.LEFT, padx=(0, 5))
    tk.Entry(dims_frame, textvariable=width_var, width=6, state='readonly').pack(side=tk.LEFT, padx=(0, 15))

    tk.Label(dims_frame, text="Height:").pack(side=tk.LEFT, padx=(15, 5))
    tk.Entry(dims_frame, textvariable=height_var, width=6, state='readonly').pack(side=tk.LEFT)

    # Convert button
    tk.Button(main_frame, text="Resize →", command=run_conversion,
              width=20, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=3, pady=12)

    # Status bar
    status_label = tk.Label(main_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_label.grid(row=5, column=0, columnspan=3, sticky="ew", **pad)

    # Make sure columns expand properly
    main_frame.columnconfigure(1, weight=1)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Launch GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()