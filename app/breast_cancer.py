import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np


def get_clean_data():
    data = pd.read_csv('../breast-cancer.csv')
    
    data = data.drop('id', axis = 1)

    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

    return data

def add_sliders(type_feat):
    st.header("Cell Nuclei Details")

    data = get_clean_data()
    if type_feat == "mean":
        slider_mean = [
            ("Radius (mean)", "radius_mean"),
            ("Texture (mean)", "texture_mean"),
            ("Perimeter (mean)", "perimeter_mean"),
            ("Area (mean)", "area_mean"),
            ("Smoothness (mean)", "smoothness_mean"),
            ("Compactness (mean)", "compactness_mean"),
            ("Concavity (mean)", "concavity_mean"),
            ("Concave Points (mean)", "concave points_mean"),
            ("Symmetry (mean)", "symmetry_mean"),
            ("Fractal Dimension (mean)", "fractal_dimension_mean")
        ]
        slider_labels = slider_mean
    elif type_feat == "se":
        slider_se =[
            ("Radius (se)", "radius_se"),
            ("Texture (se)", "texture_se"),
            ("Perimeter (se)", "perimeter_se"),
            ("Area (se)", "area_se"),
            ("Smoothness (se)", "smoothness_se"),
            ("Compactness (se)", "compactness_se"),
            ("Concavity (se)", "concavity_se"),
            ("Concave Points (se)", "concave points_se"),
            ("Symmetry (se)", "symmetry_se"),
            ("Fractal Dimension (se)", "fractal_dimension_se")
        ]
        slider_labels = slider_se
    else:
        slider_worst =[
            ("Radius (worst)", "radius_worst"),
            ("Texture (worst)", "texture_worst"),
            ("Perimeter (worst)", "perimeter_worst"),
            ("Area (worst)", "area_worst"),
            ("Smoothness (worst)", "smoothness_worst"),
            ("Compactness (worst)", "compactness_worst"),
            ("Concavity (worst)", "concavity_worst"),
            ("Concave Points (worst)", "concave points_worst"),
            ("Symmetry (worst)", "symmetry_worst"),
            ("Fractal Dimension (worst)", "fractal_dimension_worst")
        ]
        slider_labels = slider_worst

    input_dict = {}

    for label, key in slider_labels:
        input_dict[key] = st.slider(
            label,
            min_value= float(0),
            max_value= float(data[key].max()),
            value = float(data[key].mean())
        )

    return input_dict

def get_scaled_val(input_dict):
    data = get_clean_data()

    X = data.drop(['diagnosis'], axis = 1)

    scaled_dict = {}

    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()

        scaled_val = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_val

    return scaled_dict

def get_radar_chart(input_data):

    input_data  = get_scaled_val(input_data)
    categories = ['Radius', 'Texture', 'Perimeter', 'Area',
                  'Smoothness', 'Compactness', 'Concavity',
                  'Concave Points', 'Symmetry', 'Fractal Dimension']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
            input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
            input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
            input_data['fractal_dimension_mean']
        ],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'],
            input_data['area_se'], input_data['smoothness_se'], input_data['compactness_se'],
            input_data['concavity_se'], input_data['concave points_se'], input_data['symmetry_se'],
            input_data['fractal_dimension_se']
        ],
        theta=categories,
        fill='toself',
        name='Standard Error'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
            input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
            input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
            input_data['fractal_dimension_worst']
        ],
        theta=categories,
        fill='toself',
        name='Worst Value'
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
    model = pickle.load(open("../model/model.pkl", "rb"))
    scaler = pickle.load(open("../model/scaler.pkl", "rb"))

    input_array = np.array(list(input_data.values())).reshape(1, -1)

    input_array_scaled = scaler.transform(input_array)

    prediction = model.predict(input_array_scaled)

    st.subheader("Cell Cluster Prediction")
    st.write("The cell cluster is: ")

    if prediction[0] == 0:
        st.write("<span class='diagnosis benign'>Benign</span>", unsafe_allow_html = True)
    else:
        st.write("<span class='diagnosis malignant'>Malignant</span>", unsafe_allow_html = True)


    st.write("Probability of being benign: ", model.predict_proba(input_array_scaled)[0][0])
    st.write("Probability of being malignant: ", model.predict_proba(input_array_scaled)[0][1])

    st.write("This app can assist medical professionals but should not be used to replace professional diagnosis")



def show_bc():
    
    with open("../assets/style.css") as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html = True)

    #input_data = add_sidebar()

    with st.container():
        st.title("Breast Cancer Predictor")
        st.page_link("https://www.kaggle.com/datasets/yasserh/breast-cancer-dataset/data", label = "Kaggle Link", icon = "🔗")
        st.write("Using the dataset from Kaggle, we will predict if the cyst could be a malignant breast cancer tumor. \
                 As a kind reminder, this application does not serve to replace professional diagnosis. \
                 This dataset has biopsy features for classification of 569 malignant and benign breast masses. \
                 SE represents the standard error of the feature, while Worst means the largest or most severe value of the feature.\
                  All credits go to @Alejandro AO - Software & AI")
    
    
    col1, col2 = st.columns([4,1])
    sliderm, sliderse, sliderw = st.columns(3)

    with sliderm:
        input_mean = add_sliders("mean")
    with sliderse:
        input_se = add_sliders("se")
    with sliderw:
        input_w = add_sliders("worst")

    input_data = {**input_mean, **input_se, **input_w}

    with col1:
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart)

    with col2:
        add_predictions(input_data)
        
