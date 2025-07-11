from tkinter import Tk, Toplevel, Canvas, filedialog, messagebox, Button, PhotoImage
import pandas as pd
from utils import relative_to_assets, OUTPUT_PATH


class I53Interface(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("401x546")
        self.configure(bg = "#FFFFFF")
        self. title("I53 Migration")

        self.rf53_df = None
        self.hos53_df = None
        self.hos35_df = None

        self.transient(parent)
        self.grab_set()

        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 546,
            width = 401,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        try:
            self.image_image_1 = PhotoImage(
                file=relative_to_assets("frame3", "image_1.png"))
            self.image_1 = self.canvas.create_image(
                200.0,
                24.0,
                image=self.image_image_1
            )
        except Exception as e:
            print(f"Could not load image_1.png: {e}")
            self.image_image_1 = None
    
        self.canvas.create_text(
            30.0,
            93.0,
            anchor="nw",
            text="INSERT THE FOLLOWING FILES:",
            fill="#000000",
            font=("Content", 24 * -1)
        )

        try:
            self.button_image_1 = PhotoImage(
                file=relative_to_assets("frame3", "button_2.png"))
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
                text="Select I53 RF File",
                command=lambda: self.button_1_clicked(),
                relief="flat"
            )

        self.button_1.place(
            x=30.0,
            y=185.0,
            width=100.0,
            height=100.0
        )
        try:
            self.button_image_2 = PhotoImage(
                file=relative_to_assets("frame3", "button_3.png"))
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
                text="Select I53 HOS File",
                command=lambda: self.button_2_clicked(),
                relief="flat"
            )

        self.button_2.place(
            x=151.0,
            y=185.0,
            width=100.0,
            height=100.0
        )

        try:
            self.button_image_3 = PhotoImage(
                file=relative_to_assets("frame3", "button_4.png"))
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
                text="Select I35 HOS File",
                command=lambda: self.button_3_clicked(),
                relief="flat"
            )

        self.button_3.place(
            x=272.0,
            y=185.0,
            width=100.0,
            height=100.0
        )

        try:
            self.button_image_4 = PhotoImage(
                file=relative_to_assets("frame3", "button_1.png"))
            self.button_4 = Button(
                self,
                image=self.button_image_4,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.button_4_clicked(),
                relief="flat"
            )
        except Exception as e:
            print(f"Could not load button_4.png: {e}")
            self.button_4 = Button(
                self,
                text="Process Files",
                command=lambda: self.button_4_clicked(),
                relief="flat"
            )

        self.button_4.place(
            x=108.5,
            y=394.5,
            width=194.5,
            height=39.0
        )

        self.resizable(False, False)

    def button_1_clicked(self):
        file_path = filedialog.askopenfilename(
            title="Select I53 RF file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            parent=self
        )
        if file_path:
            try:
                self.rf53_df = pd.read_csv(file_path, encoding='latin1')
                print(f"I53 RF file loaded successfully: {file_path}")
                messagebox.showinfo("Success", f"I53 RF file loaded successfully!\nRows: {self.rf53_df.shape[0]}, Columns: {self.rf53_df.shape[1]}", parent=self)
            except Exception as e:
                print(f"Error loading I53 RF file: {e}")
                messagebox.showerror("Error", f"Failed to load I53 RF file:\n{str(e)}", parent=self)
                self.rf53_df = None
    
    def button_2_clicked(self):
        file_path = filedialog.askopenfilename(
            title="Select I53 HOS file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            parent=self
        )
        if file_path:
            try:
                self.hos53_df = pd.read_csv(file_path, encoding='latin1')
                print(f"I53 HOS file loaded successfully: {file_path}")
                messagebox.showinfo("Success", f"I53 HOS file loaded successfully!\nRows: {self.hos53_df.shape[0]}, Columns: {self.hos53_df.shape[1]}", parent=self)
            except Exception as e:
                print(f"Error loading I53 HOS file: {e}")
                messagebox.showerror("Error", f"Failed to load I53 HOS file:\n{str(e)}", parent=self)
                self.hos53_df = None
    
    def button_3_clicked(self):
        file_path = filedialog.askopenfilename(
            title="Select I35 HOS file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            parent=self
        )
        if file_path:
            try:
                self.hos35_df = pd.read_csv(file_path, encoding='latin1')
                print(f"I35 HOS file loaded successfully: {file_path}")
                messagebox.showinfo("Success", f"I35 HOS file loaded successfully!\nRows: {self.hos35_df.shape[0]}, Columns: {self.hos35_df.shape[1]}", parent=self)
            except Exception as e:
                print(f"Error loading I35 HOS file: {e}")
                messagebox.showerror("Error", f"Failed to load I35 HOS file:\n{str(e)}", parent=self)
                self.hos35_df = None
    
    def button_4_clicked(self):
        if self.rf53_df is None:
            messagebox.showwarning("Warning", "Please select I53 RF file first!", parent=self)
            return
        
        if self.hos53_df is None:
            messagebox.showwarning("Warning", "Please select I53 HOS file first!", parent=self)
            return
        
        if self.hos35_df is None:
            messagebox.showwarning("Warning", "Please select I35 HOS file first!", parent=self)
            return
        
        try:
            #Filter data for specific countries
            countries_rf53_df = self.rf53_df[self.rf53_df["Country"].isin(["ES", "PT", "NL", "DK", "BE", "SE", "FI", "NO"])].copy()
            countries_hos35_df = self.hos35_df[self.hos35_df["Country"].isin(["ES", "PT", "NL", "DK", "BE", "SE", "FI", "NO"])].copy()

            #create lookup key and merge files
            countries_rf53_df["lookup_key"] = countries_rf53_df["Country"].astype(str) + countries_rf53_df["Attribute Value Code"].astype(str)
            countries_hos35_df["lookup_key"] = countries_hos35_df["Country"].astype(str) + countries_hos35_df["Attribute Value Code"].astype(str)

            df_output = pd.merge(countries_rf53_df, countries_hos35_df[["lookup_key"]], on='lookup_key', how='inner')

            #save split files by country
            split_files = self.save_split_files_by_country(df_output)

            #prepare message
            message = ""
            if split_files:
                message += f"Split files saved: {len(split_files)} country files created in I53 folder"
            else:
                message += "Note: No split files were created (check console for details)"
                
            messagebox.showinfo("Results", message, parent=self)
            
        except Exception as e:
            print(f"Error processing files: {e}")
            messagebox.showerror("Error", f"Failed to process files:\n{str(e)}", parent=self)

    def save_split_files_by_country(self, df_output):
        """Save separate Excel files for each country"""
        try:
            # Use parents=True to create parent directories if needed
            i53_folder = OUTPUT_PATH / "Output" / "I53"
            i53_folder.mkdir(parents=True, exist_ok=True)
            
            print(f"I53 folder path: {i53_folder}")

            country_column = "Country"
            filename_prefix = "I53_"
            unique_countries = df_output[country_column].unique()
            print(f"Countries found: {unique_countries}")

            saved_files = []

            for country in unique_countries:
                country_df = df_output[df_output[country_column] == country].copy()
                country_df = country_df.iloc[:, :-5]
                
                filename = f"{filename_prefix}{country}.xlsx"
                file_path = i53_folder / filename
                
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

def call_i53_gui(parent_window):
    """Function to create and show the I53 interface as a child window"""
    interface = I53Interface(parent_window)
    return interface

if __name__ == "__main__":
    root = Tk()
    call_i53_gui(root)
    root.mainloop()
