import customtkinter as ctk
from PIL import Image
import datetime
import os
from food_data import food_items

# Set up theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class FoodbankApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.center_window()
        self.title("Foodbanked")
        self.configure(fg_color="white")
        self.current_frame = None

        self.page_history = []
        self.current_frame_args = ()
        self.current_frame_kwargs = {}
        self.last_search_query = None

        arrow_img = Image.open("assets/back_button.png").resize((32, 32), Image.Resampling.LANCZOS)
        self.back_icon = ctk.CTkImage(light_image=arrow_img, dark_image=arrow_img, size=(32, 32))

        self.logo_path = "assets/new_fb_logo_transparent.png"
        self.show_main_page()

    def center_window(self, width=500, height=500):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_main_page(self):
        self.page_history = []
        self.current_frame_args = ()
        self.current_frame_kwargs = {}
        self.last_search_query = None
        self.switch_frame(MainPage, record_history=False)


    def perform_search(self):
        query = self.search_var.get().strip().lower()
        if not query:
            return

        self.last_search_query = query
        matches = [
            (key, data["label"], data["shelf_life_years"], data["shelf_life_display"])
            for key, data in food_items.items()
            if query in data["label"].lower()
        ]

        self.switch_frame(SearchResultsPage, matches, query=query)


    def load_image(self):
        if os.path.exists(self.logo_path):
            img = Image.open(self.logo_path).convert("RGBA")
            img.thumbnail((250, 200), Image.Resampling.LANCZOS)
            self.logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            logo = ctk.CTkLabel(self.main_frame, image=self.logo_img, text="")
            logo.pack(pady=10)


    def switch_frame(self, frame_class, *args, record_history=True, **kwargs):
        if self.current_frame is not None:
            if record_history:
                self.page_history.append((self.current_frame.__class__, self.current_frame_args, self.current_frame_kwargs))
            self.current_frame.destroy()

        self.current_frame_args = args
        self.current_frame_kwargs = kwargs

        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)


    def show_category_page(self):
        self.switch_frame(CategoryPage)


    def add_back_button(self, frame, command):
        back_btn = ctk.CTkButton(
            frame,
            text="",
            image=self.back_icon,
            width=36,
            height=36,
            corner_radius=18,
            command=command,
            fg_color="white",
            hover_color="white",
        )
        back_btn.place(relx=0.0, rely=1.0, x=20, y=-20, anchor="sw")


    def add_start_over_button(self, frame):
        start_btn = ctk.CTkButton(
            frame,
            text="Start Over",
            width=100,
            height=36,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_main_page,
            corner_radius=10,
            fg_color="#4a90e2",
            hover_color="#357ABD",
            text_color="white"
        )
        start_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")


    def go_back(self):
        if self.page_history:

            frame_class, args, kwargs = self.page_history.pop()
            self.switch_frame(frame_class, *args, **kwargs, record_history=False)

        else:
            self.show_main_page()


class MainPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")

        ctk.CTkLabel(
            self,
            text="Welcome to Foodbanked!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="black"
        ).pack(pady=(30, 20))

        if os.path.exists(master.logo_path):
            img = Image.open(master.logo_path).convert("RGBA")
            img.thumbnail((250, 200), Image.Resampling.LANCZOS)
            master.logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            logo = ctk.CTkLabel(self, image=master.logo_img, text="")
            logo.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Get Started",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=40,
            width=180,
            corner_radius=20,
            text_color="white",
            fg_color="#4a90e2",
            hover_color="#357ABD",
            command=master.show_category_page
        ).pack(pady=(30, 20))

        master.search_var = ctk.StringVar(value=master.last_search_query or "")
        # Save the entry as an attribute so we can bind to it
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search for a food item...",
            textvariable=master.search_var,
            width=300
        )
        self.search_entry.pack(pady=(10, 5))

        # 🔑 Bind Enter key to trigger search
        self.search_entry.bind("<Return>", lambda event: master.perform_search())

        ctk.CTkButton(
            self,
            text="Search",
            command=master.perform_search,
            width=100,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            fg_color="#4a90e2",
            hover_color="#357ABD",
            text_color="white"
        ).pack()


class SearchResultsPage(ctk.CTkFrame):
    def __init__(self, master, results, query=None):
        super().__init__(master)
        self.configure(fg_color="white")

        self.master = master
        self.results = results or []
        self.query = query or ""
        self.per_page = 8
        self.current_page = 0

        if self.query:
            master.last_search_query = self.query

        # Title
        ctk.CTkLabel(
            self,
            text="Search Results",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

        # Results container (fixed position)
        self.results_container = ctk.CTkFrame(self, fg_color="white")
        # self.results_container.pack(expand=True)
        self.results_container.pack(fill="both", expand=True, anchor="n")

        # Navigation arrows below results
        self.nav_container = ctk.CTkFrame(self, fg_color="white")
        self.nav_container.pack(pady=(10, 20))

        self.prev_button = ctk.CTkButton(
            self.nav_container,
            text="<",
            width=40,
            height=30,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="black",
            fg_color="white",
            hover_color="#e0e0e0",
            command=self.prev_page
        )
        self.prev_button.grid(row=0, column=0, padx=10)

        self.next_button = ctk.CTkButton(
            self.nav_container,
            text=">",
            width=40,
            height=30,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="black",
            fg_color="white",
            hover_color="#e0e0e0",
            command=self.next_page
        )
        self.next_button.grid(row=0, column=1, padx=10)

        # Back and Start Over
        master.add_back_button(self, command=master.go_back)
        master.add_start_over_button(self)

        # First draw
        self.update_results()

    def update_results(self):
        # Clear current results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        # Get current page slice
        start = self.current_page * self.per_page
        end = start + self.per_page
        page_results = self.results[start:end]

        for key, label, years, display in page_results:
            ctk.CTkButton(
                self.results_container,
                text=label,
                width=360,
                font=ctk.CTkFont(size=14),
                command=lambda k=key, y=years, l=label, d=display: self.master.switch_frame(ResultPage, k, l, y, d)
            ).pack(pady=5)

        # Enable/disable arrows
        total_pages = (len(self.results) - 1) // self.per_page
        self.prev_button.configure(state="normal" if self.current_page > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_page < total_pages else "disabled")

    def next_page(self):
        if self.current_page < (len(self.results) - 1) // self.per_page:
            self.current_page += 1
            self.update_results()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_results()


class CategoryPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")

        label = ctk.CTkLabel(self, text="Select Product Category:", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        categories = [
            ("Shelf-Stable", ShelfStablePage),
            ("Refrigerated", RefrigeratedPage),
            ("Frozen", FrozenPage),
            ("Fresh Produce", ProducePage),
            ("Baby Food", BabyFoodPage)
        ]

        for text, target in categories:
            btn = ctk.CTkButton(
                self,
                text=text,
                height=40,
                width=200,
                font=ctk.CTkFont(size=16),
                command=lambda t=target: master.switch_frame(t)
            )
            btn.pack(pady=8)

        master.add_back_button(self, command=master.show_main_page)
        master.add_start_over_button(self)


class ShelfStablePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")

        ctk.CTkLabel(self, text="Shelf-Stable Subcategories", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        categories = [
            ("Canned / Jarred", ContainsTomatoesPage),
            ("Dry Goods", DryGoodsPage),
            ("Beverages", BeveragesPage),
            ("Condiments / Sauces / Syrups", CondimentsPage),
        ]

        for text, page in categories:
            ctk.CTkButton(
                self,
                text=text,
                width=250,
                height=40,
                font=ctk.CTkFont(size=14),
                command=lambda p=page: master.switch_frame(p)
            ).pack(pady=6)

        master.add_back_button(self, command=lambda: master.switch_frame(CategoryPage))
        master.add_start_over_button(self)


class ContainsTomatoesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")

        # Question text
        ctk.CTkLabel(
            self,
            text="Does the item contain tomatoes?",
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="center"
        ).pack(pady=(40, 20))
        
        label = "Canned / Jarred Tomato Products"
        matching_key = "canned_jarred_tomato_products"
        # Yes Button → Go to ResultsPage
        ctk.CTkButton(
            self,
            text="Yes",
            width=200,
            font=ctk.CTkFont(size=16),
            command=lambda k=matching_key, l=label, d="18 months", y=1.5: master.switch_frame(ResultPage, k, l, y, d)
            # command=lambda: master.switch_frame(ResultPage)
        ).pack(pady=10)

        # No Button → Go to CannedJarredPage
        ctk.CTkButton(
            self,
            text="No",
            width=200,
            font=ctk.CTkFont(size=16),
            command=lambda: master.switch_frame(CannedJarredPage)
        ).pack(pady=10)

        # Optional: Add navigation buttons
        master.add_back_button(self, command=lambda: master.switch_frame(ShelfStablePage))
        master.add_start_over_button(self)


class CannedJarredPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")

        ctk.CTkLabel(
            self,
            text="Canned / Jarred Items",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))

        canned_items = [
            (item["label"], item["shelf_life_years"]) 
            for item in food_items.values() 
            if item.get("subcategory") == "Canned / Jarred" and item.get("label") != "Canned / Jarred Tomato Products"
        ]

        for label, years in canned_items:
            # find the key from the label
            matching_key = next(
                (k for k, v in food_items.items() if v["label"] == label), 
                None
            )
            if not matching_key:
                continue  # skip if key not found
            d = food_items[matching_key].get("shelf_life_display", f"{years:.2f} years")

            ctk.CTkButton(
                self,
                text=label,
                width=350,
                font=ctk.CTkFont(size=14),
                command=lambda k=matching_key, l=label, d=d, y=years: master.switch_frame(ResultPage, k, l, y, d)
            ).pack(pady=4)

        master.add_back_button(self, command=lambda: master.switch_frame(ShelfStablePage))
        master.add_start_over_button(self)


class ResultPage(ctk.CTkFrame):
    def __init__(self, master, key, item_name, shelf_life_years, shelf_life_display=None):
        super().__init__(master)
        self.configure(fg_color="white")
        self.item_name = item_name
        # Get the subcategory from the dictionary
        self.subcategory = food_items.get(key, {}).get("subcategory", "Unknown")

        # print(f"subcategory: {self.subcategory}")

        self.shelf_life_years = shelf_life_years
        self.shelf_life_display = shelf_life_display or f"{shelf_life_years:.2f} years"
        self.master = master

        text = self.item_name

        # Split at the first " ("
        if " (" in text:
            before_paren, after_paren = text.split(" (", 1)
            formatted_text = f"{before_paren}\n({after_paren}"
        else:
            formatted_text = text

        ctk.CTkLabel(
            self,
            text=formatted_text,
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="center",  # center multiline lines
            anchor="center"    # center in the widget itself
        ).pack(pady=(30, 15))

        # Store variables for checkboxes
        self.check_vars = []
        self.questions = self.get_questions(item_name, self.subcategory)
        self.build_question_form()

        master.add_back_button(self, command=master.go_back)
        master.add_start_over_button(self)

    def get_questions(self, item_name, subcategory):
        """Return a list of yes/no safety questions based on item category"""
        lower = item_name.lower()
        if "canned" in subcategory.lower() or "jarred" in subcategory.lower():
            return [
                "Is the can rusted?",
                "Is there any leakage?",
                "Is the rim dented?"
            ]
        elif "jar" in lower or "jarred" in lower:
            return [
                "Is the seal broken?",
                "Is there any leakage?",
                "Is the lid bulging?"
            ]
        elif "baby food" in lower:
            return [
                "Is the packaging damaged?",
                "Is the safety seal broken?"
            ]
        elif "dry goods" in subcategory.lower():
            return [
                "Is the packaging damaged?",
                "Is there any sign of pests?",
                "Is the product discolored or has an off smell?"
            ]
        elif "beverage" in subcategory.lower():
            return [
                "Is the packaging damaged?",
                "Is there any leakage?",
                "Is the product discolored or has an off smell?"
            ]
        else:
            return []  # No extra questions for other types

    # def build_question_form(self):
    def build_question_form(self):
        if self.questions:
            ctk.CTkLabel(
                self,
                text="Please inspect the item:",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=(10, 10))

            container = ctk.CTkFrame(self, fg_color="transparent")
            container.pack(pady=(5, 10), fill="x")

            self.check_vars = []

            for q in self.questions:
                var = ctk.BooleanVar(value=False)

                # Wrap checkbox in a narrow frame to prevent stretching
                frame = ctk.CTkFrame(container, fg_color="transparent", width=300)
                frame.pack(fill="x", pady=2, padx=40)

                checkbox = ctk.CTkCheckBox(
                    frame,
                    text=q,
                    variable=var,
                    font=ctk.CTkFont(size=14)
                )
                checkbox.pack(anchor="w")

                self.check_vars.append(var)

            ctk.CTkButton(
                self,
                text="Submit Answers",
                command=self.evaluate_answers,
                fg_color="#4a90e2",
                hover_color="#357ABD",
                text_color="white"
            ).pack(pady=(20, 10))

        else:
            self.show_shelf_life_result()

    def evaluate_answers(self):
        if any(var.get() for var in self.check_vars):
            # If any issues found, show discard message
            self.show_discard_message()
        else:
            self.show_shelf_life_result()

    def show_discard_message(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self,
            text="⚠️ Discard Item",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="red"
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self,
            text="This item is not safe for donation\nbased on your answers.",
            font=ctk.CTkFont(size=16),
            text_color="red",
            justify="center"
        ).pack(pady=(5, 20))

        self.master.add_back_button(self, command=self.master.go_back)
        self.master.add_start_over_button(self)

    def show_shelf_life_result(self):
        for widget in self.winfo_children():
            widget.destroy()

        today = datetime.date.today()
        # if self.shelf_life_years is infinite, set is_infinite to True
        is_infinite = self.shelf_life_years == float('inf')
        if not is_infinite:
            shelf_life_days = int(self.shelf_life_years * 365)
            cutoff_date = today - datetime.timedelta(days=shelf_life_days)

        if " (" in self.item_name:
            before_paren, after_paren = self.item_name.split(" (", 1)
            display_text = f"{before_paren}\n({after_paren}"
        else:
            display_text = self.item_name

        # Create label with centered multiline text
        ctk.CTkLabel(
            self,
            text=display_text,
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="center",
            anchor="center"
        ).pack(pady=(30, 15))

        ctk.CTkLabel(
            self,
            # text=f"Recommended Shelf Life: {self.shelf_life_years:.2f} years\n"
            text=f"Recommended Shelf Life: {self.shelf_life_display}\n"
                 f"✅ Acceptable if date on package is on or after:" if not is_infinite else "✅ Product is acceptable",
            font=ctk.CTkFont(size=16),
            text_color="green",
            justify="center"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self,
            text=cutoff_date.strftime('%B %d, %Y') if not is_infinite else "Indefinite Shelf Life",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="green"
        ).pack(pady=(0, 20))

        self.master.add_back_button(self, command=self.master.go_back)
        self.master.add_start_over_button(self)


class DryGoodsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")
        
        ctk.CTkLabel(
            self, 
            text="Dry Goods", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))
        
        # Get all unique sub_sub_categories from dry goods items
        sub_sub_categories = list(set(
            item.get("sub_sub_category", "")
            for item in food_items.values()
            if item.get("subcategory") == "Dry Goods" and item.get("sub_sub_category")
        ))
        
        # Sort the categories for consistent display
        sub_sub_categories.sort()
        
        # Create frame for buttons
        btn_frame = ctk.CTkFrame(self, fg_color="white")
        btn_frame.pack(pady=10, padx=20, fill="x")
        
        # Create two columns by splitting the list roughly in half
        half = (len(sub_sub_categories) + 1) // 2
        col1 = sub_sub_categories[:half]
        col2 = sub_sub_categories[half:]
        
        # Use grid layout for two columns
        for row_index in range(half):
            if row_index < len(col1):
                btn1 = ctk.CTkButton(
                    btn_frame,
                    text=col1[row_index],
                    font=ctk.CTkFont(size=16),
                    command=lambda s=col1[row_index]: self.go_to_sub_sub_category(s)
                )
                btn1.grid(row=row_index, column=0, sticky="ew", padx=(0, 10), pady=5)
            
            if row_index < len(col2):
                btn2 = ctk.CTkButton(
                    btn_frame,
                    text=col2[row_index],
                    font=ctk.CTkFont(size=16),
                    command=lambda s=col2[row_index]: self.go_to_sub_sub_category(s)
                )
                btn2.grid(row=row_index, column=1, sticky="ew", pady=5)
        
        # Make columns expand equally
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        master.add_back_button(self, command=lambda: master.switch_frame(ShelfStablePage))
        master.add_start_over_button(self)

    def go_to_sub_sub_category(self, sub_sub_category):
        # This method should navigate to a page showing items in this sub_sub_category
        # You'll need to implement this based on your app structure
        self.master.switch_frame(DryGoodsSubPage, sub_sub_category)

class DryGoodsSubPage(ctk.CTkFrame):
    def __init__(self, master, sub_sub_category):
        super().__init__(master)
        self.configure(fg_color="white")
        self.sub_sub_category = sub_sub_category
        
        ctk.CTkLabel(
            self,
            text=sub_sub_category,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))
        
        # Get all items in this sub_sub_category
        sub_items = [
            (item["label"], item["shelf_life_years"])
            for item in food_items.values()
            if item.get("subcategory") == "Dry Goods" and item.get("sub_sub_category") == sub_sub_category
        ]
        
        for label, years in sub_items:
            # Find the key from the label
            matching_key = next(
                (k for k, v in food_items.items() if v["label"] == label),
                None
            )
            if not matching_key:
                continue  # skip if key not found
            
            # Get display text
            d = food_items[matching_key].get("shelf_life_display", f"{years:.2f} years")
            
            ctk.CTkButton(
                self,
                text=label,
                width=350,
                font=ctk.CTkFont(size=14),
                command=lambda k=matching_key, l=label, d=d, y=years: master.switch_frame(ResultPage, k, l, y, d)
            ).pack(pady=4)
        
        master.add_back_button(self, command=lambda: master.switch_frame(DryGoodsPage))
        master.add_start_over_button(self)


class BeverageSubPage(ctk.CTkFrame):
    def __init__(self, master, sub_sub_category):
        super().__init__(master)
        self.configure(fg_color="white")
        self.sub_sub_category = sub_sub_category
        
        ctk.CTkLabel(
            self,
            text=sub_sub_category,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))
        
        # Get all items in this sub_sub_category
        sub_items = [
            (item["label"], item["shelf_life_years"])
            for item in food_items.values()
            if item.get("subcategory") == "Beverages" and item.get("sub_sub_category") == sub_sub_category
        ]
        
        for label, years in sub_items:
            # Find the key from the label
            matching_key = next(
                (k for k, v in food_items.items() if v["label"] == label),
                None
            )
            if not matching_key:
                continue  # skip if key not found
            
            # Get display text
            d = food_items[matching_key].get("shelf_life_display", f"{years:.2f} years")
            
            ctk.CTkButton(
                self,
                text=label,
                width=350,
                font=ctk.CTkFont(size=14),
                command=lambda k=matching_key, l=label, d=d, y=years: master.switch_frame(ResultPage, k, l, y, d)
            ).pack(pady=4)
        
        master.add_back_button(self, command=lambda: master.switch_frame(BeveragesPage))
        master.add_start_over_button(self)


class BeveragesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")
        
        ctk.CTkLabel(
            self, 
            text="Beverages", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))
        
        # Define the beverage categories
        beverage_categories = [
            "Coffee",
            "Juice", 
            "Milk",
            "Tea",
            "Water",
            "Other"
        ]
        
        # Create buttons in a single column
        for category in beverage_categories:
            ctk.CTkButton(
                self,
                text=category,
                width=150,
                font=ctk.CTkFont(size=14),
                command=lambda c=category: self.go_to_sub_sub_category(c)
            ).pack(pady=4)
        
        master.add_back_button(self, command=lambda: master.switch_frame(ShelfStablePage))
        master.add_start_over_button(self)
    
    def go_to_sub_sub_category(self, sub_sub_category):
        self.master.switch_frame(BeverageSubPage, sub_sub_category)


class CondimentsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")
        
        ctk.CTkLabel(
            self, 
            text="Condiments / Sauces", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))
        
        # Get all condiment items
        condiment_items = [
            (item["label"], item["shelf_life_years"])
            for item in food_items.values()
            if item.get("subcategory") == "Condiments"
        ]
        
        # Create frame for buttons
        btn_frame = ctk.CTkFrame(self, fg_color="white")
        btn_frame.pack(pady=10, padx=20, fill="x")
        
        # Create two columns by splitting the list roughly in half
        half = (len(condiment_items) + 1) // 2
        col1 = condiment_items[:half]
        col2 = condiment_items[half:]
        
        # Use grid layout for two columns
        for row_index in range(half):
            if row_index < len(col1):
                label, years = col1[row_index]
                # Find the key from the label
                matching_key = next(
                    (k for k, v in food_items.items() if v["label"] == label),
                    None
                )
                if matching_key:
                    # Get display text
                    d = food_items[matching_key].get("shelf_life_display", f"{years:.2f} years")
                    
                    btn1 = ctk.CTkButton(
                        btn_frame,
                        text=label,
                        width=350,
                        font=ctk.CTkFont(size=14),
                        command=lambda k=matching_key, l=label, d=d, y=years: master.switch_frame(ResultPage, k, l, y, d)
                    )
                    btn1.grid(row=row_index, column=0, sticky="ew", padx=(0, 10), pady=4)
            
            if row_index < len(col2):
                label, years = col2[row_index]
                # Find the key from the label
                matching_key = next(
                    (k for k, v in food_items.items() if v["label"] == label),
                    None
                )
                if matching_key:
                    # Get display text
                    d = food_items[matching_key].get("shelf_life_display", f"{years:.2f} years")
                    
                    btn2 = ctk.CTkButton(
                        btn_frame,
                        text=label,
                        width=350,
                        font=ctk.CTkFont(size=14),
                        command=lambda k=matching_key, l=label, d=d, y=years: master.switch_frame(ResultPage, k, l, y, d)
                    )
                    btn2.grid(row=row_index, column=1, sticky="ew", pady=4)
        
        # Make columns expand equally
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        master.add_back_button(self, command=lambda: master.switch_frame(ShelfStablePage))
        master.add_start_over_button(self)


class RefrigeratedPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")
        
        ctk.CTkLabel(
            self, 
            text="Refrigerated Items", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))
        
        # Define the refrigerated categories
        refrigerated_categories = [
            "Produce (cut varieties)",
            "Dairy/Eggs/Cooler Items", 
            "Meats",
            "Prepared/Deli Foods"
        ]
        
        # Create buttons in a single column
        for category in refrigerated_categories:
            ctk.CTkButton(
                self,
                text=category,
                width=350,
                font=ctk.CTkFont(size=14),
                command=lambda c=category: self.go_to_refrigerated_subcategory(c)
            ).pack(pady=4)
        
        master.add_back_button(self, command=lambda: master.show_category_page())
        master.add_start_over_button(self)
    
    def go_to_refrigerated_subcategory(self, subcategory):
        # Navigate to the appropriate subcategory page
        self.master.switch_frame(RefrigeratedSubPage, subcategory)


class RefrigeratedSubPage(ctk.CTkFrame):
    def __init__(self, master, subcategory):
        super().__init__(master)
        self.configure(fg_color="white")
        self.subcategory = subcategory

        ctk.CTkLabel(
            self,
            text=f"{subcategory} Items",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        ctk.CTkButton(self, text="Back", command=master.show_category_page).pack(pady=20)

class FrozenPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")
        ctk.CTkLabel(self, text="Frozen Items", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkButton(self, text="Back", command=master.show_category_page).pack(pady=20)


class ProducePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")
        ctk.CTkLabel(self, text="Fresh Produce", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkButton(self, text="Back", command=master.show_category_page).pack(pady=20)


class BabyFoodPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white")
        ctk.CTkLabel(self, text="Baby Food", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkButton(self, text="Back", command=master.show_category_page).pack(pady=20)


# --- Run App ---
if __name__ == "__main__":
    app = FoodbankApp()
    app.mainloop()
