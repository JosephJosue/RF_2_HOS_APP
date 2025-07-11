from tkinter import Tk, Toplevel, Canvas, filedialog, messagebox, Button, PhotoImage
import pandas as pd
from utils import relative_to_assets, OUTPUT_PATH


class I38Interface(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("401x546")
        self.configure(bg="#FFFFFF")
        self.title("I38 Migration")

        # Initialize DataFrame storage
        self.rf38_df = None
        self.hos38_df = None
        self.hos37_df = None

        # Make this window modal
        self.transient(parent)
        self.grab_set()

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=546,
            width=401,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # --- Header Image ---
        try:
            self.image_image_1 = PhotoImage(
                file=relative_to_assets("frame5", "image_1.png"))
            self.image_1 = self.canvas.create_image(
                200.0,
                24.0,
                image=self.image_image_1
            )
        except Exception as e:
            print(f"Could not load image_1.png: {e}")

        self.canvas.create_text(
            30.0,
            93.0,
            anchor="nw",
            text="INSERT THE FOLLOWING FILES:",
            fill="#000000",
            font=("Content", 24 * -1)
        )
        
        # --- Button Definitions ---
        self.create_buttons()

        self.resizable(False, False)

    def create_buttons(self):
        """Creates and places all buttons on the canvas."""
        # Process Files Button
        try:
            self.button_image_process = PhotoImage(file=relative_to_assets("frame5", "button_1.png"))
            self.process_button = Button(self, image=self.button_image_process, borderwidth=0, highlightthickness=0, command=self.process_files, relief="flat")
        except Exception:
            self.process_button = Button(self, text="Process Files", command=self.process_files)
        self.process_button.place(x=108.5, y=394.5, width=194.5, height=39.0)

        # Select I38 RF File Button
        try:
            self.button_image_rf38 = PhotoImage(file=relative_to_assets("frame5", "button_2.png"))
            self.rf38_button = Button(self, image=self.button_image_rf38, borderwidth=0, highlightthickness=0, command=self.select_rf38_file, relief="flat")
        except Exception:
            self.rf38_button = Button(self, text="Select I38 RF", command=self.select_rf38_file)
        self.rf38_button.place(x=30.0, y=185.0, width=100.0, height=100.0)

        # Select I38 HOS File Button
        try:
            self.button_image_hos38 = PhotoImage(file=relative_to_assets("frame5", "button_3.png"))
            self.hos38_button = Button(self, image=self.button_image_hos38, borderwidth=0, highlightthickness=0, command=self.select_hos38_file, relief="flat")
        except Exception:
            self.hos38_button = Button(self, text="Select I38 HOS", command=self.select_hos38_file)
        self.hos38_button.place(x=151.0, y=185.0, width=100.0, height=100.0)

        # Select I37 HOS File Button
        try:
            self.button_image_hos37 = PhotoImage(file=relative_to_assets("frame5", "button_4.png"))
            self.hos37_button = Button(self, image=self.button_image_hos37, borderwidth=0, highlightthickness=0, command=self.select_hos37_file, relief="flat")
        except Exception:
            self.hos37_button = Button(self, text="Select I37 HOS", command=self.select_hos37_file)
        self.hos37_button.place(x=272.0, y=185.0, width=100.0, height=100.0)

    def select_file(self, title, df_attribute):
        """Generic method to open a file dialog and load a CSV."""
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            parent=self
        )
        if not file_path:
            return
        try:
            df = pd.read_csv(file_path, encoding='latin1')
            setattr(self, df_attribute, df)
            print(f"{df_attribute} file loaded successfully: {file_path}")
            messagebox.showinfo(
                "Success",
                f"{title} loaded successfully!\nRows: {df.shape[0]}, Columns: {df.shape[1]}",
                parent=self
            )
        except Exception as e:
            print(f"Error loading {title}: {e}")
            messagebox.showerror("Error", f"Failed to load {title}:\n{str(e)}", parent=self)
            setattr(self, df_attribute, None)

    def select_rf38_file(self):
        self.select_file("Select I38 RF File", "rf38_df")

    def select_hos38_file(self):
        self.select_file("Select I38 HOS File", "hos38_df")

    def select_hos37_file(self):
        self.select_file("Select I37 HOS File", "hos37_df")

    def process_files(self):
        """Validates, merges, and processes the loaded files."""
        if self.rf38_df is None or self.hos38_df is None or self.hos37_df is None:
            messagebox.showwarning("Warning", "Please select all three files (I38 RF, I38 HOS, I37 HOS) before processing.", parent=self)
            return

        try:
            # Filter data for respective countries
            countries = ["ES", "PT", "NL", "DK", "BE", "SE", "FI", "NO"]
            countries_rf38_df = self.rf38_df[self.rf38_df["Country"].isin(countries)].copy()
            countries_hos38_df = self.hos38_df[self.hos38_df["Country"].isin(countries)].copy()
            countries_hos37_df = self.hos37_df[self.hos37_df["Country"].isin(countries)].copy()

            # Create lookup key for each DataFrame
            for df in [countries_rf38_df, countries_hos38_df, countries_hos37_df]:
                df["lookup_key"] = df["Country"].astype(str) + df["Attribute Value Code"].astype(str)

            # Merge I38 files
            i38_merge_df = pd.merge(countries_rf38_df, countries_hos38_df[["lookup_key"]], on='lookup_key', how='inner')
            # Merge I38 and I37 files
            i38_and_i37_merge_df = pd.merge(i38_merge_df, countries_hos37_df[["lookup_key"]], on='lookup_key', how='inner')

            if i38_and_i37_merge_df.empty:
                messagebox.showinfo("No Matches", "No matching records were found between the files.", parent=self)
                return

            # Save the final merged data split by country
            split_files = self.save_split_files_by_country(i38_and_i37_merge_df)
            
            message = f"Process complete!\nFound {len(i38_and_i37_merge_df)} matching records.\n\n"
            if split_files:
                message += f"Split files saved: {len(split_files)} country files created in I38 folder."
            else:
                message += "Note: No split files were created. Check the console for errors."
            
            messagebox.showinfo("Results", message, parent=self)

        except Exception as e:
            print(f"Error processing files: {e}")
            messagebox.showerror("Error", f"Failed to process files:\n{str(e)}", parent=self)

    def save_split_files_by_country(self, df_to_split):
        """Saves the processed DataFrame into separate Excel files for each country."""
        try:
            i38_folder = OUTPUT_PATH / "Output" / "I38"
            i38_folder.mkdir(parents=True, exist_ok=True)
            print(f"Output folder: {i38_folder}")

            country_column = "Country"
            filename_prefix = "I38_"
            unique_countries = df_to_split[country_column].unique()
            print(f"Countries found: {unique_countries}")

            saved_files = []
            for country in unique_countries:
                country_df = df_to_split[df_to_split[country_column] == country].copy()
                
                # Drop the lookup key and other merge-related columns
                country_df = country_df.iloc[:, :-5]

                filename = f"{filename_prefix}{country}.xlsx"
                file_path = i38_folder / filename

                print(f"Attempting to save: {file_path}")
                country_df.to_excel(str(file_path), index=False, engine='openpyxl')

                if file_path.exists():
                    saved_files.append(str(file_path))
                    print(f"✓ Successfully saved file for {country}: {file_path}")
                else:
                    print(f"✗ Failed to create file for {country}: {file_path}")

            return saved_files
        except Exception as e:
            print(f"Error saving split files: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to save split files:\n{str(e)}", parent=self)
            return []

def call_i38_gui(parent_window):
    """Function to create and show the I38 interface."""
    interface = I38Interface(parent_window)
    return interface

# For testing purposes
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the main window
    app = I38Interface(root)
    root.mainloop()
