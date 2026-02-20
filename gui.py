import tkinter as tk
from tkinter import ttk, messagebox


# ──────────────────────────────────────────────
# Colour Palette & Style Constants
# ──────────────────────────────────────────────
BG_DARK       = "#1e1e2e"
BG_CARD       = "#2a2a3d"
BG_INPUT      = "#33334d"
FG_PRIMARY    = "#cdd6f4"
FG_SECONDARY  = "#a6adc8"
ACCENT        = "#89b4fa"
ACCENT_HOVER  = "#74c7ec"
ACCENT_ACTIVE = "#b4befe"
BORDER_COLOR  = "#45475a"
SUCCESS_GREEN = "#a6e3a1"
FONT_FAMILY   = "Segoe UI"


# ──────────────────────────────────────────────
# Root Window
# ──────────────────────────────────────────────
root = tk.Tk()
root.title("Sorting Algorithm Benchmark")
root.configure(bg=BG_DARK)
root.resizable(False, False)

# Centre the window on the screen
window_width, window_height = 520, 620
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x_pos = (screen_w - window_width) // 2
y_pos = (screen_h - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")


# ──────────────────────────────────────────────
# Helper – Rounded‑look Card Frame
# ──────────────────────────────────────────────
def make_card(parent, **kwargs):
    """Return a Frame styled as a dark card."""
    frame = tk.Frame(
        parent,
        bg=BG_CARD,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1,
        **kwargs,
    )
    return frame


# ──────────────────────────────────────────────
# Title Section
# ──────────────────────────────────────────────
title_label = tk.Label(
    root,
    text="⚡  Sorting Benchmark",
    font=(FONT_FAMILY, 20, "bold"),
    fg=ACCENT,
    bg=BG_DARK,
)
title_label.pack(pady=(28, 4))

subtitle_label = tk.Label(
    root,
    text="Compare algorithm performance side‑by‑side",
    font=(FONT_FAMILY, 10),
    fg=FG_SECONDARY,
    bg=BG_DARK,
)
subtitle_label.pack(pady=(0, 20))


# ──────────────────────────────────────────────
# Input Card – Number of Values
# ──────────────────────────────────────────────
input_card = make_card(root)
input_card.pack(padx=32, pady=(0, 16), fill="x")

input_header = tk.Label(
    input_card,
    text="Number of Values",
    font=(FONT_FAMILY, 11, "bold"),
    fg=FG_PRIMARY,
    bg=BG_CARD,
    anchor="w",
)
input_header.pack(padx=20, pady=(16, 4), fill="x")

input_desc = tk.Label(
    input_card,
    text="How many random integers should be generated for sorting?",
    font=(FONT_FAMILY, 9),
    fg=FG_SECONDARY,
    bg=BG_CARD,
    anchor="w",
)
input_desc.pack(padx=20, fill="x")

num_var = tk.StringVar(value="1000")
num_entry = tk.Entry(
    input_card,
    textvariable=num_var,
    font=(FONT_FAMILY, 13),
    fg=FG_PRIMARY,
    bg=BG_INPUT,
    insertbackground=ACCENT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT,
    justify="center",
)
num_entry.pack(padx=20, pady=(10, 18), ipady=6, fill="x")


# ──────────────────────────────────────────────
# Algorithm Selection Card
# ──────────────────────────────────────────────
algo_card = make_card(root)
algo_card.pack(padx=32, pady=(0, 16), fill="x")

algo_header = tk.Label(
    algo_card,
    text="Select Algorithms",
    font=(FONT_FAMILY, 11, "bold"),
    fg=FG_PRIMARY,
    bg=BG_CARD,
    anchor="w",
)
algo_header.pack(padx=20, pady=(16, 4), fill="x")

algo_desc = tk.Label(
    algo_card,
    text="Choose one or more algorithms to benchmark:",
    font=(FONT_FAMILY, 9),
    fg=FG_SECONDARY,
    bg=BG_CARD,
    anchor="w",
)
algo_desc.pack(padx=20, fill="x")

# Algorithm definitions: (display name, expected complexity)
ALGORITHMS = [
    ("Selection Sort", "O(n²)"),
    ("Bubble Sort",    "O(n²)"),
    ("Merge Sort",     "O(n log n)"),
    ("Quick Sort",     "O(n log n)"),
]

algo_vars = {}  # name -> BooleanVar

checks_frame = tk.Frame(algo_card, bg=BG_CARD)
checks_frame.pack(padx=20, pady=(12, 18), fill="x")

for idx, (name, complexity) in enumerate(ALGORITHMS):
    var = tk.BooleanVar(value=False)
    algo_vars[name] = var

    row = tk.Frame(checks_frame, bg=BG_CARD)
    row.pack(fill="x", pady=3)

    cb = tk.Checkbutton(
        row,
        text=name,
        variable=var,
        font=(FONT_FAMILY, 11),
        fg=FG_PRIMARY,
        bg=BG_CARD,
        selectcolor=BG_INPUT,
        activebackground=BG_CARD,
        activeforeground=ACCENT,
        highlightthickness=0,
        bd=0,
        anchor="w",
    )
    cb.pack(side="left")

    complexity_label = tk.Label(
        row,
        text=complexity,
        font=(FONT_FAMILY, 9, "italic"),
        fg=FG_SECONDARY,
        bg=BG_CARD,
    )
    complexity_label.pack(side="right", padx=(0, 8))


# ──────────────────────────────────────────────
# Select / Deselect All Buttons
# ──────────────────────────────────────────────
toggle_frame = tk.Frame(algo_card, bg=BG_CARD)
toggle_frame.pack(padx=20, pady=(0, 16), fill="x")


def select_all():
    for v in algo_vars.values():
        v.set(True)


def deselect_all():
    for v in algo_vars.values():
        v.set(False)


select_all_btn = tk.Button(
    toggle_frame,
    text="Select All",
    font=(FONT_FAMILY, 9),
    fg=ACCENT,
    bg=BG_INPUT,
    activebackground=BORDER_COLOR,
    activeforeground=ACCENT_HOVER,
    relief="flat",
    cursor="hand2",
    command=select_all,
)
select_all_btn.pack(side="left", padx=(0, 8))

deselect_all_btn = tk.Button(
    toggle_frame,
    text="Deselect All",
    font=(FONT_FAMILY, 9),
    fg=FG_SECONDARY,
    bg=BG_INPUT,
    activebackground=BORDER_COLOR,
    activeforeground=FG_PRIMARY,
    relief="flat",
    cursor="hand2",
    command=deselect_all,
)
deselect_all_btn.pack(side="left")


# ──────────────────────────────────────────────
# Run Benchmark Button
# ──────────────────────────────────────────────
def on_run_hover(event):
    run_btn.configure(bg=ACCENT_HOVER)


def on_run_leave(event):
    run_btn.configure(bg=ACCENT)


def run_benchmark():
    """Placeholder – validates inputs but does not sort yet."""
    # Validate number input
    raw = num_var.get().strip()
    if not raw.isdigit() or int(raw) <= 0:
        messagebox.showwarning(
            "Invalid Input",
            "Please enter a positive integer for the number of values.",
        )
        return

    # Check at least one algorithm selected
    selected = [name for name, var in algo_vars.items() if var.get()]
    if not selected:
        messagebox.showwarning(
            "No Algorithm Selected",
            "Please select at least one sorting algorithm.",
        )
        return

    # Placeholder feedback
    messagebox.showinfo(
        "Coming Soon",
        f"Benchmark not wired up yet!\n\n"
        f"Values: {raw}\n"
        f"Algorithms: {', '.join(selected)}",
    )


run_btn = tk.Button(
    root,
    text="Run Benchmark",
    font=(FONT_FAMILY, 13, "bold"),
    fg=BG_DARK,
    bg=ACCENT,
    activebackground=ACCENT_ACTIVE,
    activeforeground=BG_DARK,
    relief="flat",
    cursor="hand2",
    command=run_benchmark,
)
run_btn.pack(padx=32, ipady=10, fill="x")
run_btn.bind("<Enter>", on_run_hover)
run_btn.bind("<Leave>", on_run_leave)


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
footer = tk.Label(
    root,
    text="Sorting Algorithm Benchmark Tool  •  v2.0",
    font=(FONT_FAMILY, 8),
    fg=BORDER_COLOR,
    bg=BG_DARK,
)
footer.pack(side="bottom", pady=(0, 14))


# ──────────────────────────────────────────────
# Start the Event Loop
# ──────────────────────────────────────────────
root.mainloop()
