import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
import os
#import pyautogui
from matplotlib.backends.backend_pdf import PdfPages

"""
DMT Version 2

Name: Peter Chao / SQA team

Description: 
This Python script is a graphical user interface (GUI) application designed to visualize and analyze data from a CSV file. 
It offers the following main functionalities:

(1)Display Landing Page: It can display a specific image ("Landing_page.jpg") within the GUI, 
which could serve as a visual reference or introduction to the application.

(2)Generate Charts: Users can select different options from a dropdown menu, including "Release," "Parent Suite," and "Browser." Each option generates a specific type of bar chart based on the data contained in the provided CSV file ("CSVTestCaseResultFull.csv"). 
These charts display the total counts of pass and fail results according to the selected criteria.

(3)Save Charts as PDF: The application provides the ability to save the generated charts as a PDF file, 
allowing users to document and share the analysis results conveniently.
"""


# Global variables
screenshot_index = 1
subdirectory = "image_data"
file_path = os.path.join(subdirectory, "CSVTestCaseResultFull.csv")
image_path = os.path.join(subdirectory, "Landing_page.jpg")
df = pd.read_csv(file_path)
canvas = None
pdf_pages = None  # Initialize PdfPages object

def display_landing_page():
    landing_page_img = Image.open("Landing_page.jpg")
    landing_page_img = landing_page_img.resize((300, 100), Image.ANTIALIAS)
    landing_page_img = ImageTk.PhotoImage(landing_page_img)
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=landing_page_img)
    canvas.image = landing_page_img

def capture_screenshot():
    global screenshot_index
    screenshot = ImageGrab.grab()
    screenshot.save(f"screenshot_{screenshot_index}.png", "PNG")
    screenshot_index += 1

def generate_chart(event):
    global canvas, pdf_pages # Add pdf_pages to the global scope
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    option = selected_option.get()

    if option == 'Landing Page':
        display_landing_page()

    elif option == 'Release':
        result_counts = df.groupby('da_app_release')['status'].value_counts().unstack(fill_value=0)
        result_counts['Total_Pass'] = result_counts['passed']
        result_counts['Total_Fail'] = result_counts['failed']
        result_counts['Total_Error'] = result_counts['error']
        colors = {'Total_Pass': 'green', 'Total_Fail': 'orange', 'Total_Error': 'red'}
        fig, ax = plt.subplots(figsize=(8, 6))
        result_counts[['Total_Pass', 'Total_Fail', 'Total_Error']].plot(kind='bar', stacked=False, ax=ax, edgecolor='black', color=colors)
        ax.set_title('Total Count of Pass and Fail by da_app_release')
        ax.set_xlabel('da_app_release')
        ax.set_ylabel('Count')
        ax.legend(title='Result')
        for p in ax.patches:
            if p.get_height() > 0:
                ax.annotate(str(int(p.get_height())),
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=9, color='black',
                            xytext=(0, 5), textcoords='offset points')
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()
        ax.set_xticks(range(len(result_counts)))
        ax.set_xticklabels(result_counts.index, rotation=45, ha='right')
        plt.tight_layout()

        # Save the current figure to PDF
        if pdf_pages is not None:
            pdf_pages.savefig(fig)

    elif option == 'Parent_Suite':
        unique_builds = df['da_app_release'].unique()  # Get unique da_app_build values
        result_counts = df.groupby(['parent_suite', 'status', 'da_app_release']).size().unstack(fill_value=0)
        print(result_counts)
        # Calculate total count of 'Pass' and 'Fail' for each 'Parent_Suite'

        unique_data_app_release = df['da_app_release'].unique()
        df_release = pd.DataFrame(unique_data_app_release)
        print("Peter Chao")

        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        result_counts[unique_builds].plot(kind='bar', stacked=False, ax=ax, edgecolor='black')
        ax.set_title('Total Count of Pass and Fail by Parent Suite')
        ax.set_xlabel('Parent Suite')
        ax.set_ylabel('Count')
        ax.legend(title='Result')

        # Add the numbers on top of the bars
        for p in ax.patches:
            if p.get_height() > 0:
                ax.annotate(str(int(p.get_height())),
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=9, color='black',
                            xytext=(0, 5), textcoords='offset points')

        # Embed the plot into tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()
        ax.set_xticks(range(len(result_counts)))
        ax.set_xticklabels(result_counts.index, rotation=45, ha='right')
        # Ensure all elements fit within the plot area
        plt.tight_layout()

        # Save the current figure to PDF
        if pdf_pages is not None:
            pdf_pages.savefig(fig)


    elif option == 'Browser':
        unique_builds = df['da_app_release'].unique()  # Get unique da_app_build values
        result_counts = df.groupby(['browser', 'status', 'da_app_release']).size().unstack(fill_value=0)

        # Calculate total count of 'Pass' and 'Fail' for each 'Browser'

        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        # result_counts[['release_v5_7_2', 'release_v5_7']].plot(kind='bar', stacked=False, ax=ax,edgecolor ='black')
        result_counts[unique_builds].plot(kind='bar', stacked=False, ax=ax, edgecolor='black')
        # unique_data_app_release.plot(kind='bar', stacked=False, ax=ax, edgecolor='black')

        ax.set_title('Total Count of Pass and Fail by Browser')
        ax.set_xlabel('Browser')
        ax.set_ylabel('Count')
        ax.legend(title='Result')

        # Add the numbers on top of the bars
        for p in ax.patches:
            if p.get_height() > 0:
                ax.annotate(str(int(p.get_height())),
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=9, color='black',
                            xytext=(0, 5), textcoords='offset points')

        # Embed the plot into tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()
        ax.set_xticks(range(len(result_counts)))
        ax.set_xticklabels(result_counts.index, rotation=45, ha='right')
        plt.tight_layout()
        if pdf_pages is not None:
            pdf_pages.savefig(fig)


def main():
    global root, selected_option, option_menu, canvas, pdf_pages

    root = tk.Tk()
    root.title("Data Mosaic Tool")

    title_font = ("Helvetica", 16)
    root.option_add("*TButton*Font", title_font)
    root.option_add("*Font", title_font)

    options = ['Release', 'Parent_Suite', 'Browser']
    selected_option = tk.StringVar()
    option_menu = ttk.Combobox(root, textvariable=selected_option, values=options)
    option_menu.pack(pady=10)

    option_menu.bind("<<ComboboxSelected>>", generate_chart)
    display_landing_page()

    # Create a PDF file to save the plots
    pdf_pages = PdfPages("plots.pdf")
    root.mainloop()

if __name__ == "__main__":
    main()
