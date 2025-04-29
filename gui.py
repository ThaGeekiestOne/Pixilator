import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import pixelate
import os


class PixelArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art Generator")
        self.root.geometry("800x600")

        self.image_path = None
        self.pixelated_image = None
        self.pixel_size = tk.IntVar(value=8)

        self.create_widgets()

    def create_widgets(self):
        controls_frame = ttk.Frame(self.root, padding=10)
        controls_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(controls_frame, text="Select Image: ").pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="Browse", command=self.browse_file).pack(
            side=tk.LEFT
        )

        ttk.Label(controls_frame, text="Pixel Size:").pack(side=tk.LEFT, padx=10)
        self.pixel_size_entry = ttk.Entry(
            controls_frame, textvariable=self.pixel_size, width=5
        )
        self.pixel_size_entry.pack(side=tk.LEFT)

        # Enhanced Pixel Size Control
        if os.name == "nt":
            self.pixel_size_entry.bind("<MouseWheel>", self.change_pixel_size)
        elif os.name == "posix":
            self.pixel_size_entry.bind("<Button-4>", self.change_pixel_size)
            self.pixel_size_entry.bind("<Button-5>", self.change_pixel_size)
        self.pixel_size_entry.bind("<Up>", self.change_pixel_size)
        self.pixel_size_entry.bind("<Down>", self.change_pixel_size)

        ttk.Button(
            controls_frame, text="Pixelate", command=self.pixelate_and_display
        ).pack(side=tk.LEFT, padx=10)

        self.save_button = ttk.Button(
            controls_frame, text="Save", command=self.save_image
        )
        self.save_button.pack(side=tk.LEFT)
        self.save_button.config(state=tk.DISABLED)

        ttk.Button(controls_frame, text="Exit", command=self.exit_app).pack(
            side=tk.RIGHT, padx=5
        )

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def browse_file(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.*")])
        if self.image_path:
            self.display_image()

    def pixelate_and_display(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        try:
            pixel_size = self.pixel_size.get()
            if pixel_size <= 0:
                messagebox.showerror("Error", "Pixel size must be greater than 0.")
                return
            self.pixelated_image = pixelate.pixelate_image(
                self.image_path, pixel_size
            )
            self.display_image()
            self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Error pixelating image: {e}")

    def display_image(self):
        self.canvas.delete("all")
        img = (
            ImageTk.PhotoImage(self.pixelated_image)
            if self.pixelated_image
            else ImageTk.PhotoImage(Image.open(self.image_path))
        )
        self.canvas.image = img
        self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
        self.canvas.config(width=img.width(), height=img.height())

    def save_image(self):
        if self.pixelated_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
            )
            if file_path:
                try:
                    self.pixelated_image.save(file_path)
                    messagebox.showinfo("Success", "Image saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving image: {e}")
        else:
            messagebox.showwarning("Warning", "No pixelated image to save.")

    def change_pixel_size(self, event):
        """Changes pixel size with mouse wheel or arrow keys."""

        if event.type == tk.EventType.MouseWheel or event.keysym == "Up":
            self.adjust_pixel_size(1)
        elif event.type == tk.EventType.MouseWheel or event.keysym == "Down":
            self.adjust_pixel_size(-1)

    def adjust_pixel_size(self, change):
        """Adjusts pixel size within limits and updates UI."""

        current_size = self.pixel_size.get()
        new_size = max(1, min(current_size + change, 50))
        self.pixel_size.set(new_size)
        self.pixel_size_entry.icursor(tk.END)
        self.pixel_size_entry.xview(tk.END)
        self.pixelate_and_display()

    def exit_app(self):
        self.root.destroy()