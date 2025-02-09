import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

# Python functions to run based on user input
from categorize_raw_statement import categorize_last_raw_statement, tell_user_next_statement_start, retrain_classifier
from compile_corrected_statements import compile_corrected_statements
from summarize_transactions import summarize_monthly_transactions

cct_version = '3.3_streamlit'

class ScriptRunnerApp:
    def __init__(self, master):
        self.master = master
        master.title(f"Credit Card Tracker v{cct_version}")

        # First time running script... download dependency files
        if "cct_init_files" not in os.listdir():
            self.init_working_directory()

        # Load PNG image
        self.img = Image.open("cct_init_files/piggybank.png")  # Replace "image.png" with the path to your PNG image
        self.img = self.img.resize((300, 350))  # Resize image as needed
        self.img_tk = ImageTk.PhotoImage(self.img)

        # Display PNG image on the homescreen
        self.img_label = tk.Label(master, image=self.img_tk)
        self.img_label.pack()

        self.label = tk.Label(master, text="Select what the app should do: ")
        self.label.pack()

        self.retrain_func_frame = tk.Frame(master)
        self.retrain_func_frame.pack()
        self.retrain_func_button = tk.Button(self.retrain_func_frame, text="train_classifier()", command=self.run_retrain_func)
        self.retrain_func_button.grid(row=0, column=0)
        self.retrain_func_desc_label = tk.Label(self.retrain_func_frame, text="(Re)-train SVM classifier if changes were made to VendorID files")
        self.retrain_func_desc_label.grid(row=0, column=1)

        if len(os.listdir('data/RawStatements/'))>0:
            next_statement_date_str = tell_user_next_statement_start()
        else:
            next_statement_date_str = 'any date'
        self.categorize_func_frame = tk.Frame(master)
        self.categorize_func_frame.pack()
        self.categorize_func_button = tk.Button(self.categorize_func_frame, text="categorize_last_raw_statement()", command=self.run_categorize_func)
        self.categorize_func_button.grid(row=1, column=0)
        self.categorize_func_desc_label = tk.Label(self.categorize_func_frame, text=f"Read and auto-categorize the most recent 'RawStatement' (Download the transactions starting on {next_statement_date_str})")
        self.categorize_func_desc_label.grid(row=0, column=0)

        self.summarize_func_frame = tk.Frame(master)
        self.summarize_func_frame.pack()
        self.summarize_func_button = tk.Button(self.summarize_func_frame, text="compile_and_summarize_transactions()", command=self.run_summarize_func)
        self.summarize_func_button.grid(row=0, column=0)
        self.summarize_func_desc_label = tk.Label(self.summarize_func_frame, text="Read and summarize 'CorrectedStatements' for all data")
        self.summarize_func_desc_label.grid(row=1, column=0, columnspan=3)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

    def init_working_directory(self):
        print("--> Making directories and downloading required files to cct_init_files/")
        subprocess.run(['mkdir', 'data'])
        subprocess.run(['mkdir', 'data/CorrectedStatements', 'data/RawStatements'])
        subprocess.run(['mkdir', 'model'])
        subprocess.run(['gdown','--folder', 'https://drive.google.com/drive/folders/1RdQUjnQV3rb6-pKMM6pYxup7rGO5w4yt?usp=drive_link'])
        print('--> Installation is complete. The GUI should have opened in another tab..')
        return

    def run_retrain_func(self):
        retrain_classifier()

    def run_categorize_func(self):
        categorize_last_raw_statement()

    def run_summarize_func(self):
        compile_corrected_statements()
        summarize_monthly_transactions()


root = tk.Tk()
app = ScriptRunnerApp(root)
root.mainloop()

