import tkinter as tk

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Hello World App")
    root.geometry("300x150")  # Set window size

    # Create a label widget
    label = tk.Label(root, text="Hello, World!12,", font=("Arial", 16))
    label.pack(pady=40)  # Add padding around the label

    # Run the application loop
    root.mainloop()

if __name__ == "__main__":
    main()
