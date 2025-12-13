import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import openpyxl
from sklearn.linear_model import LinearRegression

# requests example
response = requests.get("https://www.google.com")
print("Status code:", response.status_code)

# numpy example
arr = np.array([1, 2, 3, 4])
print("Numpy array mean:", np.mean(arr))

# pandas example
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
print("Pandas DataFrame:\n", df)

# matplotlib example
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Simple Plot")
plt.show()

# beautifulsoup4 example
soup = BeautifulSoup(response.text, 'html.parser')
print("Title tag:", soup.title)

# openpyxl example
wb = openpyxl.Workbook()
ws = wb.active
ws['A1'] = "Hello Excel"
wb.save("sample.xlsx")

# scikit-learn example
X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])
model = LinearRegression()
model.fit(X, y)
print("Prediction for 5:", model.predict([[5]]))