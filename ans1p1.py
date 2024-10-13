# Shantanu Barua, S377141
# https://github.com/Shantanu-Barua/hit137_assignment3.git

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Base class for managing the overall app layout
class BaseYouTubeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Like Interface")
        self.geometry("1000x800")  # size for display
        self._video_list = []  # Encapsulation: private attribute to store video information

        self.create_background()
        self.create_menu_bar()
        self.create_search_area()
        self.create_video_area()

    def create_background(self):
        # Adding a background image
        self.bg_image = Image.open("ans1p1_img/background_image.jpg") 
        self.bg_image = self.bg_image.resize((1000, 800), Image.LANCZOS) # Bakgroud display size
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

    def create_menu_bar(self):
        # Creating a menu bar with Home button
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        home_menu = tk.Menu(self.menu_bar, tearoff=0)
        home_menu.add_command(label="Home", command=self.show_home)  # Home button to show all videos

        self.menu_bar.add_cascade(label="Home", menu=home_menu)

    def create_search_area(self):
        # Search bar area (Encapsulation: hides UI setup)
        self.search_frame = tk.Frame(self, bg="white")
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Search Videos:", bg="white")
        self.search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_videos)
        self.search_button.pack(side=tk.LEFT, padx=5)

    def create_video_area(self):
        # Video area to display video results
        self.video_frame = tk.Frame(self, bg="white")
        self.video_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    def search_videos(self):
        
        pass

# Multiple Inheritance: Mixins for additional functionalities
class VideoLikeMixin:
    @staticmethod
    def like_video(func):
        def wrapper(self, *args, **kwargs):
            # Logic before liking the video
            print("Liking the video...")
            func(self, *args, **kwargs)
            # Logic after liking the video
            print("Video liked!")
        return wrapper

# YouTube like search functionalities 
class YouTubeApp(BaseYouTubeApp, VideoLikeMixin):
    def __init__(self):
        super().__init__()
        # Video data with titles and corresponding thumbnail image paths
        self._video_list = [
            {"title": "Cloudy Mountains", "thumbnail": "ans1p1_img/Video-1.jpeg", "Description" : "Cloudy Mountain is a majestic peak shrouded in mist, its summit often hidden from view. The dense clouds that cling to its slopes create a mysterious and ethereal atmosphere, inviting exploration and wonder."},
            {"title": "Meeting ocean", "thumbnail": "ans1p1_img/Video-2.jpeg", "Description" : "Meeting Ocean is a tranquil coastal location where the land meets the sea. The gentle lapping of waves against the shore and the salty breeze create a serene and calming atmosphere, perfect for relaxation and contemplation."},
            {"title": "Great Swamps", "thumbnail": "ans1p1_img/Video-3.jpeg", "Description" : "Great Swamps is a vast wetland area characterized by its dense vegetation and network of waterways. The swamp's unique ecosystem supports a diverse array of plant and animal life, making it a captivating and ecologically important destination."},
            {"title": "Winter lake", "thumbnail": "ans1p1_img/Video-4.jpeg", "Description" : "Winter Lake is a frozen expanse of water, its surface transformed into a shimmering sheet of ice. The surrounding landscape is often blanketed in snow, creating a peaceful and serene winter wonderland."},
            {"title": "Star lit night over mountains", "thumbnail": "ans1p1_img/Video-5.jpg", "Description" : "Starlit Night Over Mountains is a breathtaking scene where the night sky, adorned with countless stars, illuminates the majestic peaks of a mountain range. The moon casts a silvery glow, creating a magical and awe-inspiring atmosphere."},
            {"title": "Train to mountains", "thumbnail": "ans1p1_img/Video-6.jpg", "Description" : "Train to Mountains is a scenic journey that takes you through picturesque landscapes and up into the majestic mountains. The winding tracks, breathtaking views, and the anticipation of reaching the summit make it an unforgettable adventure."},
        ]
        # Display all available video suggestions initially
        self.show_home()

    def search_videos(self):
        query = self.search_entry.get()
        if query:
            self.show_videos(query)
        else:
            messagebox.showwarning("Input Error", "Please enter a search term")

    def show_videos(self, query):
        for widget in self.video_frame.winfo_children():
            widget.destroy()  # Clear previous results

        # Filter video results based on the query
        results = [video for video in self._video_list if query.lower() in video['title'].lower()]
        if results:
            for video in results:
                VideoWidget(self.video_frame, video["title"], video["thumbnail"], video["Description"])
        else:
            no_results = tk.Label(self.video_frame, text="No results found.", bg="white")
            no_results.pack()

    def show_home(self):
        #Displays all available videos when the Home button is clicked.
        self.show_videos("")

# Polymorphism: Dynamic behavior of the video widget
class VideoWidget(tk.Frame):
    def __init__(self, parent, video_title, thumbnail_path, description):
        super().__init__(parent, bg="white")
        self.video_title = video_title
        self.thumbnail_path = thumbnail_path
        self.description = description
        self.pack(pady=5, padx=5, fill=tk.X)
        self.create_widgets()

    def create_widgets(self):
        try:
            # Load and display the thumbnail
            img = Image.open(self.thumbnail_path)
            img.thumbnail((150, 100))  # Resize the image to thumbnail size
            img = ImageTk.PhotoImage(img)

            self.thumbnail_label = tk.Label(self, image=img, bg="white")
            self.thumbnail_label.image = img  # Keep reference to avoid garbage collection
            self.thumbnail_label.pack(side=tk.LEFT, padx=5)
            # Bind click event to the thumbnail to open a larger image
            self.thumbnail_label.bind("<Button-1>", self.open_video_detail)

        except Exception as e:
            print(f"Error loading image: {e}")
            self.thumbnail_label = tk.Label(self, text="Thumbnail not available", bg="white")
            self.thumbnail_label.pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(self, text=self.video_title, bg="white")
        self.label.pack(side=tk.LEFT, padx=5)

        self.like_button = tk.Button(self, text="Like", command=self.like_button_clicked, bg="white")
        self.like_button.pack(side=tk.RIGHT)
    
    def open_video_detail(self, event):
        #Open a new window showing a larger image and description.
        detail_window = tk.Toplevel(self)
        detail_window.title(self.video_title)
        detail_window.geometry("1200x600") # pop-up window size

        # Display a larger version of the image
        try:
            img = Image.open(self.thumbnail_path)
            img = img.resize((800, 400), Image.LANCZOS)  # Resize image to fit the new pop-up window
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(detail_window, image=img)
            img_label.image = img  # Keep reference to avoid garbage collection
            img_label.pack(pady=10)

        except Exception as e:
            img_label = tk.Label(detail_window, text="Video not available")
            img_label.pack(pady=10)

        # Add video description
        description_label = tk.Label(detail_window, text=f"Description: {self.description}", wraplength=400)
        description_label.pack(pady=5)

    @VideoLikeMixin.like_video
    def like_button_clicked(self):
        
        messagebox.showinfo("Liked", f"You liked {self.video_title}")

if __name__ == "__main__":
    app = YouTubeApp()
    app.mainloop()



# https://github.com/Shantanu-Barua/hit137_assignment3.git