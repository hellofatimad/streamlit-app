#import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle
import shap
import matplotlib.pyplot as plt

#st.set_page_config(layout = 'wide', initial_sidebar_state = 'expanded')
#st.title("Predicting Breast Cancer")

def create_model(data):
    X = data.drop(['diagnosis'], axis = 1)
    y = data['diagnosis']

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    #test model
    y_pred = model.predict(X_test)
    print('Accuracy of our model: ', accuracy_score(y_test, y_pred))
    print("Classification report: \n", classification_report(y_test, y_pred))

    return model, scaler



def get_clean_data():
    data = pd.read_csv('../breast-cancer.csv')
    
    data = data.drop('id', axis = 1)

    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

    return data

def main():
    data = get_clean_data()
    
    model, scaler = create_model(data)

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

if __name__ == '__main__':
    main()



