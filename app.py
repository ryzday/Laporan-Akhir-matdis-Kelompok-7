import tkinter as tk
from tkinter import messagebox

class FSA:
    def __init__(self):
        self.state = 'q0'
        self.biodata = {}

    def screening(self, inputs):
        if self.state == 'q2':
            inp = inputs[0]
            if inp == 'Y':
                self.state = 'q3'
            elif inp == 'T':
                self.state = 'q7'
            else:
                self.state = 'q_invalid'
        return self.state

    def hasil_screening(self):
        if self.state == 'q3':
            return "DITERIMA"
        elif self.state == 'q7':
            return "TIDAK DITERIMA"
        elif self.state == 'q_invalid':
            return "INPUT TIDAK LENGKAP / TIDAK VALID"
        else:
            return "SCREENING BELUM LENGKAP"
    
class ScreeningApp:
    def __init__(self, root):
        self.fsa = FSA()
        self.root = root
        self.root.title("Screening Penerimaan Siswa Baru")
        self.root.geometry("500x400")  
        self.create_form_ui()

    def create_form_ui(self):
        self.frame_form = tk.Frame(self.root, padx=10, pady=10)
        self.frame_form.pack()

        tk.Label(self.frame_form, text="=== FORM BIODATA SISWA ===", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(self.frame_form, text="Nama Lengkap").grid(row=1, column=0, sticky="w")
        self.entry_nama = tk.Entry(self.frame_form, width=40)
        self.entry_nama.grid(row=1, column=1)

        tk.Label(self.frame_form, text="Jenis Kelamin (L/P)").grid(row=2, column=0, sticky="w")
        self.entry_jk = tk.Entry(self.frame_form, width=10)
        self.entry_jk.grid(row=2, column=1, sticky="w")

        tk.Label(self.frame_form, text="Asal Sekolah").grid(row=3, column=0, sticky="w")
        self.entry_sekolah = tk.Entry(self.frame_form, width=40)
        self.entry_sekolah.grid(row=3, column=1)

        self.btn_lanjut = tk.Button(self.frame_form, text="Lanjut ke Screening", command=self.to_screening)
        self.btn_lanjut.grid(row=4, column=0, columnspan=2, pady=10)

    def to_screening(self):
        nama = self.entry_nama.get().strip()
        jk = self.entry_jk.get().strip().upper()
        sekolah = self.entry_sekolah.get().strip()

        if not nama or not jk or not sekolah or jk not in ['L', 'P']:
            messagebox.showwarning("Input Tidak Valid", "Harap lengkapi semua biodata dengan benar.")
            return

        self.fsa.biodata = {
            'nama': nama,
            'jenis_kelamin': jk,
            'asal_sekolah': sekolah
        }
        self.fsa.state = 'q2'

        self.frame_form.pack_forget()
        self.create_screening_ui()

    def create_screening_ui(self):
        self.frame_screening = tk.Frame(self.root, padx=10, pady=10)
        self.frame_screening.pack()

        tk.Label(self.frame_screening, text="=== SCREENING PENILAIAN ===", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(self.frame_screening, text="Nilai Ujian (0-100)").grid(row=1, column=0, sticky="w")
        self.entry_nilai_ujian = tk.Entry(self.frame_screening, width=10)
        self.entry_nilai_ujian.grid(row=1, column=1, sticky="w")

        self.btn_proses = tk.Button(self.frame_screening, text="Proses Screening", command=self.proses_screening)
        self.btn_proses.grid(row=2, column=0, columnspan=2, pady=10)

        self.text_hasil = tk.Text(self.frame_screening, width=60, height=10, state='disabled')
        self.text_hasil.grid(row=3, column=0, columnspan=2)

    def proses_screening(self):
        try:
            nilai_ujian = int(self.entry_nilai_ujian.get())

            if not (0 <= nilai_ujian <= 100):
                raise ValueError

            self.fsa.state = 'q2'
            simbols = ['Y' if nilai_ujian >= 80 else 'T']
            state_akhir = self.fsa.screening(simbols)
            hasil = self.fsa.hasil_screening()

            self.text_hasil.config(state='normal')
            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(tk.END, "=== HASIL SCREENING ===\n")
            self.text_hasil.insert(tk.END, f"Nama          : {self.fsa.biodata['nama']}\n")
            self.text_hasil.insert(tk.END, f"Jenis Kelamin : {self.fsa.biodata['jenis_kelamin']}\n")
            self.text_hasil.insert(tk.END, f"Asal Sekolah  : {self.fsa.biodata['asal_sekolah']}\n")
            self.text_hasil.insert(tk.END, f"Nilai Ujian   : {nilai_ujian}\n")
            self.text_hasil.insert(tk.END, f"Status Akhir  : {state_akhir}\n")
            self.text_hasil.insert(tk.END, f"Hasil         : {hasil}\n")
            self.text_hasil.config(state='disabled')

        except ValueError:
            messagebox.showerror("Input Salah", "Masukkan nilai antara 0 hingga 100.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreeningApp(root)
    root.mainloop()
