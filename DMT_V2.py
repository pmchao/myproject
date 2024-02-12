import time

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
import os
#from mpl_toolkits.mplot3d import Axes3D

# Define the subdirectory name
subdirectory = "image_data"
file_path = os.path.join(subdirectory, "CSVTestCaseResultFull.csv")
image_path = os.path.join(subdirectory, "Landing_page.jpg")

# Load the CSV file into a pandas DataFrame
#file_path = "image_data/CSVTestCaseResultFull.csv"
file_path = "CSVTestCaseResultFull.csv"
df = pd.read_csv(file_path)

# Create the main application window
root = tk.Tk()
root.title("Data Mosaic Tool")

# Increase title font size
title_font = ("Helvetica", 16)  # Adjust the font family and size
root.option_add("*TButton*Font", title_font)
root.option_add("*Font", title_font)


# Dropdown menu options
#options = ['Landing Page','Release', 'Parent_Suite', 'Browser']
options = ['Release', 'Parent_Suite', 'Browser']
selected_option = tk.StringVar()

# Dropdown menu
option_menu = ttk.Combobox(root, textvariable=selected_option, values=options)
option_menu.pack(pady=10)
canvas =None

def display_landing_page():
    landing_page_img = Image.open("Landing_page.jpg")
    landing_page_img = landing_page_img.resize((300, 100), Image.ANTIALIAS)
    landing_page_img = ImageTk.PhotoImage(landing_page_img)
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=landing_page_img)
    canvas.image = landing_page_img  # Keep a reference to the image



# Function to generate and display the chart based on the selected option
def generate_chart(event):
    global canvas  # Use the global canvas variable
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    option = selected_option.get()

    if option == 'Landing Page':
        display_landing_page()  # Display the landing page image

    elif option == 'Release':
        # Group by 'da_app_release' and calculate the count of 'result' values
        result_counts = df.groupby('da_app_release')['status'].value_counts().unstack(fill_value=0)

        # Calculate total count of 'Pass' and 'Fail' for each 'da_app_release'
        result_counts['Total_Pass'] = result_counts['passed']
        result_counts['Total_Fail'] = result_counts['failed']
        result_counts['Total_Error'] = result_counts['error']

        # Define color mapping for different result types
        colors = {'Total_Pass': 'green', 'Total_Fail': 'orange', 'Total_Error': 'red'}

        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(8, 6))

        result_counts[['Total_Pass', 'Total_Fail','Total_Error']].plot(kind='bar', stacked=False, ax=ax, edgecolor='black',color=colors)

        ax.set_title('Total Count of Pass and Fail by da_app_release')
        ax.set_xlabel('da_app_release')
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

    elif option == 'Parent_Suite':
        # Group by 'Parent_Suite' and calculate the count of 'result' values
        #result_counts = df.groupby('parent_suite')['status'].value_counts().unstack(fill_value=0)
        unique_builds = df['da_app_release'].unique()  # Get unique da_app_build values
        result_counts = df.groupby(['parent_suite', 'status', 'da_app_release']).size().unstack(fill_value=0)
        print (result_counts)
        # Calculate total count of 'Pass' and 'Fail' for each 'Parent_Suite'

        unique_data_app_release = df['da_app_release'].unique()
        df_release = pd.DataFrame(unique_data_app_release)
        print("Peter Chao")

       # Plot the bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        #result_counts[['test_v5_7', 'test_v5_7_2']].plot(kind='bar', stacked=False, ax=ax,edgecolor ='black')
        result_counts[unique_builds].plot(kind='bar', stacked=False, ax=ax, edgecolor='black')

        #result_counts[[result_counts[[unique_data_app_release[0], unique_data_app_release[1]]].plot(kind='bar', stacked=False, ax=ax,edgecolor ='black'), 'test_v5_7_2']].plot(kind='bar', stacked=False, ax=ax, edgecolor='black')
        #result_counts[df_release.iloc[0,0],df_release.iloc[1,0]].plot(kind='bar', stacked=False,ax=ax, edgecolor='black')

        # unique_data_app_release.plot(kind='bar', stacked=False, ax=ax, edgecolor='black')
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

    elif option == 'Browser':
        # Group by 'Browser' and calculate the count of 'result' values
        #result_counts = df.groupby('browser')['status'].value_counts().unstack(fill_value=0)
        #Peter Chao
        unique_builds = df['da_app_release'].unique()  # Get unique da_app_build values
        result_counts = df.groupby(['browser', 'status', 'da_app_release']).size().unstack(fill_value=0)

        # Calculate total count of 'Pass' and 'Fail' for each 'Browser'


        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        #result_counts[['release_v5_7_2', 'release_v5_7']].plot(kind='bar', stacked=False, ax=ax,edgecolor ='black')
        result_counts[unique_builds].plot(kind='bar', stacked=False, ax=ax, edgecolor='black')
        #unique_data_app_release.plot(kind='bar', stacked=False, ax=ax, edgecolor='black')

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

# Start the main event loop
option_menu.bind("<<ComboboxSelected>>", generate_chart)
display_landing_page()
root.mainloop()
