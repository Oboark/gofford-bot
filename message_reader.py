import json
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

with open('data/messages.json') as f:
        messages = json.load(f)

hour_msg = np.zeros(24)

for a in messages:
    for b in messages[a]:
        hour = b['t'].split('/')[3]
        hour_msg[int(hour)] += 1
        print(hour)

print(hour_msg)
plt.plot(hour_msg)
plt.xlabel('Hour')
plt.ylabel('Number of Messages')
plt.show()
