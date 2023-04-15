

clusters_one_time_wind = dict()

number_of_clusters = 7

for i in range(10):
    clusters_one_time_wind[i] = i*2

print(clusters_one_time_wind)



clusters_one_time_wind_offshore = dict()
keys = list(clusters_one_time_wind.keys())
keys_offshore = keys[number_of_clusters:]
i = 0
for key in keys_offshore:
    clusters_one_time_wind_offshore[i] = clusters_one_time_wind[key]
    del clusters_one_time_wind[key]
    i += 1


print(clusters_one_time_wind)
print(clusters_one_time_wind_offshore)
