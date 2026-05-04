import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title='Car Market Analyzer',
    page_icon='🚗',
    layout='wide'
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0d0f1a;
        color: #e8eaf0;
    }
    .stApp { background: linear-gradient(135deg, #0d0f1a 0%, #111827 100%); }
    h1, h2, h3 { font-family: 'Space Mono', monospace !important; }

    .hero { text-align: center; padding: 36px 20px 10px; }
    .hero h1 {
        font-size: 2.4rem;
        background: linear-gradient(90deg, #f59e0b, #ef4444, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .hero p { color: #9ca3af; font-size: 1rem; max-width: 620px; margin: 0 auto; line-height: 1.7; }

    .metric-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
    }
    .metric-label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; font-family: 'Space Mono', monospace; }
    .metric-value { font-size: 28px; font-weight: 700; font-family: 'Space Mono', monospace; color: #f0f4ff; }
    .metric-value.amber { color: #fbbf24; }
    .metric-value.red   { color: #f87171; }
    .metric-value.indigo{ color: #818cf8; }
    .metric-value.green { color: #34d399; }

    .section-title {
        font-family: 'Space Mono', monospace;
        font-size: 1rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 28px 0 12px;
        border-left: 3px solid #f59e0b;
        padding-left: 12px;
    }
    .info-box {
        background: rgba(245,158,11,0.07);
        border-left: 3px solid #f59e0b;
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        color: #fde68a;
        font-size: 0.88rem;
        line-height: 1.7;
        margin-bottom: 16px;
    }
    hr { border-color: rgba(255,255,255,0.06); }
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load & clean data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('vehicles_us.csv')
    df['model_year'] = df['model_year'].fillna(df['model_year'].median()).astype(int)
    df['odometer']   = df['odometer'].fillna(df['odometer'].median())
    df['cylinders']  = df['cylinders'].fillna(df['cylinders'].median())
    df['paint_color']= df['paint_color'].fillna('unknown')
    df['is_4wd']     = df['is_4wd'].fillna(0).astype(int)
    df['brand']      = df['model'].str.split().str[0].str.capitalize()
    df = df[df['price'].between(500, 150000)]
    df = df[df['odometer'] < 400000]
    return df

car_data = load_data()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🚗 Car Market Analyzer</h1>
    <p>Explore 51,000+ U.S. vehicle listings. Understand pricing patterns, mileage trends,
    and market dynamics — all in one interactive dashboard.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.markdown("## 🔧 Filters")

brands = sorted(car_data['brand'].unique())
selected_brands = st.sidebar.multiselect("Brand", brands, default=[], placeholder="All brands")

conditions = sorted(car_data['condition'].unique())
selected_conditions = st.sidebar.multiselect("Condition", conditions, default=[], placeholder="All conditions")

fuel_types = sorted(car_data['fuel'].unique())
selected_fuels = st.sidebar.multiselect("Fuel Type", fuel_types, default=[], placeholder="All fuel types")

price_min, price_max = st.sidebar.slider(
    "Price Range ($)", int(car_data['price'].min()), int(car_data['price'].max()), (1000, 50000), step=500
)
year_min, year_max = st.sidebar.slider(
    "Model Year", int(car_data['model_year'].min()), int(car_data['model_year'].max()), (2010, 2019)
)

# Apply filters
filtered = car_data[car_data['price'].between(price_min, price_max) & car_data['model_year'].between(year_min, year_max)]
if selected_brands:     filtered = filtered[filtered['brand'].isin(selected_brands)]
if selected_conditions: filtered = filtered[filtered['condition'].isin(selected_conditions)]
if selected_fuels:      filtered = filtered[filtered['fuel'].isin(selected_fuels)]

st.sidebar.markdown(f"**{len(filtered):,}** vehicles match your filters")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Vehicles Found</div><div class="metric-value indigo">{len(filtered):,}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Median Price</div><div class="metric-value amber">${filtered["price"].median():,.0f}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Avg Odometer</div><div class="metric-value red">{filtered["odometer"].mean():,.0f} mi</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Avg Days Listed</div><div class="metric-value green">{filtered["days_listed"].mean():.0f} days</div></div>', unsafe_allow_html=True)

st.markdown("---")

PLOT_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#9ca3af'),
    xaxis=dict(gridcolor='rgba(255,255,255,0.04)', zerolinecolor='rgba(255,255,255,0.08)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.04)', zerolinecolor='rgba(255,255,255,0.08)'),
    margin=dict(l=10, r=10, t=30, b=10), height=360,
)

# ── Row 1 ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Price & Mileage Distribution</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(filtered, x="price", nbins=60, title="Price Distribution", color_discrete_sequence=["#f59e0b"])
    fig.update_layout(**PLOT_THEME)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(filtered, x="odometer", nbins=60, title="Odometer Distribution", color_discrete_sequence=["#818cf8"])
    fig.update_layout(**PLOT_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2 ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Price Relationships</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    fig = px.scatter(
        filtered.sample(min(3000, len(filtered))), x="odometer", y="price",
        color="condition", title="Price vs Odometer by Condition",
        opacity=0.6, color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_layout(**PLOT_THEME)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.box(
        filtered, x="condition", y="price", title="Price by Condition",
        color="condition", color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_layout(**PLOT_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3 ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Market Insights</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    top_brands = filtered.groupby('brand')['price'].median().sort_values(ascending=False).head(15).reset_index()
    fig = px.bar(
        top_brands, x="price", y="brand", orientation='h',
        title="Median Price by Brand (Top 15)", color="price",
        color_continuous_scale=["#818cf8", "#f59e0b", "#ef4444"]
    )
    fig.update_layout(**PLOT_THEME, height=420)
    st.plotly_chart(fig, use_container_width=True)

with col6:
    fuel_counts = filtered['fuel'].value_counts().reset_index()
    fuel_counts.columns = ['fuel', 'count']
    fig = px.pie(
        fuel_counts, names='fuel', values='count', title="Listings by Fuel Type",
        color_discrete_sequence=px.colors.qualitative.Vivid, hole=0.45
    )
    fig.update_layout(**PLOT_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ── Price trend by year ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Price Trend by Model Year</div>', unsafe_allow_html=True)
price_by_year = filtered.groupby('model_year')['price'].median().reset_index().sort_values('model_year')
fig = px.area(price_by_year, x='model_year', y='price', title="Median Price by Model Year", color_discrete_sequence=["#f59e0b"])
fig.update_traces(fill='tozeroy', fillcolor='rgba(245,158,11,0.12)')
fig.update_layout(**PLOT_THEME, height=300)
st.plotly_chart(fig, use_container_width=True)

# ── Raw data ──────────────────────────────────────────────────────────────────
st.markdown("---")
if st.checkbox("📋 Show raw data sample"):
    st.markdown('<div class="info-box">Showing a random sample of 100 records from your filtered selection.</div>', unsafe_allow_html=True)
    st.dataframe(filtered.sample(min(100, len(filtered))).reset_index(drop=True), use_container_width=True, hide_index=True)
