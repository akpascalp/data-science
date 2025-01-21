import requests
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.metrics import jaccard_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
import sklearn.metrics as metrics
from io import StringIO

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillUp/labs/ML-FinalAssignment/Weather_Data.csv"

def fetch_data(url):
    response = requests.get(url, verify=True)
    return pd.read_csv(StringIO(response.text))


df = fetch_data(URL)

df.head()

df_sydney_processed = pd.get_dummies(
    data=df, columns=["RainToday", "WindGustDir", "WindDir9am", "WindDir3pm"]
)
# Convert 'RainTomorrow' to numeric
df_sydney_processed['RainTomorrow'] = df_sydney_processed['RainTomorrow'].map({'Yes': 1, 'No': 0})


df_sydney_processed.drop("Date", axis=1, inplace=True)
df_sydney_processed = df_sydney_processed.astype(float)
features = df_sydney_processed.drop(columns="RainTomorrow", axis=1)
Y = df_sydney_processed["RainTomorrow"]

x_train, x_test, y_train, y_test = train_test_split(
    features, Y, test_size=0.2, random_state=10
)

LinearReg = LinearRegression()
LinearReg.fit(x_train, y_train)

predictions = LinearReg.predict(x_test)

LinearRegression_MAE = metrics.mean_absolute_error(y_test, predictions)
LinearRegression_MSE = metrics.mean_squared_error(y_test, predictions)
LinearRegression_R2 = metrics.r2_score(y_test, predictions)

Report = pd.DataFrame(
    {
        "Metric": ["Mean Absolute Error", "Mean Squared Error", "R2 Score"],
        "Value": [LinearRegression_MAE, LinearRegression_MSE, LinearRegression_R2],
    }
)
print(Report)


KNN = KNeighborsClassifier(n_neighbors=4).fit(x_train, y_train)

predictions = KNN.predict(x_test)
KNN_Accuracy_Score = metrics.accuracy_score(y_test, predictions)
KNN_JaccardIndex = jaccard_score(y_test, predictions)
KNN_F1_Score = f1_score(y_test, predictions)

Report = pd.DataFrame(
    {
        "Metric": ["Accuracy Score", "Jaccard Index", "F1 Score"],
        "Value": [KNN_Accuracy_Score, KNN_JaccardIndex, KNN_F1_Score],
    }
)
print(Report)

Tree = DecisionTreeClassifier(criterion="entropy", max_depth=4).fit(x_train, y_train)
predictions = Tree.predict(x_test)
Tree_Accuracy_Score = metrics.accuracy_score(y_test, predictions)
Tree_JaccardIndex = jaccard_score(y_test, predictions)
Tree_F1_Score = f1_score(y_test, predictions)

Report = pd.DataFrame(
    {
        "Metric": ["Accuracy Score", "Jaccard Index", "F1 Score"],
        "Value": [Tree_Accuracy_Score, Tree_JaccardIndex, Tree_F1_Score],
    }
)
print(Report)


x_train, x_test, y_train, y_test = train_test_split(
    features, Y, test_size=0.2, random_state=1
)


LR = LogisticRegression(C=0.01, solver="liblinear").fit(x_train, y_train)
predictions = LR.predict(x_test)
predict_proba = LR.predict_proba(x_test)
LR_Accuracy_Score = metrics.accuracy_score(y_test, predictions)
LR_JaccardIndex = jaccard_score(y_test, predictions)
LR_F1_Score = f1_score(y_test, predictions)
LR_Log_Loss = log_loss(y_test, predictions)

Report = pd.DataFrame(
    {
        "Metric": ["Accuracy Score", "Jaccard Index", "F1 Score", "Log Loss"],
        "Value": [LR_Accuracy_Score, LR_JaccardIndex, LR_F1_Score, LR_Log_Loss],
    }
)
print(Report)


SVM = svm.SVC(kernel="rbf").fit(x_train, y_train)
predictions = SVM.predict(x_test)
SVM_Accuracy_Score = metrics.accuracy_score(y_test, predictions)
SVM_JaccardIndex = jaccard_score(y_test, predictions)
SVM_F1_Score = f1_score(y_test, predictions)


Report = pd.DataFrame(
    {
        "Metric": ["Accuracy Score", "Jaccard Index", "F1 Score"],
        "Value": [SVM_Accuracy_Score, SVM_JaccardIndex, SVM_F1_Score],
    }
)
print(Report)
