import os
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder, StandardScaler
import streamlit as st

# Đường dẫn lưu trữ model
MODEL_PATH = 'models/model_xgb.json'

@st.cache_resource
def get_ai_system():
    """
    Hàm trung tâm: Kiểm tra file model, nếu có thì load, nếu không thì train.
    """
    # 1. Luôn load dữ liệu để lấy danh sách LabelEncoder (quan trọng cho UI)
    df = pd.read_csv('data/VN_House_price_Clean2.csv')
    
    num_features = ['Area', 'Access Road', 'Floors', 'Bedrooms', 'Bathrooms', 'Frontage']
    cat_features = ['City', 'District', 'Legal status', 'Furniture state']
    
    # Khởi tạo Encoders và Scaler
    label_encoders = {}
    for col in cat_features:
        le = LabelEncoder()
        le.fit(df[col])
        label_encoders[col] = le
        
    scaler = StandardScaler()
    scaler.fit(df[num_features])

    model_xgb = xgb.XGBRegressor()

    # 2. KIỂM TRA FILE MODEL
    if os.path.exists(MODEL_PATH):
        # TH: Đã có model -> Load nhanh
        model_xgb.load_model(MODEL_PATH)
    else:
        # TH: Chưa có model -> Tiến hành huấn luyện (Chạy logic từ Notebook của bạn)
        st.warning("⚠️ Không tìm thấy model có sẵn. Hệ thống đang tiến hành huấn luyện mới (có thể mất vài phút)...")
        
        X = df[num_features + cat_features].copy()
        y = df["Price"]
        
        # Transform dữ liệu để train
        for col in cat_features:
            X[col] = label_encoders[col].transform(X[col])
        X[num_features] = scaler.transform(X[num_features])
        
        # Huấn luyện với bộ tham số tốt nhất từ Notebook của bạn
        model_xgb = xgb.XGBRegressor(
            n_estimators=1200, 
            learning_rate=0.02, 
            max_depth=7, 
            random_state=42
        )
        model_xgb.fit(X, y)
        
        # Lưu lại cho lần sau
        if not os.path.exists('models'): os.makedirs('models')
        model_xgb.save_model(MODEL_PATH)
        st.success("✅ Đã huấn luyện và lưu model thành công!")

    return model_xgb, scaler, label_encoders

def predict_price_xgb(inputs, model_xgb, scaler, label_encoders):
    """
    Hàm dự đoán nhận đầu vào từ giao diện
    """
    input_df = pd.DataFrame([inputs])
    
    num_features = ['Area', 'Access Road', 'Floors', 'Bedrooms', 'Bathrooms', 'Frontage']
    cat_features = ['City', 'District', 'Legal status', 'Furniture state']

    # Encode & Scale
    for col in cat_features:
        input_df[col] = label_encoders[col].transform(input_df[col])
    input_df[num_features] = scaler.transform(input_df[num_features])
    
    return model_xgb.predict(input_df)[0]