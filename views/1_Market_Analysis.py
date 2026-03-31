import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_helper import load_data, get_stats
from utils.model_loader import get_ai_system

df = load_data()

st.markdown("""
    <style>
    .stat-card {
        background: white;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        text-align: center;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.05);
        border-color: #6366f1;
    }
    .stat-label { 
        color: #64748b; 
        font-size: 0.75rem; 
        font-weight: 700; 
        text-transform: uppercase; 
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .stat-value { 
        color: #0f172a;
        font-size: 2.2rem; 
        font-weight: 800; 
        margin: 0;
        line-height: 1.2;
    }
    .stat-unit { color: #94a3b8; font-size: 0.85rem; font-weight: 500; }

    .ai-badge {
        background: #f1f5f9;
        color: #475569;
        padding: 5px 15px;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 1px;
        border: 1px solid #e2e8f0;
        display: inline-block;
        margin-bottom: 15px;
    }

    .stPlotlyChart {
        background: white;
        border-radius: 20px;
        border: 1px solid #f1f5f9;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("### 📊 Phân Tích Thị Trường")

with st.container():
    c_f1, c_f2, c_f3 = st.columns(3)
    with c_f1:
        city = st.selectbox("📍 Chọn Thành phố", sorted(df['City'].unique()))
    with c_f2:
        districts = sorted(df[df['City'] == city]['District'].unique())
        district = st.selectbox("🏢 Chọn Quận/Huyện", ["Toàn thành phố"] + districts)
    with c_f3:
        legal_options = df['Legal status'].unique()
        legal = st.multiselect("⚖️ Tình trạng pháp lý", legal_options, default=legal_options)

filtered_df = df[df['City'] == city]
if district != "Toàn thành phố":
    filtered_df = filtered_df[filtered_df['District'] == district]
filtered_df = filtered_df[filtered_df['Legal status'].isin(legal)]

st.write("")

avg_p, avg_m2, count = get_stats(filtered_df)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'''<div class="stat-card">
        <p class="stat-label">Giá trung bình</p>
        <p class="stat-value">{avg_p:.2f}</p>
        <p class="stat-unit">Tỷ VNĐ / Căn</p>
    </div>''', unsafe_allow_html=True)
with c2:
    st.markdown(f'''<div class="stat-card">
        <p class="stat-label">Đơn giá niêm yết</p>
        <p class="stat-value">{avg_m2:.1f}</p>
        <p class="stat-unit">Triệu VNĐ / m²</p>
    </div>''', unsafe_allow_html=True)
with c3:
    st.markdown(f'''<div class="stat-card">
        <p class="stat-label">Số lượng tin đăng</p>
        <p class="stat-value">{count:,}</p>
        <p class="stat-unit">Bất động sản thực tế</p>
    </div>''', unsafe_allow_html=True)

st.write("") 

col_l, col_r = st.columns([1.6, 1])

with col_l:
    st.markdown("#### 💹 Mặt bằng giá theo Quận/Huyện")
    dist_stats = filtered_df.groupby('District')['Price_per_m2'].mean().reset_index().sort_values('Price_per_m2', ascending=True)
    
    fig = px.bar(dist_stats.tail(15), x='Price_per_m2', y='District', orientation='h',
                 color='Price_per_m2', color_continuous_scale='Blues',
                 labels={'Price_per_m2': 'Triệu/m²', 'District': 'Khu vực'})
    
    fig.update_layout(height=450, margin=dict(l=0, r=10, t=10, b=0),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.markdown("#### 💎 Tỷ lệ pháp lý")
    legal_counts = filtered_df['Legal status'].value_counts().reset_index()
    fig_pie = px.pie(legal_counts, values='count', names='Legal status', hole=0.7,
                     color_discrete_sequence=['#6366f1', '#818cf8', '#a5b4fc', '#c7d2fe'],
                     labels={'count': 'Số lượng', 'Legal status': 'Trạng thái'})
    fig_pie.update_layout(height=450, showlegend=True, 
                          legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()
model, scaler, encoders = get_ai_system()

c_ai_1, c_ai_2 = st.columns([1, 2.2])

with c_ai_1:
    st.markdown('<div class="ai-badge">NEXHOME AI CORE</div>', unsafe_allow_html=True)
    st.markdown("#### Hiệu năng mô hình")
    st.write("Mô hình XGBoost được tối ưu hóa để dự đoán giá trị dựa trên hạ tầng và vị trí địa lý.")
    
    st.metric("Độ chính xác (R² Score)", "87.5%", help="Chỉ số phản ánh mức độ khớp của mô hình với dữ liệu thực tế.")
    st.caption("Cập nhật dữ liệu: Năm 2026.")

with c_ai_2:
    st.markdown("##### Phân tán: Diện tích vs Giá trị")
    fig_scatter = px.scatter(filtered_df.sample(min(800, len(filtered_df))), 
                             x='Area', y='Price', color='District',
                             size='Price_per_m2', 
                             labels={'Area': 'Diện tích (m²)', 'Price': 'Giá (Tỷ)', 'District': 'Quận/Huyện'},
                             hover_data=['Address'],
                             color_discrete_sequence=px.colors.qualitative.Safe)
    fig_scatter.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)

with st.expander("🔎 Xem bảng dữ liệu chi tiết (Top 100 kết quả)"):
    # Đổi tên cột hiển thị trong dataframe
    view_df = filtered_df[['Address', 'Area', 'Price', 'District', 'Legal status']].head(100).copy()
    view_df.columns = ['Địa chỉ', 'Diện tích (m²)', 'Giá (Tỷ)', 'Quận/Huyện', 'Pháp lý']
    st.dataframe(view_df, use_container_width=True, hide_index=True)