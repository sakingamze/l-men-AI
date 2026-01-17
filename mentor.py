# mentor.py
import streamlit as st
from google import genai
from auth import create_user_table, register_user, login_user
from pdf_report import generate_pdf
import matplotlib.pyplot as plt
import os

# --------------------
# İlk kurulum 
# --------------------
create_user_table()

st.set_page_config(page_title="✨ Lümen-AI", page_icon="✨", layout="wide")

# --------------------
# Session kontrolü
# --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --------------------
# GİRİŞ / KAYIT
# --------------------
if not st.session_state.logged_in:
    st.title("✨ Lümen-AI Giriş")

    tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])

    with tab1:
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        if st.button("Giriş"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Giriş başarılı!")
                st.rerun()
            else:
                st.error("Hatalı kullanıcı adı veya şifre")

    with tab2:
        new_user = st.text_input("Yeni Kullanıcı Adı")
        new_pass = st.text_input("Yeni Şifre", type="password")
        if st.button("Kayıt Ol"):
            if register_user(new_user, new_pass):
                st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
            else:
                st.error("Bu kullanıcı adı zaten var")

    st.stop()

# --------------------
# GİRİŞ SONRASI SIDE BAR
# --------------------
if "user" in st.session_state:
    st.sidebar.success(f"👤 Giriş yapan: {st.session_state.user}")
    if st.sidebar.button("Çıkış Yap"):
        st.session_state.logged_in = False
        del st.session_state.user  # Kullanıcı bilgisini temizle
        st.rerun()

# --------------------
# Gemini Client
# --------------------
client = genai.Client()
MODEL_NAME = "models/gemini-2.5-flash"

# --------------------
# CSS ( gri, beyaz yazı)
# --------------------
st.markdown("""
<style>
body { background-color: #2f2f2f; color: #ffffff; }
h1,h2,h3,h4 { color: #ffffff; }
.stTextArea textarea { background-color: #3c3c3c; color: white; }
.stButton>button { background-color: #5a5a5a; color: white; border-radius: 8px; font-weight: bold; }
.stButton>button:hover { background-color: #777777; }
.stSelectbox select { background-color: #3c3c3c; color: white; }
</style>
""", unsafe_allow_html=True)

# --------------------
# HEADER
# --------------------
st.header("✨ Lümen-AI")
st.write("Kodunu paylaş, yapay zekâ analiz etsin 🌟")

# --------------------
# Junior / Senior
# --------------------
st.subheader("Mentör Seviyesi")
col_role1, col_role2 = st.columns(2)
junior = col_role1.button("Junior")
senior = col_role2.button("Senior")
role = "Junior" if junior else "Senior" if senior else "Junior"

# --------------------
# Çoklu Dil Seçimi
# --------------------
language = st.selectbox("Kod Dili Seçin:", ["Python", "JavaScript", "Java", "C#"])

# --------------------
# Kod Alanı
# --------------------
col1, col2 = st.columns(2)
with col1:
    code_input = st.text_area("Analiz edilecek kodu buraya yapıştır:", height=400)
    analyze_button = st.button("🔍 Analiz Et")

with col2:
    st.subheader("📝 Mentorun Analizi")
    if analyze_button:
        if code_input.strip():
            with st.spinner("Kodu inceliyorum, lütfen bekleyin..."):
                try:
                    # --------------------
                    # AI Prompt
                    # --------------------
                    prompt = f"""
Sen tecrübeli bir yazılım mentörüsün. Rol: {role}, Dil: {language}

Aşağıdaki kodu:
1. Hatalar açısından incele
2. Daha temiz ve doğru yazım öner
3. Gerekirse refactor edilmiş örnek ver
4.sorulan sorulara mantıklı ve nazik yanıtlar ver
5. Kodun kalitesini 1-10 arası puanla
6.Hataları kategoriye ayır: Syntax, Mantık, Performans, Güvenlik
7. Açıklamaları Türkçe, net ve kısa yap
8. Eğer rol Junior ise motivasyon ver: "Bugün hata yapan X Junior’dan birisin, bu çok normal"
9. Otomatik test önerileri üret
10. Kod performans ve güvenlik analizi yap
Kod:
{code_input}
"""
                    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                    analysis_text = response.text

                    # --------------------
                    # Analizi Göster
                    # --------------------
                    st.markdown(analysis_text)

                    # --------------------
                    # Otomatik Test Grafiği
                    # --------------------
                    fig, ax = plt.subplots(figsize=(5,3))
                    categories = ["Syntax", "Mantık", "Performans", "Güvenlik"]
                    counts = [analysis_text.count(cat) for cat in categories]
                    ax.bar(categories, counts, color="#1f77b4")
                    ax.set_title("Hata Kategorileri Görselleştirmesi")
                    st.pyplot(fig)

                    # --------------------
                    # PDF Rapor
                    # --------------------
                    pdf_path = generate_pdf(username=st.session_state.user, role=role, analysis_text=analysis_text)
                    if os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="📄 PDF Raporu İndir",
                                data=pdf_file,
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf"
                            )

                except KeyboardInterrupt:
                    st.warning("⚠️ İşlem kullanıcı tarafından iptal edildi.")
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("⚠️ Lütfen analiz edilecek bir kod girin.")
