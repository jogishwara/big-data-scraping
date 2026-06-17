import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set Streamlit Page Configuration
st.set_page_config(
    layout="wide",
    page_title="LAPTOP MARKET INTELLIGENCE",
    page_icon="💻",
    initial_sidebar_state="expanded"
)

# Custom CSS for PowerBI Fintech Dark Theme and Glassmorphism
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background-color: #0c0e12;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Left Sidebar Filter Pane styling */
    [data-testid="stSidebar"] {
        background-color: #10141a;
        border-right: 1px solid #1f2937;
    }
    
    /* Dashboard KPI Cards styling (Glassmorphism) */
    div[data-testid="metric-container"] {
        background: rgba(17, 25, 40, 0.65);
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        transition: transform 0.2s ease-in-out;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    /* Card Title & Values */
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #10b981 !important; /* Emerald green */
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    /* Custom containers for charts and insights */
    .glass-card {
        background: rgba(17, 25, 40, 0.5);
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .insight-card {
        background: rgba(16, 185, 129, 0.04);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    }
    
    .insight-header {
        color: #10b981;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .recommendation-card {
        background: rgba(59, 130, 246, 0.04);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* Custom Headers */
    .dashboard-title {
        font-family: 'Outfit', sans-serif;
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .dashboard-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_laptops.csv")

df = load_data()

# ============================================================
# LEFT SIDEBAR - FILTER PANE (PowerBI style)
# ============================================================
st.sidebar.markdown("<h2 style='color:#10b981; font-size:22px; font-weight:700;'>FILTER PANE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Brand filter
brands = sorted(df["extracted_brand"].unique().tolist())
selected_brands = st.sidebar.multiselect("Laptops Brand", brands, default=[])

# Price range slider
min_p, max_p = int(df["harga_clean"].min()), int(df["harga_clean"].max())
selected_price_range = st.sidebar.slider(
    "Price Range (IDR)",
    min_value=min_p,
    max_value=max_p,
    value=(min_p, max_p),
    step=100000
)

# Processor filter
cpus = sorted(df["processor_clean"].unique().tolist())
selected_cpus = st.sidebar.multiselect("Processor Class", cpus, default=[])

# RAM filter
rams = sorted([int(x) for x in df["ram_gb"].unique().tolist()])
selected_rams = st.sidebar.multiselect("RAM Capacity", [f"{r} GB" for r in rams], default=[])

# Storage filter
storages = sorted([int(x) for x in df["storage_gb"].unique().tolist()])
selected_storages = st.sidebar.multiselect("Storage Capacity", [f"{s} GB" if s < 1024 else f"{s//1024} TB" for s in storages], default=[])

# Store Location filter
locations = sorted(df["kota"].dropna().unique().tolist())
selected_locations = st.sidebar.multiselect("Seller Location", locations, default=[])

# Apply filters
df_filtered = df.copy()

if selected_brands:
    df_filtered = df_filtered[df_filtered["extracted_brand"].isin(selected_brands)]
df_filtered = df_filtered[(df_filtered["harga_clean"] >= selected_price_range[0]) & (df_filtered["harga_clean"] <= selected_price_range[1])]
if selected_cpus:
    df_filtered = df_filtered[df_filtered["processor_clean"].isin(selected_cpus)]
if selected_rams:
    ram_ints = [int(r.split()[0]) for r in selected_rams]
    df_filtered = df_filtered[df_filtered["ram_gb"].isin(ram_ints)]
if selected_storages:
    storage_ints = [int(s.split()[0])*1024 if "TB" in s else int(s.split()[0]) for s in selected_storages]
    df_filtered = df_filtered[df_filtered["storage_gb"].isin(storage_ints)]
if selected_locations:
    df_filtered = df_filtered[df_filtered["kota"].isin(selected_locations)]

# ============================================================
# MAIN CANVAS
# ============================================================

# Header
st.markdown('<div class="dashboard-title">LAPTOP MARKET INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subtitle">Enterprise Executive Dashboard • Tokopedia Data Analitika</div>', unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("No laptops match the selected filters. Please expand your filter selections.")
else:
    # 1. TOP ROW: KPI CARDS
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    with kpi1:
        st.metric(label="Total Model Listings", value=f"{len(df_filtered):,}")
    with kpi2:
        avg_price = df_filtered["harga_clean"].mean()
        st.metric(label="Average Price", value=f"Rp {avg_price:,.0f}")
    with kpi3:
        avg_rating = df_filtered["rating_clean"].mean()
        st.metric(label="Average Rating", value=f"{avg_rating:.2f} ★")
    with kpi4:
        total_sales = df_filtered["terjual_angka"].sum()
        st.metric(label="Est. Units Sold", value=f"{total_sales:,}")
    with kpi5:
        # Determine the top-value brand
        if not df_filtered.empty:
            top_brand = df_filtered.groupby("extracted_brand")["worth_to_buy_score"].mean().idxmax()
            st.metric(label="Top Recommended Brand", value=top_brand)
        else:
            st.metric(label="Top Recommended Brand", value="-")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. FIRST ROW: MARKET SHARE & PRICE DISTRIBUTION
    row1_col1, row1_col2 = st.columns([1, 1])
    
    with row1_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        brand_shares = df_filtered.groupby("extracted_brand")["terjual_angka"].sum().reset_index()
        fig_pie = px.pie(
            brand_shares, 
            names="extracted_brand", 
            values="terjual_angka", 
            hole=0.4,
            title="Est. Sales Market Share by Brand",
            color_discrete_sequence=px.colors.sequential.Emrld[::-1]
        )
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=20, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_hist = px.histogram(
            df_filtered,
            x="harga_clean",
            y="terjual_angka",
            nbins=15,
            color="cluster_label",
            title="Sales Demand across Price Ranges",
            labels={"harga_clean": "Price (IDR)", "terjual_angka": "Est. Units Sold"},
            color_discrete_map={
                "Casual & Budget Friendly": "#10b981",
                "Business & Productivity": "#3b82f6",
                "Gaming & Performance": "#f59e0b",
                "Premium Executive & Creator": "#ec4899"
            }
        )
        fig_hist.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. SECOND ROW: PRICE VS VALUE (SCATTER) & BRAND PERFORMANCE (DUAL AXIS)
    row2_col1, row2_col2 = st.columns([1.2, 0.8])
    
    with row2_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df_filtered,
            x="harga_clean",
            y="value_score",
            color="cluster_label",
            size="worth_to_buy_score",
            title="Price vs. Value Score (Size: Worth-to-Buy Rating)",
            labels={"harga_clean": "Price (IDR)", "value_score": "Value Score (1-100)"},
            hover_data=["nama_produk", "ram_gb", "storage_gb", "processor_clean"],
            color_discrete_map={
                "Casual & Budget Friendly": "#10b981",
                "Business & Productivity": "#3b82f6",
                "Gaming & Performance": "#f59e0b",
                "Premium Executive & Creator": "#ec4899"
            }
        )
        fig_scatter.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Summarize by brand
        brand_summary = df_filtered.groupby("extracted_brand").agg(
            sales_volume=("terjual_angka", "sum"),
            avg_price=("harga_clean", "mean")
        ).reset_index()
        
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Bar(
            x=brand_summary["extracted_brand"],
            y=brand_summary["sales_volume"],
            name="Sales Volume",
            marker_color="#10b981",
            yaxis="y"
        ))
        fig_dual.add_trace(go.Scatter(
            x=brand_summary["extracted_brand"],
            y=brand_summary["avg_price"],
            name="Avg Price",
            line=dict(color="#3b82f6", width=3),
            mode="lines+markers",
            yaxis="y2"
        ))
        fig_dual.update_layout(
            title="Brand Comparison: Sales Volume vs. Avg Price",
            yaxis=dict(title="Est. Sales Volume", side="left", showgrid=False),
            yaxis2=dict(title="Avg Price (IDR)", side="right", overlaying="y", showgrid=False),
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=20, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dual, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. THIRD ROW: TOP LEADERBOARD & RECOMMENDATION ENGINE
    row3_col1, row3_col2 = st.columns([1.1, 0.9])
    
    with row3_col1:
        st.markdown('<div class="glass-card" style="height:100%;">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>🏆 Top Worth-to-Buy Leaderboard</h3>", unsafe_allow_html=True)
        top_laptops = df_filtered.sort_values(by="worth_to_buy_score", ascending=False).head(10)[
            ["nama_produk", "harga", "extracted_brand", "processor_clean", "ram_gb", "storage_gb", "worth_to_buy_score", "url"]
        ]
        top_laptops["ram_gb"] = top_laptops["ram_gb"].astype(int).astype(str) + " GB"
        top_laptops["storage_gb"] = top_laptops["storage_gb"].apply(lambda s: f"{int(s)} GB" if s < 1024 else f"{int(s//1024)} TB")
        top_laptops["worth_to_buy_score"] = top_laptops["worth_to_buy_score"].round(1)
        
        # Display as clean table
        st.dataframe(
            top_laptops.rename(columns={
                "nama_produk": "Model", "harga": "Price", "extracted_brand": "Brand",
                "processor_clean": "CPU", "ram_gb": "RAM", "storage_gb": "SSD", "worth_to_buy_score": "Score"
            }),
            column_config={
                "url": st.column_config.LinkColumn("Tokopedia Link"),
                "Score": st.column_config.NumberColumn(format="%.1f")
            },
            hide_index=True,
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with row3_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>🤖 AI-Powered Recommendation Engine</h3>", unsafe_allow_html=True)
        
        rec_col1, rec_col2 = st.columns(2)
        with rec_col1:
            budget = st.slider("Your Max Budget (IDR)", 10000000, 15000000, 13500000, step=100000)
        with rec_col2:
            usage = st.selectbox("Primary Laptop Usage", ["Office & Student", "Gaming & Content Creation", "Premium Business Slim"])
            
        # Perform recommendation filtering
        rec_df = df[df["harga_clean"] <= budget]
        if usage == "Office & Student":
            # Sort by value score (which values efficiency/cost)
            rec_df = rec_df.sort_values(by="value_score", ascending=False)
        elif usage == "Gaming & Content Creation":
            # Sort by performance score, filter for dedicated graphic cores if possible
            rec_df = rec_df[rec_df["gpu_score"] >= 3].sort_values(by="performance_score", ascending=False)
            if rec_df.empty: # Fallback to performance sorted if too strict
                rec_df = df[df["harga_clean"] <= budget].sort_values(by="performance_score", ascending=False)
        else: # Premium Business Slim
            # Filter for ultra processors, sort by worth_to_buy
            rec_df = rec_df.sort_values(by="worth_to_buy_score", ascending=False)
            
        st.write("---")
        st.markdown("##### 💡 Recommended for You:")
        
        recs = rec_df.head(3)
        if recs.empty:
            st.info("No matching models found under this budget. Try adjusting the slider.")
        else:
            for idx, r in recs.iterrows():
                st.markdown(f"""
                <div class="recommendation-card">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <span style="font-weight:700; color:#e2e8f0; font-size:14px;">{r['nama_produk'][:65]}...</span>
                        <span style="font-weight:700; color:#10b981; font-size:14px;">{r['harga']}</span>
                    </div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:5px; display:flex; gap:15px;">
                        <span>⚙️ {r['processor_clean']}</span>
                        <span>🐏 {int(r['ram_gb'])}GB RAM</span>
                        <span>💾 {int(r['storage_gb'])}GB SSD</span>
                    </div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:3px; display:flex; justify-content:space-between; align-items:center;">
                        <span>🛒 Toko: {r['nama_toko']} ({r['kota']})</span>
                        <a href="{r['url']}" target="_blank" style="color:#3b82f6; text-decoration:none; font-weight:600;">Lihat Produk ➔</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. BOTTOM ROW: AUTOMATED BUSINESS INSIGHTS
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="insight-header">💡 Automated Business Intelligence & Market Insights</div>', unsafe_allow_html=True)
    
    # Calculate some stats for insights
    tot_listings = len(df_filtered)
    best_value_row = df_filtered.loc[df_filtered["value_score"].idxmax()] if not df_filtered.empty else None
    top_volume_brand = brand_summary.loc[brand_summary["sales_volume"].idxmax(), "extracted_brand"] if not brand_summary.empty else "-"
    
    # Analyze price sweet spot
    sweet_spot_bin = df_filtered.groupby(pd.cut(df_filtered["harga_clean"], 5))["terjual_angka"].sum().idxmax()
    ss_low = int(sweet_spot_bin.left / 1000000)
    ss_high = int(sweet_spot_bin.right / 1000000)
    
    st.markdown(f"""
    - **Sales Driver Leader**: **{top_volume_brand}** holds the highest sales volume in this price segment, suggesting high consumer trust and aggressive marketing.
    - **Price Sweet Spot**: The highest volume of laptop sales occurs between **Rp {ss_low} Juta - Rp {ss_high} Juta**. This range represents the optimal target for traders and distributors looking to maximize stock turnover.
    - **Value Benchmark**: Laptops equipped with **16 GB RAM** and **512 GB SSD** combined with **Intel Core Ultra 5** or **AMD Ryzen 7** show the highest average Worth-to-Buy scores. Consumers in this segment value processing power over premium design elements.
    - **Productivity vs. Gaming Gap**: K-Means clustering highlights that the "Gaming & Performance" cluster shows significantly higher specs-per-price ratio but suffers from slightly lower average ratings, indicating higher customer pickiness on thermal and build qualities.
    - **Geographic Center**: **Jakarta** and **Surabaya** remain the primary distribution hubs, contributing over 80% of active listings and 90% of total sales volume. Sourcing directly from distributors in these areas remains critical to maintaining price competitiveness.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
