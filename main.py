import tkinter as tk
from tkinter import scrolledtext
from brain import ChatBot  # Import the chatbot brain

class ChatbotGUI:
    def __init__(self, root):
        # Save the window
        self.root = root

        # Set the window title
        self.root.title("Yudhi's AI Assistant")

        # Set the window size
        self.root.geometry("400x500")

        # Set the background color
        self.root.configure(bg="#2c3e50")

        # Connect the GUI to the chatbot brain
        self.bot = ChatBot("Yudhi")

        # Create the title bar at the top
        self.title_label = tk.Label(
            root,
            text="Yudhi AI",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white",
            pady=10
        )
        # Stretch it across the full width
        self.title_label.pack(fill=tk.X)

        # Create the chat log box with a scroll bar
        self.chat_display = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#2c3e50",
            state=tk.DISABLED # Locked so the user cannot type in it
        )
        # Place it in the middle with some padding
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Show a greeting when the app opens
        self.show_message("Yudhi", "Hello my name is Yudhi. How can I help you?")

        # Create the bottom bar that holds the text box and button
        self.input_frame = tk.Frame(root, bg="#2c3e50")
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10), ipady=12)

        # Create the box where the user types their message
        self.entry_box = tk.Entry(self.input_frame, font=("Arial", 12), bg="white", fg="black")
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)

        # Let the user press Enter to send instead of clicking the button
        self.entry_box.bind("<Return>", self.handle_send)

        # Create the Send button
        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            font=("Arial", 10, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            command=self.handle_send
        )
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0), ipady=4)

    def handle_send(self, event=None):
        # Read what the user typed and clean it up
        user_text = self.entry_box.get().strip()

        # Do nothing if the box was empty
        if user_text == "":
            return

        # Clear the text box
        self.entry_box.delete(0, tk.END)

        # Show the user's message in the chat log
        self.show_message("You", user_text)

        # Send the message to the brain and get a reply
        reply = self.bot.get_reply(user_text)

        # If the reply is a joke, show the setup then wait 3 seconds for the punchline
        if type(reply) == list:
            self.show_message("Yudhi", reply[0])
            self.root.after(3000, lambda: self.show_message("Yudhi", "..." + reply[1]))
        else:
            # Show a normal reply right away
            self.show_message("Yudhi", reply)

    def show_message(self, sender, text):
        # Unlock the chat log to add a new message
        self.chat_display.config(state=tk.NORMAL)

        # Add the message to the bottom of the log
        self.chat_display.insert(tk.END, sender + ": " + text + "\n\n")

        # Lock the chat log again
        self.chat_display.config(state=tk.DISABLED)

        # Scroll down so the new message is visible
        self.chat_display.yview(tk.END)

# Start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)

    # Bring the window to the front when it opens
    root.lift()
    root.attributes('-topmost', True)

    # Keep the window open until the user closes it
    root.mainloop()





