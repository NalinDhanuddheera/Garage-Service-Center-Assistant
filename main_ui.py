import tkinter as tk
from tkinter import messagebox
from inference_engine import GarageServiceAssistant, VehicleIssue

# Function to handle issue diagnosis
def diagnose_issue():
    issue = issue_var.get()
    if not issue:
        messagebox.showwarning("Input Error", "Please select a vehicle issue.")
        return

    # Initialize the engine
    engine = GarageServiceAssistant("knowledge_base.json")
    engine.reset()
    engine.declare(VehicleIssue(issue=issue))
    engine.run()

    solutions = [fact['solution'] for fact in engine.facts.values() if 'solution' in fact]
    if solutions:
        result_label.config(text=f"Solution: {solutions[0]}", fg="green")
    else:
        result_label.config(text="No solution found for the issue.", fg="red")

# Create the main window
root = tk.Tk()
root.title("Garage Service Center Assistant")
root.geometry("500x400")  # Adjust window size
root.configure(bg="#f0f0f5")  # Light grey background

# Header Frame
header_frame = tk.Frame(root, bg="#003366", pady=10)
header_frame.pack(fill="x")

header_label = tk.Label(header_frame, text="Garage Service Center Assistant", 
                        bg="#003366", fg="white", font=("Helvetica", 18, "bold"))
header_label.pack()

# Main Content Frame
content_frame = tk.Frame(root, bg="#f0f0f5", padx=20, pady=20)
content_frame.pack(expand=True, fill="both")

# Issue Selection Section
issue_label = tk.Label(content_frame, text="Select Vehicle Issue:", bg="#f0f0f5", 
                    fg="#333333", font=("Helvetica", 14, "bold"))
issue_label.pack(anchor="w", pady=10)

issue_var = tk.StringVar()
issues = [
    "engine_won’t_start",
    "unusual_noise",
    "overheating"
]

for issue in issues:
    tk.Radiobutton(content_frame, text=issue.replace('_', ' ').title(), 
                variable=issue_var, value=issue, bg="#f0f0f5", fg="#333333", 
                font=("Helvetica", 12), anchor="w").pack(anchor="w", padx=20)

# Diagnose Button
button_frame = tk.Frame(content_frame, bg="#f0f0f5")
button_frame.pack(pady=20)

diagnose_button = tk.Button(button_frame, text="Diagnose", 
                            command=diagnose_issue, bg="#0059b3", 
                            fg="white", font=("Helvetica", 14, "bold"), 
                            relief="raised", padx=10, pady=5)
diagnose_button.pack()

# Result Section
result_label = tk.Label(content_frame, text="", bg="#f0f0f5", 
                        fg="#333333", font=("Helvetica", 12), wraplength=450)
result_label.pack(pady=10)

# Footer Frame
footer_frame = tk.Frame(root, bg="#003366", pady=10)
footer_frame.pack(fill="x")

footer_label = tk.Label(footer_frame, text="Powered by AI Expert System", 
                        bg="#003366", fg="white", font=("Helvetica", 10, "italic"))
footer_label.pack()

# Run the application
root.mainloop()
