from tkinter import *
import sqlite3

def main():
    window = Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.title("Max Allocation")
    app_width = 680
    app_height = 680
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

    topframe = Frame(window)
    topframe.pack(anchor=CENTER)

    with sqlite3.connect("maxAllocation.db") as db:
        cursor = db.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            size REAL NOT NULL);
            """)

    def rCalScreen():
        rCalWindow = Toplevel(window)
        rCalWindow.title("R Calculator")
        app_width = int(screen_width / 2)
        app_height = int(screen_height / 2)
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        rCalWindow.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        for widget in rCalWindow.winfo_children():
            widget.destroy()

        def addR():
            totalR = float(entR.get()) + float(totR.get())
            totR.delete(0, "end")
            totR.insert(0, totalR)

        lblR = Label(rCalWindow, text="R:")
        lblR.pack(padx=10, pady=5, side=TOP)


        entR = Entry(rCalWindow)
        entR.pack(padx=10, pady=5, side=TOP)
        entR.insert(0, "0")

        lblTotR = Label(rCalWindow, text="Total R:")
        lblTotR.pack(padx=10, pady=5, side=TOP)

        totR = Entry(rCalWindow)
        totR.pack(padx=10, pady=5, side=TOP)
        totR.insert(0, "0")

        butRCounter = Button(rCalWindow, text="Add", font=("Arial", 12), command=addR)
        butRCounter.pack(pady=50)

    butRCounter = Button(topframe, text="R Calculator", font=("Arial", 12), command=rCalScreen)
    butRCounter.pack(pady=50)

    window.mainloop()

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
