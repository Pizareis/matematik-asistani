import streamlit as st
import fitz
import os

st.set_page_config(page_title="Matematik Notu Asistanı", page_icon="📐", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffe0f0, #ffc2e0, #ffb3d9, #ff99cc);
    background-size: 400% 400%;
    animation: gradyan 8s ease infinite;
}
@keyframes gradyan {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #ff69b4, #ff1493) !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    padding: 0.6rem 1.2rem !important;
    box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4) !important;
    transition: transform 0.2s !important;
}
div[data-testid="stButton"] button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(255, 20, 147, 0.5) !important;
}
div[data-testid="stTextInput"] input {
    border: 2px solid #ff69b4 !important;
    border-radius: 10px !important;
    background: rgba(255,255,255,0.8) !important;
}
h1, h2, h3 {
    color: #cc0066 !important;
}
.kart {
    background: rgba(255,255,255,0.5);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    border: 2px solid #ffb6c1;
    margin: 10px;
}
</style>
""", unsafe_allow_html=True)

# Sayfa yönetimi
if "sayfa" not in st.session_state:
    st.session_state["sayfa"] = "hosgeldin"

# ─────────────────────────────────────────
# 🌸 SAYFA 1: HOŞGELDİN
# ─────────────────────────────────────────
if st.session_state["sayfa"] == "hosgeldin":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; font-size:3rem'>🌸 Hoş Geldin Şekerim! 🌸</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#cc0066; font-size:1.3rem'>Matematik asistanına hoş geldin 💕 Sana nasıl yardımcı olabilirim?</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='kart'>📚<br><b>Ders Notlarına Bak</b><br><small>PDF notlarını görüntüle</small></div>", unsafe_allow_html=True)
        if st.button("📚 Notlara Git", use_container_width=True, key="notlar_btn"):
            st.session_state["sayfa"] = "notlar"
            st.rerun()

    with col2:
        st.markdown("<div class='kart'>💬<br><b>Soru Sormak İstiyorum</b><br><small>Notlardan soru sor</small></div>", unsafe_allow_html=True)
        if st.button("💬 Soru Sor", use_container_width=True, key="soru_btn"):
            st.session_state["sayfa"] = "notlar"
            st.session_state["direkt_sekme"] = "💬 Soru Sor"
            st.rerun()

    with col3:
        st.markdown("<div class='kart'>❓<br><b>Sınava Hazırlanmak</b><br><small>Sınav sorusu üret</small></div>", unsafe_allow_html=True)
        if st.button("❓ Sınava Hazırlan", use_container_width=True, key="sinav_btn"):
            st.session_state["sayfa"] = "notlar"
            st.session_state["direkt_sekme"] = "❓ Sınav Sorusu Üret"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ff69b4; font-size:0.9rem'>✨ Hocandan sevgiyle 💕</p>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 📚 SAYFA 2: NOTLAR
# ─────────────────────────────────────────
elif st.session_state["sayfa"] == "notlar":
    col_geri, col_baslik = st.columns([1, 8])
    with col_geri:
        if st.button("⬅️ Geri"):
            st.session_state["sayfa"] = "hosgeldin"
            st.session_state.pop("secili_not", None)
            st.session_state.pop("direkt_sekme", None)
            st.rerun()
    with col_baslik:
        st.markdown("<h2>📚 Ders Notları</h2>", unsafe_allow_html=True)

    NOTLAR_KLASOR = "notlar"

    if not os.path.exists(NOTLAR_KLASOR):
        os.makedirs(NOTLAR_KLASOR)
        st.warning("⚠️ 'notlar' klasörü oluşturuldu. PDF dosyalarını buraya ekle!")
        st.stop()

    pdf_dosyalar = [f for f in os.listdir(NOTLAR_KLASOR) if f.endswith(".pdf")]

    if not pdf_dosyalar:
        st.warning("⚠️ 'notlar' klasöründe hiç PDF bulunamadı! Klasöre PDF ekle 🌸")
        st.stop()

    cols = st.columns(3)
    for i, pdf in enumerate(sorted(pdf_dosyalar)):
        ders_adi = pdf.replace("_", " ").replace(".pdf", "")
        with cols[i % 3]:
            if st.button(f"📄 {ders_adi}", use_container_width=True, key=pdf):
                st.session_state["secili_not"] = pdf
                st.rerun()

    # Not seçildiyse göster
    if "secili_not" in st.session_state:
        secili_not = st.session_state["secili_not"]
        ders_adi = secili_not.replace("_", " ").replace(".pdf", "")

        st.divider()
        st.subheader(f"📖 {ders_adi}")

        pdf_yolu = os.path.join(NOTLAR_KLASOR, secili_not)
        doc = fitz.open(pdf_yolu)
        full_text = ""
        for page in doc:
            full_text += page.get_text()

        st.caption(f"📃 {len(doc)} sayfa yüklendi")

        with st.expander("📖 Notun içeriğini önizle"):
            st.write(full_text[:1500] + "...")

        st.divider()

        varsayilan = st.session_state.get("direkt_sekme", "💬 Soru Sor")
        sekmeler = ["💬 Soru Sor", "📝 Özet Çıkar", "❓ Sınav Sorusu Üret"]
        varsayilan_idx = sekmeler.index(varsayilan) if varsayilan in sekmeler else 0

        sekme = st.radio("Ne yapmak istiyorsun?", sekmeler,
                         index=varsayilan_idx, horizontal=True)

        if sekme == "💬 Soru Sor":
            soru = st.text_input("Soruyu yaz:", placeholder="Örnek: Özdeğer nedir?")
            prompt_tip = "soru-cevap"
        elif sekme == "📝 Özet Çıkar":
            soru = st.text_input("Hangi konunun özetini istiyorsun?", placeholder="Örnek: Matris çarpımı")
            prompt_tip = "özet"
        else:
            soru = st.text_input("Hangi konuda soru üreteyim?", placeholder="Örnek: Determinant")
            prompt_tip = "soru-üret"

        api_key = st.text_input("🔑 API Key:", type="password",
                                 help="console.anthropic.com adresinden alabilirsin")

        if st.button("🚀 Gönder", type="primary") and soru and api_key:
            import anthropic
            baglam = full_text[:4000]

            if prompt_tip == "soru-cevap":
                mesaj = f"Aşağıdaki matematik notlarına dayanarak soruyu Türkçe cevapla:\n\n{baglam}\n\nSoru: {soru}"
            elif prompt_tip == "özet":
                mesaj = f"Aşağıdaki matematik notlarından '{soru}' konusunu Türkçe özetle, madde madde açıkla:\n\n{baglam}"
            else:
                mesaj = f"Aşağıdaki matematik notlarına göre '{soru}' konusunda 5 sınav sorusu üret, zorluk seviyelerini belirt:\n\n{baglam}"

            client = anthropic.Anthropic(api_key=api_key)
            with st.spinner("🤖 Düşünüyor..."):
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": mesaj}]
                )

            st.markdown("### 💡 Cevap:")
            st.markdown(response.content[0].text)
            