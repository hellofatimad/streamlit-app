import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np



def get_clean_data():
    data = pd.read_csv('../data-ori.csv')

    data['SOURCE'] = data['SOURCE'].map({'in': 1, 'out': 0})
    data['SEX'] = data['SEX'].map({'F': 1, 'M': 0})

    return data

def add_sliders():
    st.header("Lab Work Details")

    data = get_clean_data()
    slider_labels = [
        ('Sex', 'SEX'),
        (' Haematocrit', 'HAEMATOCRIT'),
        (' Haemoglobins', 'HAEMOGLOBINS'),
        ('Erythrocyte','ERYTHROCYTE'),
        ('Leucocyte', 'LEUCOCYTE'),
        ('Thrombocyte', 'THROMBOCYTE'),
        ('Mean Corpuscular Hemoglobin (MCH)', 'MCH'),
        ('Mean Corpuscular Hemoglobin Concentration (MCHC)', 'MCHC'),
        ('Mean Corpuscular Volume (MCV)', 'MCV'),
        ('Age', 'AGE')
    ]

    input_dict = {}
    sex_op = {'F': 1, 'M': 0}

    for label, key in slider_labels:
        if label == 'Sex':
            selected_sex = st.selectbox(label, list(sex_op.keys()))
            input_dict[key] = sex_op[selected_sex]
        else:
            input_dict[key] = st.slider(
                label,
                min_value= float(0),
                max_value= float(data[key].max()),
                value = float(data[key].mean())
            )

    return input_dict

def get_scaled_val(input_dict):
    data = get_clean_data()

    X = data.drop(['SOURCE'], axis = 1)

    scaled_dict = {}

    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()

        scaled_val = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_val

    return scaled_dict

def get_radar_chart(input_data):

    input_data  = get_scaled_val(input_data)
    categories = ['HAEMATOCRIT', 'HAEMOGLOBINS', 'ERYTHROCYTE', 
                  'LEUCOCYTE', 'THROMBOCYTE',	'MCH', 'MCHC', 'MCV','AGE']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['HAEMATOCRIT'], input_data['HAEMOGLOBINS'], input_data['ERYTHROCYTE'],
            input_data['LEUCOCYTE'], input_data['THROMBOCYTE'], input_data['MCH'],
            input_data['MCHC'], input_data['MCV'], input_data['AGE'],
        ],
        theta=categories,
        fill='toself',
        name='Current Patient'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        )),
    showlegend=True
    )

    return fig

def add_predictions(input_data):
    model = pickle.load(open("../model/ptmodel.pkl", "rb"))
    scaler = pickle.load(open("../model/ptscaler.pkl", "rb"))

    input_array = np.array(list(input_data.values())).reshape(1, -1)

    input_array_scaled = scaler.transform(input_array)

    prediction = model.predict(input_array_scaled)

    st.subheader("Patient Experience Prediction")

    if prediction[0] == 1:
        st.write("<span class='experience inpatient'>Inpatient</span>", unsafe_allow_html = True)
    else:
        st.write("<span class='experience outpatient'>Outpatient</span>", unsafe_allow_html = True)


    st.write("Probability of being inpatient: ", model.predict_proba(input_array_scaled)[0][1])
    st.write("Probability of being outpatient: ", model.predict_proba(input_array_scaled)[0][0])
    st.write("")
    st.write("")
    st.write("This data was imported from Kaggle. It is an electronic health record predicting collected from a hospital from Indonesia. \
             It contains blood work results.")




def pt_exp():

    with open("../assets/style.css") as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html = True)

    #input_data = add_sidebar()


    with st.container():
        st.title("Patient Care Experience Predictor")
        st.page_link("https://www.kaggle.com/datasets/saurabhshahane/patient-treatment-classification?select=data-ori.csv", label="Kaggle link", icon ="🔗")
        #st.write("Using the dataset from Kaggle, we will predict if the cyst could be a malignant breast cancer tumor. \
                # As a kind reminder, this application does not serve to replace professional diagnosis.")
    
    
    
    col1, col2 = st.columns([4,1])
    #sliderm = st.columns()

    
    input_data = add_sliders()


    with col1:
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart)

    with col2:
        add_predictions(input_data)
        
if __name__ == "__main__":
    pt_exp()
