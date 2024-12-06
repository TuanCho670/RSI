import streamlit as st
from tradingview_ta import TA_Handler, Interval
from datetime import datetime

# Thiết lập trang
st.set_page_config(
    page_title="RSI Monitor",
    page_icon="📈"
)

# Tiêu đề
st.title("RSI Bitcoin Monitor")
st.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Container chính
with st.container():
    try:
        # 1 giờ
        handler_1h = TA_Handler(
            symbol="BTCUSDT",
            exchange="BINANCE",
            screener="crypto",
            interval=Interval.INTERVAL_1_HOUR
        )
        rsi_1h = handler_1h.get_analysis().indicators["RSI"]
        st.metric("RSI 1 giờ", f"{rsi_1h:.2f}")
        
        # 4 giờ
        handler_4h = TA_Handler(
            symbol="BTCUSDT",
            exchange="BINANCE",
            screener="crypto",
            interval=Interval.INTERVAL_4_HOURS
        )
        rsi_4h = handler_4h.get_analysis().indicators["RSI"]
        st.metric("RSI 4 giờ", f"{rsi_4h:.2f}")
        
        # 1 ngày
        handler_1d = TA_Handler(
            symbol="BTCUSDT",
            exchange="BINANCE",
            screener="crypto",
            interval=Interval.INTERVAL_1_DAY
        )
        rsi_1d = handler_1d.get_analysis().indicators["RSI"]
        st.metric("RSI 1 ngày", f"{rsi_1d:.2f}")
        
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {str(e)}")

# Nút refresh
if st.button('Làm mới dữ liệu'):
    st.rerun()
