import re
from tkinter import *
import sqlite3
from tkinter import messagebox


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
    global accountId
    accountId = 0

    global pattern
    pattern = r'[^A-Za-z0-9]+'

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
            global accountId
            totalR = float(entR.get()) + float(totR.get())
            if accountId != 0:
                sql = "UPDATE accounts SET size=? WHERE id = ?"

                cursor.execute(sql, (totalR, accountId,))
            totR.delete(0, "end")
            totR.insert(0, totalR)


        lblNameD = Label(rCalWindow, text="Account Name: ")
        lblNameD.pack(padx=10, pady=5, side=TOP)

        lblName = Label(rCalWindow, text="<<None Selected>>")
        lblName.pack(padx=10, pady=5, side=TOP)

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

        butRCounter = Button(rCalWindow, text="Add", command=addR)
        butRCounter.pack(pady=50)

        def accountScreen():
            accScreen = Toplevel(rCalWindow)
            accScreen.title("Account Select")
            app_width = int(screen_width / 2)
            app_height = int(screen_height / 2)
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2)
            accScreen.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

            for widget in accScreen.winfo_children():
                widget.destroy()

            scrollBar = Scrollbar(accScreen, bg="grey")

            scrollBar.pack(side=RIGHT, fill=BOTH)
            accountList = Listbox(accScreen, selectmode=BROWSE, yscrollcommand=scrollBar.set)

            scrollBar.config(command=accountList.yview)
            accountList.pack(fill=BOTH, pady=10, padx=10)

            cursor.execute("SELECT * FROM accounts")
            global arrayA
            arrayA = cursor.fetchall()

            for z in range(0, len(arrayA)):
                accountList.insert(z, f'Name: {arrayA[z][1]} Description: {arrayA[z][2]} R: {arrayA[z][3]}')

            def selectedAccount():
                global accountId
                while True:
                    if accountList.curselection() == ():
                        break
                    choice = int(re.sub(pattern, '', str(accountList.curselection()))) + 1
                    if choice == ():
                        accountList.showwarning("showwarning", "Please select an account entry.")
                        break
                    cursor.execute('SELECT * FROM accounts WHERE id = ?', (choice,))

                    accountId = choice
                    ent = cursor.fetchall()
                    size = ent[0][3]
                    name = ent[0][1]
                    totR.delete(0, "end")
                    totR.insert(0, size)
                    lblName.config(text=name)
                    accScreen.destroy()
                    break


            butOk = Button(accScreen, text="Select", command=selectedAccount)
            butOk.pack(padx=10, pady=5, side=TOP)

            '''def deleteAccount():
                while True:
                    if accountList.curselection() == ():
                        break
                    choice = int(re.sub(pattern, '', str(accountList.curselection()))) + 1
                    print(choice)
                    if choice == ():
                        accountList.showwarning("showwarning", "Please select an account entry.")
                        break
                    cursor.execute('SELECT size FROM accounts WHERE id = ?', (choice,))
                    size = cursor.fetchall()
                    cursor.execute('SELECT name FROM accounts WHERE id = ?', (choice,))
                    name = cursor.fetchall()
                    name = re.sub(pattern, '', str(name))
                    print(name)
                    if messagebox.askyesno("Deleting Entry", f"Are you sure you want to delete diary: {name}"):
                        sql = "DELETE FROM accounts WHERE id = ?"
                        cursor.execute(sql, (choice,))
                        db.commit()
                        accountList.delete(choice)
                        accScreen.destroy()
                        accountScreen()
                    break

            butDeleteAcc = Button(accScreen, text="Delete Account", command=deleteAccount)
            butDeleteAcc.pack(padx=10, pady=5, side=BOTTOM)'''

            def createAccountScreen():
                createAccScreen = Toplevel(accScreen)
                createAccScreen.title("Create Acccount")
                app_width = int(screen_width / 2)
                app_height = int(screen_height / 2)
                x = (screen_width / 2) - (app_width / 2)
                y = (screen_height / 2) - (app_height / 2)
                createAccScreen.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

                for widget in createAccScreen.winfo_children():
                    widget.destroy()

                lblName = Label(createAccScreen, text="Account Name:")
                lblName.pack(padx=10, pady=5, side=TOP)

                entName = Entry(createAccScreen)
                entName.pack(padx=10, pady=5, side=TOP)
                entName.insert(0, "Enter a name for the account")

                lblDesc = Label(createAccScreen, text="Description:")
                lblDesc.pack(padx=10, pady=5, side=TOP)

                entDesc = Entry(createAccScreen)
                entDesc.pack(padx=10, pady=5, side=TOP)
                entDesc.insert(0, "Enter a description for the account")

                lblInitR = Label(createAccScreen, text="Account starting R:")
                lblInitR.pack(padx=10, pady=5, side=TOP)

                entInitR = Entry(createAccScreen)
                entInitR.pack(padx=10, pady=5, side=TOP)
                entInitR.insert(0, "0")

                def createAcc():
                    name = entName.get()

                    description = entDesc.get()

                    size = float(entInitR.get())

                    insert_fields = """INSERT INTO accounts(name, description, size)
                                                    VALUES (?, ?, ?)"""
                    cursor.execute(insert_fields, (name, description, size))
                    db.commit()


                    createAccScreen.destroy()
                    accScreen.destroy()

                    accountScreen()

                butCreate = Button(createAccScreen, text="Create account", command=createAcc)
                butCreate.pack(padx=10, pady=5, side=TOP)


            butCreateAcc = Button(accScreen, text="Create Account", command=createAccountScreen)
            butCreateAcc.pack(padx=10, pady=5, side=TOP)

        butAccount = Button(rCalWindow, text="Select Account", command=accountScreen)
        butAccount.pack(pady=50)

    butRCounter = Button(topframe, text="R Calculator", command=rCalScreen)
    butRCounter.pack(pady=50)

    window.mainloop()

if __name__ == '__main__':
    main()

