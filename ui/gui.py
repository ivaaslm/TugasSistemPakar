import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import sys
import os

ACCENT = "#E75480"
ACCENT_LIGHT = "#FFB3C6"
BG = "#FFF5F8"
CARD = "#FFFFFF"
TEXT = "#222222"
SHADOW = "#d9c5cf"
BADGE = "#FF7BA9"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from inference_engine.engine import run_inference
    INFERENCE_READY = True
except ImportError:
    INFERENCE_READY = False
    print("WARNING: inference engine tidak tersedia. Menggunakan fungsi dummy.")
    def run_inference(gejala_list):
        return "SIMULASI: Kemungkinan P01 (80%). Ini hasil dummy."

GEJALA_DATA = {
    "G01": "Kulit payudara berwarna kemerahan",
    "G02": "Terdapat benjolan pada payudara",
    "G03": "Payudara mengoreng atau menjadi borok (luka-luka)",
    "G04": "Tidak terdapat benjolan pada payudara",
    "G05": "Tidak terdapat metastasis pada kelenjar getah bening regional di ketiak/aksila",
    "G06": "Terdapat benjolan pada payudara berukuran diameter 2 cm atau kurang",
    "G07": "Terdapat benjolan pada payudara berukuran diameter 2 cm hingga 5 cm",
    "G08": "Terdapat metastasis ke kelenjar getah bening regional di ketiak/aksila yang dapat digerakkan ",
    "G09": "Terdapat benjolan pada payudara berukuran diameter lebih dari 5 cm",
    "G10": "Terdapat metastasis ke kelenjar getah bening regional di ketiak/aksila yang sulit digerakkan",
    "G11": "Terdapat benjolan pada payudara ukuran berapa saja",
    "G12": "Terdapat metastasis ke kelenjar getah bening di atas tulang selangka/di dekat tulang sternum",
    "G13": "Tidak terdapat metastasis jauh",
    "G14": "Terdapat metastasis jauh"
}

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

class ExpertSystemGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Pakar Diagnosa Kanker Payudara")
        master.configure(bg=BG)
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', lambda e: master.attributes('-fullscreen', False))

        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.h2_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        self.chk_font = font.Font(family="Helvetica", size=11)

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

    def _build_landing(self):
        f = self.landing_frame

        header_canv = tk.Canvas(f, height=120, highlightthickness=0, bg=BG)
        header_canv.pack(fill=tk.X, pady=(0,12))
        self._draw_gradient(header_canv, "#FFDFEA", ACCENT, f.winfo_screenwidth(), 120)
        header_canv.create_text(30, 40, anchor="w", text="Sistem Pakar Diagnosa Kanker Payudara",
                                font=self.title_font, fill=TEXT)
        header_canv.create_text(30, 80, anchor="w",
                                text="Edukasi • Indikasi Awal • Arahan Tindak Lanjut",
                                font=self.normal_font, fill=TEXT)

        main_card = tk.Frame(f, bg=CARD, bd=0)
        main_card.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        left = tk.Frame(main_card, bg=CARD)
        right = tk.Frame(main_card, bg=CARD)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(24,12), pady=18)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12,24), pady=18)

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

        tf = tk.Frame(left, bg=CARD)
        tf.pack(fill=tk.BOTH, expand=True, pady=(6,0))
        tk.Label(tf, text="Visual Stadium (ringkasan)", font=self.h2_font, bg=CARD, fg=TEXT).pack(anchor="w", padx=6, pady=(6,2))
        canvas = tk.Canvas(tf, bg=CARD, height=180, highlightthickness=0)
        canvas.pack(fill=tk.X, padx=6, pady=6)

        w = canvas.winfo_reqwidth() if canvas.winfo_reqwidth() > 200 else 900
        margin = 40
        nodes = 4
        step = (w - 2*margin) / (nodes - 1)
        y = 90
        colors = ["#8bc34a", "#ffb74d", "#ff8a65", "#e57373"]
        labels = ["Stadium 0\n(Terlokalisir)", "Stadium I\n(≤2 cm)", "Stadium II-III\n(Regional)", "Stadium IV\n(Metastasis)"]
        for i in range(nodes):
            x = margin + i*step
            if i < nodes-1:
                canvas.create_line(x, y, x+step, y, width=6, fill="#f0d6df", capstyle="round")
            canvas.create_oval(x-18, y-18, x+18, y+18, fill=colors[i], outline="")
            canvas.create_text(x, y, text=str(i), font=self.h2_font, fill="white")
            canvas.create_text(x, y+40, text=labels[i], font=self.normal_font, fill=TEXT)

        chips_frame = tk.Frame(left, bg=CARD)
        chips_frame.pack(fill=tk.X, pady=(12,6))
        tk.Label(chips_frame, text="Faktor Risiko:", bg=CARD, font=self.h2_font, fg=TEXT).pack(anchor="w", padx=6)
        chips_inner = tk.Frame(chips_frame, bg=CARD)
        chips_inner.pack(fill=tk.X, padx=6, pady=6)
        risks = ["Usia >50", "Riwayat keluarga", "BrC genetik", "Konsumsi alkohol", "Obesitas", "Hormon"]
        for r in risks:
            lb = tk.Label(chips_inner, text=r, bg=BADGE, fg="white", padx=8, pady=4, font=self.normal_font)
            lb.pack(side=tk.LEFT, padx=6, pady=4)

        tk.Label(right, text="Mengapa penting?", font=self.h2_font, bg=CARD, fg=TEXT).pack(anchor="w", pady=(6,0), padx=6)
        summary = ("Deteksi dini memungkinkan pengobatan yang lebih efektif. segera konsultasikan ke dokter.")
        tk.Label(right, text=summary, wraplength=320, justify="left", bg=CARD, fg=TEXT, font=self.normal_font).pack(anchor="w", padx=6, pady=(4,12))

        action_frame = tk.Frame(right, bg=CARD)
        action_frame.pack(fill=tk.X, padx=6, pady=(6,12))
        tk.Label(action_frame, text="Langkah Prioritas (informasi):", font=self.h2_font, bg=CARD, fg=TEXT).pack(anchor="w")

        steps = [
            "SADARI - Pemeriksaan mandiri secara rutin.",
            "Periksa ke fasilitas kesehatan bila curiga atau menemukan benjolan.",
            "Mamografi/USG bila direkomendasikan oleh dokter."
        ]

        for i, step_text in enumerate(steps, 1):
            step_label = tk.Label(action_frame, text=f"{i}. {step_text}",
                                  bg=CARD, anchor="w", justify="left", font=self.normal_font,
                                  wraplength=300)
            step_label.pack(fill=tk.X, pady=2, padx=(12, 6))

        cta_frame = tk.Frame(right, bg=CARD)
        cta_frame.pack(fill=tk.X, pady=(8,0), padx=6)
        start_btn = tk.Button(cta_frame, text="→ Mulai Diagnosa", command=lambda: self.show_frame("main"),
                              bg=ACCENT, fg="white", font=self.h2_font, bd=0, padx=12, pady=10)
        start_btn.pack(fill=tk.X, pady=(0,8))
        add_hover(start_btn, ACCENT, ACCENT_LIGHT)

    def _build_main(self):
        f = self.main_frame

        top = tk.Frame(f, bg=BG)
        top.pack(fill=tk.X, pady=(0,8))
        tk.Label(top, text="Sistem Pakar Diagnosa Kanker Payudara", font=self.title_font, bg=BG, fg=TEXT).pack(side=tk.LEFT, padx=4)
        back = tk.Button(top, text="← Kembali", command=lambda: self.show_frame("landing"),
                         bg=CARD, fg=TEXT, bd=0, padx=8, pady=6)
        back.pack(side=tk.RIGHT, padx=6)
        add_hover(back, CARD, "#f6f6f6")

        grid = tk.Frame(f, bg=BG)
        grid.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)

        def create_tile(r, c, title, accent_icon="📌"):
            sh = tk.Frame(grid, bg=SHADOW)
            sh.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            tile = tk.Frame(grid, bg=CARD, bd=0)
            tile.grid(row=r, column=c, sticky="nsew", padx=(8,8), pady=(8,8))
            hdr = tk.Frame(tile, bg=CARD)
            hdr.pack(fill=tk.X, padx=10, pady=8)
            tk.Label(hdr, text=f"{accent_icon}  {title}", font=self.h2_font, bg=CARD, fg=ACCENT).pack(anchor="w")
            return tile

        t1 = create_tile(0, 0, "Pilih Gejala", accent_icon="🩺")
        self.gejala_vars = {code: tk.BooleanVar() for code in GEJALA_DATA.keys()}

        canvas1 = tk.Canvas(t1, bg=CARD, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(t1, orient="vertical", command=canvas1.yview)
        h_scrollbar = ttk.Scrollbar(t1, orient="horizontal", command=canvas1.xview)

        chk_holder = tk.Frame(canvas1, bg=CARD)
        canvas_window = canvas1.create_window((0, 0), window=chk_holder, anchor="nw")

        def _on_chk_config(event):
            canvas1.configure(scrollregion=canvas1.bbox("all"))
            try:
                canvas1.itemconfig(canvas_window, width=chk_holder.winfo_reqwidth())
            except:
                pass

        chk_holder.bind("<Configure>", _on_chk_config)
        canvas1.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set, height=220)

        canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8,2), pady=6)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,6), pady=6)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, padx=(8,2), pady=(0,6))

        # checkbox font uses self.normal_font
        for code, desc in GEJALA_DATA.items():
            cb = tk.Checkbutton(chk_holder, text=f"[{code}] {desc}", variable=self.gejala_vars[code],
                                bg=CARD, anchor="w", justify="left", font=self.normal_font,
                                fg=TEXT, activeforeground=ACCENT, selectcolor=ACCENT_LIGHT)
            cb.pack(anchor="w", padx=6, pady=4)

        def _get_delta(event):
            d = 0
            if hasattr(event, "delta"):
                try:
                    d = int(event.delta / 120)
                except:
                    try:
                        d = int(event.delta)
                    except:
                        d = 0
            return d

        def _on_mousewheel(event):
            delta = _get_delta(event)
            canvas1.yview_scroll(-delta, "units")

        def _on_button4(event):
            canvas1.yview_scroll(-1, "units")
        def _on_button5(event):
            canvas1.yview_scroll(1, "units")
        def _on_button6(event):
            canvas1.xview_scroll(-1, "units")
        def _on_button7(event):
            canvas1.xview_scroll(1, "units")

        def _on_shift_mousewheel(event):
            delta = _get_delta(event)
            canvas1.xview_scroll(-delta, "units")

        def _bind_scrolls(e):
            canvas1.bind_all("<MouseWheel>", _on_mousewheel)      
            canvas1.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)
            canvas1.bind_all("<Button-4>", _on_button4)            
            canvas1.bind_all("<Button-5>", _on_button5)           
            canvas1.bind_all("<Button-6>", _on_button6)            
            canvas1.bind_all("<Button-7>", _on_button7)            

        def _unbind_scrolls(e):
            try:
                canvas1.unbind_all("<MouseWheel>")
                canvas1.unbind_all("<Shift-MouseWheel>")
                canvas1.unbind_all("<Button-4>")
                canvas1.unbind_all("<Button-5>")
                canvas1.unbind_all("<Button-6>")
                canvas1.unbind_all("<Button-7>")
            except:
                pass

        canvas1.bind("<Enter>", _bind_scrolls)
        canvas1.bind("<Leave>", _unbind_scrolls)

        t2 = create_tile(0, 1, "Ringkasan Stadium", accent_icon="📊")
        stadium_text = ("Stadium 0: Terlokalisir\n\n"
                        "Stadium I: Tumor kecil (≤2 cm)\n\n"
                        "Stadium II–III: Tumor lebih besar dan/atau kelenjar regional terlibat\n\n"
                        "Stadium IV: Metastasis jauh")
        tk.Label(t2, text=stadium_text, bg=CARD, fg=TEXT, justify="left", font=self.normal_font, wraplength=360).pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        t3 = create_tile(1, 0, "Tips & Tindakan Awal", accent_icon="💡")
        tips = ("• Lakukan SADARI setiap bulan.\n"
                "• Bila menemukan perubahan, segera konsultasikan.\n"
                "• Pemeriksaan lanjutan: mamografi/USG/biopsi.\n\n"
                "Catatan: Aplikasi hanya sebagai indikasi awal.")
        tk.Label(t3, text=tips, bg=CARD, fg=TEXT, justify="left", font=self.normal_font, wraplength=420).pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        t4 = create_tile(1, 1, "Hasil Diagnosa", accent_icon="🧾")
        self.result_label = tk.Label(t4, text="Tekan tombol di bawah untuk memproses diagnosa.",
                                     bg=CARD, fg=ACCENT, font=self.normal_font, wraplength=360, justify="left")
        self.result_label.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

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

    def _draw_gradient(self, canvas, color1, color2, w, h):
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
        header = tk.Button(parent, text="▶ " + title, anchor="w", bd=0, bg=CARD, font=self.normal_font)
        header.pack(fill=tk.X, padx=8, pady=(4,0))
        body = tk.Frame(parent, bg="#fbf7fb")
        lbl = tk.Label(body, text=content, wraplength=920, justify="left", bg="#fbf7fb", font=self.normal_font)
        lbl.pack(fill=tk.X, padx=12, pady=8)
        body.pack(fill=tk.X, padx=8)
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
            self.result_label.config(text=f"Hasil:\n{hasil}", fg=TEXT, justify="left")
        except Exception as e:
            messagebox.showerror("Error", f"Ada kesalahan saat memproses: {e}")
            self.result_label.config(text="ERROR PADA LOGIKA INFERENSI", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpertSystemGUI(root)
    root.mainloop()
