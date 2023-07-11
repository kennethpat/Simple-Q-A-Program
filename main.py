"""
HOW TO RUN:

This program was tested on macOS only.
However, if you have the required components installed
correctly, you should be able to run the code on 
Microsoft Windows as well.

Please make sure that you have the following installed:
Python 3, tkinter, nltk

To run the program, launch a new terminal and simply
run the following command:
python3 main.py

If the above-mentioned components are correctly installed,
you should see the main window of the program.

To exit the program, simply close the main window.
If you have the answer windows opened, closing the main
window will also make the program exit.
"""

import requests
import nltk
import tkinter as tk
from bs4 import BeautifulSoup
from googlesearch import search
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tkinter import messagebox, scrolledtext
nltk.download("punkt")
nltk.download("stopwords")

def search_topic(topic):
    query = topic + " wikipedia"
    search_results = search(query, num_results=5)
    urls = []
    for url in search_results:
        urls.append(url)
    return urls

def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.get_text(separator=" ")
    return content

def answer_question(content, question):
    sentences = sent_tokenize(content)
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(question)
    keywords = [word for word in words if word.lower() not in stop_words]

    matching_sentences = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if all(keyword.lower() in sentence_lower for keyword in keywords):
            matching_sentences.append(sentence)

    if matching_sentences:
        return matching_sentences[0]
    else:
        return "I'm sorry, I don't have an answer to that question."

def ask_button_click():
    topic = entry_topic.get()
    question = entry_question.get()

    if topic == "":
        messagebox.showwarning("Missing Topic", "Please enter a topic.")
        return

    if question == "":
        messagebox.showwarning("Missing Question", "Please enter a question.")
        return

    urls = search_topic(topic)
    if urls:
        content = scrape_content(urls[0])
        answer = answer_question(content, question)

        answer_window = tk.Toplevel(window)
        answer_window.title("Answer")
        answer_window.geometry("800x600")

        answer_text = scrolledtext.ScrolledText(answer_window, wrap=tk.WORD, font=("Menlo", 24))
        answer_text.pack(fill=tk.BOTH, expand=True)
        answer_text.insert(tk.END, answer)
    else:
        messagebox.showinfo("No Results", "No results found for the topic.")

def main():
    global window 
    window = tk.Tk()
    window.title("Simple Q&A Program")
    window.geometry("600x300")
    global label_topic
    label_topic = tk.Label(window, text="Topic:", font=("Lucida Grande", 32))
    label_topic.pack()
    global entry_topic
    entry_topic = tk.Entry(window, width=25, font=("Lucida Grande", 32), borderwidth=5)
    entry_topic.pack()

    label_question = tk.Label(window, text="Question:", width=25, font=("Lucida Grande", 32), borderwidth=5)
    label_question.pack()
    global entry_question 
    entry_question = tk.Entry(window, width=25, font=("Lucida Grande", 32), borderwidth=5)
    entry_question.pack()

    ask_button = tk.Button(window, text="Ask", font=("Lucida Grande", 32), command=ask_button_click)
    ask_button.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
