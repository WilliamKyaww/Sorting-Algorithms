import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
import threading
import copy

# Import the sorting functions from algorithm_functions.py
from algorithm_functions import selection_sort, bubble_sort, merge_sort, quick_sort


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
FONT_FAMILY   = "Segoe UI"

# One colour per algorithm – visually distinct, pastel‑friendly
ALGO_COLOURS = {
    "Selection Sort": "#f38ba8",  # pink
    "Bubble Sort":    "#fab387",  # peach
    "Merge Sort":     "#a6e3a1",  # green
    "Quick Sort":     "#89b4fa",  # blue
}


# ──────────────────────────────────────────────
# Algorithm Definitions
# ──────────────────────────────────────────────
ALGORITHMS = [
    ("Selection Sort", "O(n²)",      selection_sort),
    ("Bubble Sort",    "O(n²)",      bubble_sort),
    ("Merge Sort",     "O(n log n)", merge_sort),
    ("Quick Sort",     "O(n log n)", quick_sort),
]


# ──────────────────────────────────────────────
# Root Window
# ──────────────────────────────────────────────
root = tk.Tk()
root.title("Sorting Algorithm Benchmark")
root.configure(bg=BG_DARK)
root.resizable(False, False)

window_width, window_height = 560, 780
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x_pos = (screen_w - window_width) // 2
y_pos = (screen_h - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")


# ──────────────────────────────────────────────
# Helper – Card Frame
# ──────────────────────────────────────────────
def make_card(parent, **kwargs):
    return tk.Frame(
        parent, bg=BG_CARD,
        highlightbackground=BORDER_COLOR, highlightthickness=1,
        **kwargs,
    )


# ──────────────────────────────────────────────
# Scrollable Container
# ──────────────────────────────────────────────
main_canvas = tk.Canvas(root, bg=BG_DARK, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scroll_frame = tk.Frame(main_canvas, bg=BG_DARK)

scroll_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")),
)
main_canvas.create_window((0, 0), window=scroll_frame, anchor="nw",
                          width=window_width - 20)
main_canvas.configure(yscrollcommand=scrollbar.set)

# Mouse‑wheel scrolling
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)


# ──────────────────────────────────────────────
# Title
# ──────────────────────────────────────────────
tk.Label(
    scroll_frame, text="⚡  Sorting Benchmark",
    font=(FONT_FAMILY, 20, "bold"), fg=ACCENT, bg=BG_DARK,
).pack(pady=(28, 4))

tk.Label(
    scroll_frame, text="Compare algorithm performance side‑by‑side",
    font=(FONT_FAMILY, 10), fg=FG_SECONDARY, bg=BG_DARK,
).pack(pady=(0, 20))


# ──────────────────────────────────────────────
# Input Card – Number of Values
# ──────────────────────────────────────────────
input_card = make_card(scroll_frame)
input_card.pack(padx=32, pady=(0, 16), fill="x")

tk.Label(
    input_card, text="Number of Values",
    font=(FONT_FAMILY, 11, "bold"), fg=FG_PRIMARY, bg=BG_CARD, anchor="w",
).pack(padx=20, pady=(16, 4), fill="x")

tk.Label(
    input_card,
    text="How many random integers should be generated for sorting?",
    font=(FONT_FAMILY, 9), fg=FG_SECONDARY, bg=BG_CARD, anchor="w",
).pack(padx=20, fill="x")

num_var = tk.StringVar(value="1000")
num_entry = tk.Entry(
    input_card, textvariable=num_var,
    font=(FONT_FAMILY, 13), fg=FG_PRIMARY, bg=BG_INPUT,
    insertbackground=ACCENT, relief="flat",
    highlightthickness=1, highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT, justify="center",
)
num_entry.pack(padx=20, pady=(10, 18), ipady=6, fill="x")


# ──────────────────────────────────────────────
# Algorithm Selection Card
# ──────────────────────────────────────────────
algo_card = make_card(scroll_frame)
algo_card.pack(padx=32, pady=(0, 16), fill="x")

tk.Label(
    algo_card, text="Select Algorithms",
    font=(FONT_FAMILY, 11, "bold"), fg=FG_PRIMARY, bg=BG_CARD, anchor="w",
).pack(padx=20, pady=(16, 4), fill="x")

tk.Label(
    algo_card, text="Choose one or more algorithms to benchmark:",
    font=(FONT_FAMILY, 9), fg=FG_SECONDARY, bg=BG_CARD, anchor="w",
).pack(padx=20, fill="x")

algo_vars = {}
checks_frame = tk.Frame(algo_card, bg=BG_CARD)
checks_frame.pack(padx=20, pady=(12, 18), fill="x")

for name, complexity, _ in ALGORITHMS:
    var = tk.BooleanVar(value=False)
    algo_vars[name] = var
    row = tk.Frame(checks_frame, bg=BG_CARD)
    row.pack(fill="x", pady=3)

    # Coloured indicator dot
    dot = tk.Label(row, text="●", font=(FONT_FAMILY, 10),
                   fg=ALGO_COLOURS[name], bg=BG_CARD)
    dot.pack(side="left", padx=(0, 4))

    tk.Checkbutton(
        row, text=name, variable=var,
        font=(FONT_FAMILY, 11), fg=FG_PRIMARY, bg=BG_CARD,
        selectcolor=BG_INPUT, activebackground=BG_CARD,
        activeforeground=ACCENT, highlightthickness=0, bd=0, anchor="w",
    ).pack(side="left")

    tk.Label(
        row, text=complexity, font=(FONT_FAMILY, 9, "italic"),
        fg=FG_SECONDARY, bg=BG_CARD,
    ).pack(side="right", padx=(0, 8))

# Toggle buttons
toggle_frame = tk.Frame(algo_card, bg=BG_CARD)
toggle_frame.pack(padx=20, pady=(0, 16), fill="x")


def select_all():
    for v in algo_vars.values():
        v.set(True)


def deselect_all():
    for v in algo_vars.values():
        v.set(False)


tk.Button(
    toggle_frame, text="Select All", font=(FONT_FAMILY, 9),
    fg=ACCENT, bg=BG_INPUT, activebackground=BORDER_COLOR,
    activeforeground=ACCENT_HOVER, relief="flat", cursor="hand2",
    command=select_all,
).pack(side="left", padx=(0, 8))

tk.Button(
    toggle_frame, text="Deselect All", font=(FONT_FAMILY, 9),
    fg=FG_SECONDARY, bg=BG_INPUT, activebackground=BORDER_COLOR,
    activeforeground=FG_PRIMARY, relief="flat", cursor="hand2",
    command=deselect_all,
).pack(side="left")


# ──────────────────────────────────────────────
# Run Benchmark Button
# ──────────────────────────────────────────────
run_btn = tk.Button(
    scroll_frame, text="Run Benchmark",
    font=(FONT_FAMILY, 13, "bold"), fg=BG_DARK, bg=ACCENT,
    activebackground=ACCENT_ACTIVE, activeforeground=BG_DARK,
    relief="flat", cursor="hand2", disabledforeground="#666680",
)
run_btn.pack(padx=32, ipady=10, fill="x")
run_btn.bind("<Enter>", lambda e: run_btn.configure(bg=ACCENT_HOVER))
run_btn.bind("<Leave>", lambda e: run_btn.configure(bg=ACCENT))

# Status label (shows "Running…" / "Done" feedback)
status_var = tk.StringVar(value="")
status_label = tk.Label(
    scroll_frame, textvariable=status_var,
    font=(FONT_FAMILY, 10), fg=FG_SECONDARY, bg=BG_DARK,
)
status_label.pack(pady=(6, 0))


# ──────────────────────────────────────────────
# Results Section (created once, updated each run)
# ──────────────────────────────────────────────
results_card = make_card(scroll_frame)
# Not packed yet – shown after first benchmark run

BAR_CHART_HEIGHT = 220
BAR_CHART_PAD    = 32

chart_canvas = tk.Canvas(
    results_card, bg=BG_CARD, highlightthickness=0,
    height=BAR_CHART_HEIGHT,
)

results_table_frame = tk.Frame(results_card, bg=BG_CARD)


def show_results(results: list[tuple[str, float]]):
    """
    Display benchmark results as a horizontal bar chart + timing table.

    Parameters
    ----------
    results : list of (algorithm_name, elapsed_seconds)
    """
    # ── Pack the card if first time ──
    results_card.pack(padx=32, pady=(16, 24), fill="x")

    # ── Header ──
    for w in results_card.winfo_children():
        w.destroy()

    tk.Label(
        results_card, text="Results",
        font=(FONT_FAMILY, 11, "bold"), fg=FG_PRIMARY, bg=BG_CARD, anchor="w",
    ).pack(padx=20, pady=(16, 10), fill="x")

    # ── Bar Chart (horizontal bars) ──
    chart = tk.Canvas(
        results_card, bg=BG_CARD, highlightthickness=0,
        height=max(len(results) * 50 + 20, 100),
    )
    chart.pack(padx=20, pady=(0, 10), fill="x")
    results_card.update_idletasks()  # so winfo_width is accurate

    chart_w = chart.winfo_width() or 440
    usable_w = chart_w - 140  # leave room for labels on the left

    max_time = max(t for _, t in results) if results else 1
    if max_time == 0:
        max_time = 1e-9  # prevent division by zero

    y = 16
    bar_h = 28
    for name, elapsed in results:
        colour = ALGO_COLOURS.get(name, ACCENT)
        bar_w = max(int((elapsed / max_time) * usable_w), 6)

        # Label on the left
        chart.create_text(
            130, y + bar_h // 2,
            text=name, anchor="e",
            fill=FG_PRIMARY, font=(FONT_FAMILY, 10),
        )
        # Bar
        chart.create_rectangle(
            140, y, 140 + bar_w, y + bar_h,
            fill=colour, outline="",
        )
        # Time on the bar
        time_str = format_time(elapsed)
        chart.create_text(
            140 + bar_w + 8, y + bar_h // 2,
            text=time_str, anchor="w",
            fill=FG_SECONDARY, font=(FONT_FAMILY, 9),
        )
        y += bar_h + 16

    # ── Detailed Table ──
    table = tk.Frame(results_card, bg=BG_CARD)
    table.pack(padx=20, pady=(0, 18), fill="x")

    # Table header
    hdr = tk.Frame(table, bg=BORDER_COLOR)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Algorithm", font=(FONT_FAMILY, 9, "bold"),
             fg=FG_SECONDARY, bg=BORDER_COLOR, width=18, anchor="w").pack(side="left", padx=8, pady=4)
    tk.Label(hdr, text="Time", font=(FONT_FAMILY, 9, "bold"),
             fg=FG_SECONDARY, bg=BORDER_COLOR, width=14, anchor="e").pack(side="left", padx=8, pady=4)
    tk.Label(hdr, text="Rank", font=(FONT_FAMILY, 9, "bold"),
             fg=FG_SECONDARY, bg=BORDER_COLOR, width=6, anchor="center").pack(side="left", padx=8, pady=4)

    # Sort by time for ranking
    ranked = sorted(results, key=lambda r: r[1])
    rank_map = {name: i + 1 for i, (name, _) in enumerate(ranked)}

    for name, elapsed in results:
        row_bg = BG_INPUT if results.index((name, elapsed)) % 2 == 0 else BG_CARD
        row = tk.Frame(table, bg=row_bg)
        row.pack(fill="x")

        colour = ALGO_COLOURS.get(name, ACCENT)
        tk.Label(row, text=f"● {name}", font=(FONT_FAMILY, 10),
                 fg=colour, bg=row_bg, width=18, anchor="w").pack(side="left", padx=8, pady=5)
        tk.Label(row, text=format_time(elapsed), font=(FONT_FAMILY, 10),
                 fg=FG_PRIMARY, bg=row_bg, width=14, anchor="e").pack(side="left", padx=8, pady=5)

        rank = rank_map[name]
        rank_text = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
        tk.Label(row, text=rank_text, font=(FONT_FAMILY, 10),
                 fg=FG_PRIMARY, bg=row_bg, width=6, anchor="center").pack(side="left", padx=8, pady=5)

    # Scroll to bottom so results are visible
    root.after(100, lambda: main_canvas.yview_moveto(1.0))


def format_time(seconds: float) -> str:
    """Return a human‑friendly string for a duration."""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.1f} µs"
    elif seconds < 1.0:
        return f"{seconds * 1_000:.2f} ms"
    else:
        return f"{seconds:.4f} s"


# ──────────────────────────────────────────────
# Benchmark Logic (runs in a background thread)
# ──────────────────────────────────────────────
def run_benchmark():
    """Validate inputs, run each selected algo, then display results."""
    raw = num_var.get().strip()
    if not raw.isdigit() or int(raw) <= 0:
        messagebox.showwarning("Invalid Input",
                               "Please enter a positive integer for the number of values.")
        return

    selected = [(n, fn) for n, _, fn in ALGORITHMS if algo_vars[n].get()]
    if not selected:
        messagebox.showwarning("No Algorithm Selected",
                               "Please select at least one sorting algorithm.")
        return

    count = int(raw)

    # Disable button while running
    run_btn.configure(state="disabled", bg=BORDER_COLOR)
    status_var.set("Generating random data…")

    def worker():
        # Generate ONE random list; give each algorithm its own copy
        base_list = [random.randint(1, 1_000_000) for _ in range(count)]
        results = []

        for i, (name, sort_fn) in enumerate(selected):
            root.after(0, lambda n=name: status_var.set(f"Running {n}…"))
            data = copy.copy(base_list)
            start = time.perf_counter()
            sort_fn(data)
            elapsed = time.perf_counter() - start
            results.append((name, elapsed))

        # Update UI on the main thread
        def finish():
            status_var.set("✓ Benchmark complete")
            run_btn.configure(state="normal", bg=ACCENT)
            show_results(results)

        root.after(0, finish)

    threading.Thread(target=worker, daemon=True).start()


run_btn.configure(command=run_benchmark)


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
tk.Label(
    scroll_frame, text="Sorting Algorithm Benchmark Tool  •  v2.0",
    font=(FONT_FAMILY, 8), fg=BORDER_COLOR, bg=BG_DARK,
).pack(pady=(20, 14))


# ──────────────────────────────────────────────
# Start the Event Loop
# ──────────────────────────────────────────────
root.mainloop()
