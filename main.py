import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import requests

# Configure the generative AI API key and model
genai.configure(api_key='AIzaSyDJC5lt2EQ1rI07apWkMXu1sqXo0Y_Ij8s')

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])


# Function to check internet connectivity
def check_internet_connection():
    try:
        requests.get('http://www.google.com', timeout=3)
        return True
    except requests.ConnectionError:
        return False


# Function to handle sending a message to the model
def send_message():
    user_input = user_entry.get()

    if user_input.lower() == 'quit':
        root.destroy()
        return

    if "typhoid" not in user_input.lower():
        messagebox.showinfo("Input Error", "Please ask a question related to typhoid.")
        return

    # Check internet connection
    if not check_internet_connection():
        response_text = "Connect to an internet error."
    else:
        # Insert user input into the dictionary
        request = {user_input}

        try:
            response = chat_session.send_message(request)
            response_text = response.text.replace("*", "")  # Remove asterisks from the response
        except Exception as e:
            response_text = "Network error: Unable to get a response."

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    chat_history.insert(tk.END, "Bot: " + response_text + "\n\n")
    chat_history.config(state=tk.DISABLED)

    user_entry.delete(0, tk.END)


# Create the main application window
root = tk.Tk()
root.title("Typhoid Fever Chatbot")

# Create a frame for the chat history
chat_frame = tk.Frame(root)
chat_frame.pack(pady=10)

# Create a scrolled text widget for the chat history
chat_history = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED, width=80, height=20)
chat_history.pack()

# Create an entry widget for user input
user_entry = tk.Entry(root, width=80)
user_entry.pack(pady=5)

# Create a send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Start the main application loop
root.mainloop()
