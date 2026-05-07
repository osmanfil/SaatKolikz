import streamlit as st

st.set_page_config(page_title="SaatKolikZ", layout="wide")

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

# ===================== SESSION =====================
if "history" not in st.session_state:
    st.session_state.history = []

# ===================== SIDEBAR =====================
st.sidebar.title("⌚ SaatKolikZ")

menu = st.sidebar.radio(
    "Menü",
    [
        "⚙ Analiz",
        "🧠 Saat Sağlığı",
        "📋 Mekanizmalar",
        "⚖ Karşılaştırma",
        "🧑‍💻 Geliştirici"
    ]
)

# ===================== ⚙ ANALİZ =====================
if menu == "⚙ Analiz":
    st.title("⚙ Mekanizma Analizi")

    mech = st.selectbox("Mekanizma seç", list(mechanisms.keys()))
    drift = st.number_input("Günlük sapma (sn)", value=0.0)

    if st.button("Analiz Et"):
        min_v, max_v = mechanisms[mech]

        st.session_state.history.append(drift)

        if drift > max_v * 1.3 or drift < min_v * 1.3:
            st.error("🔴 Bakım Gerekli")
        elif drift > max_v or drift < min_v:
            st.warning("🟡 Tolerans Dışı")
        else:
            st.success("🟢 Normal")

# ===================== 🧠 SAĞLIK =====================
elif menu == "🧠 Saat Sağlığı":
    st.title("🧠 Saat Sağlığı")

    if not st.session_state.history:
        st.info("Henüz veri girilmedi")
    else:
        avg = sum(st.session_state.history) / len(st.session_state.history)

        st.write(f"Ortalama sapma: {round(avg,2)} sn/gün")

        if abs(avg) < 5:
            st.success("🟢 Saat çok sağlıklı")
        elif abs(avg) < 20:
            st.warning("🟡 Kontrol önerilir")
        else:
            st.error("🔴 Servis gerekli")

# ===================== 📋 MEKANİZMALAR =====================
elif menu == "📋 Mekanizmalar":
    st.title("📋 Mekanizma Listesi")

    for name, (min_v, max_v) in mechanisms.items():
        st.write(f"**{name}** → {min_v} / {max_v} sn/gün")

# ===================== ⚖ KARŞILAŞTIRMA =====================
elif menu == "⚖ Karşılaştırma":
    st.title("⚖ Mekanizma Karşılaştırma")

    for name, (min_v, max_v) in mechanisms.items():
        avg = (abs(min_v) + abs(max_v)) / 2

        if avg <= 5:
            level = "🟢 Çok Hassas"
        elif avg <= 20:
            level = "🟡 Orta"
        else:
            level = "🔴 Düşük Hassasiyet"

        st.write(f"**{name}** → {level}")

# ===================== 🧑‍💻 GELİŞTİRİCİ =====================
elif menu == "🧑‍💻 Geliştirici":
    st.title("🧑‍💻 Geliştirici")

    st.subheader("⌚ SaatKolikZ")
    st.write("Made by osmn")

    st.info("""
Bu uygulama mekanik saatlerin günlük sapmalarını analiz etmek ve saat sağlığını değerlendirmek için geliştirilmiştir.

Amaç:
- Mekanizma karşılaştırma
- Sapma analizi
- Saat sağlığı tahmini

Versiyon: 1.0
""")

    st.success("Made with ❤️ by osmn")
