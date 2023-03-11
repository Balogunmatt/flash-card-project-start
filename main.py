from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
try:
    my_data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    french_word_df = pd.read_csv("data/french_words.csv")
    french_word_list = french_word_df.to_dict(orient="records")
else:
    french_word_list = my_data.to_dict(orient="records")
    next_word = {}


def word_choice():
    global french_word_list, next_word, flip_timer
    window.after_cancel(flip_timer)
    next_word = random.choice(french_word_list)
    canvas.itemconfig(text_lang, text="French", fill="black")
    canvas.itemconfig(text_word, text=next_word["French"], fill="black")
    canvas.itemconfig(img, image=front_image)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(img, image=back_image)
    canvas.itemconfig(text_word, text=next_word["English"], fill="white")
    canvas.itemconfig(text_lang, text="English", fill="white")

def is_known():
    french_word_list.remove(next_word)
    print(len(french_word_list))
    my_data = pd.DataFrame(french_word_list)
    my_data.to_csv("data/words_to_learn.csv", index=False)
    word_choice()


window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flash card")

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
img = canvas.create_image(400, 263, image=front_image)
text_lang = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
text_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=word_choice)
unknown_button.grid(column=0, row=1)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)

word_choice()

window.mainloop()
