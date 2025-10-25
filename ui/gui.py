import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import sys
import os

# ------------------- KONSTANTA WARNA & STYLING -------------------
ACCENT = "#E75480"        # aksen utama (merah jambu keunguan)
ACCENT_LIGHT = "#FFB3C6"  # aksen lembut
BG = "#FFF5F8"            # background aplikasi
CARD = "#FFFFFF"          # warna kartu/tile
TEXT = "#222222"
SHADOW = "#d9c5cf"
BADGE = "#FF7BA9"

# ------------------- IMPORT ENGINE (SAMA DENGAN SEBELUMNYA) -------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from inference_engine.engine import run_inference
    INFERENCE_READY = True
except ImportError:
    INFERENCE_READY = False
    print("WARNING: inference engine tidak tersedia. Menggunakan fungsi dummy.")
    def run_inference(gejala_list):
        return "SIMULASI: Kemungkinan P01 (80%). Ini hasil dummy."

# ------------------- DATA GEJALA -------------------
GEJALA_DATA = {
    "G04": "Tidak terdapat benjolan pada payudara",
    "G05": "Tidak terdapat metastasis pada kelenjar getah bening regional di ketiak/aksila",
    "G06": "Terdapat benjolan pada payudara berukuran diameter 2 cm atau kurang",
    "G07": "Terdapat benjolan pada payudara berukuran diameter 2 cm hingga 5 cm",
    "G13": "Tidak terdapat metastasis jauh",
    "G01": "Kulit payudara berwarna kemerahan",
    "G14": "Terdapat metastasis jauh"
}

# ------------------- UTIL: Hover untuk tombol -------------------
def add_hover(btn, bg, hover_bg):
    def on_enter(e):
        try:
            btn.configure(background=hover_bg)
        except:
            pass
    def on_leave(e):
        try:
            btn.configure(background=bg)
        except:
            pass
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ------------------- APLIKASI -------------------
class ExpertSystemGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Pakar Kanker Payudara — Visual + Info Interaktif")
        master.configure(bg=BG)
        # fullscreen
        master.attributes('-fullscreen', True)
        # allow exit fullscreen with Esc
        master.bind('<Escape>', lambda e: master.attributes('-fullscreen', False))

        # Font
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.h2_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)

        # container stack
        self.container = tk.Frame(master, bg=BG)
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)

        self.landing_frame = tk.Frame(self.container, bg=BG)
        self.main_frame = tk.Frame(self.container, bg=BG)
        for f in (self.landing_frame, self.main_frame):
            f.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._build_landing()
        self._build_main()

        self.show_frame("landing")

    def show_frame(self, name):
        if name == "landing":
            self.landing_frame.lift()
        else:
            self.main_frame.lift()

    # ------------------- Landing Page (DIROMBAK MENJADI VISUAL) -------------------
    def _build_landing(self):
        f = self.landing_frame

        # Header gradient (Canvas)
        header_canv = tk.Canvas(f, height=120, highlightthickness=0, bg=BG)
        header_canv.pack(fill=tk.X, pady=(0,12))
        self._draw_gradient(header_canv, "#FFDFEA", ACCENT, f.winfo_screenwidth(), 120)
        header_canv.create_text(30, 40, anchor="w", text="Sistem Konsultasi Kanker Payudara",
                                font=self.title_font, fill=TEXT)
        header_canv.create_text(30, 80, anchor="w",
                                text="Edukasi • Indikasi Awal • Arahan Tindak Lanjut",
                                font=self.normal_font, fill=TEXT)

        # MAIN CARD area: kiri visual + kanan ringkasan & CTA
        main_card = tk.Frame(f, bg=CARD, bd=0)
        main_card.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        left = tk.Frame(main_card, bg=CARD)
        right = tk.Frame(main_card, bg=CARD)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(24,12), pady=18)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12,24), pady=18)

        # ===== LEFT: Visual infographic + statistik cepat =====
        # Top: statistik cards (3 kecil)
        stat_frame = tk.Frame(left, bg=CARD)
        stat_frame.pack(fill=tk.X, pady=(0,12))
        for i, (label, value, emoji) in enumerate([
            ("Deteksi Dini", "Penting", "🔎"),
            ("Kemungkinan Jinak", "Sering", "✅"),
            ("Perlu Dokter", "Konsultasi", "🩺"),
        ]):
            card = tk.Frame(stat_frame, bg=ACCENT_LIGHT if i==0 else CARD, bd=0, relief=tk.FLAT)
            card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=8)
            tk.Label(card, text=emoji + "  " + label, bg=card["bg"], font=self.normal_font, fg=TEXT).pack(anchor="w", padx=10, pady=(8,0))
            tk.Label(card, text=value, bg=card["bg"], font=self.h2_font, fg=ACCENT if i==0 else TEXT).pack(anchor="w", padx=10, pady=(2,10))

        # Middle: Infographic timeline of stadium (canvas)
        tf = tk.Frame(left, bg=CARD)
        tf.pack(fill=tk.BOTH, expand=True, pady=(6,0))
        tk.Label(tf, text="Visual Stadium (ringkasan)", font=self.h2_font, bg=CARD, fg=TEXT).pack(anchor="w", padx=6, pady=(6,2))
        canvas = tk.Canvas(tf, bg=CARD, height=180, highlightthickness=0)
        canvas.pack(fill=tk.X, padx=6, pady=6)

        # draw a horizontal timeline with 4 nodes
        w = canvas.winfo_reqwidth() if canvas.winfo_reqwidth() > 200 else 900
        margin = 40
        nodes = 4
        step = (w - 2*margin) / (nodes - 1)
        y = 90
        colors = ["#8bc34a", "#ffb74d", "#ff8a65", "#e57373"]
        labels = ["Stadium 0\n(Terlokalisir)", "Stadium I\n(≤2 cm)", "Stadium II-III\n(Regional)", "Stadium IV\n(Metastasis)"]
        for i in range(nodes):
            x = margin + i*step
            # line
            if i < nodes-1:
                canvas.create_line(x, y, x+step, y, width=6, fill="#f0d6df", capstyle="round")
            # node circle
            canvas.create_oval(x-18, y-18, x+18, y+18, fill=colors[i], outline="")
            canvas.create_text(x, y, text=str(i), font=self.h2_font, fill="white")
            # label
            canvas.create_text(x, y+40, text=labels[i], font=self.normal_font, fill=TEXT)

        # Bottom: risk factor chips (wrap)
        chips_frame = tk.Frame(left, bg=CARD)
        chips_frame.pack(fill=tk.X, pady=(12,6))
        tk.Label(chips_frame, text="Faktor Risiko:", bg=CARD, font=self.h2_font, fg=TEXT).pack(anchor="w", padx=6)
        chips_inner = tk.Frame(chips_frame, bg=CARD)
        chips_inner.pack(fill=tk.X, padx=6, pady=6)
        risks = ["Usia >50", "Riwayat keluarga", "BrC genetik", "Konsumsi alkohol", "Obesitas", "Hormon"]
        for r in risks:
            lb = tk.Label(chips_inner, text=r, bg=BADGE, fg="white", padx=8, pady=4, font=self.normal_font)
            lb.pack(side=tk.LEFT, padx=6, pady=4)

        # ===== RIGHT: Ringkasan teks + indikator actionable =====
        tk.Label(right, text="Mengapa penting?", font=self.h2_font, bg=CARD, fg=TEXT).pack(anchor="w", pady=(6,0), padx=6)
        summary = ("Deteksi dini memungkinkan pengobatan yang lebih efektif. segera konsultasikan ke dokter.")
        tk.Label(right, text=summary, wraplength=320, justify="left", bg=CARD, fg=TEXT, font=self.normal_font).pack(anchor="w", padx=6, pady=(4,12))

        # Actionable items -> Checklist (disabled)
        action_frame = tk.Frame(right, bg=CARD)
        action_frame.pack(fill=tk.X, padx=6, pady=(6,12))
        tk.Label(action_frame, text="Langkah Prioritas (informasi):", font=self.h2_font, bg=CARD, fg=TEXT).pack(anchor="w")

        # checklist steps (disabled)
        steps = [
            "SADARI - Pemeriksaan mandiri",
            "Periksa ke fasilitas bila curiga",
            "Mamografi/USG bila direkomendasikan"
        ]
        self.action_vars = {}
        for name in steps:
            var = tk.BooleanVar(value=False)
            # checkbutton dibuat disabled sehingga hanya bersifat tampilan
            cb = tk.Checkbutton(action_frame, text=name, variable=var,
                                bg=CARD, anchor="w", justify="left", font=self.normal_font,
                                state=tk.DISABLED)
            cb.pack(fill=tk.X, pady=6, padx=6)
            self.action_vars[name] = var

        # status indikator (tetap menampilkan 0/X selesai karena disabled)
        status_row = tk.Frame(action_frame, bg=CARD)
        status_row.pack(fill=tk.X, pady=(8,0), padx=6)
        total = len(self.action_vars)
        self.check_status_label = tk.Label(status_row, text=f"0/{total} selesai (read-only)", bg=CARD, font=self.normal_font)
        self.check_status_label.pack(side=tk.LEFT)

        # tombol reset dinonaktifkan karena checklist read-only
        reset_chk_btn = tk.Button(status_row, text="Reset Checklist", state=tk.DISABLED,
                                  bg="lightgrey", fg=TEXT, bd=0, padx=8, pady=6)
        reset_chk_btn.pack(side=tk.RIGHT)
        add_hover(reset_chk_btn, "lightgrey", "#efefef")

        # CTA buttons
        cta_frame = tk.Frame(right, bg=CARD)
        cta_frame.pack(fill=tk.X, pady=(8,0), padx=6)
        start_btn = tk.Button(cta_frame, text="→ Mulai Diagnosa", command=lambda: self.show_frame("main"),
                              bg=ACCENT, fg="white", font=self.h2_font, bd=0, padx=12, pady=10)
        start_btn.pack(fill=tk.X, pady=(0,8))
        add_hover(start_btn, ACCENT, ACCENT_LIGHT)

        learn_btn = tk.Button(cta_frame, text="Simpan Panduan Singkat (.txt)", command=self._save_helper_text,
                               bg="#f6f0f7", fg=TEXT, font=self.normal_font, bd=0, padx=12, pady=8)
        learn_btn.pack(fill=tk.X)
        add_hover(learn_btn, "#f6f0f7", "#eee6f0")

        # ===== FAQ accordion (collapsible) di bagian bawah seluruh card =====
        faq_card = tk.Frame(f, bg=CARD)
        faq_card.pack(fill=tk.X, padx=12, pady=(6,12))
        tk.Label(faq_card, text="FAQ Singkat — Klik untuk buka/tutup", font=self.h2_font, bg=CARD, fg=TEXT).pack(anchor="w", padx=8, pady=(8,4))
        faqs = [
            ("Apakah aplikasi ini pengganti dokter?", "Tidak. Aplikasi hanya memberikan indikasi awal. Konsultasikan ke dokter."),
            ("Apa yang harus dilakukan bila menemukan benjolan?", "Segera periksa ke fasilitas kesehatan untuk evaluasi lanjutan."),
            ("Seberapa sering SADARI?", "Idealnya setiap bulan, terutama setelah haid selesai.")
        ]
        for q, a in faqs:
            self._create_accordion(faq_card, q, a)

    # ------------------- Main (Bento dengan visual) -------------------
    def _build_main(self):
        f = self.main_frame

        # Top bar
        top = tk.Frame(f, bg=BG)
        top.pack(fill=tk.X, pady=(0,8))
        tk.Label(top, text="Aplikasi Konsultasi — Bentō", font=self.title_font, bg=BG, fg=TEXT).pack(side=tk.LEFT, padx=4)
        back = tk.Button(top, text="← Kembali", command=lambda: self.show_frame("landing"),
                         bg=CARD, fg=TEXT, bd=0, padx=8, pady=6)
        back.pack(side=tk.RIGHT, padx=6)
        add_hover(back, CARD, "#f6f6f6")

        # Grid 2x2 area
        grid = tk.Frame(f, bg=BG)
        grid.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Make 2 columns equal
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)

        # TILE helper: create shadow + tile
        def create_tile(r, c, title, accent_icon="📌"):
            # shadow
            sh = tk.Frame(grid, bg=SHADOW)
            sh.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            # tile above
            tile = tk.Frame(grid, bg=CARD, bd=0)
            tile.grid(row=r, column=c, sticky="nsew", padx=(8,8), pady=(8,8))
            # header
            hdr = tk.Frame(tile, bg=CARD)
            hdr.pack(fill=tk.X, padx=10, pady=8)
            tk.Label(hdr, text=f"{accent_icon}  {title}", font=self.h2_font, bg=CARD, fg=ACCENT).pack(anchor="w")
            return tile

        # Tile 1: Gejala (top-left)
        t1 = create_tile(0, 0, "Pilih Gejala", accent_icon="🩺")
        self.gejala_vars = {code: tk.BooleanVar() for code in GEJALA_DATA.keys()}
        # scrollable frame for many checkbox (canvas+frame)
        canvas1 = tk.Canvas(t1, bg=CARD, highlightthickness=0)
        scrollbar1 = ttk.Scrollbar(t1, orient="vertical", command=canvas1.yview)
        chk_holder = tk.Frame(canvas1, bg=CARD)
        chk_holder.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
        canvas1.create_window((0, 0), window=chk_holder, anchor="nw")
        canvas1.configure(yscrollcommand=scrollbar1.set, height=220)
        canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8,2), pady=6)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,6), pady=6)

        for code, desc in GEJALA_DATA.items():
            cb = tk.Checkbutton(chk_holder, text=f"[{code}] {desc}", variable=self.gejala_vars[code],
                                bg=CARD, anchor="w", justify="left", font=self.normal_font)
            cb.pack(fill=tk.X, padx=6, pady=3)

        # Tile 2: Stadium (top-right)
        t2 = create_tile(0, 1, "Ringkasan Stadium", accent_icon="📊")
        stadium_text = ("Stadium 0: Terlokalisir\n\n"
                        "Stadium I: Tumor kecil (≤2 cm)\n\n"
                        "Stadium II–III: Tumor lebih besar dan/atau kelenjar regional terlibat\n\n"
                        "Stadium IV: Metastasis jauh")
        tk.Label(t2, text=stadium_text, bg=CARD, fg=TEXT, justify="left", font=self.normal_font, wraplength=360).pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        # Tile 3: Tips (bottom-left)
        t3 = create_tile(1, 0, "Tips & Tindakan Awal", accent_icon="💡")
        tips = ("• Lakukan SADARI setiap bulan.\n"
                "• Bila menemukan perubahan, segera konsultasikan.\n"
                "• Pemeriksaan lanjutan: mamografi/USG/biopsi.\n\n"
                "Catatan: Aplikasi hanya sebagai indikasi awal.")
        tk.Label(t3, text=tips, bg=CARD, fg=TEXT, justify="left", font=self.normal_font, wraplength=420).pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        # Tile 4: Hasil & aksi (bottom-right)
        t4 = create_tile(1, 1, "Hasil Diagnosa", accent_icon="🧾")
        self.result_label = tk.Label(t4, text="Tekan tombol di bawah untuk memproses diagnosa.",
                                     bg=CARD, fg=ACCENT, font=self.normal_font, wraplength=360, justify="left")
        self.result_label.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # Buttons area
        btnf = tk.Frame(t4, bg=CARD)
        btnf.pack(fill=tk.X, padx=10, pady=(0,12))
        self.process_btn = tk.Button(btnf, text="PROSES DIAGNOSA", command=self.proses_diagnosa,
                                     bg=ACCENT, fg="white", font=self.h2_font, bd=0, padx=10, pady=10)
        if not INFERENCE_READY:
            self.process_btn.configure(state=tk.DISABLED, text="ENGINE ERROR - CEK engine.py", bg="grey")
        self.process_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,6))
        add_hover(self.process_btn, ACCENT, ACCENT_LIGHT)

        reset_btn = tk.Button(btnf, text="Reset", command=self.reset_gejala, bg="lightgrey", fg=TEXT, bd=0, padx=10, pady=10)
        reset_btn.pack(side=tk.LEFT)
        add_hover(reset_btn, "lightgrey", "#efefef")

    # gradient helper (horizontal)
    def _draw_gradient(self, canvas, color1, color2, w, h):
        # draw vertical stripes to simulate gradient
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        steps = 80
        for i in range(steps):
            r = int(r1 + (r2 - r1) * (i / steps))
            g = int(g1 + (g2 - g1) * (i / steps))
            b = int(b1 + (b2 - b1) * (i / steps))
            color = f"#{r:02x}{g:02x}{b:02x}"
            x0 = int(i * (w / steps))
            x1 = int((i + 1) * (w / steps))
            canvas.create_rectangle(x0, 0, x1, h, outline=color, fill=color)

    def _hex_to_rgb(self, h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _create_accordion(self, parent, title, content):
        """Simple accordion: klik tombol untuk toggle show/hide content."""
        header = tk.Button(parent, text="▶ " + title, anchor="w", bd=0, bg=CARD, font=self.normal_font)
        header.pack(fill=tk.X, padx=8, pady=(4,0))
        body = tk.Frame(parent, bg="#fbf7fb")
        lbl = tk.Label(body, text=content, wraplength=920, justify="left", bg="#fbf7fb", font=self.normal_font)
        lbl.pack(fill=tk.X, padx=12, pady=8)
        body.pack(fill=tk.X, padx=8)
        # start collapsed
        body.forget()

        def toggle():
            if body.winfo_ismapped():
                body.forget()
                header.configure(text="▶ " + title)
            else:
                body.pack(fill=tk.X, padx=8)
                header.configure(text="▼ " + title)
        header.configure(command=toggle)

    def _save_helper_text(self):
        helper = (
            "Panduan Singkat - Kanker Payudara\n\n"
            "1. Lakukan SADARI setiap bulan.\n"
            "2. Periksa ke fasilitas jika menemukan benjolan atau perubahan.\n"
            "3. Pemeriksaan lanjutan: mamografi/USG/biopsi sesuai rekomendasi dokter.\n\n"
            "Catatan: Ini hanya panduan singkat. Konsultasikan ke tenaga medis untuk diagnosis pasti."
        )
        try:
            with open("panduan_singkat.txt", "w", encoding="utf-8") as f:
                f.write(helper)
            messagebox.showinfo("Sukses", "Panduan singkat tersimpan sebagai 'panduan_singkat.txt'.")
        except Exception as e:
            messagebox.showerror("Gagal Simpan", f"Tidak dapat menyimpan: {e}")

    def reset_gejala(self):
        for v in self.gejala_vars.values():
            v.set(False)
        self.result_label.config(text="Tekan tombol di bawah untuk memproses diagnosa.", fg=ACCENT)

    def proses_diagnosa(self):
        gejala_dipilih = [code for code, var in self.gejala_vars.items() if var.get()]
        if not gejala_dipilih:
            messagebox.showwarning("Input Kosong", "Silakan pilih setidaknya satu gejala.")
            return
        try:
            hasil = run_inference(gejala_dipilih)
            # tampilkan hasil dengan format rapi
            self.result_label.config(text=f"Hasil:\n{hasil}", fg=TEXT, justify="left")
        except Exception as e:
            messagebox.showerror("Error", f"Ada kesalahan saat memproses: {e}")
            self.result_label.config(text="ERROR PADA LOGIKA INFERENSI", fg="red")

    def save_result(self):
        # simpan isi result_label ke file txt
        content = self.result_label.cget("text")
        try:
            with open("hasil_diagnosa.txt", "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Sukses", "Hasil disimpan ke file 'hasil_diagnosa.txt'.")
        except Exception as e:
            messagebox.showerror("Gagal Simpan", f"Tidak dapat menyimpan: {e}")

# ------------------- RUN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpertSystemGUI(root)
    root.mainloop()
