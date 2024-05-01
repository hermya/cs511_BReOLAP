# Re-plotting the graph with the updated values after the execution reset
import matplotlib.pyplot as plt
import numpy as np


# Restored data
data_rows = [50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 12800000]
avg_query_time_clickhouse = [0.022663068, 0.029992148, 0.0551334, 0.085294295, 0.191208181, 0.279847713, 0.835593477, 1.661534449, 2.995554958]
avg_query_time_pinot = [0.069887049, 0.089898966, 0.133202959, 0.269089524, 0.579836381, 1.234116344, 2.545039265] + [None, None]
avg_query_time_druid = [0.197280274, 0.435512761, 0.815685253, 1.546365054,2.97170546] + [ None, None, None, None]
avg_query_time_starrocks = [0.028272358, 0.028422352, 0.036710731, 0.050109521, 0.088488675, 0.161077829, 0.314793154, 0.515610712, 1.000044542]

# Plotting the line graph
plt.figure(figsize=(12, 8))
plt.plot(data_rows, avg_query_time_clickhouse, label='ClickHouse', marker='o', color='red')
plt.plot(data_rows[:len(avg_query_time_pinot)], avg_query_time_pinot, label='Pinot', marker='o', color='blue')
plt.plot(data_rows[:len(avg_query_time_druid)], avg_query_time_druid, label='Druid', marker='o', color='green')
plt.plot(data_rows, avg_query_time_starrocks, label='StarRocks', marker='o', color='purple')

plt.xlabel('Number of Data Rows')
plt.ylabel('Average Query Time (seconds)')
plt.title('Average Query Time vs. Number of Data Rows for Different Databases')
plt.legend(prop={'size': 14, 'weight': 'bold'})
#plt.grid(False, which='both', linestyle='-', linewidth='0.5')
plt.xscale('log')
plt.yscale('log')

minor_ticks = np.power(2, np.arange(0, 9, 1)) * 50000  # More finely spaced ticks
#print(minor_ticks)
plt.xticks(data_rows, minor_ticks, rotation = 'horizontal')

ytick_values = [0.0125, 0.025, 0.05, 0.2, 0.4, 1.6, 3.2, 6.4]

plt.gca().set_yticks(ytick_values, minor=True)
plt.gca().set_yticklabels([f'{value:.2f}' for value in ytick_values], minor=True)

plt.show()


# Re-plotting the graph with the updated values after the execution reset
import matplotlib.pyplot as plt
import numpy as np


# Restored data
data_rows = [50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 12800000]
avg_query_time_clickhouse = [0.008328631,
0.008801806,
0.013436792,
0.018865414,
0.018213031,
0.025161971,
0.04223787,
0.071986358,
0.126461899
]
avg_query_time_pinot = [0.060131228,
0.065084628,
0.065590235,
0.070159194,
0.102210164,
0.136284787,
0.20533103
] + [None, None]
avg_query_time_druid = [0.01879611,
0.016649843,
0.032503036,
0.050864115,
0.053049225
] + [ None, None, None, None]
avg_query_time_starrocks = [0.013122679,
0.014679038,
0.021244861,
0.036795424,
0.059944932,
0.114232966,
0.226253925,
0.205402757,
0.346676485
]

# Plotting the line graph
plt.figure(figsize=(12, 8))
plt.plot(data_rows, avg_query_time_clickhouse, label='ClickHouse', marker='o', color='red')
plt.plot(data_rows[:len(avg_query_time_pinot)], avg_query_time_pinot, label='Pinot', marker='o', color='blue')
plt.plot(data_rows[:len(avg_query_time_druid)], avg_query_time_druid, label='Druid', marker='o', color='green')
plt.plot(data_rows, avg_query_time_starrocks, label='StarRocks', marker='o', color='purple')

plt.xlabel('Number of Data Rows')
plt.ylabel('Average Query Time (seconds)')
plt.title('Average Query Time vs. Number of Data Rows for Different Databases')
plt.legend(prop={'size': 14, 'weight': 'bold'})
#plt.grid(True, which='both', linestyle='-', linewidth='0.5')
plt.xscale('log')
plt.yscale('log')

minor_ticks = np.power(2, np.arange(0, 9, 1)) * 50000  # More finely spaced ticks
#print(minor_ticks)
plt.xticks(data_rows, minor_ticks, rotation = 'horizontal')

ytick_values = [0.01, 0.02, 0.05, 0.1, 0.15, 0.25]

plt.gca().set_yticks(ytick_values, minor=True)
plt.gca().set_yticklabels([f'{value:.2f}' for value in ytick_values], minor=True)

# plt.gca().set_xticks(data_rows, minor=False)
plt.show()
