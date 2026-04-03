import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. ENTERPRISE CONFIGURATION
st.set_page_config(
    page_title="Romina Export Command", 
    page_icon="☕", 
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 20px;
        border-radius: 10px;
    }
    .stDataFrame { background-color: #161B22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. FAILSAFE DATA LOADING
@st.cache_data
def load_audit_data():
    # Looking for the file generated in Phase 3
    path = 'romina_final_audit_v2.csv'
    if not os.path.exists(path):
        return None
    data = pd.read_csv(path)
    data['Inspection_Date'] = pd.to_datetime(data['Inspection_Date'])
    return data

df = load_audit_data()

# Global Crash Protection
if df is None:
    st.error("CRITICAL ERROR: Database Not Found")
    st.info("Please ensure 'romina_final_audit_v2.csv'.")
    st.stop()

# 3. SIDEBAR: OFFICER CONTROLS
st.sidebar.title("Export Controls")
st.sidebar.markdown("---")
selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
selected_stations = st.sidebar.multiselect("Focus Stations", options=df['Station'].unique(), default=df['Station'].unique())

# Apply Filter Logic
mask = (df['Region'].isin(selected_region)) & (df['Station'].isin(selected_stations))
f_df = df[mask]

# 4. HEADER & STRATEGIC KPIs
st.title("☕ Revenue Maximizer")
st.subheader("Senior Officer Intelligence Dashboard")

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.metric("Total Portfolio Gross", f"${f_df['Gross_Revenue_USD'].sum()/1e6:.1f}M")
with m2:
    shrinkage = f_df['Shrinkage_Loss_USD'].sum()
    st.metric("Shrinkage Loss", f"${shrinkage/1e6:.2f}M", delta="-1.5% Weight", delta_color="inverse")
with m3:
    trapped = f_df[f_df['Status'] == 'Rejected']['Retained_Forex_USD'].sum()
    st.metric("Trapped FOREX", f"${trapped/1e6:.2f}M", delta="ECTA Rejection", delta_color="inverse")
with m4:
    gain = f_df['Premium_Gain_USD'].sum()
    st.metric("EUDR Strategy Gain", f"${gain/1e6:.2f}M", delta="+22% Target")
with m5:
    compliance = (f_df['EUDR_Verified'].mean()) * 100
    st.metric("Compliance Rate", f"{compliance:.1f}%")

st.divider()

# 5. VISUAL INTELLIGENCE
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Revenue Velocity vs. Market Timing")
    trend = f_df.groupby('Inspection_Date')['Gross_Revenue_USD'].sum().reset_index()
    fig_trend = px.area(trend, x='Inspection_Date', y='Gross_Revenue_USD', 
                        template="plotly_dark", color_discrete_sequence=['#00D4FF'])
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.markdown("### Station Premium Leaderboard")
    leaderboard = f_df.groupby('Station')['Premium_Gain_USD'].sum().sort_values().reset_index()
    fig_bar = px.bar(leaderboard, x='Premium_Gain_USD', y='Station', orientation='h', 
                     template="plotly_dark", color='Premium_Gain_USD', color_continuous_scale='RdYlGn')
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. ACTIONABLE AUDIT TABLE
st.markdown("### Priority Action: Rejected Lots ($15.7M Gross Blocked)")
rejections = f_df[f_df['Status'] == 'Rejected'][['Lot_ID', 'Station', 'Defect_Type', 'Quantity_MT', 'Retained_Forex_USD']]
st.dataframe(rejections.sort_values(by='Retained_Forex_USD', ascending=False), use_container_width=True, hide_index=True)

# 7. PROFESSIONAL SIGNATURE & FOOTER
st.divider() 

st.caption("**© 2026 Romina PLC Digital Transformation Initiative**")
st.caption("**Developed by **Aklilu Abera** | Import/Export Officer | Supply Chain Data Analyst**")

st.sidebar.markdown("---")
if st.sidebar.button("📤 Generate Senior Briefing"):
    st.sidebar.success("Briefing compiled. Focus: Belete Tanga Re-inspection & Germany Export Priority.")
