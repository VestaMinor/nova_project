import calendar
import sqlite3, datetime
import tkinter as tk
from calendar import Calendar
from sched import scheduler
from tkinter import ttk
from tkcalendar import DateEntry
from tkcalendar import Calendar

current_month = datetime.datetime.now().month #jelenlegi hónap
current_year = datetime.datetime.now().year #jelenlegi év





conn = sqlite3.connect('nova.db')
cursor = conn.cursor()

#cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY AUTOINCREMENT, nev TEXT, beosztas TEXT)''')
#conn.commit()

#Navigate, Optimize, Validate, Accomplish - NOVA


schedule_list = ["Mass", "Uppermass", "Magnifica", "Vállalat", "Jelzálog"]
close_types_list = ["Kódos", "Kulcsos", "Kódos/kulcsos"]


class Registration:

    def profile_checker(name, card_id, schedulers, registration_root, status_label):
        name = name.get()
        card_id = card_id.get()
        schedulers = schedulers.get()


        if schedulers in schedule_list:

            cursor.execute("SELECT name FROM profiles WHERE card_id = ?", (card_id,))
            result = cursor.fetchone()

            if result == None:
                print("Profil létrehozása!")

                cursor.execute("INSERT INTO profiles (schedule, name, card_id) VALUES (?, ?, ?)", (schedulers, name, card_id))
                conn.commit()

                status_label.config(text="Kész!", fg="green")
                root.after(1500, lambda: registration_root.destroy())


            else:
                print("Létezik ilyen profil!")
                status_label.config(text="Sikertelen!", fg="red")
                root.after(2000, lambda: status_label.config(text="Profil már létezik!"))
                root.after(4000, lambda: status_label.config(text=""))


        else:
            status_label.config(text="Kérlek a kijelölt beosztások közül válassz!", fg="red")
            root.after(2000, lambda: status_label.config(text=""))




    def registration_window():

        registration_root = tk.Tk()
        registration_root.title("NOVA - regisztráció")
        registration_root.geometry("400x200")

        registration_label = tk.Label(registration_root, text="Regisztráció")
        registration_label.place(relx=0.5, rely=0.1, anchor="center")



        get_name_label = tk.Label(registration_root, text="Neved:")
        get_name_label.place(relx=0.1, rely=0.25, anchor="center")
        get_name = tk.Entry(registration_root)
        get_name.place(relx=0.35, rely=0.25, anchor="center")


        card_id_label = tk.Label(registration_root, text="Kártya azonosító (6 számjegy):")
        card_id_label.place(relx=0.25, rely=0.4, anchor="center")
        get_card_id = tk.Entry(registration_root)
        get_card_id.place(relx=0.65, rely=0.4, anchor="center")



        schedule_label = tk.Label(registration_root, text="Beosztás:")
        schedule_label.place(relx=0.1, rely=0.55, anchor="center")

        schedulers = ttk.Combobox(registration_root, values=schedule_list)
        schedulers.place(relx=0.35, rely=0.55, anchor="center")

        close_type_label = tk.Label(registration_root, text="Kulcsos/kódos:")
        close_type_label.place(relx=0.14, rely=0.7, anchor="center")

        close_type = ttk.Combobox(registration_root, values=close_types_list)
        close_type.place(relx=0.44, rely=0.7, anchor="center")


        status_label = tk.Label(registration_root, text="")
        status_label.place(relx=0.7, rely=0.87, anchor="center")

        upload_profile_button = tk.Button(registration_root, text="Regisztrálás", command=lambda: Registration.profile_checker(get_name, get_card_id, schedulers, registration_root, status_label))
        upload_profile_button.place(relx=0.5, rely=0.87, anchor="center")

        registration_root.mainloop()







class Profile:

    def set_new_days(self):


        def upload_days():
            start_date = start_date_button.get_date()
            end_date = end_date_button.get_date()

            #dátumok stringgé alakítás datetime-al
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")


            if start_date > end_date:
                print("KEZDŐ ÉRTÉK NEM LEHET NAGYOBB!")

            else:

                db_days = []

                cursor.execute("SELECT days FROM reserved_days")
                days_result = cursor.fetchall()

                if days_result == []:
                    print("Még nincs lefoglalt nap!")

                    current = start_date
                    while current <= end_date:
                        cursor.execute("INSERT INTO reserved_days (user_id, days) VALUES (?, ?)",
                                       (card_id_entry.get(), current.strftime("%Y-%m-%d")))
                        conn.commit()
                        current += datetime.timedelta(days=1)

                        set_status_label.config(text="Sikeres hozzáadás!", fg="green")
                        set_root.after(1500, lambda: set_status_label.config(text=""))
                        cal.selection_set(current)



                elif days_result != []:

                    for day in days_result:
                        db_days.append(day[0])


                    if start_str in db_days or end_str in db_days:
                        set_status_label.config(text="Már lefoglalt napot nem foglalhatsz le!", fg="red")
                        set_root.after(1500, lambda: set_status_label.config(text=""))

                    elif start_str not in db_days and end_str not in db_days:

                        current = start_date
                        while current <= end_date:
                            cursor.execute("INSERT INTO reserved_days (user_id, days) VALUES (?, ?)", (card_id_entry.get(), current.strftime("%Y-%m-%d")))
                            conn.commit()
                            current += datetime.timedelta(days=1)

                            set_status_label.config(text="Sikeres hozzáadást!", fg="green")
                            set_root.after(1500, lambda: set_status_label.config(text=""))
                            cal.selection_set(current)

        set_root = tk.Tk()
        set_root.geometry("500x500")
        set_root.title("NOVA - Hozzáadás")

        #kezdő dátum
        start_date_label = tk.Label(set_root, text="Kezdő dátum:")
        start_date_label.place(relx=0.22, rely=0.15, anchor="center")

        start_date_button = DateEntry(set_root, width=12, background='darkblue', foreground='white', borderwidth=2)
        start_date_button.place(relx=0.22, rely=0.2, anchor="center")

        #befejező dátum
        end_date_label = tk.Label(set_root, text="Záró dátum:")
        end_date_label.place(relx=0.22, rely=0.25, anchor="center")

        end_date_button = DateEntry(set_root, width=12, background='darkblue', foreground='white', borderwidth=2)
        end_date_button.place(relx=0.22, rely=0.3, anchor="center")

        cal = Calendar(set_root, background='darkblue', foreground='white')
        cal.place(relx=0.7, rely=0.25, anchor="center")

        #kijelölt piros napok
        cal.tag_config('piros', background='red', foreground='white')

        #lefoglalt napok kijelölése
        cursor.execute("SELECT days FROM reserved_days")
        days_result = cursor.fetchall()

        if days_result == []:
            print("Nem volt lefoglalva nap!")


        else:
            for day in days_result:
                day = datetime.datetime.strptime(day[0], "%Y-%m-%d").date()
                cal.calevent_create(day, '', 'piros')

        set_status_label = tk.Label(set_root, text="")
        set_status_label.place(relx=0.5, rely=0.8, anchor="center")

        excuted_button = tk.Button(set_root, text="Hozzáadás", command=lambda: upload_days())
        excuted_button.place(relx=0.5, rely=0.9, anchor="center")


    def login_checker(card_id):
        cursor.execute("SELECT name FROM profiles WHERE card_id = ?", (card_id,))
        result_name = cursor.fetchone()

        if result_name == None:
            status_label.config(text="Nincs ilyen azonosító!", fg="red")
            root.after(2000, lambda: status_label.config(text=""))

        else:
            Profile.login_window(result_name[0]) #Ha minden feltétel teljesül, akkor belép a rendszerbe
            global card_id_entry



    def exit_program(login_root):
        root.destroy()
        login_root.destroy()

    def login_window(result_name, days_result):
        login_root = tk.Tk()
        login_root.geometry("800x300")
        login_root.title(f"NOVA - Üdvözöllek {result_name}!")

        #felső menüsor
        menu_bar = tk.Menu(login_root)
        login_root.config(menu=menu_bar)

        #menü opciók
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="   Fájl   ", menu=menu_file)
        menu_file.add_command(label="Kilépés", command=lambda: Profile.exit_program(login_root))


        closure_label = tk.Label(login_root, text="Zárás menü:", font=("Arial", 11))
        closure_label.place(relx=0.15, rely=0.05, anchor="center")

        add_day_button = tk.Button(login_root, text="Nap(ok) hozzáadása", width=20, command=lambda: Profile.set_new_days(self=None))
        add_day_button.place(relx=0.15, rely=0.15, anchor="center")

        modification_day_button = tk.Button(login_root, text="Nap(ok) módosítása", width=20)
        modification_day_button.place(relx=0.15, rely=0.25, anchor="center")

        delete_day_button = tk.Button(login_root, text="Nap(ok) törlése", width=20)
        delete_day_button.place(relx=0.15, rely=0.35, anchor="center")


        statistic_label = tk.Label(login_root, text="Profil statisztika:", font=("Arial", 11))
        statistic_label.place(relx=0.8, rely=0.05, anchor="center")


        #zárt napok számának lekérdezése
        cursor.execute("SELECT * FROM reserved_days WHERE strftime('%m') = '05' AND card_id = ?", (card_id_entry.get(),))




        year_statistic = tk.Label(login_root, text=f"Éves: {days_result[0]} nap")
        year_statistic.place(relx=0.8, rely=0.15, anchor="center")








root = tk.Tk()

root.title("NOVA - bejelentkezés")
root.geometry("400x400")

login_label = tk.Label(root, text="Bejelentkezés")
login_label.place(relx=0.5, rely=0.1, anchor="center")

card_id_label = tk.Label(root, text="Kártya azonosító (6 számjegy):")
card_id_label.place(relx=0.5, rely=0.3, anchor="center")
card_id_entry = tk.Entry(root)
card_id_entry.place(relx=0.5, rely=0.37, anchor="center")

status_label = tk.Label(root, text="")
status_label.place(relx=0.5, rely=0.55, anchor="center")

login_button = tk.Button(root, text="Belépés", width=20, command=lambda: Profile.login_checker(card_id_entry.get()))
login_button.place(relx=0.5, rely=0.45, anchor="center")



registration_label = tk.Label(root, text="Nincs még fiókod?")
registration_label.place(relx=0.5, rely=0.85, anchor="center")

registration_button = tk.Button(root, text="Regisztráció", command=lambda: Registration.registration_window())
registration_button.place(relx=0.5, rely=0.92, anchor="center")



root.mainloop()

