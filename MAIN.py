#Description
"""Système de gestion d'une base de données des étudiants en python.
Réalisé par L'krim Mohamed-Anouar, Adil Bouchnita, Elannid Ilyass.
SICS3, ENSAO, 2022. """

#Importation des bibliothèques
import csv
import mimetypes
import re
import smtplib
import statistics
from tkinter.messagebox import showinfo, showwarning, showerror, askokcancel
from datetime import datetime
from functools import partial
from tkinter import *
from tkinter import ttk, filedialog
import tkinter.messagebox as mb
import cx_Oracle
from PIL import ImageTk, Image
from fpdf import FPDF
from tkcalendar import DateEntry
from email.message import EmailMessage

#définition des classes
class Login():
    #déclaration des variables
    global con, cursor
    #en cas de l'erreur:"cx_Oracle.DatabaseError: DPI-1047: Cannot locate a 64-bit Oracle Client library: "The specified module could not be found"." Veuillez dé-commenter la ligne suivante en remplaçant PATH par le chemin du dossier d'installation python. Si l'erreur persiste, installez instant client pour oracle cx et copier les fichiers dll dans PATH.
    # cx_Oracle.init_oracle_client(lib_dir=r"PATH")
    #Dans la ligne suivante il fault remplacer system/system par le login et le mot de passe de la base de données oracle cx. Assurez vous que cette opération est faite pour toute ligne identique dans le code à voir les lignes 360 et 651.
    con = cx_Oracle.connect('system/system@localhost:1521/XE')
    cursor = con.cursor()

    #déclaration des fonctions
    def __init__(self):

        global apoge, tkWindow, password, username, var1, my_label, cmp, mod

        tkWindow = Tk()
        password = StringVar()
        apoge = StringVar()
        username = StringVar()
        var1 = IntVar()
        self.cmp = 3
        # creation des tables dans la base de donnee
        try:

            cursor.execute("create table login(nom varchar2(30),password varchar2(30),class varchar2(30),id number)")
            cursor.execute(
                "create table note(id number,python float,securite float,crypto float,so float,bigdata float,ma_learning float)");
            cursor.execute(
                "create table etudiants(id number,name varchar2(30),prenom varchar2(30),email varchar2(30),genre varchar2(30),d2n varchar2(30),filiere varchar2(30),image varchar2(30))")
            cursor.execute("insert into login values('admin',123,'admin',0)")
            cursor.execute(
                "INSERT INTO etudiants(id, name, prenom, email, GENRE, d2n, filiere, image) VALUES(1, 'lkrim', 'anouar', 'anouarlkrim48@gmail.com', 'male', '20/10/2001', 'sics3', null)")
            cursor.execute(
                "INSERT INTO login(id, nom, password,class ) VALUES (1, 'anouar.lkrim', 'anouar.lkrim', 'etudiant')")
            cursor.execute(
                "INSERT INTO note (id,securite, crypto,so, bigdata,ma_learning,python) VALUES ({},{},{},{},{},{},{})".format(
                    1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
            con.commit()
        except:
            pass

        tkWindow.title('ENSAO')
        tkWindow.resizable(0, 0)
        screen_width = tkWindow.winfo_screenwidth()
        screen_height = tkWindow.winfo_screenheight()
        window_height = 421
        window_width = 770
        a = int((screen_width / 2) - (window_width / 2))
        b = int((screen_height / 2) - (window_height / 2))
        tkWindow.geometry("{}x{}+{}+{}".format(window_width, window_height, a, b))

        frame = Frame(tkWindow, bg="#4f85e8")
        frame.place(x=0, y=0, width=306, height=421)
        frame2 = Frame(tkWindow, bg="black")
        frame2.place(x=306, y=0, width=464, height=421)
        bg1 = PhotoImage(file="group-of-diverse-grads-throwing-caps-up-in-the-sky_ccexpress (1).gif")
        my_label = Label(frame2, image=bg1)
        my_label.place(x=0, y=0, width=464, height=421)

        frame3 = Frame(tkWindow, bg="white")
        frame3.place(x=171, y=113, width=397, height=210)

        Label(frame3, bg="white").grid(row=0, column=0)
        Label(frame3, text="LOGIN:", font="Times 25", bg="#ffffff").grid(row=1, column=0)
        Entry(frame3, textvariable=username, borderwidth=3).grid(row=1, column=1)
        Label(frame3, text="APOGEE:", font="Times 25", bg="#ffffff").grid(row=2, column=0)
        Entry(frame3, textvariable=apoge, borderwidth=3).grid(row=2, column=1)
        Label(frame3, text="MOT-DE-PASSE:", font="Times 25", bg="#ffffff").grid(row=3, column=0)
        global pas
        pas = Entry(frame3, textvariable=password, show='*', borderwidth=3)
        pas.grid(row=3, column=1)


        c1 = Checkbutton(frame3, text='visibilité du mdp', variable=var1, onvalue=1, offvalue=0, command=self.visible).grid(
            row=4, column=0)

        validateLogin = partial(self.validateLogin, username, password, apoge)
        loginButton = Button(frame3, text="LOGIN", font="15", command=validateLogin).grid(row=5, column=0)
        loginButton = Button(frame3, text="RESET", font="15", command=self.reset).grid(row=5, column=1)

        tkWindow.mainloop()

    def reset(self):
        apoge.set("")
        username.set("")
        password.set("")

    def visible(self):
        if var1.get():
            pas.configure(show='')
        else:
            pas.configure(show="*")

    def validateLogin(self, username, password, apoge):
        list = cursor.execute("select * from login")
        test = True
        if apoge.get().isdigit() and apoge.get() != "" and username.get() != "" and password.get() != "":

            for i in list:
                if username.get() == i[0] and password.get() == i[1] and str(i[3]) == apoge.get():
                    test = False
                    if i[2] == "admin":
                        showinfo("Succès", "La connexion a été bien établie.\n Vous êtes administrateur.")
                        global mode_compte,id_compte
                        mode_compte="admin"
                        id_compte=i[3]
                        tkWindow.destroy()
                        b = bienvenu()
                    elif i[2] == "etudiant":
                        mode_compte = "etudiant"
                        id_compte = i[3]
                        showinfo("Succès", "La connexion a été bien établie.\n Vous êtes étudiant.")
                        tkWindow.destroy()
                        b = bienvenu()
        else:
            test = False
            showwarning("Erreur!",
                            "Veuillez vérifier le suivant:\n1)Cetraines entrées sont vides !\n2)Entrez un chiffre dans le champs 'APOGEE'.")

        if test:
            self.cmp -= 1
            if self.cmp == 0:
                tkWindow.destroy()
            else:
                showwarning("Erreur!",
                            "N°APOGEE ou le nom ou mot de passe est incorrect.\n(Il vous reste {} tentatives.)\n".format(
                                self.cmp))


class gestion_student(Login):

    def __init__(self):

        global moncanvas, id_student, idimg, tkWindow1, tab1, frame1, frame2, student_id_e, student_name_e, dob, student_fname_e, student_email_e, student_gender_e, student_filier_e, iid
        # creation d'une interface
        tkWindow1 = Tk()
        tkWindow1['bg'] = '#4f85e8'
        tkWindow1.title("Gestion Etudiants")
        tkWindow1.resizable(0, 0)
        screen_width = tkWindow1.winfo_screenwidth()
        screen_height = tkWindow1.winfo_screenheight()
        window_height = 520
        window_width = 1251
        a = int((screen_width / 2) - (window_width / 2))
        b = int((screen_height / 2) - (window_height / 2))
        tkWindow1.geometry("{}x{}+{}+{}".format(window_width, window_height, a, b))

        frame1 = Frame(tkWindow1, bg="#6ac2b4")
        frame1.place(x=400, y=0, width=849, height=519)
        tab1 = ttk.Treeview(frame1)
        id_student = StringVar()
        student_name_e = StringVar()
        student_fname_e = StringVar()
        student_email_e = StringVar()
        student_filier_e = StringVar()
        student_gender_e = StringVar()
        student_id_e = StringVar()
        frame2 = Frame(tkWindow1, bg="#46a7f1")
        dob = DateEntry(frame2, font=("Arial", 12), width=15)


        canvas = Canvas(tkWindow1, width=320, height=100)
        canvas.place(x=71, y=0)
        img = open(r'ensalogo.jpeg')
        img = (Image.open(r'ensalogo.jpeg'))
        resized_image = img.resize((320, 100), Image.ANTIALIAS)
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor=NW, image=new_image)

        # cration de table
        tab1['columns'] = ("ID", "NOM", "PRENOM", "EMAIL", "GENRE", "DATE DE NAISSANCE", "FILIERE")
        tab1.column("ID", anchor=CENTER, width=40)
        tab1.column("NOM", anchor=CENTER, width=80)
        tab1.column("PRENOM", anchor=CENTER, width=80)
        tab1.column("EMAIL", anchor=CENTER, width=100)
        tab1.column("GENRE", anchor=CENTER, width=80)
        tab1.column("DATE DE NAISSANCE", anchor=CENTER, width=100)
        tab1.column("FILIERE", anchor=CENTER, width=80)
        tab1.heading('ID', text='ID')
        tab1.heading('NOM', text='NOM')
        tab1.heading('PRENOM', text='PRENOM')
        tab1.heading('EMAIL', text='EMAIL')
        tab1.heading('GENRE', text='GENRE')
        tab1.heading('DATE DE NAISSANCE', text='DATE DE NAISSANCE')
        tab1.heading('FILIERE', text='FILIERE')
        tab1['show'] = 'headings'
        tab1.place(x=50, y=43, width=750, height=446)

        frame2.place(x=70, y=110, width=308, height=385)
        Label(frame2, text="Id :", font="Times 20", bg="#46a7f1", fg="black").grid(row=0, column=0)
        Label(frame2, text="Nom :", font="Times 20", bg="#46a7f1", fg="black").grid(row=1, column=0)
        Label(frame2, text="Prenom :", font="Times 20", bg="#46a7f1", fg="black").grid(row=2, column=0)
        Label(frame2, text="E-mail :", font="Times 20", bg="#46a7f1", fg="black").grid(row=3, column=0)
        Label(frame2, text="Genre :", font="Times 20", bg="#46a7f1", fg="black").grid(row=5, column=0)
        Label(frame2, text="Date :", font="Times 20", bg="#46a7f1", fg="black").grid(row=6, column=0)
        Label(frame2, text="Filière :", font="Times 20", bg="#46a7f1", fg="black").grid(row=4, column=0)


        ###entry dse champs

        Entry(frame2, width=20, textvariable=id_student).grid(row=0, column=1)
        Entry(frame2, width=20, textvariable=student_name_e).grid(row=1, column=1)
        Entry(frame2, width=20, textvariable=student_fname_e).grid(row=2, column=1)
        Entry(frame2, width=20, textvariable=student_email_e).grid(row=3, column=1)
        OptionMenu(frame2, student_filier_e, "CP1", "CP2", "SICS-3", "SICS-4", "SICS-5").grid(row=4, column=1)
        OptionMenu(frame2, student_gender_e, "Male", "Female").grid(row=5, column=1)
        dob.grid(row=6, column=1)

        # Button:
        Label(frame2, bg="#46a7f1").grid(row=7, column=1)
        Button(frame2, text="VIDER", font="15", command=self.vider).grid(row=8, column=1)
        Button(frame2, text="RECHERCHER", font="15", command=self.recherche).grid(row=8, column=0)
        Label(frame2, text="------------------------------", bg="#46a7f1", fg="black").grid(row=9, column=0)
        Label(frame2, text="------------------------------", bg="#46a7f1", fg="black").grid(row=9, column=1)
        Button(frame2, text="MODIFIER", font="15", command=self.modifier).grid(row=10, column=0)
        Button(frame2, text="SUPPRIMER", font="15", command=self.supprimer).grid(row=10, column=1)
        Button(tkWindow1, text="RETOUR", font="15", command=self.retour).grid(row=10, column=1)

        # si a selection va faire un mouvement
        tab1.bind('<ButtonRelease-1>', self.remplir)
        tab1.bind('<Double-1>', self.double_clik)
        list = cursor.execute("select * from etudiants order by id")
        for i in list:
            tab1.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        tkWindow1.mainloop()

        # ----------------------------------------ReCHERCHE------------------------------------------------

    def recherche(self):
        for i in tab1.get_children():
            tab1.delete(i)

        reqa = "SELECT * FROM etudiants where 1 = 1 "
        if student_name_e.get() != "":
            reqa += " and name like '%" + student_name_e.get().upper() + "%'"
        if student_fname_e.get() != "":
            reqa += " and prenom like '%" + student_fname_e.get().upper() + "%'"
        if student_email_e.get() != "":
            reqa += " and email like '%" + student_email_e.get().upper() + "%'"
        if student_gender_e.get() != "":
            reqa += " and genre = '" + student_gender_e.get().upper() + "'"
        if student_filier_e.get() != "":
            reqa += " and filiere = '" + student_filier_e.get().upper() + "'"
        if id_student.get() != "":
            reqa = "SELECT * FROM etudiants where id={}".format(int(id_student.get()))
        reqa+=" order by id"

        list = cursor.execute(reqa)
        for i in list:
            tab1.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

        # ---------------------------------------------------------------------------------

    def double_clik(self, event):
        mot = tab1.selection()[0]
        iid = tab1.item(mot)['values'][0]
        tkWindow1.destroy()
        n = note_etu(iid)

    def remplir(self, event):

        mot = tab1.selection()[0]
        student_name_e.set(tab1.item(mot)['values'][1])
        student_fname_e.set(tab1.item(mot)['values'][2])
        student_email_e.set(tab1.item(mot)['values'][3])
        student_gender_e.set(tab1.item(mot)['values'][4])
        student_filier_e.set(tab1.item(mot)['values'][6])
        dob.set_date(tab1.item(mot)['values'][5])

    def vider(self):

        for i in tab1.get_children():
            tab1.delete(i)

        id_student.set("")
        student_name_e.set("")
        student_fname_e.set("")
        student_email_e.set("")
        student_gender_e.set("")
        student_filier_e.set("")
        dob.set_date(datetime.now())

    def emailcheck(self, email):  # return 1 for non-validate email
        if (re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)):
            return True

        else:
            return False

    def modifier(self):
        mot = tab1.selection()[0]
        iid = tab1.item(mot)['values'][0]

        if student_name_e.get() == "" or student_fname_e.get() == "" or not self.emailcheck(student_email_e.get()):
            showerror('Erreur!',
                      "Veuillez vérifier le suivant :\n1)Cetraines entrées sont vides !\n2)L'email doit être du format XXX@YYY.ZZ .")
        else:
            requete = "update etudiants set name ='{}' , prenom = '{}' ,email='{}' , genre = '{}' ,d2n='{}'  ,filiere = '{}' ," \
                      " image = '{}'  where id ={}"\
                .format(
                student_name_e.get().upper(), student_fname_e.get().upper(), student_email_e.get().upper(),
                student_gender_e.get().upper(), dob.get(), student_filier_e.get().upper(), "null", iid)

            cursor.execute(requete)
            con.commit()
            showinfo("Succès", "Modification réussite.")

    def supprimer(self):
        mot = tab1.selection()[0]
        iid = tab1.item(mot)['values'][0]
        if askokcancel("SUPPRIMER", "Voulez-vous vraiment supprimer cette ligne ?"):
            cursor.execute("delete from etudiants where id={}".format(iid))
            cursor.execute("delete from note where id={}".format(iid))
            cursor.execute("delete from login where id={}".format(iid))
            con.commit()
            showinfo("Succès", "Suppression réussite.")
            self.vider()
            list = cursor.execute("SELECT * FROM etudiants order by id")
            for i in list:
                tab1.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    def retour(self):
        tkWindow1.destroy()
        b=bienvenu()


class note_etu(Login):
    #début classe notes
    #déclaration des fonctions
    def __init__(self,iid):
        #déclaration des variables
        global moncanvas, idimg, x, moyenne, tab1, var1, tkWindow2, frame1, frame2, python, id, securite, crypto, so, big_data, machine, label_nom,id
        tkWindow2 = Tk()
        frame2 = Frame(tkWindow2, bg="#d3cf9d")
        frame1 = Frame(tkWindow2, bg="#4f85e8")
        tab1 = ttk.Treeview(frame1)
        con = cx_Oracle.connect('system/system@localhost:1521/XE')
        cursor = con.cursor()
        id_student = IntVar()
        python = DoubleVar()
        securite = DoubleVar()
        crypto = DoubleVar()
        so = DoubleVar()
        big_data = DoubleVar()
        machine = DoubleVar()
        moyenne = DoubleVar()
        var1 = IntVar()
        label_nom = Label(frame1)
        label_nom.place(x=30, y=10)
        id = iid
        self.x = 0

        # creation d'une interface

        tkWindow2['bg'] = '#6395bb'
        tkWindow2.title("NOTE")
        tkWindow2.resizable(0, 0)
        screen_width = tkWindow2.winfo_screenwidth()
        screen_height = tkWindow2.winfo_screenheight()
        window_height = 400
        window_width = 1000
        a = int((screen_width / 2) - (window_width / 2))
        b = int((screen_height / 2) - (window_height / 2))
        tkWindow2.geometry("{}x{}+{}+{}".format(window_width, window_height, a, b))

        frame1.place(x=60, y=150, width=849, height=519)
        style = ttk.Style

        # cration de table

        tab1['columns'] = ("ID", "PYTHON", "SECURITE", "CRYPTOGRAPHIE", "S.O", "BIG_DATA", "MACHINE_LEARNING")
        tab1.column("ID", anchor=CENTER, width=80)
        tab1.column("PYTHON", anchor=CENTER, width=80)
        tab1.column("SECURITE", anchor=CENTER, width=100)
        tab1.column("CRYPTOGRAPHIE", anchor=CENTER, width=100)
        tab1.column("S.O", anchor=CENTER, width=50)
        tab1.column("BIG_DATA", anchor=CENTER, width=80)
        tab1.column("MACHINE_LEARNING", anchor=CENTER, width=100)
        tab1.heading('ID', text='ID')
        tab1.heading('PYTHON', text='PYTHON')
        tab1.heading('SECURITE', text='SECURITE')
        tab1.heading('CRYPTOGRAPHIE', text='CRYPTOGRAPHIE')
        tab1.heading('S.O', text='S.O')
        tab1.heading('BIG_DATA', text='BIG_DATA')
        tab1.heading('MACHINE_LEARNING', text='MACHINE_LEARNING')
        tab1['show'] = 'headings'
        tab1.place(x=25, y=43, width=800, height=150)

        frame2.place(x=0, y=0, width=1251, height=150)

        Label(frame2, text="PYTHON :", font="15", bg="#d3cf9d", fg="black").grid(row=1, column=0)
        Label(frame2, text="SECURITE :", font="15", bg="#d3cf9d", fg="black").grid(row=1, column=2)
        Label(frame2, text="CRYPTOGRAPHIE :", font="15", bg="#d3cf9d", fg="black").grid(row=1, column=4)
        Label(frame2, text="S.O :", font="15", bg="#d3cf9d", fg="black").grid(row=2, column=0)
        Label(frame2, text="BIG_DATA :", font="15", bg="#d3cf9d", fg="black").grid(row=2, column=2)
        Label(frame2, text="MACHINE_LEARNING :", font="15", bg="#d3cf9d", fg="black").grid(row=2, column=4)


        Label(frame2, text="    MOYENNE :", font="15", bg="#d3cf9d", fg='red').grid(row=2, column=6)

        ###entry des champs

        Entry(frame2, width=10, textvariable=python).grid(row=1, column=1)
        Entry(frame2, width=10, textvariable=securite).grid(row=1, column=3)
        Entry(frame2, width=10, textvariable=crypto).grid(row=1, column=5)
        Entry(frame2, width=10, textvariable=so).grid(row=2, column=1)
        Entry(frame2, width=10, textvariable=big_data).grid(row=2, column=3)
        Entry(frame2, width=10, textvariable=machine).grid(row=2, column=5)
        moy = Entry(frame2, width=10, textvariable=moyenne, font='15', state='disabled', fg="white").grid(row=2,
                                                                                                          column=7)

        # Button:
        Label(frame2, bg="#d3cf9d").grid(row=3, column=1)
        if mode_compte=="admin":
            Label(frame2, text="AFFICHER TOUT:", font="15", bg="#d3cf9d").grid(row=1, column=6)
            Checkbutton(frame2, variable=var1, onvalue=1, offvalue=0, bg="#d3cf9d", command=self.visible).grid(row=1,column=7)
            Button(frame2, text="ENREGISTRER", font="15", command=self.modifier).place(y=100, x=350)
            Button(tkWindow2, text="ACTUALISER", font="15", command=self.actualiser).place(y=100, x=500)
            Button(frame1, text="ENVOYER", font="15", command=self.send_email).place(y=10, x=650)
        Button(frame1, text="PDF", font="15", command=self.pdf).place(y=10, x=780)
        Button(frame2, text="RETOUR", font="15", command=self.retour).grid(row=0, column=0)
        list = cursor.execute("SELECT * FROM note where id={} ".format(id))
        for i in list:
            tab1.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            break
        list_nom = cursor.execute("SELECT * FROM etudiants where id={} ".format(id))
        for j in list_nom:
            nom = j[1]
            prenom = j[2]
            break
        label_nom.configure(text=nom + " " + prenom + " :", font="Verdana 15 underline", bg="#d3bbdf", fg="black")

        tab1.bind('<ButtonRelease-1>', self.remplir)

        tkWindow2.mainloop()

    def modifier(self):
      try:
        if python.get()<0 or python.get()>20 or securite.get()<0 or securite.get()>20 or crypto.get()<0 or crypto.get()>20 or \
                so.get()<0 or so.get()>20 or big_data.get()<0 or big_data.get()>20 or machine.get()<0 or machine.get()>20 :
            showwarning("Erreur!",
                        "La note doit être comprise entre 0 et 20.")
        else:
            requete = "update note set SECURITE ={} , CRYPTO = {} ,SO={} , BIGDATA = {} ,MA_LEARNING={}  ,PYTHON = {}   where id ={}".format(
            python.get(), securite.get(), crypto.get(),
            so.get(), big_data.get(), machine.get(), id)
            cursor.execute(requete)
            con.commit()
            showinfo("Succès", "Modification réussite.")
      except:
          showwarning("Erreur!","Les champs doivent contenir des nombres.")

    def send_email(self):
        with open("contactsfile.csv") as fileh:
            reader = csv.reader(fileh)
            next(reader)
            for name, email in reader:
                message = EmailMessage()
                sender = "test4pythonproject@gmail.com"
                recipient = email
                message['From'] = sender
                message['To'] = recipient
                message['Subject'] = 'NOTES SICS-3:'
                body = "Bonjour " + name + " voici les notes :\n bonne chance "
                message.set_content(body)
                mime_type, _ = mimetypes.guess_type('note\note.pdf')
                mime_type, mime_subtype = mime_type.split('/')
                with open('note/note.pdf', 'rb') as file:
                    filedata = file.read()
                    file_name = file.name
                    message.add_attachment(filedata, maintype='pdf', subtype='pdf', filename=file_name)
                    """message.add_attachment(file.read(),
                                           maintype=mime_type,
                                           subtype=mime_subtype,
                                           filename='note\note.pdf')"""
                mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
                mail_server.set_debuglevel(1)
                mail_server.login("test4pythonproject@gmail.com", 'Azer123@')
                mail_server.send_message(message)
                mail_server.quit()

    def actualiser(self):
        for i in tab1.get_children():
            tab1.delete(i)
        if self.x:
            reqa = "SELECT * FROM note "
        else:
            reqa = "SELECT * FROM note where id={}".format(self.id)
        list = cursor.execute(reqa)

        for i in list:
            tab1.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    def pdf(self):
        txt = open('note/note.txt', 'w')
        x = ""

        for i in tab1.get_children():
            list = cursor.execute("select name,prenom from etudiants where id={}".format(tab1.item(i)["values"][0]))
            for j in list:
                x += "nom :" + str(j[0]) + " , prenom :" + str(j[1])
                x += "\npython : " + str(tab1.item(i)["values"][1]) + "\nsecurite : " + str(
                    tab1.item(i)["values"][2]) + "\ncryptographie : " + str(
                    tab1.item(i)["values"][3]) + "\nsystem : " + str(tab1.item(i)["values"][4]) + "\nbig_data : " + str(
                    tab1.item(i)["values"][5]) + "\nmachin_learning : " + str(tab1.item(i)["values"][6])
                x += "\n--------------------------------------------\n"
        txt.write(x)
        txt.close()
        f = open('note/note.txt', 'r')
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=10)
        for i in f:
            pdf.cell(200, 10, txt=i, ln=1)
        pdf.output('note/note.pdf')
        pdf.close()

    def remplir(self, event):

        mot = tab1.selection()[0]
        self.id = tab1.item(mot)['values'][0]
        python.set(tab1.item(mot)['values'][1])
        securite.set(tab1.item(mot)['values'][2])
        crypto.set(tab1.item(mot)['values'][3])
        so.set(tab1.item(mot)['values'][4])
        big_data.set(tab1.item(mot)['values'][5])
        machine.set(tab1.item(mot)['values'][6])
        s = [float(tab1.item(mot)['values'][1]), float(tab1.item(mot)['values'][2]), float(tab1.item(mot)['values'][3]),
             float(tab1.item(mot)['values'][4]), float(tab1.item(mot)['values'][5]), float(tab1.item(mot)['values'][6])]
        moyenne.set("{:.2f}".format(statistics.mean(s)))
        list = cursor.execute("select name,prenom from etudiants where id={}".format(tab1.item(mot)['values'][0]))
        for i in list:
            nv_text = i[0] + " " + i[1]

        label_nom.configure(text=nv_text+" :")

    def visible(self):
        if var1.get():
            self.x = 1
        else:
            self.x = 0

    def retour(self):
        tkWindow2.destroy()
        if mode_compte=="admin":
            g = gestion_student()
        else :
            b=bienvenu()


class bienvenu(Login):
    #début classe bienvenu
    #déclaration des fonctions
    def etudiant(self):
        tkWindow1.destroy()
        g = gestion_student()
    def affiche_note(self):
        tkWindow1.destroy()
        n=note_etu(id_compte)
    def retour(self):
        tkWindow1.destroy()
        l = Login()
    def ajoute_etu(self):
        tkWindow1.destroy()
        a=ajoute_etudiants()
    def gestion_comp(self):
        tkWindow1.destroy()
        g=gestion_compte()
    def __init__(self):
        global tkWindow1
        tkWindow1 = Tk()
        tkWindow1.title('ENSAO')
        tkWindow1.resizable(0, 0)
        screen_width = tkWindow1.winfo_screenwidth()
        screen_height = tkWindow1.winfo_screenheight()
        window_height = 555
        window_width = 850
        a = int((screen_width / 2) - (window_width / 2))
        b = int((screen_height / 2) - (window_height / 2))
        tkWindow1.geometry("{}x{}+{}+{}".format(window_width, window_height, a, b))
        frame = Frame(tkWindow1, bg="#4f85e8")
        frame.pack(fill=X)
        Label(frame, text="BIENVENUE", font="Times 45", bg="#BFC9CA").pack(fill=X)

        def change_photo(event):
            image_ouvre = Image.open("ensao_autre.jpg")
            photo = ImageTk.PhotoImage(image_ouvre)
            label_image.config(image=photo)
            label_image.image = photo

        def photo_retour(event):
            image_ouvre = Image.open("content_oujda-ensao.jpg")
            image_ouvre.resize(size=(frame1.winfo_reqwidth(), frame1.winfo_reqheight()))
            photo = ImageTk.PhotoImage(image_ouvre)
            label_image.config(image=photo)
            label_image.image = photo

        frame1 = Frame(tkWindow1, bg="#2471A3")
        frame1.place(x=0, y=70, width=849, height=519)
        image_ouvre = Image.open("content_oujda-ensao.jpg")
        photo = ImageTk.PhotoImage(image_ouvre)
        label_image = Label(frame1, image=photo)
        label_image.pack()
        label_image.bind("<Enter>", change_photo)
        label_image.bind("<Leave>", photo_retour)

        # créer un menu
        menubar = Menu(tkWindow1)
        # créer un sous-menu
        filemenu = Menu(menubar, tearoff=0)
        if mode_compte=="admin":
            filemenu.add_command(label="Gestion_comptes", command=self.gestion_comp)
            filemenu.add_command(label="Gestion_etudiants", command=self.etudiant)
            filemenu.add_command(label="Ajouter_etudiants", command=self.ajoute_etu)
        else:
            filemenu.add_command(label="Afficher_notes", command=self.affiche_note)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="Quit", command=self.retour)

        # afficher le menu
        tkWindow1.config(menu=menubar)
        tkWindow1.mainloop()


class ajoute_etudiants:
    global con, cursor
    con = cx_Oracle.connect('system/system@localhost:1521/XE')
    cursor = con.cursor()
    def import_csv(self):
        csv_file = filedialog.askopenfilename()
        file = open(csv_file,"r")
        contents = csv.reader(file,delimiter=";")
        list = cursor.execute('select id from etudiants order by id')
        for i in list:
            x = i[0]
        x += 1
        cmp=0
        for ligne in contents:
            cmp+=1
            cursor.execute("INSERT INTO etudiants (id,name, prenom,email, GENRE,d2n,filiere,image) VALUES ({},'{}','{}','{}','{}','{}','{}','{}')"
                           .format(x,ligne[0].upper(),ligne[1].upper(),ligne[2].upper(),ligne[3],ligne[4],ligne[5],"null"))
            cursor.execute(
                "INSERT INTO login (id,nom, password,class) VALUES ({},'{}','{}','{}')"
                .format(x, ligne[0]+"."+ligne[1], ligne[0]+"."+ligne[1],"etudiant"))
            cursor.execute("INSERT INTO note (id,securite, crypto,so, bigdata,ma_learning,python) VALUES ({},{},{},{},{},{},{})".format(
                x, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
            x+=1
        con.commit()
        self.renitialiser()
        mb.showinfo('Student added', "Bien ajouté\n{} étudiants importés".format(cmp))

    def emailcheck(self,email): #return 1 for non-validate email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            return 0
        else:
            return 1

    def renitialiser(self):
        for i in tree.get_children():
            tree.delete(i)
        list = cursor.execute("select * from etudiants order by id")
        for i in list:
            tree.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    def cancel(self):
        add_student.destroy()
        g = bienvenu()

    def save(self):
        global  student_name_e, student_fname_e, student_email_e, dob, student_gender_e, student_filier_e
        student_name = student_name_e.get()
        student_fname = student_fname_e.get()
        student_email = student_email_e.get()
        student_gender = student_gender_e.get()
        student_birth = dob.get_date()
        student_branche = student_filier_e.get()
        isemailvalid = self.emailcheck(student_email)
    #check entry
        if not student_name or not student_fname or not student_email or not student_gender or not student_birth:
            mb.showerror('Erreur!', "Cetrains entrées sont vides!")
        elif not student_name.isalpha() or not student_fname.isalpha():
            mb.showerror('Erreur!', "Le nom ou le prenom est invalid!")
        elif isemailvalid:
            mb.showerror('Erreur!', "L'e-mail n\'est pas valid!")
        else:
            list=cursor.execute('select id from etudiants order by id')
            for i in list:
                x=i[0]
            x+=1
            requete="INSERT INTO etudiants (id, name, prenom,email, GENRE,d2n,filiere,image) VALUES ({},'{}','{}','{}','{}','{}','{}',{})"\
                .format(x,student_name.upper(), student_fname.upper(), student_email.upper(), student_gender, student_birth, student_branche,"null")
            cursor.execute(requete)
            requete = "INSERT INTO note (id,securite, crypto,so, bigdata,ma_learning,python) VALUES ({},{},{},{},{},{},{})".format(
                x,0.0,0.0,0.0,0.0,0.0,0.0)
            print(requete)
            cursor.execute(requete)
            cursor.execute(
                "INSERT INTO login (id,nom, password,class) VALUES ({},'{}','{}','{}')"
                    .format(x, student_name+"."+student_fname, student_name+"."+student_fname, "etudiant"))

            mb.showinfo('Student added', f"L'etudiant {student_name} {student_fname} est ajouté avec succès.")
            con.commit()
            self.renitialiser()

#choosing fonts
    headlabelfont = ("bold", 15,)
    labelfont = ('Helvetica', 12)
    entryfont = ('Helvetica', 12)

#initialisation gui
    def __init__(self):
        global add_student
        add_student = Tk()
        add_student.title('Ajouter un étudiant')
        add_student.resizable(0, 0)
        screen_width = add_student.winfo_screenwidth()
        screen_height = add_student.winfo_screenheight()
        window_height = 600
        window_width = 1200
        a = int((screen_width / 2) - (window_width / 2))
        b = int((screen_height / 2) - (window_height / 2))
        add_student.geometry("{}x{}+{}+{}".format(window_width, window_height, a, b))
        global   tkWindow1, tab1, student_name_e, dob, student_fname_e, student_email_e, student_gender_e, student_filier_e


        student_name_e= StringVar()
        student_fname_e= StringVar()
        student_email_e= StringVar()
        student_filier_e= StringVar()
        student_gender_e= StringVar()

#coloring
        headlabelfont = ("bold", 15,)
        labelfont = ('Helvetica', 12)
        entryfont = ('Helvetica', 12)
        left_bg = "#2471A3"
        center_bg = "#AED6F1"
        title_bg = "#BFC9CA"

        Label(add_student, text="Ajouter un étudiant", font=headlabelfont, bg=title_bg).pack(fill=X)


        left_frame = Frame(add_student, bg=left_bg)
        left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

        center_frame = Frame(add_student, bg=center_bg)
        center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
        global right_frame,tree
        right_frame = Frame(add_student, bg="#DFE0E0")
        right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)
        tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE, columns=(
        'Student ID', "Name", "family name", "Email Address", "Gender", "Date of Birth", "filiere"))

        #fill left frame
###labels
        Label(left_frame, text="Nom :", font=labelfont, bg=left_bg).place(relx=0.375, rely=0.05)
        Label(left_frame, text="Prenom :", font=labelfont, bg=left_bg).place(relx=0.345, rely=0.18)
        Label(left_frame, text="E-mail :", font=labelfont, bg=left_bg).place(relx=0.375, rely=0.31)
        Label(left_frame, text="Genre", font=labelfont, bg=left_bg).place(relx=0.375, rely=0.44)
        Label(left_frame, text="Date de naissance :", font=labelfont, bg=left_bg).place(relx=0.25, rely=0.57)
        Label(left_frame, text="Filière :", font=labelfont, bg=left_bg).place(relx=0.375, rely=0.7)
        Label(left_frame, text="", font=labelfont, bg=left_bg)
###entry
        Entry(left_frame,width=20, textvariable=student_name_e, font=entryfont).place(x=30, rely=0.1)
        Entry(left_frame,width=20, textvariable=student_fname_e, font=entryfont).place(x=30, rely=0.23)
        Entry(left_frame,width=20, textvariable=student_email_e, font=entryfont).place(x=30, rely=0.36)
        OptionMenu(left_frame, student_filier_e, "CP1","CP2","SICS-3","SICS-4","SICS-5").place(x=60, rely=0.75, relwidth=0.5)
        OptionMenu(left_frame, student_gender_e, "Male", "Female").place(x=60, rely=0.49, relwidth=0.5)
        dob = DateEntry(left_frame, font=("Arial", 12), width=15)
        dob.place(x=40, rely=0.62)

    #center frame

        Button(center_frame, text='Sauvegarder', font=labelfont, command=self.save, width=14).place(relx=0.20, rely=0.15)
        Button(add_student, text='Retour', font=labelfont, command=self.cancel, width=14).place(x=0, y=0)
        Button(center_frame, text='Reinitialiser', font=labelfont, command=self.renitialiser, width=14).place(relx=0.20, rely=0.30)
        Button(center_frame, text='Importer CSV', font=labelfont,command=self.import_csv, width=14).place(relx=0.20, rely=0.45)



#right Frame


        canvas = Canvas(right_frame, width = 600, height=150)
        canvas.pack()
        img = open(r'ensalogo.jpeg')
        img= (Image.open(r'ensalogo.jpeg'))
        resized_image= img.resize((600,150), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)
        canvas.create_image(0,0, anchor=NW, image=new_image)

        #display_records
        tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,columns=('Student ID', "Name", "family name", "Email Address", "Gender", "Date of Birth", "filiere"))
        tree.place(y=110, relwidth=1, relheight=0.75, relx=0)

        #X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
        Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

        #X_scroller.pack(side=BOTTOM, fill=X)
        Y_scroller.pack(side=RIGHT, fill=Y)

        tree.config(yscrollcommand=Y_scroller.set)

        tree.heading('Student ID', text='ID', anchor=CENTER)
        tree.heading('Name', text='Prenom', anchor=CENTER)
        tree.heading('family name', text='Nom', anchor=CENTER)
        tree.heading('Email Address', text='email', anchor=CENTER)
        tree.heading('Gender', text='Gender', anchor=CENTER)
        tree.heading('Date of Birth', text='DOB', anchor=CENTER)
        tree.heading('filiere', text='FILIERE', anchor=CENTER)

        tree.column('#0', width=0, stretch=NO)
        tree.column('#1', width=40, stretch=NO)
        tree.column('#2', width=140, stretch=NO)
        tree.column('#3', width=200, stretch=NO)
        tree.column('#4', width=80, stretch=NO)
        tree.column('#5', width=80, stretch=NO)
        tree.column('#6', width=80, stretch=NO)
        tree.column('#7', width=150, stretch=NO)

        list = cursor.execute("select * from etudiants order by id")
        for i in list:
            tree.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        add_student.mainloop()


class gestion_compte(Login):

    def modifier(self):
        mot = tree.selection()[0]
        iid = tree.item(mot)['values'][0]
        if name_login.get() == "" or passwd.get() == "" or confir_passwd.get() == "":
            mb.showerror('Erreur!', "Cetraines entrées sont vides!")
        elif passwd.get() != confir_passwd.get():
            mb.showerror('Erreur!', "Le mot de pass et la confirmation ne sont pas identiques.")
        else:
            requete = "update login set nom ='{}' , password = '{}' ,class='{}' where id={}".format(
                name_login.get(), passwd.get(), clas.get(),iid)
            cursor.execute(requete)
            con.commit()
            mb.showinfo("Succès", "Modification réussite.")
            self.renitialiser()

    def remplir(self,event):
        mot = tree.selection()[0]
        id = tree.item(mot)['values'][0]
        print(id)
        name_login.set(tree.item(mot)['values'][1])
        passwd.set(tree.item(mot)['values'][2])
        confir_passwd.set(tree.item(mot)['values'][2])
        clas.set(tree.item(mot)['values'][3])

    def supprimer(self):
        mot = tree.selection()[0]
        iid = tree.item(mot)['values'][0]
        if mb.askokcancel("SUPPRIMER", "Voulez-vous vraiment supprimer cette ligne?"):
            cursor.execute("delete from login where id={}".format(iid))
            con.commit()
            mb.showinfo("Succès", "Suppression réussite.")
            self.renitialiser()

    def renitialiser(self):
        for i in tree.get_children():
            tree.delete(i)
        list = cursor.execute("select * from login order by id")
        for i in list:
            tree.insert(parent='', index='end', values=(i[3], i[0], i[1], i[2]))

    def cancel(self):
        gestion.destroy()
        b=bienvenu()

    def compte_existe(self,login):
        list = cursor.execute("select * from login")
        test = False
        for i in list:
            if i[0]==login:
                test=True
        return test

    def save(self):
    #check entry
        if name_login.get()=="" or  passwd.get()=="" or confir_passwd.get()=="":
            mb.showerror('Erreur!', "Cetraines entrées sont vides!")
        elif passwd.get()!=confir_passwd.get():
                mb.showerror('Erreur!', "Le mot de pass et la confirmation ne sont pas identiques.")
        elif self.compte_existe(name_login.get()):
                mb.showerror('Erreur!', "Ce compte est déjà existant !")
        else:
                list=cursor.execute('select id from login order by id')
                for i in list:
                  x=i[0]
                x+=1
                requete="INSERT INTO login (id, nom, password,class) VALUES ({},'{}','{}','{}')".format(x,name_login.get(), passwd.get(), clas.get())
                cursor.execute(requete)
                mb.showinfo('Gestion compte', f"Compte {name_login.get()} ajouté avec succès.")
                self.renitialiser()
                con.commit()

    headlabelfont = ("bold", 15,)
    labelfont = ('Helvetica', 12)
    entryfont = ('Helvetica', 12)

    def __init__(self):
        global gestion,tkWindow1, tab1,name_login,passwd,confir_passwd,clas
        gestion = Tk()
        gestion.title('Gestion des comptes')
        gestion.resizable(0, 0)
        screen_width = gestion.winfo_screenwidth()
        screen_height = gestion.winfo_screenheight()
        window_height = 600
        window_width = 1200
        a = int((screen_width / 2) - (window_width / 2))
        b = int((screen_height / 2) - (window_height / 2))
        gestion.geometry("{}x{}+{}+{}".format(window_width, window_height, a, b))



        name_login= StringVar()
        passwd= StringVar()
        confir_passwd=StringVar()
        clas= StringVar()
#coloring
        headlabelfont = ("bold", 15,)
        labelfont = ('Helvetica', 12)
        entryfont = ('Helvetica', 12)
        left_bg = "#2471A3"
        center_bg = "#AED6F1"
        title_bg = "#BFC9CA"

        Label(gestion, text="Gestion des Comptes", font=headlabelfont, bg=title_bg).pack(fill=X)


        left_frame = Frame(gestion, bg=left_bg)
        left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

        center_frame = Frame(gestion, bg=center_bg)
        center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
        global right_frame,tree
        right_frame = Frame(gestion, bg="#DFE0E0")
        right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)
        tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE, columns=(
        "id","login","passwd","class"))

        #fill left frame
###labels
        Label(left_frame, text="NOM UTILISATEUR :", font=labelfont, bg=left_bg).place(relx=0.05, rely=0.05)
        Label(left_frame, text="MOT DE PASSE :", font=labelfont, bg=left_bg).place(relx=0.05, rely=0.18)
        Label(left_frame, text="CONFIRMATION :", font=labelfont, bg=left_bg).place(relx=0.05, rely=0.31)
        Label(left_frame, text="CLASS", font=labelfont, bg=left_bg).place(relx=0.05, rely=0.44)

        ###entry
        Entry(left_frame,width=15, textvariable=name_login, font=entryfont).place(x=10, rely=0.11)
        Entry(left_frame,width=15, textvariable=passwd, font=entryfont).place(x=10, rely=0.25)
        Entry(left_frame,width=15, textvariable=confir_passwd, font=entryfont).place(x=10, rely=0.37)
        OptionMenu(left_frame, clas, "admin","etudiant").place(relx=0.1, rely=0.5, relwidth=0.5)


        #center frame

        Button(center_frame, text='Ajouter', font=labelfont, command=self.save, width=14).place(relx=0.2, rely=0.15)
        Button(gestion, text='Retour', font=labelfont, command=self.cancel, width=14).place(x=0, y=0)
        Button(center_frame, text='Rénitialiser', font=labelfont, command=self.renitialiser, width=14).place(relx=0.2, rely=0.30)
        Button(center_frame, text='Modifier', font=labelfont,command=self.modifier, width=14).place(relx=0.2, rely=0.45)
        Button(center_frame, text='Supprimer', font=labelfont,command=self.supprimer, width=14).place(relx=0.2, rely=0.60)

        canvas = Canvas(right_frame, width = 600, height=150)
        canvas.pack()
        img = open(r'ensalogo.jpeg')
        img = (Image.open(r'ensalogo.jpeg'))
        resized_image = img.resize((600, 150), Image.ANTIALIAS)
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor=NW, image=new_image)

        tree = ttk.Treeview(right_frame, height=60, selectmode=BROWSE,columns=("id","login","passwd","class"))
        tree.place(y=110, relwidth=1, relheight=0.75, relx=0)

        #X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
        Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

        #X_scroller.pack(side=BOTTOM, fill=X)
        Y_scroller.pack(side=RIGHT, fill=Y)

        tree.config(yscrollcommand=Y_scroller.set)

        tree.heading('id', text='ID', anchor=CENTER)
        tree.heading('login', text='LOGIN', anchor=CENTER)
        tree.heading('passwd', text='PASSWD', anchor=CENTER)
        tree.heading('class', text='CLASS', anchor=CENTER)


        tree.column('#0', width=0, )
        tree.column('#1', width=60 )
        tree.column('#2', width=60 )
        tree.column('#3', width=60 )
        tree.column('#4', width=60)

        tree.bind('<ButtonRelease-1>', self.remplir)

        list = cursor.execute("select * from login order by id")
        for i in list:
            tree.insert(parent='', index='end', values=(i[3],i[0], i[1], i[2] ))
        gestion.mainloop()


l = Login()
