import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageChannelMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("Create BPR Mask")
        self.root.geometry("1100x600")
        self.root.configure(bg="#343541")
        self.root.iconbitmap("logo.ico")

        self.images = {"Red": None, "Green": None, "Blue": None, "Alpha": None}
        self.channel_labels = ["Red: Metallic", "Green: AO", "Blue: Height", "Alpha: Smoothness"]
        self.image_labels = {}
        self.status_var = tk.StringVar()
        self.status_var.set("")
        self.preview_size = (200, 200)
        self.output_size = None
        self.black_image = Image.new("RGBA", (1, 1), "black")

        self.create_interface()

    def create_interface(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.create_title_label()
        self.create_buttons()
        self.create_image_labels()
        self.create_generate_button()
        self.create_status_label()
        self.create_author_tab()

    def create_title_label(self):
        title_label = tk.Label(self.root, text="Image Channel Merger", font=("Helvetica", 18), bg="#343541", fg="white")
        title_label.grid(row=0, columnspan=len(self.channel_labels), pady=20)

    def create_buttons(self):
        for idx, channel in enumerate(self.channel_labels):
            button = tk.Button(self.root, text=channel, command=lambda c=channel: self.load_image(c),
                               bg="#444654", fg="white")
            button.grid(row=1, column=idx, padx=10, pady=20, sticky="n")
            self.root.columnconfigure(idx, weight=1)  # Равномерное размещение

    def create_generate_button(self):
        generate_button = tk.Button(self.root, text="Generate", command=self.generate_image, bg="#444654",
                                    fg="white", height=2)  # Установка высоты в 2 строки
        generate_button.grid(row=3, columnspan=len(self.channel_labels), padx=10, pady=20, sticky="nsew")

    def create_image_labels(self):
        for idx, channel in enumerate(self.channel_labels):
            self.image_labels[channel] = tk.Label(self.root)
            self.image_labels[channel].grid(row=2, column=idx, padx=20, pady=20)

    def create_status_label(self):
        status_label = tk.Label(self.root, textvariable=self.status_var, bg="#343541", fg="white")
        status_label.grid(row=4, columnspan=len(self.channel_labels), padx=20, pady=20)

    def create_author_tab(self):
        author_tab = tk.Frame(self.root)
        author_tab.grid(row=5, columnspan=len(self.channel_labels), padx=20, pady=20)
        self.create_author_info(author_tab)

    def create_author_info(self, parent):
        author_label = tk.Label(parent, text="Creator: Lubivy Sergei Nikolaevich", font=("Helvetica", 12), fg="white", bg="#343541")
        author_label.pack(side="left")
        year_label = tk.Label(parent, text="2023", font=("Helvetica", 12), fg="white", bg="#343541")
        year_label.pack(side="right")

    def load_image(self, channel):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            try:
                image = Image.open(file_path)
                if self.output_size is None:
                    self.output_size = image.size
                self.images[channel] = image
                self.update_image_label(channel, image)
                self.update_status("Image loaded successfully for channel {}".format(channel))
            except Exception as e:
                self.update_status("Error loading image: {}".format(str(e)))

    def update_image_label(self, channel, image):
        image.thumbnail(self.preview_size)
        photo = ImageTk.PhotoImage(image)
        self.image_labels[channel].configure(image=photo)
        self.image_labels[channel].image = photo

    def generate_image(self):
        if self.output_size is None:
            self.update_status("Please load an image first")
            return

        try:
            channels = [self.images.get(channel, self.black_image) for channel in self.channel_labels]
            resized_channels = [image.resize(self.output_size) for image in channels]
            merged_image = Image.merge("RGBA", resized_channels)

            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                try:
                    merged_image.save(save_path)
                    self.update_status("Image generated and saved successfully")
                    self.open_saved_image(save_path)
                except Exception as e:
                    self.update_status("Error generating image: {}".format(str(e)))
        except Exception as e:
            messagebox.showerror("Error", "An error occurred: {}".format(str(e)))

    def open_saved_image(self, path):
        saved_image = Image.open(path)
        saved_image.show()

    def update_status(self, message):
        self.status_var.set(message)


if __name__ == "__main__":
    root = tk.Tk()

    app = ImageChannelMerger(root)
    root.mainloop()