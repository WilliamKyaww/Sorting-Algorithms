import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random import shuffle, sample

# Import the sorting functions from algorithm functions.py
from algorithm_functions import selection_sort, bubble_sort, merge_sort, quick_sort

# Create a function to create labels
def create_label(text):
    label = tk.Label(window, text=text)
    label.pack()

# Create a function to create buttons
def create_button(text, command):
    button = tk.Button(window, text=text, command=command)
    button.pack()

# Create the GUI window
window = tk.Tk()
window.title("Sorting Algorithm Selector")

# Function to sort the list based on the selected algorithm
def sort_list():
    selected_algorithm = algorithm_var.get()
    num_of_numbers = int(num_of_numbers_var.get())

    unsorted_list = sample(range(1, 101), num_of_numbers)  # Generate random unsorted numbers

    sorting_functions = {
        "Selection Sort": selection_sort,
        "Bubble Sort": bubble_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }

    if selected_algorithm in sorting_functions:
        sorted_list = sorting_functions[selected_algorithm](unsorted_list)
        result_label.config(text=f"Sorted List: {sorted_list}")

        # Display the generated unsorted numbers
        unsorted_label.config(text=f"Unsorted Numbers: {', '.join(map(str, unsorted_list))}")
    else:
        messagebox.showerror("Error", "Please select a sorting algorithm.")

# Create a label and entry for the number of unsorted numbers
create_label("Enter the number of unsorted numbers:")
num_of_numbers_var = tk.StringVar()
num_of_numbers_entry = tk.Entry(window, textvariable=num_of_numbers_var)
num_of_numbers_entry.pack()

# Create a dropdown to select the sorting algorithm
create_label("Select Sorting Algorithm:")
algorithm_var = tk.StringVar()
algorithm_dropdown = ttk.Combobox(window, textvariable=algorithm_var, state="readonly")
algorithm_dropdown['values'] = ("Selection Sort", "Bubble Sort", "Merge Sort", "Quick Sort")
algorithm_dropdown.pack()

# Create a button to sort the list
create_button("Sort", sort_list)

# Label to display the sorted list
result_label = tk.Label(window, text="")
result_label.pack()

# Label to display the unsorted numbers
unsorted_label = tk.Label(window, text="")
unsorted_label.pack()

window.mainloop()
