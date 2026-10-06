import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
import csv
import os
import pandas as pd
from tkinter import messagebox as tkmb
from tkcalendar import Calendar
from datetime import datetime


class Registrasi:
    def __init__(self, root, login_interface):
        self.root = root
        self.root.title("Registrasi")
        self.root.geometry("320x580+500+50")
        self.login_interface = login_interface

        # Background image
        image_path = "background.png"
        self.bg_image = ctk.CTkImage(Image.open(image_path), size=(320, 580))
        bg_label = ctk.CTkLabel(self.root, image=self.bg_image, text="")
        bg_label.place(relwidth=1, relheight=1)

        # Frame for inputs
        self.frame = ctk.CTkFrame(self.root,
                                  fg_color="white",
                                  corner_radius=0)
        self.frame.place(relx=0.5, rely=0.77, anchor="center")

        # Username input
        self.input_username = ctk.CTkEntry(self.frame,
                                           placeholder_text="Buat Username Anda",
                                           width=230)
        self.input_username.pack(pady=(10, 15))

        # Password input
        self.input_password = ctk.CTkEntry(self.frame,
                                           placeholder_text="Buat Password Anda",
                                           width=230, show="*")
        self.input_password.pack(pady=(0, 15))

        # Buttons
        ctk.CTkButton(self.frame,
                      text="Confirm",
                      width=230,
                      fg_color="#4D3488",
                      hover_color="#C5B0F6", 
                      font=("Poppins", 14, "bold"),
                      command=self.simpan_data).pack(pady=(0, 10))
        ctk.CTkButton(self.frame,
                      text="Back to Login",
                      width=230,
                      fg_color="#4D3488",
                      hover_color="#C5B0F6", 
                      font=("Poppins", 14, "bold"), command=self.back_to_login).pack()

    def simpan_data(self):
        username = self.input_username.get()
        password = self.input_password.get()

        if not username or not password:
            tkmb.showwarning("Warning", "Semua harus diisi!")
            return

        file_path = "data_user.csv"
    
        # Check if username already exists
        if os.path.exists(file_path):
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                for row in reader:
                    if row[0] == username:
                        tkmb.showwarning("Warning", "Username sudah ada. Gunakan username lain.")
                        return

        # Append new user data
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if os.stat(file_path).st_size == 0:
                writer.writerow(["username", "password"])
            writer.writerow([username, password])

        tkmb.showinfo("Success", "Registrasi berhasil!")
    
        # Reload users data to reflect new registration
        self.login_interface.load_users()
    
        self.back_to_login()

    def back_to_login(self):
        self.root.destroy()
        self.login_interface.root.deiconify()

class LoginInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("320x580+500+50")
        self.root.configure(fg_color="#4D3488")

        # Background image
        image_path = "background.png"
        self.bg_image = ctk.CTkImage(Image.open(image_path), size=(320, 580))
        bg_label = ctk.CTkLabel(self.root, image=self.bg_image, text="")
        bg_label.place(relwidth=1, relheight=1)

        # Frame for inputs
        self.frame = ctk.CTkFrame(self.root,
                                  fg_color="white",
                                  corner_radius=0)
        self.frame.place(relx=0.5, rely=0.78, anchor="center")

        # Username input
        self.input_username = ctk.CTkEntry(self.frame,
                                           placeholder_text="Username",
                                           width=230)
        self.input_username.pack(pady=(10, 15))

        # Password input
        self.input_password = ctk.CTkEntry(self.frame,
                                           placeholder_text="Password",
                                           show="*",
                                           width=230)
        self.input_password.pack(pady=(0, 20))

        # Buttons
        ctk.CTkButton(self.frame,
                      text="Log In",
                      command=self.login,
                      fg_color="#4D3488",
                      hover_color="#C5B0F6", 
                      font=("Poppins", 14, "bold"),
                      width=230).pack(pady=(0, 10))
        ctk.CTkButton(self.frame,
                      text="Registrasi",
                      command=self.regist,
                      fg_color="#4D3488",
                      hover_color="#C5B0F6", 
                      font=("Poppins", 14, "bold"),
                      width=230).pack()

        # Load users
        self.load_users()

    def login(self):
        username = self.input_username.get()
        password = self.input_password.get()

        if not username and not password:  # Jika username dan password kosong
            tkmb.showwarning("Login Gagal", "Akun belum terdaftar. Silakan lakukan registrasi.")
        elif username in self.users_dict:  # Jika username terdaftar
            if self.users_dict[username] == password:  # Jika password cocok
                self.pencari_kos(username)  # Login berhasil
            else:
                tkmb.showwarning("Login Gagal", "Password salah. Silakan coba lagi.")
        else:  # Jika username tidak terdaftar
            tkmb.showwarning("Login Gagal", "Username dan password tidak terdaftar. Silakan lakukan registrasi.")

    def regist(self):
        self.root.withdraw()
        new_window = ctk.CTkToplevel(self.root)
        Registrasi(new_window, self)

    def load_users(self):
        # Pastikan file data_user.csv ada
        if not os.path.exists("data_user.csv"):
            with open("data_user.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["username", "password"])  # Menulis header jika file tidak ada

        # Membaca data pengguna dari file CSV
        users_dict = {}
        with open("data_user.csv", mode='r') as pengguna:
            pengguna_reader = csv.reader(pengguna)
            next(pengguna_reader, None)
            for row in pengguna_reader:
                if len(row) >= 2:
                    users_dict[row[0]] = row[1]
                else:
                    print(f"Skipped invalid row: {row}")

        self.users_dict = users_dict

    def pencari_kos(self, username):
        self.root.withdraw()
        new_window = ctk.CTkToplevel(self.root)
        Penyewakos(new_window, username, self.root)


class Penyewakos:
    def __init__(self, root, username, login_window):
        self.root = root
        self.login_window = login_window
        self.username = username
        self.root.title(f"Beranda - {self.username}")
        self.root.geometry("320x580+500+50")
        self.root.configure(fg_color="#4D3488")

        # Tambah Gambar untuk Background
        image_path = "background1.png"
        self.bg_image = ctk.CTkImage(Image.open(image_path), size=(320, 580))
        bg_label = ctk.CTkLabel(self.root, image=self.bg_image, text="")
        bg_label.place(relwidth=1, relheight=1)

        # Menampilkan username yang benar
        ctk.CTkLabel(self.root, 
                    text=f"Selamat Datang {self.username}",
                    font=('Poppins', 16, "bold"),
                    text_color="white").pack(pady=25)

        self.frame = ctk.CTkFrame(self.root, corner_radius=0, width=270)
        self.frame.configure(fg_color="white")
        self.frame.place(relx= 0.5, rely=0.2, anchor="center")
        
        #carikos
        ctk.CTkButton(self.frame, 
                      text="Cari Kos",
                      fg_color="#4D3488", 
                      text_color="white",
                      hover_color="#C5B0F6",
                      font=("Poppins", 14, "bold"),
                      corner_radius=10,
                      width=270,
                      command=self.cari_kos).pack(fill="x", padx=5, pady=5)
        #kos saya
        ctk.CTkButton(self.root,
                      text="Kos Saya",
                      text_color="#4D3488",
                      hover_color="#C5B0F6",
                      font=("Poppins", 14, "bold"),
                      fg_color="white",
                      command=self.kos_saya).place(relx=0.75, rely=0.96, anchor="center")
        #profil
        ctk.CTkButton(self.root,
                      text="Profil",
                      text_color="#4D3488",
                      hover_color="#C5B0F6",
                      font=("Poppins", 14, "bold"),
                      fg_color="white",
                      command=self.profil).place(relx=0.25, rely=0.96, anchor="center")
    #cari_kos
    def cari_kos(self,):
        self.root.withdraw()
        new_window = ctk.CTkToplevel(self.root)
        cari_kos(new_window, self.root,self.username)
    #kos_saya
    def kos_saya(self):
        self.root.withdraw()
        new_window = ctk.CTkToplevel()
        kos_saya(new_window, self.username)
    #profil
    def profil(self):
        self.root.withdraw()  
        new_window = ctk.CTkToplevel()
        profil(new_window, self.username, self.login_window)  


class profil:
    def __init__(self, root, username, login_window):
        self.root = root
        self.username = username
        self.login_window = login_window  
        self.root.title("Profil Saya")
        self.root.geometry("320x580+500+50")
        self.root.configure(fg_color="white")

        # Menampilkan username yang benar
        ctk.CTkLabel(self.root, 
                     text=f"Halo {self.username}!",
                     font=('Poppins', 16, "bold"),
                     text_color="#4D3488").pack(pady=25)

        # Tombol logout
        ctk.CTkButton(self.root,
                      text="Log Out",
                      text_color="white",
                      fg_color="#4D3488",
                      hover_color="#C5B0F6",
                      font=("Poppins", 14, "bold"),
                      width=270,
                      command=self.log_out).place(relx=0.5, rely=0.85, anchor="center")

    #logout
    def log_out(self):
        self.root.withdraw()
        new_window = ctk.CTkToplevel(self.root)
        LoginInterface(new_window)  


class kos_saya:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Kos Saya")
        self.root.geometry("320x580+500+50")
        self.root.configure(fg_color="white")

        # Label judul
        ctk.CTkLabel(self.root, 
                     text="Histori Pemesanan Kos", 
                     font=("Poppins", 16, "bold"), 
                     text_color="#4D3488").pack(pady=15)

        # Frame scrollable untuk menampilkan histori
        self.histori_frame = ctk.CTkScrollableFrame(self.root, fg_color="#4D3488")
        self.histori_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tampilkan histori pemesanan
        self.tampilkan_histori()

        # Tombol kembali
        ctk.CTkButton(self.histori_frame,
                      text="Kembali",
                      text_color="#4D3488",
                      fg_color="white",
                      hover_color="#C5B0F6",
                      font=("Poppins", 14, "bold"),
                      width=270,
                      command=self.back).pack(pady=15, padx=10, fill="x")
        
    def tampilkan_histori(self):
        try:
            # Baca file CSV histori pemesanan
            with open('histori_pemesanan.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                found = False

                # Loop melalui setiap baris data
                for row in reader:
                    if row["Username"] == self.username:
                        found = True
                        
                        ctk.CTkLabel(
                            self.histori_frame,
                            text=(f"{row['Nama Kos']}"),
                            text_color="white",
                            font=("Poppins", 14, "bold"), anchor="center").pack(pady=10)
                        
                        if row.get("Foto") and os.path.isfile(row["Foto"]):
                            try:
                                image = Image.open(row["Foto"]).resize((260, 190))  # Sesuaikan ukuran gambar
                                photo = CTkImage(light_image=image, size=(260, 190))
                                ctk.CTkLabel(self.histori_frame, image=photo, text="").pack(pady=10)
                            except Exception as e:
                                print(f"Error memuat gambar {row['Foto']}: {e}")
                        
                        ctk.CTkLabel(
                            self.histori_frame,
                            text=(
                                f"Nama Kamar: {row['Nama Kamar']}\n"
                                f"Alamat: {row['Alamat']}\n"
                                f"Kampus: {row['Kampus']}\n"
                                f"Daerah: {row['Daerah']}\n"
                                f"Tipe Kos: {row['Tipe Kos']}\n"
                                f"Harga: {row['Harga']}\n"
                                f"Fasilitas: {row['Fasilitas']}\n"
                                f"Aturan: {row['Aturan']}\n"
                                f"Metode Pembayaran: {row['Metode Pembayaran']}\n"
                                f"Tanggal Mulai Masuk Kos: {row['Tanggal Mulai Masuk Kos']}\n"
                                f"Tanggal Pemesanan: {row['Tanggal Pemesanan']}\n"
                            ),
                            text_color="white",
                            font=("Poppins", 12),
                            anchor="w",
                            justify="left",
                        ).pack(padx=10, pady=10, fill="x")

                # Jika tidak ditemukan data untuk username
                if not found:
                    ctk.CTkLabel(
                        self.histori_frame,
                        text="Belum ada histori pemesanan.",
                        text_color="gray",
                        font=("Poppins", 12)
                    ).pack(pady=20)

        except FileNotFoundError:
            # Jika file CSV tidak ditemukan
            ctk.CTkLabel(
                self.histori_frame,
                text="Histori pemesanan belum tersedia.",
                text_color="gray",
                font=("Poppins", 12)
            ).pack(pady=20)

    def back(self):
        self.root.withdraw()
        new_window = ctk.CTkToplevel()
        Penyewakos(new_window, self.username, self.root)

class cari_kos:
    def __init__(self, root, main_window, username):
        self.root = root
        self.main_window = main_window
        self.username = username
        self.root.title("Cari Kos")
        self.root.geometry("320x580+500+50")
        self.root.configure(fg_color="white")

        self.header_label = ctk.CTkLabel(self.root,
                                         text="Halo Penyewa Kos!",
                                         text_color="#4D3488",
                                         font=('Poppins', 16, "bold"))
        self.header_label.grid(row=0, column=0, columnspan=3, pady=(15, 5), padx=0, sticky="n")

        # konfigurasi scroll bar agar menyesuaikan jendela
        self.root.grid_columnconfigure(0, weight=1, minsize=320)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(self.root, fg_color="#4D3488")
        self.scroll_frame.grid(row=1, column=0, columnspan=3, pady=(5, 15), padx=15, sticky="nsew")
        self.scroll_frame.grid_rowconfigure(6, weight=1)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Menu Daerah Kampus
        self.daerah_kampus = ctk.CTkOptionMenu(self.scroll_frame,
                                                values=Kampus,
                                                fg_color="white",
                                                text_color="#4D3488",
                                                button_color="white",
                                                button_hover_color="#C5B0F6",
                                                dropdown_fg_color="white",
                                                dropdown_hover_color="#C5B0F6",
                                                dropdown_text_color="#4D3488",
                                                font=("Poppins", 14, "bold"))
        self.daerah_kampus.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        self.daerah_kampus.set("Daerah Kampus")

        # Menu Daerah Kos
        self.daerah_kos = ctk.CTkOptionMenu(self.scroll_frame,
                                            values=[],
                                            fg_color="white",
                                            text_color="#4D3488",
                                            button_color="white",
                                            button_hover_color="#C5B0F6",
                                            dropdown_fg_color="white",
                                            dropdown_hover_color="#C5B0F6",
                                            dropdown_text_color="#4D3488",
                                            font=("Poppins", 14, "bold"))
        self.daerah_kos.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.daerah_kos.set("Daerah Kos")

        # Filter Tipe Kos
        self.tipe_kos = ctk.CTkOptionMenu(self.scroll_frame,
                                          values=Tipe_Kos,
                                          fg_color="white",
                                          text_color="#4D3488",
                                          button_color="white",
                                          button_hover_color="#C5B0F6",
                                          dropdown_fg_color="white",
                                          dropdown_hover_color="#C5B0F6",
                                          dropdown_text_color="#4D3488",
                                          font=("Poppins", 14, "bold"))
        self.tipe_kos.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        self.tipe_kos.set("Tipe Kos")

        # Fasilitas Kos Label
        self.Fasilitas = ctk.CTkLabel(self.scroll_frame,
                                          text="Pilih Fasilitas:",
                                          font=("Poppins", 14, "bold"),
                                          text_color="white")
        self.Fasilitas.grid(row=3, column=0, pady=15, padx=10, sticky="w")

        # Fasilitas Kos Checkbox Frame
        self.frame = ctk.CTkFrame(self.scroll_frame, fg_color="white")
        self.frame.grid(row=4, column=0, pady=5, padx=10, sticky="ew")

        self.selected_fasilitas = {}
        Fasilitas_Kos = ["Kasur", "Kipas", "AC", "Lemari", "WI-FI", "TV", "Dapur Bersama", "Kamar Mandi Luar", "Kamar Mandi Dalam"]

        for idx, fasilitas in enumerate(Fasilitas_Kos):
            self.selected_fasilitas[fasilitas] = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(self.frame, text=fasilitas, width=250, variable=self.selected_fasilitas[fasilitas])
            checkbox.grid(row=idx, column=0, pady=5, padx=5, sticky="w")

        # Aturan Kos Label
        self.Aturan = ctk.CTkLabel(self.scroll_frame,
                               text="Aturan Kos:",
                               font=("Poppins", 14, "bold"),
                               text_color="white")
        self.Aturan.grid(row=5, column=0, pady=5, padx=10, sticky="w")

        # Aturan Kos Checkbox Frame
        self.frame2 = ctk.CTkFrame(self.scroll_frame, fg_color="white")
        self.frame2.grid(row=6, column=0, pady=5, padx=10, sticky="ew")

        self.selected_aturan = {}
        Aturan_Kos = ["Akses 24 Jam", "2 Orang", "1 Orang", "Boleh bawa hewan peliharaan"]

        for idx, aturan in enumerate(Aturan_Kos):
            self.selected_aturan[aturan] = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(self.frame2, text=aturan, width=250, variable=self.selected_aturan[aturan])
            checkbox.grid(row=idx, column=0, pady=10, padx=10, sticky="w")

        # Tombol Cari
        self.cari_kos = ctk.CTkButton(self.scroll_frame,
                                      text="Cari Kos",
                                      fg_color="white",
                                      text_color="#4D3488",
                                      hover_color="#C5B0F6",
                                      width=270,
                                      font=("Poppins", 14, "bold"),
                                      command=self.button_cari)
        self.cari_kos.grid(row=7, column=0, pady=15, padx=10, sticky="ew")

        # Tombol Kembali
        self.kembali = ctk.CTkButton(self.scroll_frame,
                                         text="Kembali",
                                         fg_color="white",
                                         hover_color="#C5B0F6",
                                         text_color="#4D3488",
                                         width=270,
                                         font=("Poppins", 14, "bold"),
                                         command=self.kembali_ke_beranda)
        self.kembali.grid(row=8, column=0, pady=15, padx=10, sticky="ew")

        # Menghubungkan perubahan pada menu kampus
        self.daerah_kampus.configure(command=self.update_daerah_kampus)

    def update_daerah_kampus(self, event=None):
        kampus = self.daerah_kampus.get()
        
        if kampus == "UNESA":
            self.daerah_kos.set("Pilih Daerah")  # Set default daerah untuk UNESA
            self.daerah_kos.configure(values=["Ketintang", "Lidah Wetan", "Jetis Kulon", "Karangrejo"])
        elif kampus == "UNAIR":
            self.daerah_kos.set("Pilih Daerah")  # Set default daerah untuk UNAIR
            self.daerah_kos.configure(values=["Kebomas", "Gubeng", "Tegalsari"])
        elif kampus == "ITS":
            self.daerah_kos.set("Pilih Daerah")  # Set default daerah untuk ITS
            self.daerah_kos.configure(values=["Keputih", "Gebang", "Mulyosari"])
        elif kampus == "UPN VETERAN JATIM":
            self.daerah_kos.set("Pilih Daerah")  # Set default daerah untuk UPN
            self.daerah_kos.configure(values=["Rungkut", "Gununganyar"])
        elif kampus == "UNTAG":
            self.daerah_kos.set("Pilih Daerah")  # Set default daerah untuk UNTAG
            self.daerah_kos.configure(values=["Sukolilo", "Manyar Rejo"])
        elif kampus == "UINSA":
            self.daerah_kos.set("Pilih Daerah")  # Set default daerah untuk UINSA
            self.daerah_kos.configure(values=["Wonosari", "Wonocolo"])

    def button_cari(self):
        kampus = self.daerah_kampus.get()
        daerah = self.daerah_kos.get()
        tipe = self.tipe_kos.get()

        selected_fasilitas = [key for key, var in self.selected_fasilitas.items() if var.get()]
        selected_aturan = [key for key, var in self.selected_aturan.items() if var.get()]

        # Cek apakah ada input yang kosong
        if kampus == "Daerah Kampus":
            kampus = None
        if daerah == "Daerah Kos":
            daerah = None
        if tipe == "Tipe Kos":
            tipe = None

        if not kampus and not daerah and not tipe and not selected_fasilitas and not selected_aturan:
            tkmb.showinfo("Peringatan", "Silakan pilih filter untuk melakukan pencarian.")
            return

        try:
            data = pd.read_csv("data_kos.csv")
            data.columns = data.columns.str.strip()
            for col in ['Kampus', 'Daerah', 'Tipe_kos', 'Fasilitas', 'Aturan']:
                data[col] = data[col].str.strip()
        except FileNotFoundError:
            tkmb.showerror("Error", "File data_kos.csv tidak ditemukan!")
            return

        # Filter data
        filtered_data = data
        if kampus:
            filtered_data = filtered_data[filtered_data['Kampus'].str.contains(kampus, case=False, na=False)]
        if daerah:
            filtered_data = filtered_data[filtered_data['Daerah'].str.contains(daerah, case=False, na=False)]
        if tipe:
            filtered_data = filtered_data[filtered_data['Tipe_kos'].str.contains(tipe, case=False, na=False)]
        for fasilitas in selected_fasilitas:
            filtered_data = filtered_data[filtered_data['Fasilitas'].str.contains(fasilitas, case=False, na=False)]
        for aturan in selected_aturan:
            filtered_data = filtered_data[filtered_data['Aturan'].str.contains(aturan, case=False, na=False)]

        if filtered_data.empty:
            tkmb.showinfo("Hasil Pencarian", "Tidak ada data yang cocok dengan filter yang dipilih.")

        # Tampilkan hasil
        if filtered_data.empty:
            tkmb.showinfo("Hasil Pencarian", "Tidak ada data yang cocok dengan filter yang dipilih.")
        else:
            self.root.withdraw()
            new_window = ctk.CTkToplevel()
            hasil_pencarian(new_window, filtered_data, self.username, self.main_window)

    def kembali_ke_beranda(self):
        self.root.destroy()
        self.main_window.deiconify()

# Values dari menu
Kampus = ["UNESA", "UNAIR", "ITS", "UPN VETERAN JATIM", "UNTAG", "UINSA"]
Daerah = ["Ketintang", "Lidah Wetan", "Gubeng", "Keputih", "Gununganyar", "Ngagel", "Wonocolo"]
Tipe_Kos = ["Putra", "Putri", "Campur"]


class hasil_pencarian:
    def __init__(self, root, data,username,main_window):
        self.root = root
        self.username= username
        self.main_window = main_window
        self.root.title("Hasil Pencarian")
        self.root.geometry("320x580+500+50")
        self.root.configure(fg_color="#4D3488")

        self.header = ctk.CTkLabel(self.root,
                                   text="Hasil Rekomendasi Kos",
                                   font=("Poppins", 16, "bold"),
                                   text_color="white")
        self.header.pack(pady=15)

        self.scroll_frame = ctk.CTkScrollableFrame(self.root, fg_color="white")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tampilkan setiap baris data
        for idx, row in data.iterrows():
            # Frame untuk setiap kos
            kos_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#4D3488")
            kos_frame.pack(fill="x", pady=5, padx=5)

            kos_frame.columnconfigure(0, weight=1)
            kos_frame.columnconfigure(1, weight=1)

            # Jika ada foto, tampilkan di atas
            if not pd.isna(row['foto']):
                try:
                    image = Image.open(row['foto']).resize((260, 190))  # Sesuaikan ukuran
                    photo = CTkImage(light_image=image, size=(260, 190))
                    image_label = ctk.CTkLabel(kos_frame, image=photo, text="")
                    image_label.grid(row=0, column=0, columnspan=2, pady=5)  # Foto berada di atas
                except FileNotFoundError:
                    print(f"File gambar {row['foto']} tidak ditemukan.")
                except Exception as e:
                    print(f"Error memuat gambar {row['foto']}: {e}")

            # Informasi kos di bawah foto
            info_label = ctk.CTkLabel(kos_frame,
                                      text=f"Nama Kos: {row['namakos']}\n"
                                           f"Kamar: {row['nama_kamar']}\n"
                                           f"Alamat: {row['alamat_kos']}\n"
                                           f"Kampus: {row['Kampus']}\n"
                                           f"Daerah: {row['Daerah']}\n"
                                           f"Tipe: {row['Tipe_kos']}\n"
                                           f"Harga: {row['Harga']}\n"
                                           f"Fasilitas: {row['Fasilitas']}\n"
                                           f"Aturan: {row['Aturan']}",
                                      text_color="white",
                                      anchor="w",
                                      justify="left")
            info_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

            pesan_button = ctk.CTkButton(kos_frame,
                                         text="Pesan Sekarang",
                                         fg_color="white",
                                         hover_color="#C5B0F6",
                                         text_color="#4D3488",
                                         font = ("Poppins", 14, "bold"),
                                         command=lambda row=row: self.pesan(row))
            pesan_button.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

    def pesan(self, kos_data):
        self.root.withdraw()
        new_window = ctk.CTkToplevel()
        Pembayaran(new_window, kos_data, self.username,self.main_window)


class Pembayaran:
    def __init__(self, root, kos_data,username,main_window):
        self.root = root
        self.kos_data = kos_data
        self.username = username
        self.main_window= main_window
        self.root.title("Pemesanan")
        self.root.geometry("320x580+500+50")
        self.root.configure(fg_color="#4D3488")

        # Label
        ctk.CTkLabel(self.root, 
                     text="Rincian Pemesanan",
                     font=('Poppins', 16, "bold"),
                     text_color="white").pack(pady=25)
        
        # Frame to hold components
        self.frame = ctk.CTkScrollableFrame(self.root, fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.8, anchor="center")

        if not pd.isna(self.kos_data['foto']):
            try:
                image = Image.open(self.kos_data['foto']).resize((260, 190))  # Ukuran gambar sesuai kebutuhan
                photo = CTkImage(light_image=image, size=(260, 190))
                image_label = ctk.CTkLabel(self.frame, image=photo, text="")
                image_label.pack(pady=5)  # Foto berada di atas rincian
            except FileNotFoundError:
                print(f"File gambar {self.kos_data['foto']} tidak ditemukan.")
            except Exception as e:
                print(f"Error memuat gambar {self.kos_data['foto']}: {e}")

        rincian_label = ctk.CTkLabel(self.frame,
                                     text=f"Nama Kos: {self.kos_data['namakos']}\n"
                                          f"Kamar: {self.kos_data['nama_kamar']}\n"
                                          f"Alamat: {self.kos_data['alamat_kos']}\n"
                                          f"Kampus: {self.kos_data['Kampus']}\n"
                                          f"Daerah: {self.kos_data['Daerah']}\n"
                                          f"Tipe: {self.kos_data['Tipe_kos']}\n"
                                          f"Harga: {self.kos_data['Harga']}\n"
                                          f"Fasilitas: {self.kos_data['Fasilitas']}\n"
                                          f"Aturan: {self.kos_data['Aturan']}",
                                     text_color="black",
                                     font=("Poppins", 12),
                                     anchor="w",
                                     justify="left")
        rincian_label.pack(padx=5, pady=10, anchor="w")

        # Kalender untuk memilih tanggal mulai ngekos
        self.start_date_label = ctk.CTkLabel(self.frame,
                                             text="Pilih Tanggal Mulai Masuk Kos:",
                                             font=("Poppins", 12, "bold"),
                                             text_color="#4D3488")
        self.start_date_label.pack(pady=10, padx=10, anchor="w")
        
        # Membuat widget kalender
        self.calendar = Calendar(self.frame, selectmode="day", date_pattern="dd-mm-yyyy")
        self.calendar.pack(pady=10, padx=10, fill="x")

        # OptionMenu for selecting payment method
        self.metode_pembayaran = ctk.CTkOptionMenu(self.frame,
                                                values=["BRI", "BNI", "BCA", "Mandiri", "BSI", "BTN"],
                                                fg_color="#4D3488",
                                                text_color="white",
                                                button_color="#4D3488",
                                                button_hover_color="#C5B0F6",
                                                dropdown_fg_color="white",
                                                dropdown_hover_color="#C5B0F6",
                                                dropdown_text_color="#4D3488",
                                                font=("Poppins", 14, "bold"))
        self.metode_pembayaran.pack(pady=10, padx=10, fill="x")
        self.metode_pembayaran.set("Pilih Metode Pembayaran")

        self.bayar = ctk.CTkButton(self.frame,
                    text="Bayar",
                    fg_color="#4D3488",
                    hover_color="#C5B0F6",
                    text_color="white",
                    font=("Poppins", 14, "bold"),
                    command=self.berhasil)
        self.bayar.pack(pady=10, padx=10, fill="x")

    # #dictionary untuk menyimpan informasi rekening
        self.rekening_info ={
            "BRI": "Rekening BRI: 123-456-7890",
            "BNI":  "Rekening BNI: 098-765-4321",
            "BCA": "Rekening BCA: 112-233-4455",
            "Mandiri": "Rekening Mandiri: 556-677-8899",
            "BSI": "Rekening BSI: 223-344-5566",
            "BTN": "Rekening BTN: 778-899-0011"
            }
    
    def berhasil(self):
        metode_pembayaran = self.metode_pembayaran.get()
        if metode_pembayaran == "Pilih Metode Pembayaran":
            tkmb.showwarning("Warning", "Silakan pilih metode pembayaran!")
            return  # Hentikan eksekusi jika validasi gagal

        selected_date = self.calendar.get_date()
        selected_date = datetime.strptime(selected_date, "%d-%m-%Y")
    
        # Baca data_kos.csv untuk mendapatkan path gambar
        try:
            data_kos = pd.read_csv("data_kos.csv")
            data_kos.columns = data_kos.columns.str.strip()
        
            # Cari baris yang sesuai dengan data kos yang dipilih
            kos_row = data_kos[
                (data_kos['namakos'] == self.kos_data['namakos']) &
                (data_kos['nama_kamar'] == self.kos_data['nama_kamar'])
            ].iloc[0]
        
            foto_path = kos_row['foto'] if not pd.isna(kos_row['foto']) else ""
        except FileNotFoundError:
            tkmb.showerror("Error", "File data_kos.csv tidak ditemukan!")
            return
        except IndexError:
            tkmb.showerror("Error", "Data kos tidak ditemukan di file data_kos.csv!")
            return

        pemesanan = {
            "Username": self.username,
            "Nama Kos": self.kos_data['namakos'],
            "Nama Kamar": self.kos_data['nama_kamar'],
            "Alamat": self.kos_data['alamat_kos'],
            "Kampus": self.kos_data['Kampus'],
            "Daerah": self.kos_data['Daerah'],
            "Tipe Kos": self.kos_data['Tipe_kos'],
            "Harga": self.kos_data['Harga'],
            "Fasilitas": self.kos_data['Fasilitas'],
            "Aturan": self.kos_data['Aturan'],
            "Metode Pembayaran": metode_pembayaran,
            "Tanggal Mulai Masuk Kos": selected_date.strftime("%d-%m-%Y"),
            "Tanggal Pemesanan": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "Foto": foto_path  # Path foto otomatis dari data_kos.csv
        }

        #tampilkan informasi rekening
        rekening_message = self.rekening_info .get(metode_pembayaran, "Rekening tidak tersedia.")
        tkmb.showinfo("Informasi Rekening", rekening_message)

        # Simpan data pemesanan ke CSV
        self.histori_pesanan(pemesanan)

        self.root.withdraw()
        new_window = ctk.CTkToplevel()
        konfirmasi(new_window, self.username, self.main_window)

    def histori_pesanan(self, pemesanan):
        file_exists = os.path.isfile('histori_pemesanan.csv')  # Cek apakah file sudah ada
        with open('histori_pemesanan.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=pemesanan.keys())
            if not file_exists or os.stat('histori_pemesanan.csv').st_size == 0:
                writer.writeheader()  # Tulis header jika file baru atau kosong
            writer.writerow(pemesanan)

class konfirmasi:
    def __init__(self, root, username,main_window):
        self.root = root
        self.username = username
        self.main_window = main_window
        self.root.title("Konfirmasi")
        self.root.geometry("320x580+500+50")
        self.root.configure(fg_color="#4D3488")

        # Header
        ctk.CTkLabel(self.root, 
                     text="Pembayaran Berhasil Dilakukan!",
                     font=('Poppins', 16, "bold"),
                     text_color="white").place(relx=0.5, rely=0.45, anchor="center")


        # Back button to return to Penyewakos class
        ctk.CTkButton(self.root,
                      text="Kembali ke beranda",
                      fg_color="white",
                      hover_color="#C5B0F6",
                      text_color="#4D3488",
                      font=("Poppins", 14, "bold"),
                      command=self.back_to_penyewakos).place(relx=0.5, rely=0.5, anchor="center")

    def back_to_penyewakos(self):
        self.root.destroy()
        self.main_window.deiconify()
   
root = ctk.CTk()
app = LoginInterface(root)
root.mainloop()
