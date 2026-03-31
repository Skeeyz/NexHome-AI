import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Đường dẫn file lưu lịch sử cục bộ
HISTORY_FILE = 'data/user_history.csv'

# 1. Cấu hình tiêu đề
st.markdown("### 📜 Lịch sử tra cứu cá nhân")
st.write("Danh sách các yêu cầu định giá và so sánh đã được thực hiện.")

# 2. Hàm tải dữ liệu lịch sử
def load_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE).to_dict('records')
    return []

# Khởi tạo hoặc cập nhật session_state từ file
if 'history_log' not in st.session_state or not st.session_state.history_log:
    st.session_state.history_log = load_history()

# 3. Giao diện khi chưa có dữ liệu
if not st.session_state.history_log:
    st.info("Bạn chưa thực hiện tra cứu nào. Lịch sử sẽ xuất hiện sau khi bạn dùng công cụ Dự báo hoặc So sánh.")
    if st.button("Thử Dự báo ngay 🔮"):
        st.switch_page("views/2_Predictions.py")
else:
    # 4. CSS cho các thẻ lịch sử
    st.markdown("""
        <style>
        .history-item {
            background-color: #ffffff;
            padding: 18px;
            border-radius: 12px;
            border-left: 6px solid #4F46E5;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border-right: 1px solid #f1f5f9;
            border-top: 1px solid #f1f5f9;
            border-bottom: 1px solid #f1f5f9;
        }
        .history-time { color: #94A3B8; font-size: 0.8rem; font-weight: 600; }
        .history-type { 
            padding: 3px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 800; text-transform: uppercase;
        }
        .type-predict { background-color: #EEF2FF; color: #4F46E5; }
        .type-compare { background-color: #FFF7ED; color: #EA580C; }
        </style>
    """, unsafe_allow_html=True)

    # Thống kê nhanh
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Tổng số lần tra cứu", len(st.session_state.history_log))
    with c2:
        last_time = st.session_state.history_log[-1]['timestamp'] if st.session_state.history_log else "N/A"
        st.write(f"🕒 Lần cuối: {last_time}")

    st.divider()

    # Hiển thị từ mới nhất đến cũ nhất
    for i, entry in enumerate(reversed(st.session_state.history_log)):
        # Phân loại màu sắc theo loại tra cứu
        type_class = "type-predict" if entry['type'] == "DỰ BÁO GIÁ" else "type-compare"
        
        with st.container():
            st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="history-type {type_class}">{entry['type']}</span>
                        <span class="history-time">{entry['timestamp']}</span>
                    </div>
                    <p style="margin: 12px 0 5px 0; font-size: 1.15rem; color: #1e293b;"><b>📍 {entry['location']}</b></p>
                    <p style="margin: 0; color: #64748b; font-size: 0.9rem; line-height: 1.4;">
                        🔹 {entry['details']}
                    </p>
                    <div style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed #e2e8f0;">
                        <span style="color: #64748b; font-size: 0.85rem;">Kết quả phân tích:</span>
                        <p style="margin: 2px 0 0 0; color: #4F46E5; font-weight: 800; font-size: 1.3rem;">
                            {entry['result']}
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Nút xóa sạch lịch sử (Cần xóa cả file CSV)
    st.sidebar.divider()
    if st.sidebar.button("🗑️ Xóa toàn bộ lịch sử", use_container_width=True):
        st.session_state.history_log = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        st.rerun()

    # Nút xuất dữ liệu
    df_hist = pd.DataFrame(st.session_state.history_log)
    csv = df_hist.to_csv(index=False).encode('utf-8-sig')
    st.sidebar.download_button(
        "📥 Tải lịch sử (.csv)",
        csv,
        "property_search_history.csv",
        "text/csv",
        use_container_width=True
    )