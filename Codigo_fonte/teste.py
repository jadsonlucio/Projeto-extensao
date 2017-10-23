import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")
data = [[1,2,3,5],[1,2,3,4],[1,2,3,5],[1,2,3,4],[1,2,3,5],[1,2,3,4]]
print(data)
sns.boxplot(data=data,color="blue");
plt.plot([1,2,3,4,5])
plt.show()