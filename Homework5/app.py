import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use('dark_background')


st.set_page_config(page_title="Sigorta Ücreti Tahmini", page_icon="💰", layout="wide")
st.title("Sigorta Ücreti Tahmin Uygulaması")
st.markdown("""
Bu uygulama, verdiğiniz bilgilere göre sağlık sigortası ücretinizi 3 farklı makine öğrenmesi modeliyle tahmin eder ve sonuçları karşılaştırır.
""")


@st.cache_resource
def load_models():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    model_files = [
        'linear_regression_model.pkl', 
        'decision_tree_model.pkl', 
        'random_forest_model.pkl', 
        'scaler.pkl', 
        'columns.pkl', 
        'metrics.pkl'
    ]
    
    for file in model_files:
        file_path = os.path.join(current_dir, file)
        if not os.path.exists(file_path):
            st.error(f"Model dosyası '{file}' bulunamadı. Lütfen önce 'save_model.py' scriptini çalıştırın.")
            st.error(f"Aranan dosya yolu: {file_path}")
            st.stop()
    
    models = {}
    for model_name in ['linear_regression', 'decision_tree', 'random_forest']:
        model_path = os.path.join(current_dir, f'{model_name}_model.pkl')
        try:
            with open(model_path, 'rb') as model_file:
                models[model_name] = pickle.load(model_file)
        except Exception as e:
            st.error(f"{model_name} modeli yüklenirken hata oluştu: {e}")
            st.stop()
    
    scaler_path = os.path.join(current_dir, 'scaler.pkl')
    try:
        with open(scaler_path, 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
    except Exception as e:
        st.error(f"Scaler yüklenirken hata oluştu: {e}")
        st.stop()
    
    columns_path = os.path.join(current_dir, 'columns.pkl')
    try:
        with open(columns_path, 'rb') as columns_file:
            columns = pickle.load(columns_file)
    except Exception as e:
        st.error(f"Sütun isimleri yüklenirken hata oluştu: {e}")
        st.stop()
    
    metrics_path = os.path.join(current_dir, 'metrics.pkl')
    try:
        with open(metrics_path, 'rb') as metrics_file:
            metrics = pickle.load(metrics_file)
    except Exception as e:
        st.error(f"Metrikler yüklenirken hata oluştu: {e}")
        st.stop()
    
    return models, scaler, columns, metrics

try:
    models, scaler, columns, metrics = load_models()
except Exception as e:
    st.error(f"Modeller yüklenirken bir hata oluştu: {e}")
    st.stop()

st.sidebar.header("Kullanıcı Bilgileri")

age = st.sidebar.slider("Yaş", 18, 100, 30)
sex = st.sidebar.radio("Cinsiyet", ["Erkek", "Kadın"])
bmi = st.sidebar.slider("Vücut Kitle İndeksi (BMI)", 15.0, 50.0, 25.0, 0.1)
children = st.sidebar.slider("Çocuk Sayısı", 0, 10, 0)
smoker = st.sidebar.radio("Sigara İçiyor musunuz?", ["Hayır", "Evet"])
region = st.sidebar.selectbox("Bölge", ["Kuzeydoğu", "Kuzeybatı", "Güneydoğu", "Güneybatı"])

def predict_charges(age, sex, bmi, children, smoker, region):
    data = {
        'age': age,
        'bmi': bmi,
        'children': children,
        'sex_male': 1 if sex == "Erkek" else 0,
        'smoker_yes': 1 if smoker == "Evet" else 0,
        'region_northwest': 1 if region == "Kuzeybatı" else 0,
        'region_southeast': 1 if region == "Güneydoğu" else 0,
        'region_southwest': 1 if region == "Güneybatı" else 0
    }
    
    data['bmi_smoker'] = data['bmi'] * data['smoker_yes']
    data['age_smoker'] = data['age'] * data['smoker_yes']
    
    df = pd.DataFrame([data])
    df = df.reindex(columns=columns, fill_value=0)
    
    scaled_data = scaler.transform(df)
    
    predictions = {
        'Linear Regression': models['linear_regression'].predict(scaled_data)[0],
        'Decision Tree': models['decision_tree'].predict(scaled_data)[0],
        'Random Forest': models['random_forest'].predict(scaled_data)[0]
    }
    
    return predictions

st.header("Sigorta Ücreti Tahmini")

col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Yaş:** {age}")
    st.info(f"**Cinsiyet:** {sex}")
with col2:
    st.info(f"**BMI:** {bmi}")
    st.info(f"**Çocuk Sayısı:** {children}")
with col3:
    st.info(f"**Sigara İçme Durumu:** {smoker}")
    st.info(f"**Bölge:** {region}")

if 'predictions_made' not in st.session_state:
    st.session_state.predictions_made = False

if 'metric_choice' not in st.session_state:
    st.session_state.metric_choice = "MSE"

predict_button = st.button("Sigorta Ücretini Tahmin Et", key="predict_button")

if predict_button or st.session_state.predictions_made:
    try:
        if predict_button:
            with st.spinner("Tahmin yapılıyor..."):
                predictions = predict_charges(age, sex, bmi, children, smoker, region)
                st.session_state.predictions = predictions
                st.session_state.predictions_made = True
        elif st.session_state.predictions_made:
            predictions = st.session_state.predictions
        else:
            st.warning("Lütfen 'Sigorta Ücretini Tahmin Et' butonuna basın.")
            st.stop()
        
        model_names = list(predictions.keys())
        values = list(predictions.values())
            
        st.subheader("Tahmin Sonuçları")
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='black')
        colors = ['#FF9999', '#66B2FF', '#99FF99']
        ax.bar(model_names, values, color=colors)
        ax.set_ylabel('Tahmini Sigorta Ücreti ($)', color='white')
        ax.set_title('Modellerin Sigorta Ücreti Tahminleri', color='white')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        
        for i, v in enumerate(values):
            ax.text(i, v + 50, f"${v:.2f}", ha='center', color='white')
        
        st.pyplot(fig)
        
        st.subheader("Modellerin Tahmin Değerleri")
        
        prediction_df = pd.DataFrame({
            'Model': model_names,
            'Tahmini Yıllık Sigorta Ücreti ($)': values
        })
        
        st.table(prediction_df.set_index('Model').style.format("${:.2f}"))
        
        st.subheader("Model Performans Metrikleri")
        
        metrics_df = pd.DataFrame({
            'Model': [],
            'MSE': [],
            'MAE': [],
            'R² Skoru': []
        })
        
        for model_name, metric in metrics.items():
            metrics_df = pd.concat([metrics_df, pd.DataFrame({
                'Model': [model_name],
                'MSE': [metric['MSE']],
                'MAE': [metric['MAE']],
                'R² Skoru': [metric['R2']]
            })], ignore_index=True)
        
        st.table(metrics_df.set_index('Model').style.format({
            'MSE': '{:.2f}',
            'MAE': '{:.2f}',
            'R² Skoru': '{:.4f}'
        }))
        
        st.subheader("Performans Metrikleri Karşılaştırması")
        
        metric_choice = st.radio(
            "Metrik seçin:", 
            ["MSE", "MAE", "R² Skoru"], 
            horizontal=True,
            key="metric_selector",
            index=["MSE", "MAE", "R² Skoru"].index(st.session_state.metric_choice)
        )
        
        st.session_state.metric_choice = metric_choice
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='black')
        
        if metric_choice == "R² Skoru":
            metric_values = [metrics[model]['R2'] for model in model_names]
            title = "R² Skoru Karşılaştırması (Yüksek değer daha iyi)"
            y_label = "R² Skoru"
            decimal_places = 4
            offset = 0.01
        elif metric_choice == "MSE":
            metric_values = [metrics[model]['MSE'] for model in model_names]
            title = "MSE Karşılaştırması (Düşük değer daha iyi)"
            y_label = "MSE"
            decimal_places = 2
            offset = 50
        else:  # MAE
            metric_values = [metrics[model]['MAE'] for model in model_names]
            title = "MAE Karşılaştırması (Düşük değer daha iyi)"
            y_label = "MAE"
            decimal_places = 2
            offset = 50
        
        ax.bar(model_names, metric_values, color=colors)
        ax.set_ylabel(y_label, color='white')
        ax.set_title(title, color='white')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        
        for i, v in enumerate(metric_values):
            if decimal_places == 4:
                ax.text(i, v + offset, f"{v:.4f}", ha='center', color='white')
            else:
                ax.text(i, v + offset, f"{v:.2f}", ha='center', color='white')
        
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Tahmin yapılırken bir hata oluştu: {e}") 