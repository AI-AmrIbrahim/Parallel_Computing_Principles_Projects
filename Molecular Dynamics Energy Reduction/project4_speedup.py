import pandas as pd
import matplotlib.pyplot as plt

data = {
    'P': [1, 1, 1, 4, 4, 4, 16, 16, 16, 64, 64, 64],
    'Fraction': [0.1, 0.5, 0.9, 0.1, 0.5, 0.9, 0.1, 0.5, 0.9, 0.1, 0.5, 0.9],
    'Initial Energy': [-6010.79030307, -6010.79030307, -6010.79030307,
                       -6010.79030306, -6010.79030306, -6010.79030306,
                       -6010.79030306, -6010.79030306, -6010.79030306,
                       -6010.79030306, -6010.79030306, -6010.79030306],
    'Minimum Energy': [-6012.31777504, -6013.36585479, -6014.39005333,
                       -6012.6664686, -6013.3171345, -6014.42925736,
                       -6011.84205178, -6012.66891402, -6012.04099322,
                       -6012.37250236, -6012.03550331, -6011.63768983],
    'Time Elapsed': [682.897049189, 686.969769239, 687.065406799,
                     169.902790308, 169.922741652, 169.917728901,
                     47.1361758709, 46.409920454, 46.4585399628,
                     13.7131843567, 12.9807114601, 12.9994375706]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate average time for each P
average_time_per_p = df.groupby('P')['Time Elapsed'].mean()
df['Average Time'] = df['P'].map(average_time_per_p)

# Calculate speedup relative to P=1
df['Speedup'] = df['Average Time'][0] / df['Average Time']

# Plot speedup curve
plt.figure(figsize=(10, 6))
plt.plot(df['P'], df['Speedup'], marker='o', linestyle='-', color='b', label='Speedup')
plt.axline(xy1=(0, 0), slope=1, linestyle='--', color='black', label='Optimal Speedup')

plt.title('Speedup Curve for Parallel Computing')
plt.xlabel('Number of Processes (P)')
plt.ylabel('Speedup (Relative to P=1)')
plt.legend()
plt.xticks(range(0, 71, 10))  # Set x-axis ticks from 1 to 70
plt.yticks(range(0, 71, 10))
plt.grid(True)
plt.show()
