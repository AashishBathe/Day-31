from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
word = {}
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
else:
    pass
finally:
    to_learn = data.to_dict(orient="records")


# -------------------------- FLASH CARD GENERATION ---------------------------- #


def random_word():
    try:
        return random.choice(to_learn)
    except IndexError:
        canvas.itemconfig(canvas_img, image=old_img)
        canvas.itemconfig(top_text, fill="black", text="CONGRATS")
        canvas.itemconfig(bot_text, fill="black", font=("Arial", 20, "normal"), text="You now know all the basic words!")
        return {}


def word_change():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = random_word()
    if word != {}:
        french_word = word["French"]
        canvas.itemconfig(canvas_img, image=old_img)
        canvas.itemconfig(top_text, fill="black", text="French")
        canvas.itemconfig(bot_text, fill="black", text=french_word)
        flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global word
    english_word = word["English"]
    canvas.itemconfig(canvas_img, image=new_img)
    canvas.itemconfig(top_text, fill="white", text="English")
    canvas.itemconfig(bot_text, fill="white", text=english_word)


# ------------------------------ NEW LIST ------------------------------------- #

def knows_card():
    global word
    to_learn.remove(word)
    df = pandas.DataFrame(to_learn)
    df.to_csv("words_to_learn.csv", index=False)
    word_change()


# ------------------------------ UI SETUP ------------------------------------- #


window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flash Card App")
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
old_img = PhotoImage(file="images/card_front.png")
new_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=old_img)
top_text = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
bot_text = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
image_cross = PhotoImage(file="images/wrong.png")
cross_button = Button(image=image_cross, bg=BACKGROUND_COLOR, borderwidth=0, command=word_change)
cross_button.grid(row=1, column=0)
image_tick = PhotoImage(file="images/right.png")
tick_button = Button(image=image_tick, bg=BACKGROUND_COLOR, borderwidth=0, command=knows_card)
tick_button.grid(row=1, column=1)
word_change()

window.mainloop()
