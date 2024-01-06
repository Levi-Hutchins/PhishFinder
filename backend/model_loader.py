import joblib
def make_prediction(values):
    model = joblib.load('./pkl/model.pkl')
    y_predict = model.predict(values)
    return y_predict

print(make_prediction([[1,-1,0,0,1,-1,-1,1,1,1,0,-1,1,0,0,-1]]))