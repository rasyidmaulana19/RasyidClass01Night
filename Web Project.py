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
</style>
""", unsafe_allow_html=True)

# ---------------- Helper functions ----------------
def display_member_photo(github_url, name):
    """Display member photo from GitHub URL."""
    st.markdown(f"""
    <div style='text-align: center; margin: 20px 0;'>
        <img src='{github_url}' 
             style='width: 180px; height: 180px; border-radius: 50%; 
                    object-fit: cover; border: 3px solid #3b82f6;
                    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);'/>
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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                    border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
            <h3 style='text-align: center; color: #60a5fa;'>👥 Team Members</h3>
            <p style='text-align: center; color: #94a3b8;'>Meet the development team</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                    border: 1px solid rgba(167, 139, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
            <h3 style='text-align: center; color: #a78bfa;'>📈 Function Analysis</h3>
            <p style='text-align: center; color: #94a3b8;'>Visualize and differentiate</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                    border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
            <h3 style='text-align: center; color: #60a5fa;'>🎯 Optimization</h3>
            <p style='text-align: center; color: #94a3b8;'>Solve word problems</p>
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
    
    st.markdown("---")
    
    # GitHub raw URL untuk foto
    github_base_url = "https://raw.githubusercontent.com/rasyidmaulana19/RasyidClass01Night/main/image/"
    
    col1, col2 = st.columns(2)
    with col1:
        display_member_photo(f"{github_base_url}rasyid.jpeg", "Rasyid Irvan Maulana")
        st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <h3 style='color: #e4e4e7;'>Rasyid Irvan Maulana</h3>
            <p style='font-weight: bold; color: #60a5fa; font-size: 1rem;'>Project Lead • Backend Architect</p>
            <p style='font-size: 0.9rem; color: #cbd5e1;'>Crafts the core system architecture and backend infrastructure that drive the entire platform.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        display_member_photo(f"{github_base_url}luthfi.jpeg", "Luthfi Ilham Pratama")
        st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <h3 style='color: #e4e4e7;'>Luthfi Ilham Pratama</h3>
            <p style='font-weight: bold; color: #a78bfa; font-size: 1rem;'>Frontend Engineer • UI/UX Designer</p>
            <p style='font-size: 0.9rem; color: #cbd5e1;'>Designs intuitive, user-centered interfaces with modern and responsive layouts.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        display_member_photo(f"{github_base_url}andrian.jpeg", "Andrian Ramadhan")
        st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <h3 style='color: #e4e4e7;'>Andrian Ramadhan</h3>
            <p style='font-weight: bold; color: #22d3ee; font-size: 1rem;'>Algorithm & Mathematics Engineer</p>
            <p style='font-size: 0.9rem; color: #cbd5e1;'>Translates complex mathematical concepts into precise and optimized algorithms.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        display_member_photo(f"{github_base_url}restu.jpeg", "Restu Imam Fakhrezi")
        st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <h3 style='color: #e4e4e7;'>Restu Imam Fakhrezi</h3>
            <p style='font-weight: bold; color: #34d399; font-size: 1rem;'>Computational Mathematics Engineer</p>
            <p style='font-size: 0.9rem; color: #cbd5e1;'>Analyzes mathematical formulations to ensure reliability and correctness.</p>
        </div>
        """, unsafe_allow_html=True)

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
