from tkinter import Tk, Toplevel, Canvas, filedialog, messagebox, Button, PhotoImage
import pandas as pd
from utils import relative_to_assets, OUTPUT_PATH


class I52Interface(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("401x546")
        self.configure(bg="#FFFFFF")
        self.title("I52 Migration")

        # Initialize DataFrame storage
        self.rf52_df = None
        self.rf51_df = None
        self.hos36_df = None

        # Make this window modal
        self.transient(parent)
        self.grab_set()

        self.canvas = Canvas(self, bg="#FFFFFF", height=546, width=401, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # --- UI Elements ---
        self.create_header()
        self.create_buttons()

        self.resizable(False, False)

    def create_header(self):
        """Creates the header image and title text."""
        try:
            self.image_image_1 = PhotoImage(file=relative_to_assets("frame4", "image_1.png"))
            self.canvas.create_image(200.0, 24.0, image=self.image_image_1)
        except Exception as e:
            print(f"Could not load image_1.png: {e}")

        self.canvas.create_text(30.0, 93.0, anchor="nw", text="INSERT THE FOLLOWING FILES:", fill="#000000", font=("Content", 24 * -1))

    def create_buttons(self):
        """Creates and places all buttons on the canvas."""
        # Process Button
        try:
            self.button_image_process = PhotoImage(file=relative_to_assets("frame4", "button_1.png"))
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

        # I52 RF File Button
        try:
            self.button_image_rf52 = PhotoImage(file=relative_to_assets("frame4", "button_2.png"))
            self.rf52_button = Button(
                self, 
                image=self.button_image_rf52, 
                borderwidth=0, 
                highlightthickness=0, 
                command=self.select_rf52_file, 
                relief="flat"
            )
        except Exception:
            self.rf52_button = Button(
                self, 
                text="Select I52 RF", 
                command=self.select_rf52_file
            )

        self.rf52_button.place(
            x=30.0, 
            y=185.0, 
            width=100.0, 
            height=100.0
        )

        # I51 RF File Button
        try:
            self.button_image_rf51 = PhotoImage(file=relative_to_assets("frame4", "button_3.png"))
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
                text="Select I51 RF", 
                command=self.select_rf51_file
            )

        self.rf51_button.place(
            x=151.0, 
            y=185.0, 
            width=100.0, 
            height=100.0
        )

        # I36 HOS File Button
        try:
            self.button_image_hos36 = PhotoImage(file=relative_to_assets("frame4", "button_4.png"))
            self.hos36_button = Button(
                self, 
                image=self.button_image_hos36, 
                borderwidth=0, 
                highlightthickness=0, 
                command=self.select_hos36_file, 
                relief="flat"
            )
        except Exception:
            self.hos36_button = Button(
                self, 
                text="Select I36 HOS", 
                command=self.select_hos36_file
            )

        self.hos36_button.place(
            x=272.0, 
            y=185.0, 
            width=100.0, 
            height=100.0
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

    def select_rf52_file(self): 
        self.select_file("Select I52 RF File", "rf52_df")
    def select_rf51_file(self): 
        self.select_file("Select I51 RF File", "rf51_df")
    def select_hos36_file(self): 
        self.select_file("Select I36 HOS File", "hos36_df")

    def process_files(self):
        """Main logic to process the loaded files."""
        if self.rf52_df is None or self.rf51_df is None or self.hos36_df is None:
            messagebox.showwarning("Warning", "Please select all three files (I52 RF, I51 RF, I36 HOS) before processing.", parent=self)
            return

        try:
            # 1. Filter data for respective countries
            countries = ["ES", "PT", "NL", "DK", "BE", "SE", "FI", "NO"]
            countries_rf52_df = self.rf52_df[self.rf52_df["Country"].isin(countries)].copy()
            countries_rf51_df = self.rf51_df[self.rf51_df["Country"].isin(countries)].copy()
            countries_hos36_df = self.hos36_df[self.hos36_df["Country"].isin(countries)].copy()

            # 2. Filter RF I51 for specific data
            rf51_os_codes = ["HEL_15T_IN", "HEL_30T_IN", "HEL_ING_IN", "EASYSWITCH_IN", "UQCM_IN"]
            rf51_os_df = countries_rf51_df[countries_rf51_df["Attribute Value Code"].isin(rf51_os_codes)].copy()

            # 3. Model I51 data to match I52 format
            converted_rows = []
            for _, row in rf51_os_df.iterrows():
                converted_rows.append({
                    'Display Group Code': 'LI', 'Country': row['Country'], 
                    'Attribute Value Code': row['Attribute Value Code'],
                    'Attribute Value Description': row['Attribute Value Description'], 
                    'Attribute Value Price Type': 'Lookup',
                    'Attribute Value FP': row['Attribute Value FP'], 
                    'Attribute Value TP': row['Attribute Value TP'],
                    'Attribute Value LP': row['Attribute Value LP'], 
                    'Attribute Value MMFP': row['Attribute Value MMFP'],
                    'Attribute Value MMTP': row['Attribute Value MMTP'], 
                    'Attribute Value MMLP': row['Attribute Value MMLP'],
                    'Attribute Deactivated YN': row['Attribute Deactivated YN'], 
                    'Customer Bank Value': row['Customer Bank Value'],
                    'RSM Type': row['RSM Type'], 
                    'RSM Consumption': row['RSM Consumption'], 
                    'Currency': row['Currency'],
                    'Local FP': row['Local FP'], 
                    'Price Book Name': row['Price Book Name'], 
                    'Server': row['Server'],
                    'Changed On': row['Changed On'], 
                    'Changed By': row['Changed By']
                })
            converted_df = pd.DataFrame(converted_rows)

            # 4. Combine with existing I52 data
            combined_i52_df = pd.concat([countries_rf52_df, converted_df], ignore_index=True)

            # 5. Create lookup keys
            combined_i52_df["lookup_key"] = combined_i52_df["Country"].astype(str) + combined_i52_df["Attribute Value Code"].astype(str)
            countries_hos36_df["lookup_key"] = countries_hos36_df["Country"].astype(str) + countries_hos36_df["Attribute Value Code"].astype(str)

            # 6. Merge to find matching values
            i52_and_i36_merge_df = pd.merge(combined_i52_df, countries_hos36_df[["lookup_key"]], on='lookup_key', how='inner')

            if i52_and_i36_merge_df.empty:
                messagebox.showinfo("No Matches", "No matching records were found after processing.", parent=self)
                return

            # 7. Save the final results
            split_files = self.save_split_files_by_country(i52_and_i36_merge_df)
            
            message = f"Process complete!\nFound {len(i52_and_i36_merge_df)} matching records.\n\n"
            if split_files:
                message += f"Split files saved: {len(split_files)} country files created in I52 folder."
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
            i52_folder = OUTPUT_PATH / "Output" / "I52"
            i52_folder.mkdir(parents=True, exist_ok=True)

            country_column = "Country"
            filename_prefix = "I52_"
            unique_countries = df_to_split[country_column].unique()
            
            saved_files = []
            for country in unique_countries:
                country_df = df_to_split[df_to_split[country_column] == country].copy()
                country_df = country_df.iloc[:, :-5] # Drop the last 5 columns

                filename = f"{filename_prefix}{country}.xlsx"
                file_path = i52_folder / filename
                country_df.to_excel(str(file_path), index=False, engine='openpyxl')

                if file_path.exists():
                    saved_files.append(str(file_path))
            return saved_files
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save split files:\n{str(e)}", parent=self)
            return []

def call_i52_gui(parent_window):
    """Function to create and show the I52 interface."""
    interface = I52Interface(parent_window)
    return interface

# For testing purposes
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    app = I52Interface(root)
    root.mainloop()

