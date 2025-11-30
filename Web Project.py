import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, diff, latex, sympify, simplify
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import io
import base64

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Aplikasi Fungsi Matematika & Optimasi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== GEN-Z MODERN NEON THEME CSS ===================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
/* Main App Background */
.stApp {
    background: radial-gradient(circle at 20% 30%, #7f5af0, #2cb67d 40%, #16161a 90%);
    background-attachment: fixed;
    color: #fffffe;
}
/* Title Styling */
h1 {
    font-weight: 900;
    font-size: 3rem;
    text-align: center;
    background: linear-gradient(90deg, #2cb67d, #7f5af0, #00c6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 3px;
    animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
  from { text-shadow: 0 0 10px rgba(255,255,255,0.3); }
  to { text-shadow: 0 0 25px rgba(255,255,255,0.7); }
}
h2, h3 {
    color: #fffffe;
    font-weight: 700;
}
/* Cards - Glassmorphism */
div[data-testid="stHorizontalBlock"] > div {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 10px 35px rgba(0,0,0,0.35);
    backdrop-filter: blur(15px);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
div[data-testid="stHorizontalBlock"] > div:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 45px rgba(0,0,0,0.5);
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(22, 22, 26, 0.45);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.15);
}
/* Navigation Radio Buttons */
.stRadio > div {
    background: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 15px;
}
/* Buttons - RGB neon hover */
.stButton > button {
    background: linear-gradient(135deg, #7f5af0, #2cb67d);
    color: white;
    border-radius: 15px;
    border: none;
    font-weight: 700;
    padding: 0.7rem 2rem;
    transition: 0.3s ease;
    box-shadow: 0 0 15px rgba(127, 90, 240, 0.6);
}
.stButton > button:hover {
    transform: scale(1.08) translateY(-4px);
    box-shadow: 0 0 25px rgba(44, 182, 125, 0.8);
    background: linear-gradient(135deg, #00c6ff, #7f5af0);
}
/* Input Box */
.stTextInput > div > input {
    background: rgba(255,255,255,0.15);
    padding: 12px;
    border-radius: 12px;
    color: white;
    border: 1px solid rgba(255,255,255,0.15);
}
/* Expander */
.streamlit-expanderHeader {
    color: #2cb67d;
    font-weight: 600;
}
/* Plot graphs frame */
.plotly-graph-div {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
/* Photo container styling */
.photo-container {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 2px solid rgba(255,255,255,0.2);
    transition: all 0.3s ease;
}
.photo-container:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Helper fungsi ----------------
def display_member_photo(uploaded_file, name):
    """Tampilkan foto anggota atau placeholder jika None."""
    if uploaded_file is not None:
        try:
            # Pastikan pointer file di awal
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
            image = Image.open(uploaded_file)
            
            # Convert ke RGB jika perlu
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Buat gambar berbentuk lingkaran
            size = min(image.size)
            image = image.crop(((image.width - size) // 2, 
                               (image.height - size) // 2,
                               (image.width + size) // 2, 
                               (image.height + size) // 2))
            
            # Resize
            image.thumbnail((300, 300))
            
            # Buat mask lingkaran
            mask = Image.new('L', image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + image.size, fill=255)
            
            # Terapkan mask
            output = Image.new('RGBA', image.size, (0, 0, 0, 0))
            output.paste(image, (0, 0))
            output.putalpha(mask)
            
            # Convert ke base64 untuk display dengan CSS
            buffered = io.BytesIO()
            output.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            st.markdown(f"""
            <div style='text-align: center; margin: 20px 0;'>
                <img src='data:image/png;base64,{img_str}' 
                     style='width: 200px; height: 200px; border-radius: 50%; 
                            object-fit: cover; border: 4px solid rgba(255,255,255,0.3);
                            box-shadow: 0 8px 25px rgba(0,0,0,0.3);'/>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Gagal menampilkan gambar {name}: {e}")
    else:
        st.markdown(f"""
        <div style='width: 200px; height: 200px; background: linear-gradient(135deg, #667eea, #764ba2); 
                    border-radius: 50%; margin: 0 auto; display: flex; align-items: center; 
                    justify-content: center; font-size: 4rem; border: 4px solid rgba(255,255,255,0.3);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.3);'>
            👤
        </div>
        """, unsafe_allow_html=True)

# ---------------- Sidebar navigasi ----------------
st.sidebar.title("📋 Navigasi")
halaman = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Beranda", "👥 Anggota Tim", "📈 Analisis Fungsi", "🎯 Pemecah Optimasi"]
)

# ---------------- Footer sidebar info ----------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Tentang")
st.sidebar.info("""
Aplikasi ini mendemonstrasikan:
- Visualisasi fungsi
- Diferensiasi simbolik
- Pemecahan masalah optimasi
- Alat matematika interaktif
""")
st.sidebar.markdown("### 🛠️ Teknologi")
st.sidebar.markdown("""
- Python
- Streamlit
- SymPy
- Plotly
- NumPy
- PIL (Image Processing)
""")

# ================== HALAMAN 1: BERANDA ==================
if halaman == "🏠 Beranda":
    st.title("🎓 Aplikasi Web Fungsi Matematika & Optimasi")
    st.markdown("### Platform Alat Kalkulus Lanjutan & Pemecahan Masalah")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='text-align: center;'>👥 Anggota Tim</h3>
            <p style='text-align: center; color: #6b7280;'>Kenali tim pengembang dan kontribusi mereka</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='text-align: center;'>📈 Analisis Fungsi</h3>
            <p style='text-align: center; color: #6b7280;'>Visualisasikan fungsi dan hitung turunannya</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='text-align: center;'>🎯 Optimasi</h3>
            <p style='text-align: center; color: #6b7280;'>Selesaikan soal cerita langkah demi langkah</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🚀 Fitur-fitur")
    st.markdown("""
    - ✅ **Visualisasi Fungsi**: Plot fungsi matematika apapun
    - ✅ **Komputasi Turunan**: Diferensiasi langkah demi langkah dengan tampilan LaTeX
    - ✅ **Pemecah Optimasi**: Selesaikan masalah optimasi dunia nyata
    - ✅ **Plot Interaktif**: Visualisasi dinamis dan responsif
    """)

# ================== HALAMAN 2: ANGGOTA TIM ==================
elif halaman == "👥 Anggota Tim":
    st.title("👥 Tim Pengembang Kami")
    st.markdown("### Kenali orang-orang di balik proyek ini")
    
    # Upload photos
    st.markdown("---")
    with st.expander("📸 Upload Foto Anggota Tim", expanded=False):
        st.markdown("**Upload foto untuk setiap anggota tim:**")
        col_upload1, col_upload2 = st.columns(2)
        with col_upload1:
            foto_rasyid = st.file_uploader("Foto Rasyid Irvan Maulana", type=['png', 'jpg', 'jpeg'], key="foto1")
            foto_luthfi = st.file_uploader("Foto Luthfi Ilham Pratama", type=['png', 'jpg', 'jpeg'], key="foto2")
        with col_upload2:
            foto_andrian = st.file_uploader("Foto Andrian Ramadhan", type=['png', 'jpg', 'jpeg'], key="foto3")
            foto_restu = st.file_uploader("Foto Restu Imam F", type=['png', 'jpg', 'jpeg'], key="foto4")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white;'>""", unsafe_allow_html=True)
        display_member_photo(foto_rasyid, "Rasyid Irvan Maulana")
        st.markdown("<h3>Rasyid Irvan Maulana</h3><p style='font-weight: bold; color: #fbbf24;'>Ketua Proyek & Pengembang Backend</p><p style='font-size: 0.9rem;'>Integrasi API, algoritma turunan, arsitektur sistem</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white;'>""", unsafe_allow_html=True)
        display_member_photo(foto_luthfi, "Luthfi Ilham Pratama")
        st.markdown("<h3>Luthfi Ilham Pratama</h3><p style='font-weight: bold; color: #fbbf24;'>Pengembang Frontend</p><p style='font-size: 0.9rem;'>Desain UI/UX, komponen Streamlit, visualisasi</p></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""<div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white;'>""", unsafe_allow_html=True)
        display_member_photo(foto_andrian, "Andrian Ramadhan")
        st.markdown("<h3>Andrian Ramadhan</h3><p style='font-weight: bold; color: #fbbf24;'>Spesialis Matematika</p><p style='font-size: 0.9rem;'>Algoritma optimasi, validasi matematis, pengujian</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white;'>""", unsafe_allow_html=True)
        display_member_photo(foto_restu, "Restu Imam F")
        st.markdown("<h3>Restu Imam F</h3><p style='font-weight: bold; color: #fbbf24;'>Spesialis Matematika</p><p style='font-size: 0.9rem;'>Algoritma optimasi, validasi matematis, pengujian</p></div>", unsafe_allow_html=True)

# ================== HALAMAN 3: ANALISIS FUNGSI ==================
elif halaman == "📈 Analisis Fungsi":
    st.title("📈 Visualisasi Fungsi & Diferensiasi")
    
    st.markdown("### 🔢 Masukkan Fungsi Matematika")
    col1, col2 = st.columns([3, 1])
    with col1:
        input_fungsi = st.text_input(
            "Fungsi (gunakan x sebagai variabel):",
            value="x**2 + 3*x + 2",
            help="Contoh: x**2, sin(x), exp(x), x**3 - 2*x"
        )
    with col2:
        rentang_x = st.slider("Rentang Plot", -20, 20, (-10, 10))
    
    try:
        x = symbols('x')
        ekspresi_fungsi = sympify(input_fungsi)
        st.markdown("### 📝 Tampilan Fungsi")
        st.latex(f"f(x) = {latex(ekspresi_fungsi)}")
    except Exception as e:
        st.error(f"❌ Error parsing fungsi: {e}")
        st.info("Gunakan sintaks Python/SymPy, contoh: x**2, sin(x), exp(x).")
        ekspresi_fungsi = None

    if ekspresi_fungsi is not None:
        if st.button("🧮 Hitung Turunan", key="hitung_turunan"):
            st.markdown("---")
            st.markdown("### 📊 Turunan Langkah demi Langkah")
            try:
                turunan = diff(ekspresi_fungsi, x)
                with st.expander("📖 Langkah-langkah Diferensiasi", expanded=True):
                    st.markdown("**Langkah 1:** Identifikasi fungsi yang akan diturunkan")
                    st.latex(f"f(x) = {latex(ekspresi_fungsi)}")
                    st.markdown("**Langkah 2:** Terapkan aturan diferensiasi")
                    if ekspresi_fungsi.is_polynomial():
                        st.markdown("- Menggunakan **Aturan Pangkat**: $\\frac{d}{dx}[x^n] = nx^{n-1}$")
                    if ekspresi_fungsi.has(sp.sin) or ekspresi_fungsi.has(sp.cos):
                        st.markdown("- Menggunakan **Aturan Trigonometri**")
                    if ekspresi_fungsi.has(sp.exp):
                        st.markdown("- Menggunakan **Aturan Eksponensial**: $\\frac{d}{dx}[e^x] = e^x$")
                    st.markdown("**Langkah 3:** Sederhanakan hasilnya")
                    turunan_sederhana = simplify(turunan)
                    st.markdown("**Langkah 4:** Turunan akhir")
                    st.latex(f"f'(x) = {latex(turunan_sederhana)}")
                st.success("✅ Turunan Berhasil Dihitung!")
                st.markdown("### 🎯 Hasil Akhir")
                st.latex(f"\\boxed{{f'(x) = {latex(turunan_sederhana)}}}")
            except Exception as e:
                st.error(f"Gagal menghitung turunan: {e}")
                turunan = None

            # Plot fungsi dan turunan (jika tersedia)
            st.markdown("---")
            st.markdown("### 📊 Visualisasi")
            colp1, colp2 = st.columns(2)
            nilai_x = np.linspace(rentang_x[0], rentang_x[1], 400)
            
            # plot fungsi asli
            with colp1:
                st.markdown("#### Fungsi Asli f(x)")
                try:
                    f_lambda = sp.lambdify(x, ekspresi_fungsi, 'numpy')
                    nilai_y = f_lambda(nilai_x)
                    fig1 = go.Figure()
                    fig1.add_trace(go.Scatter(x=nilai_x, y=nilai_y, mode='lines', name='f(x)', line=dict(width=3)))
                    fig1.update_layout(title="Fungsi Asli", xaxis_title="x", yaxis_title="f(x)", hovermode='x', template='plotly_white')
                    st.plotly_chart(fig1, use_container_width=True)
                except Exception:
                    st.error("Tidak dapat memplot fungsi ini dalam rentang yang diberikan.")
            # plot turunan
            with colp2:
                st.markdown("#### Turunan f'(x)")
                try:
                    if 'turunan' in locals() and turunan is not None:
                        turunan_lambda = sp.lambdify(x, turunan, 'numpy')
                        nilai_dy = turunan_lambda(nilai_x)
                        fig2 = go.Figure()
                        fig2.add_trace(go.Scatter(x=nilai_x, y=nilai_dy, mode='lines', name="f'(x)", line=dict(width=3)))
                        fig2.update_layout(title="Fungsi Turunan", xaxis_title="x", yaxis_title="f'(x)", hovermode='x', template='plotly_white')
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("Tekan tombol 'Hitung Turunan' terlebih dahulu untuk melihat plot turunan.")
                except Exception:
                    st.error("Tidak dapat memplot turunan dalam rentang yang diberikan.")

# ================== HALAMAN 4: OPTIMASI ==================
elif halaman == "🎯 Pemecah Optimasi":
    st.title("🎯 Pemecah Soal Cerita Optimasi")
    st.markdown("### 📝 Masukkan Masalah Optimasi Anda")
    
    contoh_masalah = {
        "Luas Persegi Panjang (Kendala Keliling)": {
            "masalah": "Seorang petani memiliki 40 meter pagar untuk memagari area persegi panjang. Dimensi apa yang akan memaksimalkan luas yang dipagari?",
            "tipe_solusi": "persegi_panjang_keliling"
        },
        "Volume Kotak (Luas Permukaan)": {
            "masalah": "Sebuah kotak terbuka dibuat dari selembar karton persegi berukuran 12 inci pada setiap sisi dengan memotong persegi yang sama dari sudut dan melipat sisi ke atas. Temukan ukuran persegi sudut yang memaksimalkan volume.",
            "tipe_solusi": "volume_kotak"
        },
        "Optimasi Produk": {
            "masalah": "Temukan dua bilangan positif yang jumlahnya 50 dan produknya maksimum.",
            "tipe_solusi": "jumlah_produk"
        }
    }
    pilihan_contoh = st.selectbox("Pilih contoh atau masukkan sendiri:", ["Masalah Kustom"] + list(contoh_masalah.keys()))
    if pilihan_contoh == "Masalah Kustom":
        teks_masalah = st.text_area("Masukkan soal cerita:", height=150, placeholder="Deskripsikan masalah optimasi Anda di sini...")
    else:
        teks_masalah = st.text_area("Masalah:", value=contoh_masalah[pilihan_contoh]["masalah"], height=150)

    if st.button("🔍 Selesaikan Masalah Optimasi"):
        if teks_masalah:
            st.markdown("---")
            st.markdown("### 🧮 Solusi")
            if pilihan_contoh == "Luas Persegi Panjang (Kendala Keliling)":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Definisikan Variabel**")
                    st.markdown("- Misalkan $x$ = panjang persegi panjang")
                    st.markdown("- Misalkan $y$ = lebar persegi panjang")
                    st.markdown("- Kendala keliling: $2x + 2y = 40$")
                    st.markdown("**Langkah 2: Ekspresikan Fungsi Objektif**")
                    st.markdown("- Objektif: Maksimalkan Luas $A = xy$")
                    st.markdown("- Dari kendala: $y = 20 - x$")
                    st.markdown("- Substitusi: $A(x) = x(20-x) = 20x - x^2$")
                    st.latex("A(x) = 20x - x^2")
                    st.markdown("**Langkah 3: Temukan Titik Kritis**")
                    st.markdown("- Ambil turunan: $A'(x) = 20 - 2x$")
                    st.latex("A'(x) = 20 - 2x")
                    st.markdown("- Set sama dengan nol: $20 - 2x = 0$ -> $x = 10$")
                    st.markdown("**Langkah 4: Verifikasi Maksimum**")
                    st.markdown("- $A''(x) = -2 < 0$ -> maksimum")
                    st.markdown("**Langkah 5: Hitung Luas Maksimum**")
                    st.markdown("- Luas Maksimum = $10 \\times 10 = 100$ meter persegi")
                st.success("✅ **Solusi:** Persegi panjang harus berbentuk persegi sisi 10 m, luas 100 m².")
                # Plot
                nilai_x = np.linspace(0, 20, 200)
                nilai_luas = nilai_x * (20 - nilai_x)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=nilai_x, y=nilai_luas, mode='lines', name='Luas', line=dict(width=3)))
                fig.add_trace(go.Scatter(x=[10], y=[100], mode='markers', name='Maksimum', marker=dict(size=15, symbol='star')))
                fig.update_layout(title="Luas vs. Panjang", xaxis_title="Panjang (x) dalam meter", yaxis_title="Luas (m²)", hovermode='x', template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            elif pilihan_contoh == "Optimasi Produk":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Definisikan Variabel**")
                    st.markdown("- Misalkan $x$ = bilangan pertama, $y$ = bilangan kedua, $x+y=50$")
                    st.markdown("**Langkah 2: Objektif**")
                    st.markdown("- Maksimalkan $P=xy$, substitusi $y=50-x$ -> $P(x)=50x-x^2$")
                    st.markdown("**Langkah 3: Titik Kritis**")
                    st.markdown("- $P'(x)=50-2x=0$ -> $x=25$")
                    st.markdown("**Langkah 4: Hasil**")
                    st.markdown("- Kedua bilangan 25 dan 25 -> produk 625")
                st.success("✅ **Solusi:** 25 dan 25, produk maksimum 625.")
                nilai_x = np.linspace(0, 50, 200)
                nilai_produk = nilai_x * (50 - nilai_x)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=nilai_x, y=nilai_produk, mode='lines', name='Produk', line=dict(width=3)))
                fig.add_trace(go.Scatter(x=[25], y=[625], mode='markers', name='Maksimum', marker=dict(size=15, symbol='star')))
                fig.update_layout(title="Produk vs. Bilangan Pertama", xaxis_title="Bilangan Pertama (x)", yaxis_title="Produk (xy)", template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            elif pilihan_contoh == "Volume Kotak (Luas Permukaan)":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Definisikan Variabel**")
                    st.markdown("- Misalkan $x$ = panjang sisi potongan (inci), karton 12×12")
                    st.markdown("**Langkah 2: Fungsi Volume**")
                    st.latex("V(x) = x(12-2x)^2 = 4x^3 - 48x^2 + 144x")
                    st.markdown("**Langkah 3: Titik Kritis**")
                    st.latex("V'(x) = 12x^2 - 96x + 144 -> x^2 - 8x +12 = 0 -> (x-2)(x-6)=0")
                    st.markdown("**Langkah 4: Hasil**")
                    st.markdown("- x=2 valid (x=6 membuat alas nol). Volume maksimum = 128 in³")
                st.success("✅ **Solusi:** Potong kotak 2 inci dari setiap sudut -> volume 128 in³.")
                nilai_x = np.linspace(0.1, 6, 200)
                nilai_volume = 4*nilai_x**3 - 48*nilai_x**2 + 144*nilai_x
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=nilai_x, y=nilai_volume, mode='lines', name='Volume', line=dict(width=3)))
                fig.add_trace(go.Scatter(x=[2], y=[128], mode='markers', name='Maksimum', marker=dict(size=15, symbol='star')))
                fig.update_layout(title="Volume vs. Ukuran Potongan", xaxis_title="Ukuran Potongan Sudut (x) in", yaxis_title="Volume (in³)", template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Untuk masalah kustom, silakan pilih salah satu contoh yang telah ditentukan untuk melihat format solusi.")
        else:
            st.warning("⚠️ Silakan masukkan masalah untuk diselesaikan.")
