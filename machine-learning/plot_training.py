import pickle
import sys
from matplotlib import pyplot as plt

file_name = sys.argv[1]

f = open(file_name, 'rb')
log = pickle.load(f)

avg_returns = [item[1]["average_return"][0] for item in log.items()]
avg_preds = [sum(item[1]["train_episode_pred_acc"]) / len(item[1]["train_episode_pred_acc"]) for item in log.items()]

c = 5
smoothed_returns = []
for i in range(len(avg_returns)):
	start = max(0, i-c)
	end = min(len(avg_returns), i+c)
	l = avg_returns[start:end]
	smoothed_returns.append(sum(l) / len(l))	

smoothed_preds = []
for i in range(len(avg_preds)):
	start = max(0, i-c)
	end = min(len(avg_preds), i+c)
	l = avg_preds[start:end]
	smoothed_preds.append(sum(l) / len(l))	

figure, axis = plt.subplots(2, 1)
axis[0].plot(smoothed_returns)
axis[1].plot(smoothed_preds)

plt.savefig("plot.png")

