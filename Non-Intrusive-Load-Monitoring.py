from sklearn.preprocessing import OneHotEncoder,LabelEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
import matplotlib
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from keras.models import Sequential
from tensorflow.python.keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional
from keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv ('/content/X_train.csv')
data.head()
#checking for null values

data.isna().sum()
data.dropna(axis=0,inplace=True)
string_columns = list(data.select_dtypes(include=['object','bool']).columns)
le = LabelEncoder()
encoded_data=data[string_columns].apply(le.fit_transform)
data.drop(string_columns ,axis=1, inplace=True)
data = pd.concat([data, encoded_data ], axis=1)
data.head()

#correlation
corr= data[data.columns].corr()['appliance_name']
corr=corr[((corr >=0.5) | (corr <= -0.2)) & (corr < 0.9) ]
print(corr)
selected_features=list(corr.index)
selected_features_df=data[selected_features]
selected_features_df

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(12,10))
cor = selected_features_df.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

X_train=selected_features_df[["current","harmonic_ratio_3","harmonic_ratio_5","transient_7","active_power"]]

X_train.head()

y_train=data['appliance_name']

X_test=pd.read_csv('/content/X_test.csv')
X_test.dropna(axis=0,inplace=True)
string_columns = list(X_test.select_dtypes(include=['object','bool']).columns)

le = LabelEncoder()
encoded_data=X_test[string_columns].apply(le.fit_transform)
X_test.drop(string_columns ,axis=1, inplace=True)
X_test = pd.concat([X_test, encoded_data ], axis=1)
# X_test=X_test[selected_features]
X_test=X_test[["current","harmonic_ratio_3","harmonic_ratio_5","transient_7","active_power"]]


y_test= pd.read_csv('/content/X_test_result.csv')
y_test=le.fit_transform(y_test['appliance_name'].astype(str))
for n, i in enumerate(y_test):
  if i == 2:
    y_test[n] = 0


from sklearn.ensemble import RandomForestClassifier
forest_clf = RandomForestClassifier(n_estimators=150)
forest_clf.fit(X_train,y_train)
y_pred_rf = forest_clf.predict(X_test)


print("Accuracy:",metrics.accuracy_score(y_test, y_pred_rf))

from sklearn.metrics import confusion_matrix
conf_matrix=confusion_matrix(y_test,y_pred_rf)
fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
 
plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()
