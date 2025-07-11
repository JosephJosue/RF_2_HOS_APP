from tkinter import Tk, Canvas, Button, PhotoImage, filedialog, Toplevel, messagebox
import pandas as pd
from utils import relative_to_assets, OUTPUT_PATH


class I01Interface(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("401x546")
        self.configure(bg="#FFFFFF")
        self.title("I01 Migration")
        
        # Initialize DataFrame storage
        self.rf01_df = None
        self.hos01_df = None
        
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
        
        try:
            self.image_image_1 = PhotoImage(
                file=relative_to_assets("frame1", "image_1.png"))
            self.image_1 = self.canvas.create_image(
                200.0,
                24.0,
                image=self.image_image_1
            )
        except Exception as e:
            print(f"Could not load image_1.png: {e}")
            self.image_image_1 = None

        try:
            self.button_image_1 = PhotoImage(
                file=relative_to_assets("frame1", "button_1.png"))
            self.button_1 = Button(
                self,
                image=self.button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.button_1_clicked(),
                relief="flat"
            )
        except Exception as e:
            print(f"Could not load button_1.png: {e}")
            self.button_1 = Button(
                self,
                text="Select RF01 File",
                command=lambda: self.button_1_clicked(),
                relief="flat"
            )

        self.button_1.place(
            x=52.5,
            y=175.5,
            width=118.5,
            height=118.5
        )

        try:
            self.button_image_2 = PhotoImage(
                file=relative_to_assets("frame1", "button_2.png"))
            self.button_2 = Button(
                self,
                image=self.button_image_2,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.button_2_clicked(),
                relief="flat"
            )
        except Exception as e:
            print(f"Could not load button_2.png: {e}")
            self.button_2 = Button(
                self,
                text="Select HOS01 File",
                command=lambda: self.button_2_clicked(),
                relief="flat"
            )

        self.button_2.place(
            x=241.0,
            y=175.5,
            width=118.5,
            height=118.5
        )

        self.canvas.create_text(
            20.0,
            93.0,
            anchor="nw",
            text="INSERT THE FOLLOWING FILES:",
            fill="#000000",
            font=("Arial", 18)
        )

        try:
            self.button_image_3 = PhotoImage(
                file=relative_to_assets("frame1", "button_3.png"))
            self.button_3 = Button(
                self,
                image=self.button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.button_3_clicked(),
                relief="flat"
            )
        except Exception as e:
            print(f"Could not load button_3.png: {e}")
            self.button_3 = Button(
                self,
                text="Process Files",
                command=lambda: self.button_3_clicked(),
                relief="flat"
            )

        self.button_3.place(
            x=108.5,
            y=394.5,
            width=194.5,
            height=39.0
        )

        self.resizable(False, False)
    
    def button_1_clicked(self):
        file_path = filedialog.askopenfilename(
            title="Select RF01 file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            parent=self
        )
        if file_path:
            try:
                self.rf01_df = pd.read_csv(file_path, encoding='latin1')
                print(f"RF01 file loaded successfully: {file_path}")
                print(f"RF01 DataFrame shape: {self.rf01_df.shape}")
                messagebox.showinfo("Success", f"RF01 file loaded successfully!\nRows: {self.rf01_df.shape[0]}, Columns: {self.rf01_df.shape[1]}", parent=self)
            except Exception as e:
                print(f"Error loading RF01 file: {e}")
                messagebox.showerror("Error", f"Failed to load RF01 file:\n{str(e)}", parent=self)
                self.rf01_df = None
    
    def button_2_clicked(self):
        file_path = filedialog.askopenfilename(
            title="Select HOS01 file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            parent=self
        )
        if file_path:
            try:
                self.hos01_df = pd.read_csv(file_path, encoding='latin1')
                print(f"HOS01 file loaded successfully: {file_path}")
                print(f"HOS01 DataFrame shape: {self.hos01_df.shape}")
                messagebox.showinfo("Success", f"HOS01 file loaded successfully!\nRows: {self.hos01_df.shape[0]}, Columns: {self.hos01_df.shape[1]}", parent=self)
            except Exception as e:
                print(f"Error loading HOS01 file: {e}")
                messagebox.showerror("Error", f"Failed to load HOS01 file:\n{str(e)}", parent=self)
                self.hos01_df = None
    
    def button_3_clicked(self):
        if self.rf01_df is None:
            messagebox.showwarning("Warning", "Please select RF01 file first!", parent=self)
            return
        
        if self.hos01_df is None:
            messagebox.showwarning("Warning", "Please select HOS01 file first!", parent=self)
            return
        
        try:
            # Filter data for specific countries
            countries_rf01_df = self.rf01_df[self.rf01_df["Country"].isin(["ES", "PT", "NL", "DK", "BE", "SE", "FI", "NO"])].copy()
            countries_hos01_df = self.hos01_df[self.hos01_df["Country"].isin(["ES", "PT", "NL", "DK", "BE", "SE", "FI", "NO"])].copy()

            # Reset indices to match iteration
            countries_rf01_df = countries_rf01_df.reset_index(drop=True)
            countries_hos01_df = countries_hos01_df.reset_index(drop=True)

            # Create a list with the columns to compare
            columns_to_compare = ["h_cost_rate", "h_trav_CM", "h_trav_PM", "mat_hand", "LaborGM", "PartsGM", "TP_LP_UP", "FP_LP_UP", "NBV_LAT", "NBV_NPC", "NBV_UPLIFT"]

            # Create a new dataframe to show the compared data
            changed_values_df = pd.DataFrame(columns=["Row", "Country", "Column", "Old Value", "New Value"])

            # Iterate through each column to compare data
            for column in columns_to_compare:
                if column in countries_hos01_df.columns and column in countries_rf01_df.columns:
                    differences = countries_hos01_df[column] != countries_rf01_df[column]
                    changes = pd.DataFrame({
                        'Row': countries_hos01_df.index[differences],
                        'Country': countries_rf01_df.loc[differences, "Country"],
                        'Column': column,
                        'Old Value': countries_hos01_df.loc[differences, column],
                        'New Value': countries_rf01_df.loc[differences, column]
                    })
                    if not changes.empty:
                        changed_values_df = pd.concat([changed_values_df, changes], ignore_index=True)
            
            # Always save split files, regardless of differences
            split_files = self.save_split_files_by_country(countries_rf01_df)
            message = ""

            if changed_values_df.empty:
                message += "No differences found between the files!\n\n"
                print("No differences found between the files.")
            else:
                print("Differences found:")
                saved_file_path = self.save_changed_values_to_excel(changed_values_df)
                message += f"Found {len(changed_values_df)} differences!\n"
                if saved_file_path:
                    message += f"Comparison results saved to:\n{saved_file_path}\n\n"
            
            if split_files:
                message += f"Split files saved: {len(split_files)} country files created in I01 folder."
            else:
                message += "Note: No split files were created (check console for details)."
            
            messagebox.showinfo("Results", message, parent=self)
                
        except Exception as e:
            print(f"Error processing files: {e}")
            messagebox.showerror("Error", f"Failed to process files:\n{str(e)}", parent=self)

    def save_changed_values_to_excel(self, changed_values_df):
        try:
            i01_folder = OUTPUT_PATH / "Output" / "I01"
            i01_folder.mkdir(parents=True, exist_ok=True)
            
            filename = "I01_changes.xlsx"
            file_path = i01_folder / filename
            
            changed_values_df.to_excel(file_path, index=False, engine='openpyxl')
            
            print(f"File saved successfully: {file_path}")
            return str(file_path)
            
        except Exception as e:
            print(f"Error saving file: {e}")
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}", parent=self)
            return None
    
    def save_split_files_by_country(self, countries_rf01_df):
        """Save separate Excel files for each country"""
        try:
            i01_folder = OUTPUT_PATH / "Output" / "I01"
            i01_folder.mkdir(parents=True, exist_ok=True)
            
            print(f"I01 folder path: {i01_folder}")
            print(f"I01 folder exists: {i01_folder.exists()}")

            country_column = "Country"
            filename_prefix = "I01_"
            unique_countries = countries_rf01_df[country_column].unique()
            print(f"Countries found: {unique_countries}")

            saved_files = []
            for country in unique_countries:
                country_df = countries_rf01_df[countries_rf01_df[country_column] == country].copy()
                country_df = country_df.iloc[:, :-4]
                
                filename = f"{filename_prefix}{country}.xlsx"
                file_path = i01_folder / filename
                
                print(f"Attempting to save: {file_path}")
                country_df.to_excel(str(file_path), index=False, engine='openpyxl')
                
                if file_path.exists():
                    saved_files.append(str(file_path))
                    print(f"✓ Successfully saved file for {country}: {file_path}")
                else:
                    print(f"✗ Failed to create file for {country}: {file_path}")

            print(f"Total files saved: {len(saved_files)}")
            return saved_files
            
        except Exception as e:
            print(f"Error saving split files: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to save split files:\n{str(e)}", parent=self)
            return []

def call_i01_gui(parent_window):
    """Function to create and show the I01 interface as a child window"""
    interface = I01Interface(parent_window)
    return interface

if __name__ == "__main__":
    root = Tk()
    call_i01_gui(root)
    root.mainloop()