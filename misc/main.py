import customtkinter as ctk
from PIL import Image
import os
import datetime
from PIL import Image

# Set appearance mode and color theme
# ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"
# ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class FoodChecker(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Foodbanked - Food Expiration Checker")
        # self.geometry("400x450")
        self.resizable(False, False)
        
        # Center the window on screen
        self.center_window()
        self.current_frame = None

        # Start with the main page
        self.show_main_page()
        
    def show_main_page(self):
        # destroy current frame if it exists
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.current_frame = self.main_frame
        # set foreground and background colors
        self.main_frame.configure(fg_color="white", bg_color="white")
        # reset month, day, year, date_type
        self.month = "Month"
        self.day = "Day"
        self.year = "Year"
        self.date_type = "Date Type"

        # Add title label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Welcome to Foodbanked!", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(30, 20))
        
        # Load and display image
        self.load_image()
        
        # Add Get Started button
        self.get_started_button = ctk.CTkButton(
            self.main_frame,
            text="Get Started",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=40,
            width=180,
            corner_radius=20,
            command=self.get_started_clicked, 
            text_color="white",
        )
        self.get_started_button.pack(pady=(30, 20))
        
        # # Add a subtitle
        # self.subtitle_label = ctk.CTkLabel(
        #     self.main_frame,
        #     text="Click the button above to begin your journey",
        #     font=ctk.CTkFont(size=12),
        #     text_color="gray"
        # )
        # self.subtitle_label.pack(pady=(0, 30))
    
    # def center_window(self):
    #     """Center the window on the screen"""
    #     self.update_idletasks()
    #     screen_width = self.winfo_screenwidth()
    #     screen_height = self.winfo_screenheight()
    #     x = ((screen_width / 2) - (400 / 2))
    #     y = ((screen_height / 2) - (450 / 2))
    #     self.geometry(f"400x450+{x}+{y}")
    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        width = 400
        height = 450
        
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        self.geometry(f"{width}x{height}+{x}+{y}")

    def load_image(self):
        """Load and display the image"""
        try:
            # Replace "your_image.jpg" with the path to your JPEG file
            image_path = "foodbank_logo.png"
            
            if os.path.exists(image_path):

                pil_image = Image.open(image_path).convert("RGBA")

                # Preserve aspect ratio while fitting within bounds
                max_width, max_height = 250, 200
                pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Convert to CTkImage
                self.image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=pil_image.size
                )
                
                # Create image label with rounded corners
                self.image_label = ctk.CTkLabel(
                    self.main_frame,
                    image=self.image,
                    text="",  # No text, just image
                    corner_radius=15
                )
                self.image_label.pack(pady=20)
            else:
                # If image not found, show placeholder
                self.placeholder_label = ctk.CTkLabel(
                    self.main_frame,
                    text="📷 Image Placeholder\n(Place your image as 'logo.jpeg')",
                    font=ctk.CTkFont(size=14),
                    width=250,
                    height=200,
                    fg_color="white",
                    corner_radius=10
                )
                self.placeholder_label.pack(pady=20)
                
        except Exception as e:
            # Error handling - show placeholder
            self.error_label = ctk.CTkLabel(
                self.main_frame,
                text=f"❌ Error loading image\n{str(e)}",
                font=ctk.CTkFont(size=12),
                width=250,
                height=200,
                fg_color="white",
                corner_radius=10
            )
            self.error_label.pack(pady=20)
    
    def create_rounded_image(self, image, radius):
        """Create rounded corners for an image"""
        # Create a mask with rounded corners
        mask = Image.new('L', image.size, 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius, fill=255)
        
        # Apply the mask to the image
        rounded_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
        rounded_image.paste(image, (0, 0))
        rounded_image.putalpha(mask)
        
        return rounded_image
    
    def get_started_clicked(self):
        """Switch to the date entry page"""
        self.main_frame.destroy()
        self.show_date_page()


    def show_second_page(self):
        """Create and show a second page with some buttons"""
        self.second_frame = ctk.CTkFrame(self)
        self.second_frame.pack(fill="both", expand=True)
        self.current_frame = self.second_frame

        self.second_frame.configure(fg_color="white", bg_color="white")

        label = ctk.CTkLabel(
            self.second_frame,
            text="Is the item in a can or jar?",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(pady=(40, 30))

        btn1 = ctk.CTkButton(self.second_frame, text="Check Food Item", height=40, width=200)
        btn1.pack(pady=10)

        btn2 = ctk.CTkButton(self.second_frame, text="Review Guidelines", height=40, width=200)
        btn2.pack(pady=10)

        self.add_back_btn(self.second_frame)
        self.add_start_over_btn(self.second_frame)

    
    def go_back(self):
        # Destroy current frame first
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        # Example logic: go back to main_frame if coming from date_frame
        if self.current_frame == self.date_frame:
            self.show_main_page()
        elif self.current_frame == self.second_frame:
            self.show_date_page()
        # Add more as needed

        else:
            # Default fallback
            self.show_main_page()

    def show_date_page(self):
        """Display a minimal date picker page with 3 dropdowns and a date type selector"""
        self.clear_frames()
        self.date_frame = ctk.CTkFrame(self)
        self.date_frame.pack(fill="both", expand=True)
        self.current_frame = self.date_frame
        self.date_frame.configure(fg_color="white", bg_color="white")

        label = ctk.CTkLabel(
            self.date_frame,
            text="Enter Date",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="black"
        )
        label.pack(pady=(40, 20))

        # Common width for dropdowns
        dropdown_width = 120

        # Month dropdown
        months = [f"{m:02}" for m in range(1, 13)]
        self.month_menu = ctk.CTkOptionMenu(self.date_frame, values=months, width=dropdown_width, text_color="white")
        self.month_menu.set(self.month)
        self.month_menu.pack(pady=10)

        # Day dropdown (limit visible height using long list)
        days = [str(d) for d in range(1, 32)]
        self.day_menu = ctk.CTkOptionMenu(self.date_frame, values=days, width=dropdown_width, text_color="white")
        self.day_menu.set(self.day)
        self.day_menu.pack(pady=10)

        # Year dropdown
        current_year = datetime.datetime.now().year
        years = [str(y) for y in range(current_year - 10, current_year + 6)]
        self.year_menu = ctk.CTkOptionMenu(self.date_frame, values=years, width=dropdown_width, text_color="white")
        self.year_menu.set(self.year)
        self.year_menu.pack(pady=10)

        # Date type dropdown
        date_types = ["Best by", "Sell by", "Use by", "Use or freeze by"]
        self.date_type_menu = ctk.CTkOptionMenu(self.date_frame, values=date_types, width=dropdown_width + 40, text_color="white")
        self.date_type_menu.set(self.date_type)
        self.date_type_menu.pack(pady=10)

        # Submit Button
        submit_btn = ctk.CTkButton(
            self.date_frame,
            text="Submit",
            height=40,
            width=95,
            command=self.submit_date,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=15,
            fg_color="#4CAF50",  # Green color
            hover_color="#45A049",
            text_color="white"
        )
        submit_btn.pack(pady=(30, 10))

        # --- Add a back button to return to the main page ---
        self.add_back_btn(self.date_frame)
        self.add_start_over_btn(self.date_frame)
 

    def clear_frames(self):
        """Destroy all visible frames before switching views"""
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

    def add_back_btn(self, frame):
        
        back_img = Image.open("back_button.png").resize((32, 32), Image.Resampling.LANCZOS)
        self.back_icon = ctk.CTkImage(light_image=back_img, dark_image=back_img, size=(32, 32))

        """Add a back button to the given frame"""
        back_btn = ctk.CTkButton(
            frame,
            text="",
            height=40,
            width=100,
            image=self.back_icon,
            command=self.go_back,
            corner_radius=10,
            fg_color="white",
            hover_color="white"
        )
        back_btn.pack(side="bottom", pady=(10, 20), anchor="sw")

    def submit_date(self):

        self.month = self.month_menu.get()
        self.day = self.day_menu.get()
        self.year = self.year_menu.get()
        self.date_type = self.date_type_menu.get()
        
        if hasattr(self, "warning_label"):
            self.warning_label.destroy()


        if self.month == "Month" or self.year == "Year":
            print("Invalid date selection")
            self.warning_label = ctk.CTkLabel(
                self.date_frame,
                text="⚠️ Please select a valid month and year.",
                text_color="red",
                font=ctk.CTkFont(size=14)
            )
            self.warning_label.pack(pady=1)
        else:
            print(f"Selected Date: {self.month}/{self.day}/{self.year} ({self.date_type})")
            self.clear_frames()
            self.show_second_page()

    def add_start_over_btn(self, frame):

        start_over_btn = ctk.CTkButton(
            frame,
            text="Start Over",
            height=32,
            width=105,
            command=self.show_main_page,
            corner_radius=8,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#4a90e2",
            hover_color="#357ABD", 
            text_color="white"    
        )
        start_over_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

def main():
    # Create and run the app
    app = FoodChecker()
    app.mainloop()

if __name__ == "__main__":
    main()