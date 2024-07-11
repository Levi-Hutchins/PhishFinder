import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from api.scripts.config.paths_config import DATA, MODEL_PATH
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# These are the features I selected to be most important when identifying a phishing link
features = [
    "having_IPhaving_IP_Address", # URL contains IP
    "URLURL_Length", # Length of the URL
    "having_At_Symbol", # URL contains @
    "Shortining_Service", # Long URL shorted eg. bit.ly...
    "double_slash_redirecting", # URL contains redirect to another site
    "having_Sub_Domain", # www.aus.go.au
    "SSLfinal_State", # URL uses HTTPS
    "Domain_registeration_length", # URL domain is registed for short period 
    "HTTPS_token", # URL contains http://https
    #"Google_Index", # Can be find via google or not- DROPPED
    #"Page_Rank", # Measures how important a page is on the internet 0 or 1 DROPPED
    #"port", # Scammers open all ports on there server to allow all services

    ]

df = shuffle(pd.read_csv(DATA))

df.dropna(inplace=True)

print(df.head)


X = df[features]
Y = df["Result"]

print(X.shape, Y.shape)

# X shape (11055, 16)
# Y shape (11055)
X.drop_duplicates()
Y.drop_duplicates()

X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.8, test_size=0.2, shuffle=True)

# Parameters were found via hyper parameter tuning doing in ProjectPrepML
knn_classifier = KNeighborsClassifier(
    n_neighbors=10,
    leaf_size=20,
    metric='minkowski',
    p=1,
    weights='distance'

)
knn_classifier.fit(X_train, y_train)
y_pred = knn_classifier.predict(X_test)



# Stats
print("---------- Model Statistics ----------\n")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1 Score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n--------------------------------------")


# pkl can be subjected to arbitrary code execution so switched to onnx 
# which is faster and more secure
initial_type = [('float_input', FloatTensorType([None, X_train.shape[1]]))]

onnx_model = convert_sklearn(knn_classifier, initial_types=initial_type)

with open(MODEL_PATH, "wb") as f:
    f.write(onnx_model.SerializeToString())

