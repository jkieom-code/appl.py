import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simple Stock Predictor", page_icon="📈")

st.title("📈 Simple Stock Predictor")
st.write("Enter a stock ticker and see its historical prices and simple forecast (SMA-based).")

# Input
ticker = st.text_input("Enter a stock ticker (e.g., AAPL):", "AAPL")
days_to_predict = st.slider("Forecast next N days:", 1, 30, 7)

if st.button("Show Forecast"):
    with st.spinner("Fetching data..."):
        try:
            # Download historical data
            df = yf.download(ticker, period="2y")
            df = df[['Close']].dropna()

            # Simple moving average (SMA) forecast
            sma_window = 20
            df['SMA'] = df['Close'].rolling(sma_window).mean()

            # Forecast: assume next N days = last SMA value
            last_sma = df['SMA'].iloc[-1]
            forecast = pd.Series([last_sma]*days_to_predict, 
                                 index=pd.date_range(df.index[-1]+pd.Timedelta(1, unit='D'),
                                                     periods=days_to_predict))

            # Plot historical and forecast
            st.subheader(f"📊 {ticker} Closing Prices")
            plt.figure(figsize=(10,5))
            plt.plot(df['Close'], label="Close")
            plt.plot(df['SMA'], label=f"{sma_window}-day SMA")
            plt.plot(forecast, label="Forecast", linestyle='--')
            plt.legend()
            st.pyplot(plt)

            # Show forecast values
            st.subheader("📅 Forecasted Prices")
            st.write(forecast)

        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")


