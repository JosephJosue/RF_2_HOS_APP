from tkinter import Tk, Toplevel, Canvas, filedialog, messagebox, Button, PhotoImage
import pandas as pd
from utils import relative_to_assets, OUTPUT_PATH


class I34Interface(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("401x546")
        self.configure(bg="#FFFFFF")
        self.title("I34 Migration")

        # Initialize DataFrame storage
        self.rf34_df = None

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
                file=relative_to_assets("frame6", "image_1.png"))
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
            text="INSERT THE FOLLOWING FILE:",
            fill="#000000",
            font=("Content", 24 * -1)
        )

        # --- Select File Button ---
        try:
            self.button_image_select = PhotoImage(
                file=relative_to_assets("frame6", "button_2.png"))
            self.select_file_button = Button(
                self,
                image=self.button_image_select,
                borderwidth=0,
                highlightthickness=0,
                command=self.select_file,
                relief="flat"
            )
        except Exception as e:
            print(f"Could not load button_2.png: {e}")
            self.select_file_button = Button(
                self,
                text="Select I34 RF File",
                command=self.select_file,
                relief="flat"
            )
        self.select_file_button.place(
            x=142.0,
            y=176.0,
            width=118.5,
            height=118.5
        )
        
        # --- Process Button ---
        try:
            self.button_image_process = PhotoImage(
                file=relative_to_assets("frame6", "button_1.png"))
            self.process_button = Button(
                self,
                image=self.button_image_process,
                borderwidth=0,
                highlightthickness=0,
                command=self.process_files,
                relief="flat"
            )
        except Exception as e:
            print(f"Could not load button_1.png: {e}")
            self.process_button = Button(
                self,
                text="Process File",
                command=self.process_files,
                relief="flat"
            )
        self.process_button.place(
            x=108.5,
            y=394.5,
            width=194.5,
            height=39.0
        )

        self.resizable(False, False)

    def select_file(self):
        """Opens a dialog to select the I34 RF CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select I34 RF file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            parent=self
        )
        if file_path:
            try:
                self.rf34_df = pd.read_csv(file_path, encoding='latin1')
                print(f"I34 RF file loaded successfully: {file_path}")
                messagebox.showinfo(
                    "Success",
                    f"I34 RF file loaded successfully!\nRows: {self.rf34_df.shape[0]}, Columns: {self.rf34_df.shape[1]}",
                    parent=self
                )
            except Exception as e:
                print(f"Error loading I34 RF file: {e}")
                messagebox.showerror("Error", f"Failed to load I34 RF file:\n{str(e)}", parent=self)
                self.rf34_df = None

    def process_files(self):
        """Processes the loaded I34 RF file and splits it by country."""
        if self.rf34_df is None:
            messagebox.showwarning("Warning", "Please select the I34 RF file first!", parent=self)
            return

        try:
            # Filter data for specific countries
            countries_rf34_df = self.rf34_df[self.rf34_df["Country"].isin(["ES", "PT", "NL", "DK", "BE", "SE", "FI", "NO"])].copy()

            if countries_rf34_df.empty:
                messagebox.showinfo("No Data", "No data found for the specified countries.", parent=self)
                return

            # Save split files by country
            split_files = self.save_split_files_by_country(countries_rf34_df)

            message = ""
            if split_files:
                message += f"Process complete!\n\nSplit files saved: {len(split_files)} country files created in I34 folder."
            else:
                message += "Note: No split files were created. Check the console for errors."

            messagebox.showinfo("Results", message, parent=self)

        except Exception as e:
            print(f"Error processing files: {e}")
            messagebox.showerror("Error", f"Failed to process files:\n{str(e)}", parent=self)

    def save_split_files_by_country(self, df_to_split):
        """Saves separate Excel files for each country."""
        try:
            # Create I34 output folder if it doesn't exist
            i34_folder = OUTPUT_PATH / "Output" / "I34"
            i34_folder.mkdir(parents=True, exist_ok=True)
            print(f"Output folder: {i34_folder}")

            country_column = "Country"
            filename_prefix = "I34_"
            unique_countries = df_to_split[country_column].unique()
            print(f"Countries found: {unique_countries}")

            saved_files = []
            for country in unique_countries:
                country_df = df_to_split[df_to_split[country_column] == country].copy()

                # Drop the last 4 columns as per the logic
                country_df = country_df.iloc[:, :-4]

                filename = f"{filename_prefix}{country}.xlsx"
                file_path = i34_folder / filename

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


def call_i34_gui(parent_window):
    """Function to create and show the I34 interface as a child window."""
    interface = I34Interface(parent_window)
    return interface


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    # You would typically hide the root window when testing a Toplevel
    root.withdraw() 
    app = I34Interface(root)
    root.mainloop()
