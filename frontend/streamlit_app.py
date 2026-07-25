# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.data_fetch import get_history
from backend.indicators import compute_indicators, compute_score

st.set_page_config(page_title="Stock Picker", layout="wide")

st.title("Stock Picker")
st.markdown("Enter a ticker symbol to analyze technical and fundamental signals. Not financial advice.")

with st.sidebar.form("input_form"):
    symbol = st.text_input("Ticker symbol", value="AAPL").upper().strip()
    period = st.selectbox("History range", ["1y", "6mo", "3mo", "1mo"])
    submit = st.form_submit_button("Analyze")

if submit and symbol:
    st.header(f"Analysis for {symbol}")
    with st.spinner("Fetching data and computing indicators..."):
        df = get_history(symbol, period)
        if df is None or df.empty:
            st.error("No data found for symbol.")
        else:
            indicators = compute_indicators(df)
            score = compute_score(indicators)
            # Summary cards
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Last Price", f"${df['Close'].iloc[-1]:.2f}")
            col2.metric("Composite Score", f"{score['confidence']:.2f}")
            col3.metric("Recommendation", score['recommendation'])
            col4.metric("Suggested Entry", f"${score['entry']:.2f}")

            # Candlestick chart with overlays
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                name="Price")])
            if 'sma50' in indicators:
                fig.add_trace(go.Scatter(x=df.index, y=indicators['sma50'], name="SMA50", line=dict(color='blue')))
            if 'sma200' in indicators:
                fig.add_trace(go.Scatter(x=df.index, y=indicators['sma200'], name="SMA200", line=dict(color='orange')))
            if 'bb_upper' in indicators:
                fig.add_trace(go.Scatter(x=df.index, y=indicators['bb_upper'], name="BB Upper", line=dict(color='gray', dash='dash')))
                fig.add_trace(go.Scatter(x=df.index, y=indicators['bb_lower'], name="BB Lower", line=dict(color='gray', dash='dash')))

            fig.update_layout(height=600, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig, use_container_width=True)

            # Indicators table
            st.subheader("Indicator Values")
            ind_df = pd.DataFrame({k: v.iloc[-1] if hasattr(v, 'iloc') else v for k, v in indicators.items()}, index=[symbol])
            st.table(ind_df.T)

            # Methodology and disclaimer
            st.markdown("### Methodology")
            st.markdown("- Composite score combines trend, momentum, volume, and fundamentals.")
            st.markdown("### Disclaimer")
            st.info("This tool is for educational purposes only and not financial advice.")
