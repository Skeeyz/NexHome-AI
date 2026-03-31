import pandas as pd
import streamlit as st
import os

# Đường dẫn file dữ liệu và lịch sử
DATA_PATH = 'data/VN_House_price_Clean2.csv'
HISTORY_PATH = 'data/user_history.csv'

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Không tìm thấy file dữ liệu tại {DATA_PATH}")
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)
    
    # 1. Tiền xử lý dữ liệu (Cực kỳ quan trọng cho Machine Learning)
    # Điền các giá trị trống bằng 0 hoặc trung bình để mô hình XGBoost không lỗi
    df['Access Road'] = df['Access Road'].fillna(0)
    df['Frontage'] = df['Frontage'].fillna(0)
    df['Floors'] = df['Floors'].fillna(1)
    
    # 2. Tính toán thêm các cột phân tích
    # Đổi tỷ sang Triệu VNĐ/m2
    df['Price_per_m2'] = (df['Price'] * 1000) / df['Area'] 
    
    return df

def get_stats(df):
    """Tính toán các chỉ số cơ bản cho Dashboard"""
    if df.empty:
        return 0, 0, 0
        
    avg_price = df['Price'].mean()
    avg_m2 = df['Price_per_m2'].mean()
    total_listings = len(df)
    
    return avg_price, avg_m2, total_listings

def save_to_history(entry):
    """Hàm ghi lịch sử tra cứu vào file CSV cục bộ"""
    # Tạo thư mục data nếu chưa có
    if not os.path.exists('data'):
        os.makedirs('data')
        
    # Chuyển entry thành DataFrame
    new_data = pd.DataFrame([entry])
    
    # Nếu file đã tồn tại thì append (viết tiếp), nếu chưa thì tạo mới có header
    if os.path.exists(HISTORY_PATH):
        new_data.to_csv(HISTORY_PATH, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(HISTORY_PATH, mode='w', header=True, index=False, encoding='utf-8-sig')