
import numpy as np

np.random.seed(1)

# 1000 random integers between 0 and 50
x = np.random.randint(0, 50, 1000)

# Positive Correlation with some noise
y = x + np.random.normal(0, 10, 1000)


data = []
print(x)
data.append(x)
data.append(y)
data.append(y)



print(np.corrcoef(data))