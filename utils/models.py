import pickle

def load_model():
    # Import model to make prediction
    with open('model/strategy2_group_target/outliers_99/best_all3.pkl', 'rb') as file:
        model = pickle.load(file)
        return model

def make_prediction(model, X):
    return model.predict(X)