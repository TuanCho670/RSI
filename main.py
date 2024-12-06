from tradingview_ta import TA_Handler, Interval
from datetime import datetime, timedelta

def get_rsi_multiple_timeframes():
    # Khởi tạo handler cho các timeframe khác nhau
    timeframes = [
        Interval.INTERVAL_1_HOUR,
        Interval.INTERVAL_4_HOURS,
        Interval.INTERVAL_1_DAY
    ]
    
    print("\n=== RSI BTCUSDT từ TradingView ===")
    print(f"Thời gian hiện tại: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-----------------------------------")
    
    for interval in timeframes:
        handler = TA_Handler(
            symbol="BTCUSDT",
            exchange="BINANCE",
            screener="crypto",
            interval=interval,
        )
        
        try:
            analysis = handler.get_analysis()
            rsi = analysis.indicators["RSI"]
            
            # In kết quả
            print(f"Timeframe {interval}:")
            print(f"RSI: {rsi:.2f}")
            print("-----------------------------------")
            
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu {interval}: {str(e)}")
            print("-----------------------------------")

# Chạy function
get_rsi_multiple_timeframes()
