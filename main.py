import streamlit as st
from tradingview_ta import TA_Handler, Interval
from datetime import datetime
import pandas as pd
import requests

# Thiết lập trang
st.set_page_config(layout="wide", page_title="RSI Monitor")

# CSS để tùy chỉnh bảng và loại bỏ cột trống
st.markdown("""
<style>
    .stMainBlockContainer {
    font-size: 30px !important;
    }
    .stDataFrame {
        width: 100% !important;
        max-width: 100% !important;
        font-size: 30px !important;
    }
    .dataframe {
        width: 100% !important;
        max-width: 100% !important;
    }
    div[data-testid="stDataFrameResizable"] {
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0rem !important;
    }
    thead tr th {
        text-align: left !important;
    }
</style>
""", unsafe_allow_html=True)

def get_usdt_pairs():
    try:
        response = requests.get('https://api.binance.com/api/v3/exchangeInfo')
        if response.status_code == 200:
            data = response.json()
            usdt_pairs = [
                symbol['symbol'] for symbol in data['symbols']
                if symbol['symbol'].endswith('USDT') 
                and symbol['status'] == 'TRADING'
                and not any(x in symbol['symbol'] for x in ['UP', 'DOWN', 'BEAR', 'BULL'])
            ]
            return sorted(usdt_pairs)
    except Exception as e:
        st.error(f"Lỗi khi lấy danh sách symbol: {str(e)}")
    return []

def get_rsi_with_symbol(rsi):
    if rsi >= 70:
        return f"🔴 {rsi:.2f}"  # Đỏ rõ
    elif rsi <= 30:
        return f"🟢 {rsi:.2f}"  # Xanh rõ
    else:
        return f"⚪ {rsi:.2f}"  # Trắng rõ

# Tiêu đề
st.title("🔍 RSI Monitor")

# Khởi tạo placeholder cho bảng
table_placeholder = st.empty()

# Khởi tạo DataFrame
df = pd.DataFrame(columns=['Symbol', 'Current Time', 'RSI'])

# Lấy danh sách symbols
symbols = get_usdt_pairs()
total_symbols = len(symbols)

# Hiển thị số lượng symbols đã xử lý
progress_text = st.empty()

for i, symbol in enumerate(symbols, 1):
    try:
        handler = TA_Handler(
            symbol=symbol,
            exchange="BINANCE",
            screener="crypto",
            interval=Interval.INTERVAL_1_DAY
        )
        analysis = handler.get_analysis()
        rsi = analysis.indicators.get("RSI", 0)
        
        # Thêm dữ liệu mới vào DataFrame
        new_row = pd.DataFrame({
            'Symbol': [symbol],
            'Current Time': [datetime.now().strftime('%H:%M:%S %d/%m/%Y')],
            'RSI': [get_rsi_with_symbol(rsi)]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Cập nhật bảng
        with table_placeholder.container():
            st.dataframe(
                df,
                hide_index=True,
                height=800,
                use_container_width=True,
                column_config={
                    "Symbol": st.column_config.TextColumn("Symbol", width=150),
                    "Current Time": st.column_config.TextColumn("Current Time", width=200),
                    "RSI": st.column_config.TextColumn("RSI", width=150)
                }
            )
        
        # Cập nhật tiến trình
        progress_text.write(f"Đã xử lý: {i}/{total_symbols} symbols")
        
    except Exception as e:
        continue

st.write(f"Cập nhật lần cuối: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")

# Nút refresh
if st.button('🔄 Làm mới dữ liệu'):
    st.rerun()
