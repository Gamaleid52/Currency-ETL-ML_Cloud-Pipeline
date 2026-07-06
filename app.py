
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
import urllib.parse
import time

# Set Page Config
st.set_page_config(page_title="Enterprise Big Data & ML Dashboard", page_icon="📈", layout="wide")

# Database Connection Settings
SERVER = "."
DATABASE = "FinancialDB"
#connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"


# Set Page Config
st.set_page_config(page_title="Enterprise Big Data & ML Dashboard", page_icon="📈", layout="wide")

# ==========================================
# 🛠️ DATABASE CONNECTION SETTINGS (CLOUD)
# ==========================================
# ⚠️ ضع الباسورد الحقيقية لـ Supabase هنا
raw_password = "theblueskyG@123"
encoded_password = urllib.parse.quote_plus(raw_password)
connection_string = f"postgresql+psycopg2://postgres:{encoded_password}@db.wzxaotzomwlkrudvmpwy.supabase.co:5432/postgres"

@st.cache_data(ttl=60)  # كاش لمدة دقيقة عشان أداء السحاب يكون سريع
def load_data():
    engine = create_engine(connection_string)
    
    # 1. سحب البيانات التاريخية الحقيقية (آخر سنتين مع مراعاة الحروف الكبيرة والرموز لـ Postgres)
    hist_query = """
    SELECT "Date", "CurrencyCode", "ExchangeRate" 
    FROM "Fact_HistoricalExchangeRates" 
    WHERE "Date" >= NOW() - INTERVAL '2 years'
    """
    df_hist = pd.read_sql(hist_query, engine)
    df_hist['Type'] = 'Actual (Historical)'
    
    # 2. سحب بيانات التوقعات من الموديل
    pred_query = """
    SELECT "Date", "CurrencyCode", "PredictedRate" AS "ExchangeRate" 
    FROM "Fact_Predictions"
    """
    df_pred = pd.read_sql(pred_query, engine)
    df_pred['Type'] = 'Machine Learning Forecast'
    
    return df_hist, df_pred

try:
    df_hist, df_pred = load_data()
    
    # Header Section
    st.title("📈 Enterprise Cloud Big Data & ML Currency Dashboard")
    current_time = time.strftime("%H:%M:%S")
    st.markdown(f"📊 **Data Source:** Supabase Cloud (PostgreSQL) | 🧠 **ML Model:** Prophet Forecast | 🔄 **Live Time:** {current_time}")
    st.divider()

    # Sidebar Filters
    st.sidebar.header("🎯 Filter Settings")
    available_currencies = list(df_pred['CurrencyCode'].unique())
    selected_currency = st.sidebar.selectbox("Select Currency to View Forecast:", available_currencies, index=0)

    # Filter Data based on selection
    currency_hist = df_hist[df_hist['CurrencyCode'] == selected_currency].sort_values('Date')
    currency_pred = df_pred[df_pred['CurrencyCode'] == selected_currency].sort_values('Date')

    # Metric Cards (Latest Actual vs Next Predicted)
    latest_actual = currency_hist['ExchangeRate'].iloc[-1] if not currency_hist.empty else 0
    next_predicted = currency_pred['ExchangeRate'].iloc[0] if not currency_pred.empty else 0
    change = next_predicted - latest_actual

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"Current {selected_currency} Rate (per 1 USD)", value=f"{latest_actual:.4f}")
    with col2:
        st.metric(label=f"Predicted {selected_currency} Rate (Tomorrow)", value=f"{next_predicted:.4f}", delta=f"{change:.4f}")
    with col3:
        st.metric(label="Forecast Horizon", value="Next 30 Days")

    st.divider()

    # 📈 Interactive Time Series Chart (Plotly)
    st.subheader(f"🔮 {selected_currency} Actual Trends vs Machine Learning Predictions")
    
    fig = go.Figure()
    
    # خط البيانات التاريخية
    fig.add_trace(go.Scatter(x=currency_hist['Date'], y=currency_hist['ExchangeRate'],
                             mode='lines', name='Actual Rate', line=dict(color='#1f77b4', width=2)))
    
    # خط التوقعات المستقبلي
    fig.add_trace(go.Scatter(x=currency_pred['Date'], y=currency_pred['ExchangeRate'],
                             mode='lines', name='ML Forecast (30 Days)', line=dict(color='#ff7f0e', width=3, dash='dash')))

    fig.update_layout(template="plotly_white", hovermode="x unified",
                      xaxis_title="Date", yaxis_title=f"Rate vs 1 USD",
                      margin=dict(l=20, r=20, t=20, b=20), height=500)
    
    st.plotly_chart(fig, use_container_width=True)

    # Layout for Raw Data Tables
    st.divider()
    left_table, right_table = st.columns(2)
    
    with left_table:
        st.subheader("📋 Recent Historical Data (Top 5)")
        st.dataframe(currency_hist.tail(5)[['Date', 'ExchangeRate']], use_container_width=True, hide_index=True)
        
    with right_table:
        st.subheader("🔮 Upcoming ML Predictions (Top 5)")
        st.dataframe(currency_pred.head(5)[['Date', 'ExchangeRate']], use_container_width=True, hide_index=True)

    # Auto rerun every 60 seconds to keep dashboard fresh
    time.sleep(60)
    st.rerun()

except Exception as e:
    st.error(f"❌ Error rendering dashboard: {e}")