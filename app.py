import streamlit as st

st.title("SaatKolikZ")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("850x600")
app.title("SaatKolikZ Made by osmn")

# ===================== VERİ =====================
mechanisms = {
    "Seiko 4R36": (-35, 45),
    "Seiko NH35": (-20, 40),
    "ETA 2824-2": (-10, 20),
    "Sellita SW200": (-10, 25),
    "Rolex 3235": (-2, 2),
    "Miyota 8215": (-20, 40),
    "Casio Quartz": (-0.5, 0.5)
}

history = []

# ===================== LAYOUT =====================
sidebar = ctk.CTkFrame(app, width=200, corner_radius=15)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

main = ctk.CTkFrame(app, corner_radius=15)
main.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# ===================== SAAT =====================
clock = ctk.CTkLabel(sidebar, text="", font=("Arial", 20))
clock.pack(pady=20)

def update_clock():
    clock.configure(text=datetime.now().strftime("%H:%M:%S"))
    app.after(1000, update_clock)

update_clock()

# ===================== SAYFA SİSTEMİ =====================
pages = {}

def show(page):
    for p in pages.values():
        p.pack_forget()
    pages[page].pack(fill="both", expand=True)

# ===================== ANALİZ SAYFASI =====================
page1 = ctk.CTkFrame(main)
pages["analiz"] = page1

ctk.CTkLabel(page1, text="⚙ Mekanizma Analiz", font=("Arial", 20)).pack(pady=10)

selected = ctk.StringVar(value="Seiko 4R36")

ctk.CTkOptionMenu(page1, values=list(mechanisms.keys()), variable=selected).pack(pady=10)

entry = ctk.CTkEntry(page1, placeholder_text="Sapma (sn/gün)")
entry.pack(pady=10)

result = ctk.CTkLabel(page1, text="", font=("Arial", 18))
result.pack(pady=10)

def analyze():
    try:
        drift = float(entry.get())
        mech = selected.get()
        min_v, max_v = mechanisms[mech]

        history.append(drift)

        if drift > max_v * 1.3 or drift < min_v * 1.3:
            result.configure(text="🔴 Bakım Gerekli", text_color="red")
        elif drift > max_v or drift < min_v:
            result.configure(text="🟡 Tolerans Dışı", text_color="orange")
        else:
            result.configure(text="🟢 Normal", text_color="green")

    except:
        result.configure(text="Geçerli değer gir!")

ctk.CTkButton(page1, text="Analiz Et", command=analyze).pack(pady=10)

# ===================== SAĞLIK SAYFASI =====================
page2 = ctk.CTkFrame(main)
pages["saglik"] = page2

ctk.CTkLabel(page2, text="🧠 Saat Sağlığı", font=("Arial", 20)).pack(pady=10)

health = ctk.CTkLabel(page2, text="", font=("Arial", 16))
health.pack(pady=20)

def check_health():
    if not history:
        health.configure(text="Veri yok")
        return

    avg = sum(history) / len(history)

    if abs(avg) < 5:
        health.configure(text="🟢 Saat çok sağlıklı")
    elif abs(avg) < 20:
        health.configure(text="🟡 Kontrol önerilir")
    else:
        health.configure(text="🔴 Servis gerekli")

ctk.CTkButton(page2, text="Analiz Et", command=check_health).pack()

# ===================== MODELLER =====================
page3 = ctk.CTkFrame(main)
pages["modeller"] = page3

ctk.CTkLabel(page3, text="📋 Mekanizmalar", font=("Arial", 20)).pack(pady=10)

for name, (min_v, max_v) in mechanisms.items():
    ctk.CTkLabel(page3, text=f"{name} → {min_v}/{max_v} sn/gün").pack(pady=5)

# ===================== KARŞILAŞTIRMA =====================
page4 = ctk.CTkFrame(main)
pages["karsilastir"] = page4

ctk.CTkLabel(page4, text="⚖ Karşılaştırma", font=("Arial", 20)).pack(pady=10)

for name, (min_v, max_v) in mechanisms.items():
    avg = (abs(min_v) + abs(max_v)) / 2

    if avg <= 5:
        lvl = "🟢 Çok Hassas"
    elif avg <= 20:
        lvl = "🟡 Orta"
    else:
        lvl = "🔴 Düşük"

    ctk.CTkLabel(page4, text=f"{name} → {lvl}").pack(pady=4)

# ===================== SIDEBAR =====================
ctk.CTkButton(sidebar, text="⚙ Analiz", command=lambda: show("analiz")).pack(pady=10)
ctk.CTkButton(sidebar, text="🧠 Sağlık", command=lambda: show("saglik")).pack(pady=10)
ctk.CTkButton(sidebar, text="📋 Modeller", command=lambda: show("modeller")).pack(pady=10)
ctk.CTkButton(sidebar, text="⚖ Karşılaştır", command=lambda: show("karsilastir")).pack(pady=10)

# default
show("analiz")

# ===================== RUN =====================
app.mainloop()
