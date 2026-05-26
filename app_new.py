import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. PAGE CONFIGURATION & STYLING ---
st.set_page_config(page_title="Nassau Candy Profitability", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Professional Styling with Dark Mode Support
st.markdown("""
    <style>
    /* ===== LIGHT MODE (DEFAULT) ===== */
    /* Main styling */
    body, [data-testid="stAppViewContainer"] { 
        background: linear-gradient(135deg, #f0f4f8 0%, #e8f0f7 100%) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }
    
    .main {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8f0f7 100%) !important;
    }
    
    /* Sidebar styling - Light Mode */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #2d5a8c 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    [data-testid="stSidebar"] .stMultiSelect, 
    [data-testid="stSidebar"] .stSlider {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* KPI Cards - Light Mode */
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .kpi-card.sales { border-left-color: #667eea; }
    .kpi-card.profit { border-left-color: #764ba2; }
    .kpi-card.margin { border-left-color: #f093fb; }
    .kpi-card.units { border-left-color: #4facfe; }
    
    .kpi-label {
        font-size: 0.875rem;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    /* ===== DARK MODE ===== */
    @media (prefers-color-scheme: dark) {
        /* Main styling - Dark */
        body, [data-testid="stAppViewContainer"] { 
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%) !important;
            color: #e0e6f0 !important;
        }
        
        .main {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%) !important;
        }
        
        /* Sidebar styling - Dark Mode */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a1628 0%, #132a4a 100%) !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #e0e6f0 !important;
        }
        
        /* Header styling - Dark Mode */
        .header {
            background: linear-gradient(135deg, #5a6dd8 0%, #6b3a96 100%) !important;
            color: white !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
        }
        
        .header h1 {
            color: white !important;
        }
        
        .header-subtitle {
            color: rgba(255, 255, 255, 0.95) !important;
        }
        
        /* KPI Cards - Dark Mode */
        .kpi-card {
            background: #1e2534 !important;
            color: #e0e6f0 !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(224, 230, 240, 0.1);
        }
        
        .kpi-card:hover {
            box-shadow: 0 4px 15px rgba(90, 109, 216, 0.2);
        }
        
        .kpi-label {
            color: #a8b0c0 !important;
        }
        
        .kpi-value {
            color: #ffffff !important;
        }
        
        /* General text elements - Dark Mode */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }
        
        /* Input elements - Dark Mode */
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stSelectbox"] select,
        [data-testid="stMultiSelect"] [role="button"] {
            background-color: #252d3d !important;
            color: #e0e6f0 !important;
            border: 1px solid rgba(224, 230, 240, 0.2) !important;
        }
        
        /* Metric container - Dark Mode */
        [data-testid="metric-container"] {
            background: #1e2534 !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(224, 230, 240, 0.1);
        }
    }
    
    /* Tab styling - Light Mode */
    [data-testid="stTabs"] [aria-selected="true"] {
        border-bottom: 3px solid #667eea;
    }
    
    /* Table styling */
    .dataframe-container {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Light Mode Metric styling */
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        color: #1e3a5f;
    }
    
    /* Sidebar Logo and Footer Styling - Light Mode */
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-header img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-header a {
        color: white;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    
    .sidebar-header a:hover {
        color: #c3cfe2;
        text-decoration: underline;
    }
    
    .sidebar-footer {
        padding: 1rem;
        background: linear-gradient(180deg, rgba(15, 31, 53, 0.8) 0%, rgba(30, 58, 95, 0.8) 100%);
        border-top: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 8px;
        text-align: center;
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 1rem;
    }
    
    .sidebar-footer a {
        color: #c3cfe2;
        text-decoration: none;
        transition: all 0.3s ease;
        display: block;
        margin: 0.5rem 0;
    }
    
    .sidebar-footer a:hover {
        color: white;
        text-decoration: underline;
    }
    
    .sidebar-credit {
        font-weight: 600;
        color: white;
        margin-bottom: 0.75rem;
        font-size: 0.8rem;
    }
    
    /* ===== DARK MODE ADDITIONAL STYLES ===== */
    @media (prefers-color-scheme: dark) {
        /* Tabs - Dark Mode */
        [data-testid="stTabs"] [aria-selected="true"] {
            border-bottom-color: #5a6dd8 !important;
        }
        
        /* Dataframe - Dark Mode */
        .dataframe-container {
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        
        /* Sidebar Header - Dark Mode */
        .sidebar-header {
            border-bottom-color: rgba(224, 230, 240, 0.2) !important;
        }
        
        .sidebar-header a {
            color: #e0e6f0 !important;
        }
        
        .sidebar-header a:hover {
            color: #a8b0c0 !important;
        }
        
        /* Sidebar Footer - Dark Mode */
        .sidebar-footer {
            background: linear-gradient(180deg, rgba(10, 22, 40, 0.9) 0%, rgba(19, 42, 74, 0.9) 100%) !important;
            border-top-color: rgba(224, 230, 240, 0.2) !important;
            color: rgba(224, 230, 240, 0.9) !important;
        }
        
        .sidebar-footer a {
            color: #a8b0c0 !important;
        }
        
        .sidebar-footer a:hover {
            color: #e0e6f0 !important;
        }
        
        .sidebar-credit {
            color: #e0e6f0 !important;
        }
        
        /* Dataframe table - Dark Mode */
        [data-testid="stDataFrame"] {
            background-color: #1e2534 !important;
        }
        
        [data-testid="stDataFrame"] tbody tr {
            border-color: rgba(224, 230, 240, 0.1) !important;
        }
        
        [data-testid="stDataFrame"] th,
        [data-testid="stDataFrame"] td {
            color: #e0e6f0 !important;
            border-color: rgba(224, 230, 240, 0.1) !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Professional Header
st.markdown("""
    <div class="header">
        <h1>🍭 Nassau Candy Analytics</h1>
        <p class="header-subtitle">Product Line Profitability & Margin Analysis Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING & CLEANING ---
@st.cache_data
def load_and_clean_data():
    # Load raw data
    df = pd.read_csv('Nassau Candy Distributor.csv')
    
    # Date Standardization
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
    
    # Financial Logic Validation (Sales - Cost = Profit)
    df['Expected_Profit'] = df['Sales'] - df['Cost']
    logic_mask = (df['Gross Profit'] - df['Expected_Profit']).abs() < 0.01
    
    # Filter Invalid Records
    df = df[(df['Sales'] > 0) & (df['Gross Profit'] > 0) & (logic_mask)].copy()
    
    # KPI Calculations
    df['Gross Margin %'] = (df['Gross Profit'] / df['Sales']) * 100
    df['Profit per Unit'] = df['Gross Profit'] / df['Units']
    
    return df

df = load_and_clean_data()

# --- FACTORY MAPPING DATA (From Document) ---
factory_data = {
    'Factory': ["Lot's O' Nuts", "Wicked Choccy's", "Sugar Shack", "Secret Factory", "The Other Factory"],
    'lat': [32.881893, 32.076176, 48.11914, 41.446333, 35.1175],
    'lon': [-111.768036, -81.088371, -96.18115, -90.565487, -89.971107],
    'Division': ["Chocolate", "Chocolate", "Sugar", "Sugar", "Other"]  # Mapped based on Reqs [cite: 94]
}
df_factories = pd.DataFrame(factory_data)

# --- 3. SIDEBAR PAGE NAVIGATION ---
with st.sidebar:
    # Sidebar Header with Logo
    st.markdown("""
    <div class="sidebar-header">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjfVXnu8h1ym8c0pwo752nkZb_gl2ymPWa2Q&s" alt="Nassau Candy Logo" style="width: 100%; max-width: 150px;">
        <br>
        <a href="https://www.nassaucandy.com/" target="_blank">🏢 Nassau Candy Distributor</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigation", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio(
        "Select Dashboard Page:",
        options=["🏠 Home", "📊 Detailed Analysis", "🗺️ Factory Analysis", "📈 Reports"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")

# --- 3.1 SIDEBAR CONTROLS (ALWAYS VISIBLE) ---
with st.sidebar:
    st.markdown("### 📊 Dashboard Filters", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("---")
        st.markdown("<h4 style='color: white;'>Filters & Settings</h4>", unsafe_allow_html=True)
        
        # Division Filter
        st.markdown("<p style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>📍 Select Divisions:</p>", unsafe_allow_html=True)
        selected_divisions = st.multiselect("Select Division", 
                                            options=df['Division'].unique(), 
                                            default=df['Division'].unique(),
                                            label_visibility="collapsed")
        
        st.markdown("")
        
        # Margin Threshold Slider
        st.markdown("<p style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>⚖️ Margin Risk Threshold:</p>", unsafe_allow_html=True)
        margin_threshold = st.slider("Margin Risk Threshold (%)", 0, 100, 20, label_visibility="collapsed")
        
        st.markdown("")
        st.markdown("---")
        st.markdown("### 🔍 Advanced Search & Filters")
        
        # Requirement: Date range selector [cite: 80]
        min_date = df['Order Date'].min()
        max_date = df['Order Date'].max()
        date_range = st.date_input("Select Date Range", [min_date, max_date])
        
        st.markdown("")
        
        # Requirement: Product search [cite: 83] (Changed from text_input to selectbox for easier navigation)
        # We add 'All Products' as the first option so you can still view the entire dataset
        product_list = ["All Products"] + sorted(df['Product Name'].unique().tolist())
        search_product = st.selectbox(
            "🔍 Select Specific Product", 
            options=product_list,
            help="Select a specific candy to analyze its individual margin performance."
        )
        
        st.markdown("")
        st.markdown("---")
        
        # Summary Stats
        st.markdown("<h4 style='color: white;'>Quick Stats</h4>", unsafe_allow_html=True)
        temp_df = df[df['Division'].isin(selected_divisions)]
        st.metric("📊 Total Records", len(temp_df))
        st.metric("🏢 Divisions Active", len(selected_divisions))
        
        # Sidebar Footer
        st.markdown("")
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-footer">
            <div class="sidebar-credit">👨‍💻 PROJECT MADE BY</div>
            <div style='color: white; font-weight: 600; margin-bottom: 0.75rem;'>AMAN SRIVASTAV</div>
            <a href="https://www.nassaucandy.com/" target="_blank">🏢 Nassau Candy</a>
            <a href="https://unifiedmentor.com/" target="_blank">🎓 Unified Mentor</a>
        </div>
        """, unsafe_allow_html=True)

# Apply Filters
mask = (df['Division'].isin(selected_divisions)) & \
       (df['Order Date'] >= pd.to_datetime(date_range[0])) & \
       (df['Order Date'] <= pd.to_datetime(date_range[1]))

# If a specific product is chosen, filter the dataframe; otherwise, show all
if search_product != "All Products":
    mask = mask & (df['Product Name'] == search_product)

filtered_df = df[mask]

# Calculate Key Metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Gross Profit'].sum()
avg_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
total_units = filtered_df['Units'].sum()

# --- MARGIN VOLATILITY CALCULATION ---
# Volatility is defined as the variability (Standard Deviation) of margin over time
if not filtered_df.empty:
    # Group by date to see how the overall margin fluctuates daily/monthly
    daily_margin = filtered_df.groupby('Order Date')['Gross Margin %'].mean()
    volatility_score = daily_margin.std()
else:
    volatility_score = 0

# ============================================================================
# PAGE 1: HOME DASHBOARD
# ============================================================================
if page == "🏠 Home":
    st.markdown("<h3 style='color: #1e3a5f; margin-top: 2rem;'>📈 Key Performance Indicators</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

    # Sales KPI
    with col1:
        st.markdown(f"""
        <div class="kpi-card sales">
            <div class="kpi-label">💰 Total Sales</div>
            <div class="kpi-value">${total_sales:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Profit KPI
    with col2:
        st.markdown(f"""
        <div class="kpi-card profit">
            <div class="kpi-label">📊 Total Profit</div>
            <div class="kpi-value">${total_profit:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Margin KPI
    with col3:
        st.markdown(f"""
        <div class="kpi-card margin">
            <div class="kpi-label">📈 Avg Margin</div>
            <div class="kpi-value">{avg_margin:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Units KPI
    with col4:
        st.markdown(f"""
        <div class="kpi-card units">
            <div class="kpi-label">📦 Total Units</div>
            <div class="kpi-value">{total_units:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Volatility KPI
    with col5:
        st.markdown(f"""
        <div class="kpi-card margin">
            <div class="kpi-label">📉 Margin Volatility</div>
            <div class="kpi-value">{volatility_score:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.75rem; color: #666;'>Lower = More Stable</p>", unsafe_allow_html=True)

    # Welcome Section with Background
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                border-radius: 15px; padding: 2rem; margin: 1rem 0; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
        <h2 style='margin: 0; text-align: center;'>🎯 Welcome to Nassau Candy Analytics Dashboard</h2>
        <p style='margin: 1rem 0; text-align: center; font-size: 1.1rem;'>
            Comprehensive profitability & margin analysis for strategic business decisions
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Dashboard Overview Sections
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    border-radius: 12px; padding: 1.5rem; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0;'>📊 Dashboard Overview</h3>
            <p style='margin: 1rem 0; line-height: 1.6;'>
                This interactive dashboard provides deep insights into your candy distribution business performance. 
                Monitor sales trends, profit margins, divisional performance, and identify at-risk products in real-time.
            </p>
            <ul style='margin-left: 1rem;'>
                <li>Real-time KPI monitoring</li>
                <li>Product-level profitability analysis</li>
                <li>Division performance tracking</li>
                <li>Risk identification system</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    border-radius: 12px; padding: 1.5rem; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0;'>🚀 Key Features</h3>
            <ul style='margin-left: 1rem; line-height: 1.8;'>
                <li><strong>Smart Filtering:</strong> Select divisions to focus analysis</li>
                <li><strong>Risk Threshold:</strong> Set custom margin thresholds (0-100%)</li>
                <li><strong>Dynamic Charts:</strong> Interactive visualizations update automatically</li>
                <li><strong>Data Tables:</strong> Export-ready detailed breakdowns</li>
                <li><strong>Pareto Analysis:</strong> Identify profit concentration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Business Insights Section
    st.markdown("<h3 style='color: #1e3a5f; text-align: center; margin-top: 2rem;'>💡 Quick Business Insights</h3>", unsafe_allow_html=True)

    # Check if filtered data is empty
    if filtered_df.empty:
        st.error("""
        ⚠️ **No data available!** 
        
        Please select at least one division from the sidebar to view insights. Follow these steps:
        1. Look at the left sidebar under "📍 Select Divisions"
        2. Check the boxes next to the divisions you want to analyze
        3. The dashboard will automatically update with your selection
        
        If no divisions appear in the list, please ensure the CSV file has been loaded correctly.
        """)
    else:
        insight_col1, insight_col2, insight_col3 = st.columns(3)

        # Insight 1: Best Performing Division
        try:
            best_div = filtered_df.groupby('Division')['Gross Profit'].sum().idxmax()
            best_div_profit = filtered_df.groupby('Division')['Gross Profit'].sum().max()
            
            with insight_col1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 12px; padding: 1.5rem; color: white; text-align: center;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                    <h4 style='margin-top: 0;'>🏆 Top Performing Division</h4>
                    <h2 style='margin: 0.5rem 0; font-size: 1.5rem;'>{best_div}</h2>
                    <p style='margin: 0; font-size: 1.1rem;'>${best_div_profit:,.0f} profit</p>
                </div>
                """, unsafe_allow_html=True)
        except:
            with insight_col1:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 12px; padding: 1.5rem; color: white; text-align: center;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                    <h4 style='margin-top: 0;'>🏆 Top Performing Division</h4>
                    <p style='margin: 0; font-size: 1rem;'>No data available</p>
                </div>
                """, unsafe_allow_html=True)

        # Insight 2: Profit Margin Health
        if avg_margin >= 20:
            margin_status = "Excellent"
            margin_color = "🟢"
        elif avg_margin >= 15:
            margin_status = "Good"
            margin_color = "🟡"
        else:
            margin_status = "At Risk"
            margin_color = "🔴"

        with insight_col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        border-radius: 12px; padding: 1.5rem; color: white; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                <h4 style='margin-top: 0;'>💪 Margin Health: {margin_color} {margin_status}</h4>
                <h2 style='margin: 0.5rem 0; font-size: 1.8rem;'>{avg_margin:.1f}%</h2>
                <p style='margin: 0; font-size: 0.9rem;'>Current overall margin</p>
            </div>
            """, unsafe_allow_html=True)

        # Insight 3: Risk Summary
        risk_count = len(filtered_df[filtered_df['Gross Margin %'] < margin_threshold]['Product Name'].unique())
        risk_severity = "Low" if risk_count <= 5 else "Medium" if risk_count <= 10 else "High"
        risk_icon = "🟢" if risk_count == 0 else "🟡" if risk_count <= 5 else "🔴"

        with insight_col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                        border-radius: 12px; padding: 1.5rem; color: white; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                <h4 style='margin-top: 0;'>⚠️ Risk Level: {risk_icon} {risk_severity}</h4>
                <h2 style='margin: 0.5rem 0; font-size: 1.8rem;'>{risk_count}</h2>
                <p style='margin: 0; font-size: 0.9rem;'>Products below {margin_threshold}% margin</p>
            </div>
            """, unsafe_allow_html=True)

    # How to Use Guide
    with st.expander("📖 How to Use This Dashboard", expanded=False):
        st.markdown("""
        ### 🎮 Dashboard Navigation Guide
        
        **Left Sidebar Controls:**
        - **📍 Select Divisions:** Filter analysis by specific divisions (multi-select available)
        - **⚖️ Margin Risk Threshold:** Set sensitivity level for identifying at-risk products (0-100%)
        - **Quick Stats:** View total records and active divisions at a glance
        
        **Navigation Pages:**
        
        1. **🏠 Home** - Dashboard overview with quick insights and KPIs
        2. **📊 Detailed Analysis** - In-depth analysis with 4 interactive tabs
        3. **📈 Reports** - Summary reports and export options
        
        ### 💡 Quick Tips
        - Adjust the margin threshold slider to see how many products are at risk
        - Use division filters to focus on specific areas
        - Hover over charts for detailed information
        - Navigate between pages using the sidebar menu
        """)

    # Performance Metrics Explanation
    with st.expander("📚 Understanding the Metrics", expanded=False):
        col_metric1, col_metric2 = st.columns(2)
        
        with col_metric1:
            st.markdown("""
            **💰 Total Sales**: Sum of all revenue from product orders
            
            **📊 Total Profit**: Gross profit across all filtered transactions
            
            **📈 Average Margin %**: Profit divided by sales, shown as percentage
            
            **📦 Total Units**: Total number of units sold across all products
            """)
        
        with col_metric2:
            st.markdown("""
            **🏆 Top Products**: Products generating highest gross profit
            
            **⚠️ Risk Products**: Items with margin below your threshold setting
            
            **📈 Market Share**: How concentrated profit is in top products
            
            **🎯 Profit Concentration**: % of total profit from top 20% of products
            """)

# ============================================================================
# PAGE 2: DETAILED ANALYSIS
# ============================================================================
elif page == "📊 Detailed Analysis":
    
    st.markdown("<h3 style='color: #1e3a5f; margin-top: 1rem;'>📈 Key Performance Indicators</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    # Sales KPI
    with col1:
        st.markdown(f"""
        <div class="kpi-card sales">
            <div class="kpi-label">💰 Total Sales</div>
            <div class="kpi-value">${total_sales:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Profit KPI
    with col2:
        st.markdown(f"""
        <div class="kpi-card profit">
            <div class="kpi-label">📊 Total Profit</div>
            <div class="kpi-value">${total_profit:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Margin KPI
    with col3:
        st.markdown(f"""
        <div class="kpi-card margin">
            <div class="kpi-label">📈 Avg Margin</div>
            <div class="kpi-value">{avg_margin:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Units KPI
    with col4:
        st.markdown(f"""
        <div class="kpi-card units">
            <div class="kpi-label">📦 Total Units</div>
            <div class="kpi-value">{total_units:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    # --- DASHBOARD TABS ---
    st.markdown("---")
    st.markdown("<h3 style='color: #1e3a5f;'>📊 Detailed Analysis</h3>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("""
        ⚠️ **No data to display!** 
        
        To view detailed analysis, please:
        1. Go to the sidebar on the left
        2. Under "📍 Select Divisions", check at least one division
        3. The detailed analysis will appear automatically
        """)
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏆 Product Profitability", 
            "🏢 Division Performance", 
            "⚠️ Margin Risk Diagnostics",
            "📈 Pareto Concentration"
        ])

        # TAB 1: Product Profitability
        with tab1:
            st.markdown("<h4 style='color: #1e3a5f;'>Top 10 Products by Profit</h4>", unsafe_allow_html=True)
            
            Product_Profitability = filtered_df.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False).head(10).reset_index()
            Product_Profitability['Rank'] = range(1, len(Product_Profitability) + 1)
            
            # Visual chart
            fig_prod = px.bar(Product_Profitability, x='Gross Profit', y='Product Name', orientation='h', 
                              title=None, color='Gross Profit', 
                              color_continuous_scale='Viridis',
                              labels={'Gross Profit': 'Profit ($)', 'Product Name': 'Product'})
            fig_prod.update_layout(showlegend=False, height=400, 
                                  plot_bgcolor='rgba(240,240,240,0.5)', 
                                  paper_bgcolor='rgba(255,255,255,0.9)',
                                  font=dict(size=11))
            st.plotly_chart(fig_prod, use_container_width=True)
            
            # Table view
            with st.expander("📋 View as Table", expanded=False):
                display_products = Product_Profitability[['Rank', 'Product Name', 'Gross Profit']].copy()
                display_products['Gross Profit'] = display_products['Gross Profit'].apply(lambda x: f"${x:,.2f}")
                st.dataframe(display_products, use_container_width=True, hide_index=True)

        # TAB 2: Division Performance
        with tab2:
            st.markdown("<h4 style='color: #1e3a5f;'>Division Revenue vs Profitability</h4>", unsafe_allow_html=True)
            
            div_perf = filtered_df.groupby('Division').agg({'Sales': 'sum', 'Gross Profit': 'sum'}).reset_index()
            div_perf['Margin %'] = (div_perf['Gross Profit'] / div_perf['Sales']) * 100
            
            # Scatter chart
            fig_div = px.scatter(div_perf, x="Sales", y="Gross Profit", size="Sales", 
                                color="Division", text="Division",
                                title=None,
                                labels={'Sales': 'Total Sales ($)', 'Gross Profit': 'Total Profit ($)'})
            fig_div.update_layout(height=400, 
                                 plot_bgcolor='rgba(240,240,240,0.5)',
                                 paper_bgcolor='rgba(255,255,255,0.9)',
                                 font=dict(size=11))
            st.plotly_chart(fig_div, use_container_width=True)
            
            # Performance Table
            st.markdown("<p style='font-weight: 600; color: #1e3a5f;'>Division Summary</p>", unsafe_allow_html=True)
            display_div = div_perf.copy()
            display_div['Sales'] = display_div['Sales'].apply(lambda x: f"${x:,.2f}")
            display_div['Gross Profit'] = display_div['Gross Profit'].apply(lambda x: f"${x:,.2f}")
            display_div['Margin %'] = display_div['Margin %'].apply(lambda x: f"{x:.2f}%")
            
            st.dataframe(display_div.rename(columns={'Sales': '💰 Total Sales', 
                                                     'Gross Profit': '📊 Total Profit',
                                                     'Margin %': '📈 Margin %',
                                                     'Division': '🏢 Division'}), 
                        use_container_width=True, hide_index=True)

    # TAB 3: Margin Risk Diagnostics
        with tab3:
            st.markdown("<h4 style='color: #1e3a5f;'>Cost vs Sales Scatter</h4>", unsafe_allow_html=True)
            
            risk_df = filtered_df[filtered_df['Gross Margin %'] < margin_threshold].copy()
            
            # Add risk flag column for visualization
            filtered_df_with_risk = filtered_df.copy()
            filtered_df_with_risk['Risk Level'] = filtered_df_with_risk['Gross Margin %'].apply(
                lambda x: '🔴 High Risk' if x < margin_threshold else '🟢 Safe'
            )
            
            # Risk chart
            fig_scatter = px.scatter(filtered_df_with_risk, x="Cost", y="Sales", color="Risk Level", 
                                    hover_data=['Product Name', 'Gross Margin %'], 
                                    title=None,
                                    color_discrete_map={'🔴 High Risk': '#FF6B6B', '🟢 Safe': '#51CF66'},
                                    labels={'Cost': 'Product Cost ($)', 'Sales': 'Sales Revenue ($)'})
            fig_scatter.update_layout(height=400,
                                     plot_bgcolor='rgba(240,240,240,0.5)',
                                     paper_bgcolor='rgba(255,255,255,0.9)',
                                     font=dict(size=11))
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Risk summary
            col_risk1, col_risk2 = st.columns(2)
            
            with col_risk1:
                if not risk_df.empty:
                    st.error(f"⚠️ **{len(risk_df['Product Name'].unique())} HIGH-RISK PRODUCTS** below {margin_threshold}% margin")
                    st.dataframe(risk_df[['Product Name', 'Division', 'Gross Margin %']].drop_duplicates()
                               .sort_values('Gross Margin %').reset_index(drop=True), use_container_width=True)
                else:
                    st.success(f"✅ **All products safe!** No products below {margin_threshold}% margin threshold")
            
            with col_risk2:
                risk_stats = filtered_df_with_risk['Risk Level'].value_counts()
                fig_risk_pie = px.pie(values=risk_stats.values, names=risk_stats.index, 
                                     title="Risk Distribution",
                                     color_discrete_map={'🔴 High Risk': '#FF6B6B', '🟢 Safe': '#51CF66'})
                fig_risk_pie.update_layout(font=dict(size=10))
                st.plotly_chart(fig_risk_pie, use_container_width=True)

        # TAB 4: Pareto Concentration
        with tab4:
            st.markdown("<h4 style='color: #1e3a5f;'>Pareto Analysis (Profit Concentration)</h4>", unsafe_allow_html=True)
            
            pareto_data = filtered_df.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False).reset_index()
            pareto_data['Cum_Profit_Pct'] = (pareto_data['Gross Profit'].cumsum() / pareto_data['Gross Profit'].sum()) * 100
            pareto_data['Rank'] = range(1, len(pareto_data) + 1)
            
            # Pareto chart
            fig_pareto = px.line(pareto_data, x='Rank', y='Cum_Profit_Pct', 
                                title=None,
                                labels={'Rank': 'Product Rank (Ordered by Profit)', 
                                       'Cum_Profit_Pct': 'Cumulative Profit %'},
                                markers=True)
            fig_pareto.add_hline(y=80, line_dash="dash", line_color="red", 
                                annotation_text="80% Threshold", annotation_position="right")
            fig_pareto.update_layout(height=400,
                                    plot_bgcolor='rgba(240,240,240,0.5)',
                                    paper_bgcolor='rgba(255,255,255,0.9)',
                                    font=dict(size=11))
            st.plotly_chart(fig_pareto, use_container_width=True)
            
            # Dependency Insight
            top_20_count = int(len(pareto_data) * 0.2)
            profit_from_top_20 = pareto_data.iloc[:top_20_count]['Gross Profit'].sum() / pareto_data['Gross Profit'].sum() * 100
            
            col_pareto1, col_pareto2 = st.columns(2)
            
            with col_pareto1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                    <h4 style='margin: 0;'>🎯 Profit Concentration</h4>
                    <h2 style='margin: 0.5rem 0;'>{profit_from_top_20:.1f}%</h2>
                    <p style='margin: 0;'>of profit from top 20% of products</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_pareto2:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            color: white; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                    <h4 style='margin: 0;'>📊 Total Products</h4>
                    <h2 style='margin: 0.5rem 0;'>{len(pareto_data)}</h2>
                    <p style='margin: 0;'>unique products analyzed</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# PAGE 2.5: FACTORY ANALYSIS
# ============================================================================
elif page == "🗺️ Factory Analysis":
    st.markdown("<h3 style='color: #1e3a5f;'>🗺️ Factory Operational Intelligence</h3>", unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.warning("""
        ⚠️ **No data to display!** 
        
        To view factory analysis, please:
        1. Go to the sidebar on the left
        2. Under "📍 Select Divisions", check at least one division
        3. The factory analysis will appear automatically
        """)
    else:
        # Calculate profit per factory
        factory_profit = filtered_df.groupby('Division')['Gross Profit'].sum().reset_index()
        map_df = df_factories.merge(factory_profit, on='Division', how='left')
        
        # Display Map
        st.markdown("#### 📍 Factory Locations & Profit Distribution")
        st.map(map_df)
        
        # Display Factory Leaderboard
        st.markdown("#### 🏭 Factory Margin Performance")
        st.markdown("---")
        
        leaderboard = map_df[['Factory', 'Division', 'Gross Profit']].sort_values(by='Gross Profit', ascending=False).reset_index(drop=True)
        leaderboard['Rank'] = range(1, len(leaderboard) + 1)
        
        # Format display
        display_leaderboard = leaderboard[['Rank', 'Factory', 'Division', 'Gross Profit']].copy()
        display_leaderboard['Gross Profit'] = display_leaderboard['Gross Profit'].fillna(0).apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(display_leaderboard, use_container_width=True, hide_index=True)
        
        # Factory Statistics
        st.markdown("#### 📊 Factory Statistics")
        col_fact1, col_fact2, col_fact3 = st.columns(3)
        
        with col_fact1:
            st.metric("🏭 Total Factories", len(df_factories))
        
        with col_fact2:
            st.metric("📍 Active Divisions", len(map_df[map_df['Gross Profit'].notna()]))
        
        with col_fact3:
            total_factory_profit = map_df['Gross Profit'].sum()
            st.metric("💰 Total Factory Profit", f"${total_factory_profit:,.2f}")

# ============================================================================
# PAGE 3: REPORTS
# ============================================================================
elif page == "📈 Reports":
    st.markdown("<h3 style='color: #1e3a5f;'>📊 Summary Reports</h3>", unsafe_allow_html=True)
    
    st.info("📄 This section contains summary reports and export options")
    
    # Executive Summary
    st.markdown("<h4 style='color: #1e3a5f;'>Executive Summary</h4>", unsafe_allow_html=True)
    
    exec_col1, exec_col2 = st.columns(2)
    
    # Calculate contribution metrics
    total_org_sales = df['Sales'].sum()
    total_org_profit = df['Gross Profit'].sum()
    
    revenue_contrib = (total_sales / total_org_sales) * 100 if total_org_sales > 0 else 0
    profit_contrib = (total_profit / total_org_profit) * 100 if total_org_profit > 0 else 0
    
    with exec_col1:
        st.markdown(f"""
        #### Key Metrics Summary
        - **Total Sales**: ${total_sales:,.2f}
        - **Total Profit**: ${total_profit:,.2f}
        - **Average Margin**: {avg_margin:.2f}%
        - **Total Units Sold**: {total_units:,}
        - **Active Divisions**: {len(selected_divisions)}
        - **Risk Threshold**: {margin_threshold}%
        
        #### Organizational Contribution
        - **Revenue Contribution**: {revenue_contrib:.2f}% of total organization
        - **Profit Contribution**: {profit_contrib:.2f}% of total organization
        """)
    
    with exec_col2:
        # Best/Worst Product
        try:
            if not filtered_df.empty and len(filtered_df.groupby('Product Name')['Gross Profit'].sum()) > 0:
                best_product = filtered_df.groupby('Product Name')['Gross Profit'].sum().idxmax()
                worst_product = filtered_df.groupby('Product Name')['Gross Profit'].sum().idxmin()
            else:
                best_product = "N/A"
                worst_product = "N/A"
        except:
            best_product = "N/A"
            worst_product = "N/A"
        
        st.markdown(f"""
        #### Product Performance
        - **Best Performing**: {best_product}
        - **Lowest Performing**: {worst_product}
        - **Total Unique Products**: {filtered_df['Product Name'].nunique()}
        - **At-Risk Products**: {len(filtered_df[filtered_df['Gross Margin %'] < margin_threshold]['Product Name'].unique())}
        """)
    
    # Export Section
    st.markdown("---")
    st.markdown("<h4 style='color: #1e3a5f;'>Data Export</h4>", unsafe_allow_html=True)
    
    # Download buttons
    col_export1, col_export2, col_export3 = st.columns(3)
    
    with col_export1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Data (CSV)",
            data=csv,
            file_name="nassau_candy_data.csv",
            mime="text/csv"
        )
    
    with col_export2:
        # Product summary
        prod_summary = filtered_df.groupby('Product Name').agg({
            'Sales': 'sum',
            'Gross Profit': 'sum',
            'Units': 'sum',
            'Gross Margin %': 'mean'
        }).reset_index().sort_values('Gross Profit', ascending=False)
        csv_prod = prod_summary.to_csv(index=False)
        st.download_button(
            label="📥 Download Product Report (CSV)",
            data=csv_prod,
            file_name="product_summary.csv",
            mime="text/csv"
        )
    
    with col_export3:
        # Division summary
        div_summary = filtered_df.groupby('Division').agg({
            'Sales': 'sum',
            'Gross Profit': 'sum',
            'Units': 'sum'
        }).reset_index()
        div_summary['Margin %'] = (div_summary['Gross Profit'] / div_summary['Sales']) * 100
        csv_div = div_summary.to_csv(index=False)
        st.download_button(
            label="📥 Download Division Report (CSV)",
            data=csv_div,
            file_name="division_summary.csv",
            mime="text/csv"
        )
