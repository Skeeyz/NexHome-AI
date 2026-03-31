import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_helper import load_data
from datetime import datetime

# 1. LOAD DỮ LIỆU
df = load_data()

# 2. HEADER
st.markdown("### ⚖️ So sánh đối đầu Bất động sản")
st.write("Nhập thông số 2 bất động sản để phân tích sự khác biệt.")

# 3. NHẬP THÔNG SỐ 2 ĐỐI TƯỢNG
with st.container():
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""<div style='padding:10px; background-color:#EEF2FF; border-radius:10px; border-left:5px solid #4F46E5;'>
                    <h5 style='margin:0; color:#4F46E5;'>🔵 Đối tượng 1</h5></div>""", unsafe_allow_html=True)
        name_1 = st.text_input("Tên định danh 1", value="BĐS A", key="n1")
        city_1 = st.selectbox("Thành phố", df['City'].unique(), key="c1")
        dist_1 = st.selectbox("Quận/Huyện", sorted(df[df['City'] == city_1]['District'].unique()), key="d1")
        avg_1 = df[df['District'] == dist_1][['Price', 'Area', 'Floors']].mean()
        
        p1 = st.number_input("Giá (Tỷ)", value=float(round(avg_1['Price'], 2)), key="p1")
        a1 = st.number_input("Diện tích (m²)", value=float(round(avg_1['Area'], 1)), key="a1")
        f1 = st.number_input("Số tầng", value=int(avg_1['Floors']), key="f1")

    with col_right:
        st.markdown("""<div style='padding:10px; background-color:#FFF7ED; border-radius:10px; border-left:5px solid #FB923C;'>
                    <h5 style='margin:0; color:#FB923C;'>🟠 Đối tượng 2</h5></div>""", unsafe_allow_html=True)
        name_2 = st.text_input("Tên định danh 2", value="BĐS B", key="n2")
        city_2 = st.selectbox("Thành phố ", df['City'].unique(), key="c2")
        dist_2 = st.selectbox("Quận/Huyện ", sorted(df[df['City'] == city_2]['District'].unique()), key="d2")
        avg_2 = df[df['District'] == dist_2][['Price', 'Area', 'Floors']].mean()
        
        p2 = st.number_input("Giá (Tỷ) ", value=float(round(avg_2['Price'], 2)), key="p2")
        a2 = st.number_input("Diện tích (m²) ", value=float(round(avg_2['Area'], 1)), key="a2")
        f2 = st.number_input("Số tầng ", value=int(avg_2['Floors']), key="f2")

st.write("")
# NÚT BẤM KÍCH HOẠT SO SÁNH
btn_compare = st.button("⚡ BẮT ĐẦU SO SÁNH ĐỐI ĐẦU", use_container_width=True, type="primary")

# 4. CHỈ CHẠY KHI BẤM NÚT
if btn_compare:
    # --- CHUẨN BỊ DỮ LIỆU ---
    categories = ['Giá cả (Tỷ)', 'Diện tích (m²)', 'Số tầng', 'Vị trí (Điểm)']
    val1 = [p1, a1, f1, 4] 
    val2 = [p2, a2, f2, 4.5]

    # --- VẼ BIỂU ĐỒ RADAR ---
    st.markdown("#### 📊 Phân tích sự khác biệt")
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=val1, theta=categories, fill='toself', name=name_1,
                                 line_color='#4F46E5', fillcolor='rgba(79, 70, 229, 0.3)'))
    fig.add_trace(go.Scatterpolar(r=val2, theta=categories, fill='toself', name=name_2,
                                 line_color='#FB923C', fillcolor='rgba(251, 146, 60, 0.3)'))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(val1 + val2) * 1.1])),
        showlegend=True, height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- LƯU LỊCH SỬ ---
    if 'history_log' not in st.session_state:
        st.session_state.history_log = []

    log_entry = {
        "type": "SO SÁNH",
        "timestamp": datetime.now().strftime("%H:%M:%S - %d/%m/%Y"),
        "location": f"{dist_1} vs {dist_2}",
        "details": f"So sánh {name_1} ({p1}B) và {name_2} ({p2}B)",
        "result": f"Chênh lệch {abs(p1-p2):.2f} Tỷ VNĐ"
    }
    from utils.data_helper import save_to_history
    save_to_history(log_entry)
    st.session_state.history_log.append(log_entry)
    

    # --- BẢNG CHI TIẾT ---
    st.markdown("#### 📝 Bảng thông số chi tiết")
    diff_price = p1 - p2
    color_p = "green" if diff_price < 0 else "red"
    st.markdown(f"""
    | Đặc điểm | {name_1} | {name_2} | Chênh lệch |
    | :--- | :--- | :--- | :--- |
    | **Giá (Tỷ)** | {p1:.2f} | {p2:.2f} | <span style='color:{color_p}'>{abs(diff_price):.2f} Tỷ</span> |
    | **Diện tích** | {a1:.1f} m² | {a2:.1f} m² | {abs(a1-a2):.1f} m² |
    | **Số tầng** | {f1} | {f2} | {abs(f1-f2)} tầng |
    """, unsafe_allow_html=True)
else:
    st.info("💡 Vui lòng điều chỉnh thông số và nhấn nút phía trên để xem kết quả so sánh.")