import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, diff, latex, sympify, simplify
import plotly.graph_objects as go

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Mathematical Functions & Optimization App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== PREMIUM DARK THEME ===================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    color: #e4e4e7;
}

h1 {
    font-weight: 900;
    font-size: 2.5rem;
    text-align: center;
    color: #60a5fa;
    letter-spacing: 2px;
    text-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
}

h2 {
    color: #e4e4e7;
    font-weight: 700;
    border-left: 4px solid #3b82f6;
    padding-left: 15px;
}

h3 {
    color: #cbd5e1;
    font-weight: 600;
}

.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 700;
    padding: 0.7rem 2rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1729, #1a1a2e);
    border-right: 1px solid rgba(59, 130, 246, 0.3);
}

.stTextInput input, .stTextArea textarea {
    background: rgba(30,41,59,0.6);
    color: #e4e4e7;
    border: 1px solid rgba(100,116,139,0.3);
    border-radius: 8px;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

div.stMarkdown strong {
    color: #60a5fa;
}

/* Team Member Card Styles */
.team-card {
    background: rgba(30,41,59,0.8);
    border-radius: 20px;
    padding: 2rem;
    border: 2px solid transparent;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.team-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 20px;
    padding: 2px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.4s ease;
}

.team-card:hover::before {
    opacity: 1;
}

.team-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
}

.member-photo {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center;
    border: 4px solid;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    transition: all 0.4s ease;
    position: relative;
    z-index: 2;
    display: block;
    margin: 0 auto;
}

.team-card:hover .member-photo {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 15px 35px rgba(59, 130, 246, 0.5);
}

.member-name {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e4e4e7;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    transition: color 0.3s ease;
}

.team-card:hover .member-name {
    color: #60a5fa;
}

.member-role {
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
}

.member-desc {
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.6;
}

.role-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.25rem;
    transition: all 0.3s ease;
}

.role-badge:hover {
    transform: scale(1.1);
}

.section-header {
    text-align: center;
    margin-bottom: 3rem;
    position: relative;
}

.section-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.section-subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    font-weight: 400;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Helper functions ----------------
def display_member_card(github_url, name, role, description, border_color, role_bg):
    """Display member card with photo and info."""
    st.markdown(f"""
    <div class='team-card'>
        <div style='text-align: center;'>
            <div style='width: 200px; height: 200px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 4px solid {border_color}; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4); position: relative;'>
                <img src='{github_url}' 
                     style='width: 100%; height: 100%; object-fit: cover; object-position: center center; transition: all 0.4s ease; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);'
                     onmouseover="this.style.transform='translate(-50%, -50%) scale(1.1) rotate(5deg)'"
                     onmouseout="this.style.transform='translate(-50%, -50%) scale(1) rotate(0deg)'"/>
            </div>
            <h3 class='member-name'>{name}</h3>
            <div class='role-badge' style='background: {role_bg}; color: white;'>
                {role}
            </div>
            <p class='member-desc'>{description}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Sidebar navigation ----------------
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Choose Page:",
    ["🏠 Home", "👥 Team Members", "📈 Function Analysis", "🎯 Optimization Solver"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 About")
st.sidebar.info("""
This application demonstrates:
- Function visualization
- Symbolic differentiation
- Optimization problem solving
- Interactive mathematical tools
""")
st.sidebar.markdown("### 🛠️ Technologies")
st.sidebar.markdown("""
- Python
- Streamlit
- SymPy
- Plotly
- NumPy
""")

# ================== PAGE 1: HOME ==================
if page == "🏠 Home":
    st.title("🎓 Mathematical Functions & Optimization Web App")
    st.markdown("### Advanced Calculus Tools & Problem Solving Platform")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Navigation Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                    border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    transition: all 0.3s ease; cursor: pointer;'
                    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(59, 130, 246, 0.4)'"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.3)'">
            <h3 style='text-align: center; color: #60a5fa;'>👥 Team Members</h3>
            <p style='text-align: center; color: #94a3b8;'>Meet the development team</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                    border: 1px solid rgba(167, 139, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    transition: all 0.3s ease; cursor: pointer;'
                    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(167, 139, 246, 0.4)'"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.3)'">
            <h3 style='text-align: center; color: #a78bfa;'>📈 Function Analysis</h3>
            <p style='text-align: center; color: #94a3b8;'>Visualize and differentiate</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                    border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    transition: all 0.3s ease; cursor: pointer;'
                    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(59, 130, 246, 0.4)'"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.3)'">
            <h3 style='text-align: center; color: #60a5fa;'>🎯 Optimization</h3>
            <p style='text-align: center; color: #94a3b8;'>Solve word problems</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Main Content - Derivative Theory
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1)); 
                padding: 2rem; border-radius: 20px; border: 2px solid rgba(59, 130, 246, 0.3);
                margin-bottom: 2rem;'>
        <h2 style='color: #60a5fa; text-align: center; font-size: 2rem; margin-bottom: 1rem;'>
            📐 Apa itu Turunan (Derivative)?
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_def1, col_def2 = st.columns([1, 1])
    
    with col_def1:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                    border-left: 4px solid #3b82f6; height: 100%;'>
            <h3 style='color: #60a5fa; margin-bottom: 1rem;'>📖 Definisi</h3>
            <p style='color: #cbd5e1; line-height: 1.8; font-size: 1rem;'>
                Turunan adalah <strong style='color: #60a5fa;'>laju perubahan suatu fungsi</strong> terhadap variabelnya. 
                Secara geometris, turunan merepresentasikan <strong style='color: #60a5fa;'>kemiringan garis singgung</strong> 
                pada suatu titik di kurva fungsi.
            </p>
            <p style='color: #94a3b8; font-style: italic; margin-top: 1rem;'>
                💡 Turunan menjawab pertanyaan: "Seberapa cepat fungsi berubah pada titik tertentu?"
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_def2:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                    border-left: 4px solid #8b5cf6; height: 100%;'>
            <h3 style='color: #a78bfa; margin-bottom: 1rem;'>🧮 Definisi Matematis</h3>
            <p style='color: #cbd5e1; line-height: 1.8;'>
                Turunan fungsi f(x) didefinisikan sebagai limit:
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}")
        st.markdown("""
        <p style='color: #94a3b8; text-align: center; margin-top: 0.5rem;'>
            atau dapat ditulis sebagai:
        </p>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{dy}{dx} = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Derivative Rules Section
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1)); 
                padding: 2rem; border-radius: 20px; border: 2px solid rgba(139, 92, 246, 0.3);
                margin-bottom: 2rem;'>
        <h2 style='color: #a78bfa; text-align: center; font-size: 2rem; margin-bottom: 1rem;'>
            📝 Rumus-Rumus Turunan
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_rule1, col_rule2, col_rule3 = st.columns(3)
    
    with col_rule1:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                    border: 2px solid rgba(59, 130, 246, 0.3); min-height: 280px;'>
            <h4 style='color: #60a5fa; text-align: center; margin-bottom: 1rem;'>⚡ Aturan Dasar</h4>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(c) = 0")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Konstanta</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(x^n) = nx^{n-1}")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Power Rule</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(cf(x)) = c \cdot f'(x)")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Constant Multiple</p>", unsafe_allow_html=True)
    
    with col_rule2:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                    border: 2px solid rgba(139, 92, 246, 0.3); min-height: 280px;'>
            <h4 style='color: #a78bfa; text-align: center; margin-bottom: 1rem;'>🔄 Trigonometri</h4>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(\sin x) = \cos x")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Sinus</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(\cos x) = -\sin x")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Cosinus</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(\tan x) = \sec^2 x")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Tangen</p>", unsafe_allow_html=True)
    
    with col_rule3:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                    border: 2px solid rgba(6, 182, 212, 0.3); min-height: 280px;'>
            <h4 style='color: #22d3ee; text-align: center; margin-bottom: 1rem;'>📈 Eksponensial & Log</h4>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(e^x) = e^x")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Exponential</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(\ln x) = \frac{1}{x}")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Natural Log</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(a^x) = a^x \ln a")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>General Exponential</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Engineering Applications
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(16, 185, 129, 0.1)); 
                padding: 2rem; border-radius: 20px; border: 2px solid rgba(6, 182, 212, 0.3);
                margin-bottom: 2rem;'>
        <h2 style='color: #22d3ee; text-align: center; font-size: 2rem; margin-bottom: 1rem;'>
            🔧 Aplikasi Turunan dalam Dunia Teknik
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    applications = [
        {
            "icon": "🚗",
            "title": "Teknik Mesin & Otomotif",
            "desc": "Menghitung kecepatan dan akselerasi kendaraan, mengoptimalkan efisiensi mesin, dan mendesain sistem transmisi.",
            "formula": r"v(t) = \frac{ds}{dt}, \quad a(t) = \frac{dv}{dt}",
            "color": "#3b82f6"
        },
        {
            "icon": "⚡",
            "title": "Teknik Elektro",
            "desc": "Menganalisis arus listrik, tegangan pada rangkaian, dan mendesain filter elektronik dengan respons frekuensi optimal.",
            "formula": r"i(t) = \frac{dq}{dt}, \quad v(t) = L\frac{di}{dt}",
            "color": "#8b5cf6"
        },
        {
            "icon": "🏗️",
            "title": "Teknik Sipil",
            "desc": "Menghitung gaya maksimum pada struktur, optimasi bentuk jembatan, dan analisis defleksi balok.",
            "formula": r"M = -EI\frac{d^2y}{dx^2}",
            "color": "#06b6d4"
        },
        {
            "icon": "🏭",
            "title": "Teknik Kimia & Proses",
            "desc": "Menentukan laju reaksi kimia, mengoptimalkan produksi, dan mengontrol suhu pada reaktor.",
            "formula": r"r = -\frac{dC}{dt} = kC^n",
            "color": "#10b981"
        },
        {
            "icon": "✈️",
            "title": "Teknik Aerospace",
            "desc": "Menghitung gaya angkat pesawat, optimasi bentuk sayap, dan analisis trajektori penerbangan.",
            "formula": r"F_L = \frac{1}{2}\rho v^2 C_L A",
            "color": "#f59e0b"
        },
        {
            "icon": "🤖",
            "title": "Robotika & AI",
            "desc": "Gradient descent untuk machine learning, path planning robot, dan kontrol motor servo.",
            "formula": r"\theta_{new} = \theta_{old} - \alpha \frac{\partial J}{\partial \theta}",
            "color": "#ec4899"
        }
    ]
    
    col_app1, col_app2 = st.columns(2)
    
    for idx, app in enumerate(applications):
        col = col_app1 if idx % 2 == 0 else col_app2
        with col:
            st.markdown(f"""
            <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                        border-left: 4px solid {app["color"]}; margin-bottom: 1rem;
                        transition: all 0.3s ease;'
                        onmouseover="this.style.transform='translateX(10px)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.3)'"
                        onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='none'">
                <h4 style='color: {app["color"]}; margin-bottom: 0.5rem;'>{app["icon"]} {app["title"]}</h4>
                <p style='color: #cbd5e1; line-height: 1.6; font-size: 0.95rem;'>{app["desc"]}</p>
            </div>
            """, unsafe_allow_html=True)
            st.latex(app["formula"])
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div style='background: rgba(30,41,59,0.6); padding: 2rem; border-radius: 15px; 
                border: 1px solid rgba(59, 130, 246, 0.3);'>
        <h3 style='color: #60a5fa; margin-bottom: 1.5rem;'>🚀 Fitur Aplikasi</h3>
    </div>
    """, unsafe_allow_html=True)
    
    features_col1, features_col2 = st.columns(2)
    with features_col1:
        st.markdown("""
        <ul style='color: #cbd5e1; line-height: 2; font-size: 1rem;'>
            <li>✅ <strong style='color: #60a5fa;'>Function Visualization</strong>: Plot fungsi matematika apapun</li>
            <li>✅ <strong style='color: #60a5fa;'>Derivative Computation</strong>: Hitung turunan step-by-step dengan LaTeX</li>
        </ul>
        """, unsafe_allow_html=True)
    with features_col2:
        st.markdown("""
        <ul style='color: #cbd5e1; line-height: 2; font-size: 1rem;'>
            <li>✅ <strong style='color: #60a5fa;'>Optimization Solver</strong>: Selesaikan masalah optimasi dunia nyata</li>
            <li>✅ <strong style='color: #60a5fa;'>Interactive Plots</strong>: Visualisasi dinamis dan responsif</li>
        </ul>
        """, unsafe_allow_html=True)

# ================== PAGE 2: TEAM MEMBERS ==================
elif page == "👥 Team Members":
    # Header Section
    st.markdown("""
    <div class='section-header'>
        <h1 class='section-title'>👥 Our Development Team</h1>
        <p class='section-subtitle'>Meet the brilliant minds behind this project</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # GitHub raw URL untuk foto
    github_base_url = "https://raw.githubusercontent.com/rasyidmaulana19/RasyidClass01Night/main/Image/"
    
    # Team Members Row 1
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        display_member_card(
            f"{github_base_url}rasyid.jpeg",
            "Rasyid Irvan Maulana",
            "🚀 Project Lead • Backend Architect",
            "Crafts the core system architecture and backend infrastructure that drive the entire platform. Expert in designing scalable solutions and optimizing performance.",
            "#3b82f6",
            "linear-gradient(135deg, #3b82f6, #2563eb)"
        )
    
    with col2:
        display_member_card(
            f"{github_base_url}luthfi.jpeg",
            "Luthfi Ilham Pratama",
            "🎨 Frontend Engineer • UI/UX Designer",
            "Designs intuitive, user-centered interfaces with modern and responsive layouts. Passionate about creating seamless user experiences.",
            "#8b5cf6",
            "linear-gradient(135deg, #8b5cf6, #7c3aed)"
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Team Members Row 2
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        display_member_card(
            f"{github_base_url}andrian.jpeg",
            "Andrian Ramadhan",
            "🧮 Algorithm & Mathematics Engineer",
            "Translates complex mathematical concepts into precise and optimized algorithms. Specializes in computational efficiency and mathematical modeling.",
            "#06b6d4",
            "linear-gradient(135deg, #06b6d4, #0891b2)"
        )
    
    with col4:
        display_member_card(
            f"{github_base_url}restu.jpeg",
            "Restu Imam Fakhrezi",
            "📐 Computational Mathematics Engineer",
            "Analyzes mathematical formulations to ensure reliability and correctness. Focuses on numerical methods and mathematical validation.",
            "#10b981",
            "linear-gradient(135deg, #10b981, #059669)"
        )

# ================== PAGE 3: FUNCTION ANALYSIS ==================
elif page == "📈 Function Analysis":
    st.title("📈 Function Visualization & Differentiation")
    
    st.markdown("### 🔢 Enter a Mathematical Function")
    col1, col2 = st.columns([3, 1])
    with col1:
        input_function = st.text_input(
            "Function (use x as variable):",
            value="x**2 + 3*x + 2",
            help="Examples: x**2, sin(x), exp(x), x**3 - 2*x"
        )
    with col2:
        x_range = st.slider("Plot Range", -20, 20, (-10, 10))
    
    try:
        x = symbols('x')
        function_expr = sympify(input_function)
        st.markdown("### 📝 Function Display")
        st.latex(f"f(x) = {latex(function_expr)}")
    except Exception as e:
        st.error(f"❌ Error parsing function: {e}")
        st.info("Use Python/SymPy syntax, examples: x**2, sin(x), exp(x).")
        function_expr = None

    if function_expr is not None:
        if st.button("🧮 Calculate Derivative", key="calc_derivative"):
            st.markdown("---")
            st.markdown("### 📊 Step-by-Step Derivative")
            try:
                derivative = diff(function_expr, x)
                with st.expander("📖 Differentiation Steps", expanded=True):
                    st.markdown("**Step 1:** Identify the function to differentiate")
                    st.latex(f"f(x) = {latex(function_expr)}")
                    st.markdown("**Step 2:** Apply differentiation rules")
                    if function_expr.is_polynomial():
                        st.markdown("- Using **Power Rule**: $\\frac{d}{dx}[x^n] = nx^{n-1}$")
                    if function_expr.has(sp.sin) or function_expr.has(sp.cos):
                        st.markdown("- Using **Trigonometric Rules**")
                    if function_expr.has(sp.exp):
                        st.markdown("- Using **Exponential Rule**: $\\frac{d}{dx}[e^x] = e^x$")
                    st.markdown("**Step 3:** Simplify the result")
                    simplified_derivative = simplify(derivative)
                    st.markdown("**Step 4:** Final derivative")
                    st.latex(f"f'(x) = {latex(simplified_derivative)}")
                st.success("✅ Derivative Successfully Calculated!")
                st.markdown("### 🎯 Final Result")
                st.latex(f"\\boxed{{f'(x) = {latex(simplified_derivative)}}}")
            except Exception as e:
                st.error(f"Failed to calculate derivative: {e}")
                derivative = None

            st.markdown("---")
            st.markdown("### 📊 Visualization")
            colp1, colp2 = st.columns(2)
            x_values = np.linspace(x_range[0], x_range[1], 400)
            
            with colp1:
                st.markdown("#### Original Function f(x)")
                try:
                    f_lambda = sp.lambdify(x, function_expr, 'numpy')
                    y_values = f_lambda(x_values)
                    fig1 = go.Figure()
                    fig1.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='f(x)', line=dict(width=3, color='#60a5fa')))
                    fig1.update_layout(title="Original Function", xaxis_title="x", yaxis_title="f(x)", template='plotly_dark')
                    st.plotly_chart(fig1, use_container_width=True)
                except Exception:
                    st.error("Cannot plot this function in the given range.")
            
            with colp2:
                st.markdown("#### Derivative f'(x)")
                try:
                    if 'derivative' in locals() and derivative is not None:
                        derivative_lambda = sp.lambdify(x, derivative, 'numpy')
                        dy_values = derivative_lambda(x_values)
                        fig2 = go.Figure()
                        fig2.add_trace(go.Scatter(x=x_values, y=dy_values, mode='lines', name="f'(x)", line=dict(width=3, color='#a78bfa')))
                        fig2.update_layout(title="Derivative Function", xaxis_title="x", yaxis_title="f'(x)", template='plotly_dark')
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("Press 'Calculate Derivative' button first to see the derivative plot.")
                except Exception:
                    st.error("Cannot plot the derivative in the given range.")

# ================== PAGE 4: OPTIMIZATION ==================
elif page == "🎯 Optimization Solver":
    st.title("🎯 Optimization Word Problem Solver")
    st.markdown("### 📝 Enter Your Optimization Problem")
    
    example_problems = {
        "Rectangle Area (Perimeter Constraint)": {
            "problem": "A farmer has 40 meters of fencing to enclose a rectangular area. What dimensions will maximize the enclosed area?",
            "solution_type": "rectangle_perimeter"
        },
        "Box Volume (Surface Area)": {
            "problem": "An open box is made from a square sheet of cardboard 12 inches on each side by cutting equal squares from the corners and folding up the sides. Find the size of the corner squares that maximizes the volume.",
            "solution_type": "box_volume"
        },
        "Product Optimization": {
            "problem": "Find two positive numbers whose sum is 50 and whose product is maximum.",
            "solution_type": "sum_product"
        }
    }
    
    example_choice = st.selectbox("Select example or enter your own:", ["Custom Problem"] + list(example_problems.keys()))
    if example_choice == "Custom Problem":
        problem_text = st.text_area("Enter word problem:", height=150, placeholder="Describe your optimization problem here...")
    else:
        problem_text = st.text_area("Problem:", value=example_problems[example_choice]["problem"], height=150)

    if st.button("🔍 Solve Optimization Problem"):
        if problem_text:
            st.markdown("---")
            st.markdown("### 🧮 Solution")
            if example_choice == "Rectangle Area (Perimeter Constraint)":
                with st.expander("📋 Step-by-Step Solution", expanded=True):
                    st.markdown("**Step 1: Define Variables**")
                    st.markdown("- Let $x$ = length of rectangle")
                    st.markdown("- Let $y$ = width of rectangle")
                    st.markdown("- Perimeter constraint: $2x + 2y = 40$")
                    st.markdown("**Step 2: Express Objective Function**")
                    st.markdown("- Objective: Maximize Area $A = xy$")
                    st.markdown("- From constraint: $y = 20 - x$")
                    st.markdown("- Substitution: $A(x) = x(20-x) = 20x - x^2$")
                    st.latex("A(x) = 20x - x^2")
                    st.markdown("**Step 3: Find Critical Points**")
                    st.markdown("- Take derivative: $A'(x) = 20 - 2x$")
                    st.latex("A'(x) = 20 - 2x")
                    st.markdown("- Set equal to zero: $20 - 2x = 0$ → $x = 10$")
                    st.markdown("**Step 4: Verify Maximum**")
                    st.markdown("- $A''(x) = -2 < 0$ → maximum")
                    st.markdown("**Step 5: Calculate Maximum Area**")
                    st.markdown("- Maximum Area = $10 \\times 10 = 100$ square meters")
                st.success("✅ **Solution:** The rectangle should be a square with sides of 10 m, area 100 m².")
                
                x_values = np.linspace(0, 20, 200)
                area_values = x_values * (20 - x_values)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=area_values, mode='lines', name='Area', line=dict(width=3, color='#60a5fa')))
                fig.add_trace(go.Scatter(x=[10], y=[100], mode='markers', name='Maximum', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Area vs. Length", xaxis_title="Length (x) in meters", yaxis_title="Area (m²)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
                
            elif example_choice == "Product Optimization":
                with st.expander("📋 Step-by-Step Solution", expanded=True):
                    st.markdown("**Step 1: Define Variables**")
                    st.markdown("- Let $x$ = first number, $y$ = second number, $x+y=50$")
                    st.markdown("**Step 2: Objective**")
                    st.markdown("- Maximize $P=xy$, substitute $y=50-x$ → $P(x)=50x-x^2$")
                    st.markdown("**Step 3: Critical Points**")
                    st.markdown("- $P'(x)=50-2x=0$ → $x=25$")
                    st.markdown("**Step 4: Result**")
                    st.markdown("- Both numbers are 25 and 25 → product is 625")
                st.success("✅ **Solution:** 25 and 25, maximum product is 625.")
                
                x_values = np.linspace(0, 50, 200)
                product_values = x_values * (50 - x_values)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=product_values, mode='lines', name='Product', line=dict(width=3, color='#a78bfa')))
                fig.add_trace(go.Scatter(x=[25], y=[625], mode='markers', name='Maximum', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Product vs. First Number", xaxis_title="First Number (x)", yaxis_title="Product (xy)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
                
            elif example_choice == "Box Volume (Surface Area)":
                with st.expander("📋 Step-by-Step Solution", expanded=True):
                    st.markdown("**Step 1: Define Variables**")
                    st.markdown("- Let $x$ = side length of cut (inches), cardboard is 12×12")
                    st.markdown("**Step 2: Volume Function**")
                    st.latex("V(x) = x(12-2x)^2 = 4x^3 - 48x^2 + 144x")
                    st.markdown("**Step 3: Critical Points**")
                    st.latex("V'(x) = 12x^2 - 96x + 144 → x^2 - 8x +12 = 0 → (x-2)(x-6)=0")
                    st.markdown("**Step 4: Result**")
                    st.markdown("- x=2 is valid (x=6 makes base zero). Maximum volume = 128 in³")
                st.success("✅ **Solution:** Cut 2-inch squares from each corner → volume is 128 in³.")
                
                x_values = np.linspace(0.1, 6, 200)
                volume_values = 4*x_values**3 - 48*x_values**2 + 144*x_values
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=volume_values, mode='lines', name='Volume', line=dict(width=3, color='#60a5fa')))
                fig.add_trace(go.Scatter(x=[2], y=[128], mode='markers', name='Maximum', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Volume vs. Cut Size", xaxis_title="Corner Cut Size (x) in", yaxis_title="Volume (in³)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 For custom problems, please select one of the predefined examples to see the solution format.")
        else:
            st.warning("⚠️ Please enter a problem to solve.")
