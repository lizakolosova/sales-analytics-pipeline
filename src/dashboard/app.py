import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from src.cache.redis_manager import get_cache
from config.settings import get_settings

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

settings = get_settings()
cache = get_cache()

@st.cache_resource
def get_db_engine():
    return create_engine(settings.database_url)

def load_recent_transactions(limit=100):
    engine = get_db_engine()
    query = text(f"""
        SELECT * FROM transactions 
        WHERE status = 'completed'
        ORDER BY timestamp DESC 
        LIMIT {limit}
    """)
    return pd.read_sql(query, engine)

def load_sales_by_hour():
    engine = get_db_engine()
    query = text("""
        SELECT 
            DATE_TRUNC('hour', timestamp) as hour,
            COUNT(*) as transaction_count,
            SUM(total_amount) as revenue
        FROM transactions
        WHERE status = 'completed'
        GROUP BY hour
        ORDER BY hour DESC
        LIMIT 24
    """)
    return pd.read_sql(query, engine)

def load_category_performance():
    engine = get_db_engine()
    query = text("""
        SELECT 
            p.category,
            COUNT(t.transaction_id) as sales_count,
            SUM(t.total_amount) as revenue
        FROM transactions t
        JOIN products p ON t.product_id = p.product_id
        WHERE t.status = 'completed'
        GROUP BY p.category
        ORDER BY revenue DESC
    """)
    return pd.read_sql(query, engine)

st.title("Real-Time Sales Analytics Dashboard")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

try:
    df_recent = load_recent_transactions(1000)
    
    total_revenue = df_recent['total_amount'].sum()
    total_transactions = len(df_recent)
    avg_transaction = df_recent['total_amount'].mean()
    
    with col1:
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with col2:
        st.metric("Transactions", f"{total_transactions:,}")
    
    with col3:
        st.metric("Avg Transaction", f"${avg_transaction:.2f}")
    
    with col4:
        conversion_rate = (df_recent['status'] == 'completed').mean() * 100
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Over Time")
        df_hourly = load_sales_by_hour()
        fig_revenue = px.line(
            df_hourly,
            x='hour',
            y='revenue',
            title='Hourly Revenue Trend'
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        st.subheader("Payment Methods")
        payment_dist = df_recent['payment_method'].value_counts()
        fig_payment = px.pie(
            values=payment_dist.values,
            names=payment_dist.index,
            title='Payment Method Distribution'
        )
        st.plotly_chart(fig_payment, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Category Performance")
        df_category = load_category_performance()
        fig_category = px.bar(
            df_category,
            x='category',
            y='revenue',
            title='Revenue by Category'
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        st.subheader("Transaction Volume")
        df_hourly = load_sales_by_hour()
        fig_volume = px.bar(
            df_hourly,
            x='hour',
            y='transaction_count',
            title='Transactions per Hour'
        )
        st.plotly_chart(fig_volume, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Recent Transactions")
    st.dataframe(
        df_recent.head(20),
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure the database is running and populated with data.")

if st.button("Refresh Data"):
    st.cache_resource.clear()
    st.rerun()
