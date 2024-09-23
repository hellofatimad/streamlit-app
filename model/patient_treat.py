import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle

#models
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

def get_clean_data():
    data = pd.read_csv('data-ori.csv')

    data['SEX'] = data['SEX'].map({'F': 1, 'M': 0})

    data['SOURCE'] = data['SOURCE'].map({'in': 1, 'out': 0})

    return data

def create_model(data):
    X = data.drop(['SOURCE'], axis = 1)
    y = data['SOURCE']

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

    model = RandomForestClassifier(max_features = None, n_estimators = 200)
    model.fit(X_train, y_train)

    #test model
    y_pred = model.predict(X_test)
    print('Accuracy of our model: ', accuracy_score(y_test, y_pred))
    print("Classification report: \n", classification_report(y_test, y_pred))

    return model, scaler

def main():
    data = get_clean_data()
    
    model, scaler = create_model(data)

    with open('ptmodel.pkl', 'wb') as f:
        pickle.dump(model, f)

    with open('ptscaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

if __name__ == '__main__':
    main()