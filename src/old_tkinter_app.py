import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

class ScriptRunnerApp:
    def __init__(self, master):
        self.master = master
        master.title(f"Credit Card Tracker v{cct_version}")

        # First time running script... download dependency files
        if "cct_init_files" not in os.listdir():
            self.init_working_directory()
        
        #if 'all_transactions.csv' in os.listdir('data'):
        #    self.check_for_category_consistency()


        # Load PNG image
        self.img = Image.open(f"cct_init_files/piggybank.png")  # Replace "image.png" with the path to your PNG image
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
        self.categorize_func_button = tk.Button(self.categorize_func_frame, text="categorize_all_raw_statements()", command=self.run_categorize_func)
        self.categorize_func_button.grid(row=1, column=0)
        self.categorize_func_desc_label = tk.Label(self.categorize_func_frame, text=f"Read and auto-categorize the most recent 'RawStatement' (Download the transactions starting on {next_statement_date_str})")
        self.categorize_func_desc_label.grid(row=0, column=0)

        self.summarize_func_frame = tk.Frame(master)
        self.summarize_func_frame.pack()
        self.summarize_func_button = tk.Button(self.summarize_func_frame, text="compile_and_summarize_transactions()", command=self.run_summarize_func)
        self.summarize_func_button.grid(row=0, column=0)
        self.summarize_func_desc_label = tk.Label(self.summarize_func_frame, text="Read and summarize 'CorrectedStatements' for all data")
        self.summarize_func_desc_label.grid(row=0, column=1)

        self.streamlit_script_frame = tk.Frame(master)
        self.streamlit_script_frame.pack()
        self.streamlit_script_button = tk.Button(self.summarize_func_frame, text="run_streamlit_app()", command=self.run_streamlit_script)
        self.streamlit_script_button.grid(row=2, column=0)
        self.streamlit_script_desc_label = tk.Label(self.streamlit_script_frame, text="Open the Streamlit App to Visualize the monthly summary")
        self.streamlit_script_desc_label.grid(row=1, column=0)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

    def init_working_directory(self):
        print("--> Making directories and downloading required files to cct_init_files/")
        subprocess.run(['mkdir', f'data'])
        subprocess.run(['mkdir', f'data/CorrectedStatements', f'data/RawStatements'])
        subprocess.run(['mkdir', 'model'])
        subprocess.run(['gdown','--folder', 'https://drive.google.com/drive/folders/1RdQUjnQV3rb6-pKMM6pYxup7rGO5w4yt?usp=drive_link'])
        print('--> Installation is complete. The GUI should have opened in another tab..')
        return
    
    def check_for_category_consistency(self):
        '''This function is run at the start-up of the app. It checks for consistency of the categories in the csv file and categories in the VendorIDs folder'''
        categories_for_current_run = load_unique_categories()
        categories_from_last_run = load_categories_from_all_transactions()
        new_categories = get_list_difference(categories_from_last_run, categories_for_current_run)
        
        if categories_from_last_run != categories_for_current_run:
            print("--> I detected that you added a vendor category/categories: ", ', '.join(new_categories))
            print("--> I will re-train the classifier and re-categorize all of the 'Corrected Statements that exist (leaving your manual changes un-touched)")
            retrain_classifier()

            for statement_fn in os.listdir('data/CorrectedStatements'):
                if '.xlsx' in statement_fn:
                    reclassify_corrected_statement(statement_fn)
            print("--> Finished re-categorizing all of the 'Corrected Statements'")
        return

    def run_retrain_func(self):
        retrain_classifier()

    def run_categorize_func(self):
        categorize_all_raw_statements()

    def run_summarize_func(self):
        compile_corrected_statements()
        summarize_monthly_transactions()

    def run_streamlit_script(self):
        subprocess.run(f'streamlit run {src_dir}/StreamlitApp.py')
        

root = tk.Tk()
app = ScriptRunnerApp(root)
root.mainloop()