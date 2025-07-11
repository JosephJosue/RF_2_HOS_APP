from tkinter import Tk, Toplevel, Canvas, filedialog, messagebox, Button, PhotoImage
import pandas as pd
from utils import relative_to_assets, OUTPUT_PATH


class I51Interface(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("401x546")
        self.configure(bg="#FFFFFF")
        self.title("I51 Migration")

        # Initialize DataFrame storage
        self.rf51_df = None
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

        # --- UI Elements ---
        self.create_header()
        self.create_buttons()

        self.resizable(False, False)

    def create_header(self):
        """Creates the header image and title text."""
        try:
            self.image_image_1 = PhotoImage(file=relative_to_assets("frame2", "image_1.png"))
            self.canvas.create_image(
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

    def create_buttons(self):
        """Creates and places all buttons on the canvas."""
        # I51 RF File Button
        try:
            self.button_image_rf51 = PhotoImage(file=relative_to_assets("frame2", "button_1.png"))
            self.rf51_button = Button(
                self, 
                image=self.button_image_rf51, 
                borderwidth=0, 
                highlightthickness=0, 
                command=self.select_rf51_file, 
                relief="flat"
            )
        except Exception:
            self.rf51_button = Button(
                self, 
                text="Select I51 RF File", 
                command=self.select_rf51_file
            )
        self.rf51_button.place(
            x=52.5, 
            y=175.5, 
            width=118.5, 
            height=118.5
        )

        # I37 HOS File Button
        try:
            self.button_image_hos37 = PhotoImage(file=relative_to_assets("frame2", "button_2.png"))
            self.hos37_button = Button(
                self, 
                image=self.button_image_hos37, 
                borderwidth=0, 
                highlightthickness=0, 
                command=self.select_hos37_file, 
                relief="flat"
            )
        except Exception:
            self.hos37_button = Button(
                self, 
                text="Select HOS37 File", 
                command=self.select_hos37_file
            )
        self.hos37_button.place(
            x=241.0, 
            y=175.5, 
            width=118.5, 
            height=118.5
        )
        
        # Process Button
        try:
            self.button_image_process = PhotoImage(file=relative_to_assets("frame2", "button_3.png"))
            self.process_button = Button(
                self, 
                image=self.button_image_process, 
                borderwidth=0, 
                highlightthickness=0, 
                command=self.process_files, 
                relief="flat"
            )
        except Exception:
            self.process_button = Button(
                self, 
                text="Process Files", 
                command=self.process_files
            )
        self.process_button.place(
            x=108.5, 
            y=394.5, 
            width=194.5, 
            height=39.0
        )

    def select_file(self, title, df_attribute):
        """Generic method to open a file dialog and load a CSV."""
        file_path = filedialog.askopenfilename(title=title, filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], parent=self)
        if not file_path: return
        try:
            df = pd.read_csv(file_path, encoding='latin1')
            setattr(self, df_attribute, df)
            messagebox.showinfo("Success", f"{title} loaded successfully!\nRows: {df.shape[0]}, Columns: {df.shape[1]}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load {title}:\n{str(e)}", parent=self)
            setattr(self, df_attribute, None)

    def select_rf51_file(self): self.select_file("Select I51 RF File", "rf51_df")
    def select_hos37_file(self): self.select_file("Select I37 HOS File", "hos37_df")

    def process_files(self):
        """Main logic to process the loaded files."""
        if self.rf51_df is None or self.hos37_df is None:
            messagebox.showwarning("Warning", "Please select both I51 RF and I37 HOS files before processing.", parent=self)
            return

        try:
            # 1. Filter data for respective countries
            countries = ["ES", "PT", "NL", "DK", "BE", "SE", "FI", "NO"]
            countries_rf51_df = self.rf51_df[self.rf51_df["Country"].isin(countries)].copy()
            countries_hos37_df = self.hos37_df[self.hos37_df["Country"].isin(countries)].copy()

            # 2. Remove specific attributes from I51 RF file
            attributes_to_remove = ["HEL_15T_IN", "HEL_30T_IN", "HEL_ING_IN", "EASYSWITCH_IN", "UQCM_IN"]
            i51_cleaned_df = countries_rf51_df[~countries_rf51_df["Attribute Value Code"].isin(attributes_to_remove)].copy()

            # 3. Create lookup keys
            i51_cleaned_df["lookup_key"] = i51_cleaned_df["Country"].astype(str) + i51_cleaned_df["Attribute Value Code"].astype(str)
            countries_hos37_df["lookup_key"] = countries_hos37_df["Country"].astype(str) + countries_hos37_df["Attribute Value Code"].astype(str)

            # 4. Merge to find matching values
            i51_and_i37_merge_df = pd.merge(i51_cleaned_df, countries_hos37_df[["lookup_key"]], on='lookup_key', how='inner')

            if i51_and_i37_merge_df.empty:
                messagebox.showinfo("No Matches", "No matching records were found after cleaning and merging the files.", parent=self)
                return

            # 5. Save the final results
            split_files = self.save_split_files_by_country(i51_and_i37_merge_df)
            
            message = f"Process complete!\nFound {len(i51_and_i37_merge_df)} matching records.\n\n"
            if split_files:
                message += f"Split files saved: {len(split_files)} country files created in I51 folder."
            else:
                message += "Note: No split files were created. Check the console for errors."
            
            messagebox.showinfo("Results", message, parent=self)

        except Exception as e:
            print(f"Error processing files: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to process files:\n{str(e)}", parent=self)

    def save_split_files_by_country(self, df_to_split):
        """Saves the processed DataFrame into separate Excel files for each country."""
        try:
            i51_folder = OUTPUT_PATH / "Output" / "I51"
            i51_folder.mkdir(parents=True, exist_ok=True)

            country_column = "Country"
            filename_prefix = "I51_"
            unique_countries = df_to_split[country_column].unique()
            
            saved_files = []
            for country in unique_countries:
                country_df = df_to_split[df_to_split[country_column] == country].copy()
                # Drop columns as per the provided logic
                country_df = country_df.iloc[:, :-5]

                filename = f"{filename_prefix}{country}.xlsx"
                file_path = i51_folder / filename
                country_df.to_excel(str(file_path), index=False, engine='openpyxl')

                if file_path.exists():
                    saved_files.append(str(file_path))
            return saved_files
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save split files:\n{str(e)}", parent=self)
            return []

def call_i51_gui(parent_window):
    """Function to create and show the I51 interface."""
    interface = I51Interface(parent_window)
    return interface

# For testing purposes
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    app = I51Interface(root)
    root.mainloop()
