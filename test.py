import numpy as np

list = [3, 4, 3, 4, 3, 3, 3, 3, 5, 5, 6]
values, count= np.unique(list,return_counts=True)
print(values)
print(count)
new_list = []
for group in values:
    new_list.append(list.pop(list.index(group)))
print(list)
print(new_list)

