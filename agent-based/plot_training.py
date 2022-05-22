import pickle
import copy
import matplotlib.pyplot as plt

f = open("log_training.dict", "rb")
results = pickle.load(f)

size_data = results["size_data"]
accuracy_data = results["win_rate"]

x = list(range(len(size_data)))
x = [a*10 for a in x]   #Convert from 10k to 1k
figure, axis = plt.subplots(1, 2)
axis[0].plot(x, size_data)
axis[0].set_xlabel("Iterations (thousands)")
axis[0].set_ylabel("Nodes expanded")
axis[1].plot(x, accuracy_data)
axis[1].set_xlabel("Iterations (thousands)")
axis[1].set_ylabel("Win rate")

plt.show()       

