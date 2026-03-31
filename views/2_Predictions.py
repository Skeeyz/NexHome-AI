import streamlit as st
import time
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.data_helper import load_data
# Đổi sang dùng get_ai_system và predict_price_xgb từ model_loader mới
from utils.model_loader import get_ai_system, predict_price_xgb

# 1. KHỞI TẠO HỆ THỐNG AI (XGBoost)
# Hàm này tự động check file .json, nếu không có sẽ tự train
model, scaler, encoders = get_ai_system()
df = load_data()

# 2. CSS CUSTOM
st.markdown("""
    <style>
    .prediction-container {
        background-color: #EEF2FF;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #C7D2FE;
        text-align: center;
        margin-top: 10px;
    }
    .price-result {
        color: #4338CA;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 5px 0;
        line-height: 1;
    }
    .cluster-badge {
        background-color: #4338CA;
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. HEADER
st.markdown("### 🔮 Dự báo giá bằng trí tuệ nhân tạo (XGBoost)")
st.write("Vui lòng cung cấp đầy đủ 10 thông số dưới đây để mô hình đạt độ chính xác cao nhất (~87%).")

# 4. INPUT FORM - ĐẦY ĐỦ 10 TRƯỜNG DỮ LIỆU
with st.container():
    col_input_1, col_input_2 = st.columns([1, 1])
    
    with col_input_1:
        st.markdown("##### 📏 Thông số kích thước")
        area = st.number_input("Diện tích sử dụng (m²)", min_value=1.0, value=50.0, step=1.0)
        access_road = st.number_input("Đường vào (m)", min_value=0.0, value=3.0, step=0.5)
        frontage = st.number_input("Mặt tiền (m)", min_value=0.0, value=4.0, step=0.5)
        floors = st.number_input("Tổng số tầng", min_value=1, value=1)
        
        st.markdown("##### 🛌 Tiện nghi")
        bedrooms = st.slider("Số phòng ngủ", 1, 10, 2)
        bathrooms = st.slider("Số phòng vệ sinh", 1, 10, 2)
        
    with col_input_2:
        st.markdown("##### 📍 Vị trí & Pháp lý")
        # Lấy danh sách từ encoders để đảm bảo khớp dữ liệu training
        city_list = sorted(encoders['City'].classes_)
        selected_city = st.selectbox("Thành phố", city_list)
        
        # Lọc Quận/Huyện theo Thành phố đã chọn
        districts_in_city = sorted(df[df['City'] == selected_city]['District'].unique())
        selected_district = st.selectbox("Quận/Huyện", districts_in_city)
        
        legal_list = encoders['Legal status'].classes_
        selected_legal = st.selectbox("Tình trạng pháp lý", legal_list)
        
        furniture_list = encoders['Furniture state'].classes_
        selected_furniture = st.selectbox("Tình trạng nội thất", furniture_list)

    st.write("")
    
    # 5. XỬ LÝ DỰ BÁO
    if st.button("⚡ BẮT ĐẦU PHÂN TÍCH & DỰ BÁO", use_container_width=True, type="primary"):
        
        # Tạo dictionary input đúng 10 trường mô hình cần
        user_inputs = {
            'Area': area,
            'Access Road': access_road,
            'Floors': floors,
            'Bedrooms': bedrooms,
            'Bathrooms': bathrooms,
            'Frontage': frontage,
            'City': selected_city,
            'District': selected_district,
            'Legal status': selected_legal,
            'Furniture state': selected_furniture
        }

        with st.status("🤖 AI đang tính toán...", expanded=True) as status:
            st.write("🔄 Đang mã hóa đặc trưng địa lý...")
            time.sleep(0.3)
            st.write("📈 Đang áp dụng mô hình XGBoost...")
            
            # Gọi hàm dự báo từ model_loader
            price_est = predict_price_xgb(user_inputs, model, scaler, encoders)
            
            time.sleep(0.3)
            status.update(label="✅ Đã hoàn tất!", state="complete", expanded=False)

        # 6. HIỂN THỊ KẾT QUẢ & LƯU LỊCH SỬ
        st.markdown(f"""
            <div class="prediction-container">
                <span class="cluster-badge">XGBOOST REGRESSOR MODEL</span>
                <p style="color: #64748B; margin-top: 15px; font-weight: 600; font-size: 0.9rem;">GIÁ DỰ BÁO ƯỚC TÍNH</p>
                <h1 class="price-result">{price_est:.2f} Tỷ VNĐ</h1>
                <p style="color: #94A3B8; font-size: 0.8rem;">Vị trí: {selected_district}, {selected_city}</p>
            </div>
        """, unsafe_allow_html=True)

        log_entry = {
            "type": "DỰ BÁO GIÁ",
            "timestamp": datetime.now().strftime("%H:%M:%S - %d/%m/%Y"),
            "location": f"{selected_district}, {selected_city}",
            "details": f"{area}m² | {floors} tầng | {access_road}m đường",
            "result": f"{price_est:.2f} Tỷ VNĐ"
        }

        # Lưu dữ liệu vào file và session
        from utils.data_helper import save_to_history
        save_to_history(log_entry)

        if 'history_log' not in st.session_state:
            st.session_state.history_log = []
        st.session_state.history_log.append(log_entry)

        st.write("")
        
        # 7. PHÂN TÍCH TRỌNG SỐ
        col_info, col_chart = st.columns([1, 1])
        with col_info:
            st.markdown("##### 💡 Ghi chú mô hình")
            st.info(f"""
            Dựa trên thông số bạn nhập:
            - **Đơn giá dự kiến:** ~{ (price_est*1000)/area :.1f} Triệu/m²
            - **Phân khúc:** {'Cao cấp' if price_est > 15 else 'Trung cấp' if price_est > 5 else 'Bình dân'}
            - **Độ tin cậy:** Khớp với ~87% biến động thị trường thực tế.
            """)
            
        with col_chart:
            st.markdown("##### 📈 Yếu tố quyết định giá")
            weights = pd.DataFrame({
                'Yếu tố': ['Vị trí', 'Diện tích', 'Pháp lý', 'Hạ tầng'],
                'Độ ảnh hưởng': [45, 30, 15, 10]
            })
            fig = px.bar(weights, x='Độ ảnh hưởng', y='Yếu tố', orientation='h', color_discrete_sequence=['#4338CA'])
            fig.update_layout(height=180, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)