from typing import List

BACKGROUND_COLOR = "#B1DDC6"
from random import *

import pandas

from tkinter import *

window = Tk()
window.title("Flashcard")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

# --------------------- UI -----------------------------


old_image = PhotoImage(file="images/card_front.png")
new_image = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(400, 263, image=old_image)
canvas.grid(row=0, column=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

# --------------------- Create new flashcards -----------------------------


random_word = {}
word_list = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    word_list = original_data.to_dict(orient="records")
else:
    word_list = data.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(canvas_image, image=new_image)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=random_word["English"])

flip_timer = window.after(3000, func=flip_card)


def is_known():
    word_list.remove(random_word)
    print(len(word_list))
    data = pandas.DataFrame(word_list)
    data.to_csv("words_to_learn.csv", index=False)

    next_card()

def next_card():
    global random_word, flip_timer, word_list
    window.after_cancel(flip_timer)
    random_word = choice(word_list)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_word["French"], fill="black")
    canvas.itemconfig(canvas_image, image=old_image)
    flip_timer = window.after(3000, func=flip_card)




card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

right_button_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_img, highlightthickness=0, borderwidth=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_button_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, borderwidth=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()






window.mainloop()