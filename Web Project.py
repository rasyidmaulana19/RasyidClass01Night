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
    page_title="Mathematical Functions & Optimization App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== PREMIUM DARK THEME WITH ACCENTS ===================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
/* Main App Background */
.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    background-attachment: fixed;
    color: #e4e4e7;
    position: relative;
}
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1), transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.08), transparent 50%);
    pointer-events: none;
}
/* Title Styling */
h1 {
    font-weight: 900;
    font-size: 3rem;
    text-align: center;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 3px;
    animation: glow 3s ease-in-out infinite alternate;
    filter: drop-shadow(0 0 20px rgba(96, 165, 250, 0.3));
}
@keyframes glow {
  from { filter: drop-shadow(0 0 10px rgba(96, 165, 250, 0.2)); }
  to { filter: drop-shadow(0 0 25px rgba(167, 139, 250, 0.4)); }
}
h2 {
    color: #f0f0f0;
    font-weight: 700;
    border-left: 4px solid #3b82f6;
    padding-left: 15px;
    margin-top: 20px;
}
h3 {
    color: #d4d4d8;
    font-weight: 600;
}
/* Cards - Enhanced Glassmorphism */
div[data-testid="stHorizontalBlock"] > div {
    background: linear-gradient(135deg, rgba(30,41,59,0.7), rgba(30,41,59,0.5));
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(100,116,139,0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
div[data-testid="stHorizontalBlock"] > div::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
    transition: left 0.5s ease;
}
div[data-testid="stHorizontalBlock"] > div:hover::before {
    left: 100%;
}
div[data-testid="stHorizontalBlock"] > div:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
    border: 1px solid rgba(59, 130, 246, 0.4);
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,23,42,0.95), rgba(30,41,59,0.95));
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(59, 130, 246, 0.2);
}
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 {
    color: #60a5fa;
    border-left: none;
    padding-left: 0;
}
/* Navigation Radio Buttons */
.stRadio > div {
    background: rgba(30,41,59,0.6);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(100,116,139,0.2);
}
.stRadio label {
    transition: all 0.2s ease;
}
.stRadio label:hover {
    color: #60a5fa !important;
    transform: translateX(5px);
}
/* Buttons - Accent Highlight */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(59, 130, 246, 0.5);
    font-weight: 700;
    padding: 0.7rem 2rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}
.stButton > button:hover::before {
    left: 100%;
}
.stButton > button:hover {
    transform: scale(1.05) translateY(-2px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5), 0 0 30px rgba(59, 130, 246, 0.3);
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    border: 1px solid rgba(96, 165, 250, 0.8);
}
/* Input Box */
.stTextInput > div > input,
.stTextArea textarea {
    background: rgba(30,41,59,0.6);
    padding: 12px;
    border-radius: 12px;
    color: #e4e4e7;
    border: 1px solid rgba(100,116,139,0.3);
    transition: all 0.3s ease;
}
.stTextInput > div > input:focus,
.stTextArea textarea:focus {
    border: 1px solid rgba(59, 130, 246, 0.6);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    background: rgba(30,41,59,0.8);
}
/* Slider */
.stSlider > div > div > div {
    background: #3b82f6 !important;
}
/* Expander */
.streamlit-expanderHeader {
    background: rgba(30,41,59,0.4);
    border-radius: 10px;
    border: 1px solid rgba(100,116,139,0.2);
    color: #60a5fa !important;
    font-weight: 600;
    transition: all 0.3s ease;
}
.streamlit-expanderHeader:hover {
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.4);
}
/* Success/Error/Info boxes */
.stSuccess {
    background: rgba(34, 197, 94, 0.1);
    border-left: 4px solid #22c55e;
    border-radius: 8px;
}
.stError {
    background: rgba(239, 68, 68, 0.1);
    border-left: 4px solid #ef4444;
    border-radius: 8px;
}
.stInfo {
    background: rgba(59, 130, 246, 0.1);
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
}
.stWarning {
    background: rgba(251, 191, 36, 0.1);
    border-left: 4px solid #fbbf24;
    border-radius: 8px;
}
/* Plot graphs frame */
.plotly-graph-div {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    border: 1px solid rgba(100,116,139,0.2);
}
/* Photo container styling */
.photo-container {
    background: rgba(30,41,59,0.5);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 2px solid rgba(100,116,139,0.25);
    transition: all 0.3s ease;
}
.photo-container:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
    border: 2px solid rgba(59, 130, 246, 0.4);
}
/* File uploader */
.stFileUploader {
    background: rgba(30,41,59,0.4);
    border-radius: 12px;
    border: 2px dashed rgba(100,116,139,0.3);
    transition: all 0.3s ease;
}
.stFileUploader:hover {
    border: 2px dashed rgba(59, 130, 246, 0.5);
    background: rgba(59, 130, 246, 0.05);
}
/* Markdown with emojis highlight */
.stMarkdown strong {
    color: #60a5fa;
    font-weight: 700;
}
/* Custom scrollbar */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
::-webkit-scrollbar-track {
    background: rgba(30,41,59,0.3);
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #3b82f6, #2563eb);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #60a5fa, #3b82f6);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Helper functions ----------------
def display_member_photo(uploaded_file, name):
    """Display member photo or placeholder if None."""
    if uploaded_file is not None:
        try:
            # Ensure file pointer is at the beginning
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
            image = Image.open(uploaded_file)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create circular image
            size = min(image.size)
            image = image.crop(((image.width - size) // 2, 
                               (image.height - size) // 2,
                               (image.width + size) // 2, 
                               (image.height + size) // 2))
            
            # Resize
            image.thumbnail((300, 300))
            
            # Create circular mask
            mask = Image.new('L', image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + image.size, fill=255)
            
            # Apply mask
            output = Image.new('RGBA', image.size, (0, 0, 0, 0))
            output.paste(image, (0, 0))
            output.putalpha(mask)
            
            # Convert to base64 for display with CSS
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
            st.error(f"Failed to display image for {name}: {e}")
    else:
        st.markdown(f"""
        <div style='width: 200px; height: 200px; background: linear-gradient(135deg, #2a2a2a, #3a3a3a); 
                    border-radius: 50%; margin: 0 auto; display: flex; align-items: center; 
                    justify-content: center; font-size: 4rem; border: 4px solid rgba(255,255,255,0.2);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.5);'>
            👤
        </div>
        """, unsafe_allow_html=True)

# ---------------- Sidebar navigation ----------------
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Choose Page:",
    ["🏠 Home", "👥 Team Members", "📈 Function Analysis", "🎯 Optimization Solver"]
)

# ---------------- Footer sidebar info ----------------
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
- PIL (Image Processing)
""")

# ================== PAGE 1: HOME ==================
if page == "🏠 Home":
    st.title("🎓 Mathematical Functions & Optimization Web App")
    st.markdown("### Advanced Calculus Tools & Problem Solving Platform")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a1a, #2a2a2a); padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);'>
            <h3 style='text-align: center; color: #ffffff;'>👥 Team Members</h3>
            <p style='text-align: center; color: #b0b0b0;'>Meet the development team and their contributions</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a1a, #2a2a2a); padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);'>
            <h3 style='text-align: center; color: #ffffff;'>📈 Function Analysis</h3>
            <p style='text-align: center; color: #b0b0b0;'>Visualize functions and compute derivatives</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a1a, #2a2a2a); padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);'>
            <h3 style='text-align: center; color: #ffffff;'>🎯 Optimization</h3>
            <p style='text-align: center; color: #b0b0b0;'>Solve word problems step by step</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🚀 Features")
    st.markdown("""
    - ✅ **Function Visualization**: Plot any mathematical function
    - ✅ **Derivative Computation**: Step-by-step differentiation with LaTeX display
    - ✅ **Optimization Solver**: Solve real-world optimization problems
    - ✅ **Interactive Plots**: Dynamic and responsive visualizations
    """)

# ================== PAGE 2: TEAM MEMBERS ==================
elif page == "👥 Team Members":
    st.title("👥 Our Development Team")
    st.markdown("### Meet the people behind this project")
    
    # Upload photos
    st.markdown("---")
    with st.expander("📸 Upload Team Member Photos", expanded=False):
        st.markdown("**Upload a photo for each team member:**")
        col_upload1, col_upload2 = st.columns(2)
        with col_upload1:
            photo_rasyid = st.file_uploader("Rasyid Irvan Maulana's Photo", type=['png', 'jpg', 'jpeg'], key="photo1")
            photo_luthfi = st.file_uploader("Luthfi Ilham Pratama's Photo", type=['png', 'jpg', 'jpeg'], key="photo2")
        with col_upload2:
            photo_andrian = st.file_uploader("Andrian Ramadhan's Photo", type=['png', 'jpg', 'jpeg'], key="photo3")
            photo_restu = st.file_uploader("Restu Imam Fakhrezi's Photo", type=['png', 'jpg', 'jpeg'], key="photo4")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);padding: 2rem; border-radius: 15px; color: white; margin-top: -40px;'>""", unsafe_allow_html=True)
        display_member_photo(photo_rasyid, "Rasyid Irvan Maulana")
        st.markdown("<h3>Rasyid Irvan Maulana</h3><p style='font-weight: bold; color: #fbbf24;'>Project Lead • Backend Architect</p><p style='font-size: 0.9rem;'>Crafts the core system architecture and backend infrastructure that drive the entire platform. Leads API integration, develops derivative logic, and ensures all system components operate consistently and efficiently.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);padding: 2rem; border-radius: 15px; color: white; margin-top: -40px;'>""", unsafe_allow_html=True)
        display_member_photo(photo_luthfi, "Luthfi Ilham Pratama")
        st.markdown("<h3>Luthfi Ilham Pratama</h3><p style='font-weight: bold; color: #fbbf24;'>Frontend Engineer • UI/UX Designer</p><p style='font-size: 0.9rem;'>Designs intuitive, user-centered interfaces with modern and responsive layouts. Creates elegant Streamlit components and visual elements that enhance usability across devices.</p></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);padding: 2rem; border-radius: 15px; color: white; margin-top: -40px;'>""", unsafe_allow_html=True)
        display_member_photo(photo_andrian, "Andrian Ramadhan")
        st.markdown("<h3>Andrian Ramadhan</h3><p style='font-weight: bold; color: #fbbf24;'>Algorithm & Mathematics Engineer</p><p style='font-size: 0.9rem;'>Translates complex mathematical concepts into precise and optimized algorithms. Validates models, refines derivative computations, and ensures mathematical accuracy throughout the application.</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);padding: 2rem; border-radius: 15px; color: white; margin-top: -40px;'>""", unsafe_allow_html=True)
        display_member_photo(photo_restu, "Restu Imam Fakhrezi")
        st.markdown("<h3>Restu Imam Fakhrezi</h3><p style='font-weight: bold; color: #fbbf24;'>Computational Mathematics Engineer</p><p style='font-size: 0.9rem;'>Analyzes mathematical formulations to ensure reliability and correctness. Develops optimization approaches, validates computational results, and stress-tests algorithm performance under diverse inputs.</p></div>", unsafe_allow_html=True)

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

            # Plot function and derivative (if available)
            st.markdown("---")
            st.markdown("### 📊 Visualization")
            colp1, colp2 = st.columns(2)
            x_values = np.linspace(x_range[0], x_range[1], 400)
            
            # plot original function
            with colp1:
                st.markdown("#### Original Function f(x)")
                try:
                    f_lambda = sp.lambdify(x, function_expr, 'numpy')
                    y_values = f_lambda(x_values)
                    fig1 = go.Figure()
                    fig1.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='f(x)', line=dict(width=3)))
                    fig1.update_layout(title="Original Function", xaxis_title="x", yaxis_title="f(x)", hovermode='x', template='plotly_white')
                    st.plotly_chart(fig1, use_container_width=True)
                except Exception:
                    st.error("Cannot plot this function in the given range.")
            # plot derivative
            with colp2:
                st.markdown("#### Derivative f'(x)")
                try:
                    if 'derivative' in locals() and derivative is not None:
                        derivative_lambda = sp.lambdify(x, derivative, 'numpy')
                        dy_values = derivative_lambda(x_values)
                        fig2 = go.Figure()
                        fig2.add_trace(go.Scatter(x=x_values, y=dy_values, mode='lines', name="f'(x)", line=dict(width=3)))
                        fig2.update_layout(title="Derivative Function", xaxis_title="x", yaxis_title="f'(x)", hovermode='x', template='plotly_white')
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
                    st.markdown("- Set equal to zero: $20 - 2x = 0$ -> $x = 10$")
                    st.markdown("**Step 4: Verify Maximum**")
                    st.markdown("- $A''(x) = -2 < 0$ -> maximum")
                    st.markdown("**Step 5: Calculate Maximum Area**")
                    st.markdown("- Maximum Area = $10 \\times 10 = 100$ square meters")
                st.success("✅ **Solution:** The rectangle should be a square with sides of 10 m, area 100 m².")
                # Plot
                x_values = np.linspace(0, 20, 200)
                area_values = x_values * (20 - x_values)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=area_values, mode='lines', name='Area', line=dict(width=3)))
                fig.add_trace(go.Scatter(x=[10], y=[100], mode='markers', name='Maximum', marker=dict(size=15, symbol='star')))
                fig.update_layout(title="Area vs. Length", xaxis_title="Length (x) in meters", yaxis_title="Area (m²)", hovermode='x', template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            elif example_choice == "Product Optimization":
                with st.expander("📋 Step-by-Step Solution", expanded=True):
                    st.markdown("**Step 1: Define Variables**")
                    st.markdown("- Let $x$ = first number, $y$ = second number, $x+y=50$")
                    st.markdown("**Step 2: Objective**")
                    st.markdown("- Maximize $P=xy$, substitute $y=50-x$ -> $P(x)=50x-x^2$")
                    st.markdown("**Step 3: Critical Points**")
                    st.markdown("- $P'(x)=50-2x=0$ -> $x=25$")
                    st.markdown("**Step 4: Result**")
                    st.markdown("- Both numbers are 25 and 25 -> product is 625")
                st.success("✅ **Solution:** 25 and 25, maximum product is 625.")
                x_values = np.linspace(0, 50, 200)
                product_values = x_values * (50 - x_values)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=product_values, mode='lines', name='Product', line=dict(width=3)))
                fig.add_trace(go.Scatter(x=[25], y=[625], mode='markers', name='Maximum', marker=dict(size=15, symbol='star')))
                fig.update_layout(title="Product vs. First Number", xaxis_title="First Number (x)", yaxis_title="Product (xy)", template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            elif example_choice == "Box Volume (Surface Area)":
                with st.expander("📋 Step-by-Step Solution", expanded=True):
                    st.markdown("**Step 1: Define Variables**")
                    st.markdown("- Let $x$ = side length of cut (inches), cardboard is 12×12")
                    st.markdown("**Step 2: Volume Function**")
                    st.latex("V(x) = x(12-2x)^2 = 4x^3 - 48x^2 + 144x")
                    st.markdown("**Step 3: Critical Points**")
                    st.latex("V'(x) = 12x^2 - 96x + 144 -> x^2 - 8x +12 = 0 -> (x-2)(x-6)=0")
                    st.markdown("**Step 4: Result**")
                    st.markdown("- x=2 is valid (x=6 makes base zero). Maximum volume = 128 in³")
                st.success("✅ **Solution:** Cut 2-inch squares from each corner -> volume is 128 in³.")
                x_values = np.linspace(0.1, 6, 200)
                volume_values = 4*x_values**3 - 48*x_values**2 + 144*x_values
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=volume_values, mode='lines', name='Volume', line=dict(width=3)))
                fig.add_trace(go.Scatter(x=[2], y=[128], mode='markers', name='Maximum', marker=dict(size=15, symbol='star')))
                fig.update_layout(title="Volume vs. Cut Size", xaxis_title="Corner Cut Size (x) in", yaxis_title="Volume (in³)", template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 For custom problems, please select one of the predefined examples to see the solution format.")
        else:
            st.warning("⚠️ Please enter a problem to solve.")
