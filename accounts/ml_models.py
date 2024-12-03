import joblib
from sklearn.linear_model import LinearRegression

def train_model(X, y):
    # Train your linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    return model

def save_model(model, filename):
    # Save the trained model
    joblib.dump(model, filename)


