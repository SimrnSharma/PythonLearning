import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# Load data from CSV files (as an example)
public_transport_data = pd.read_csv('public_transport_gps_data.csv')
traffic_sensor_data = pd.read_csv('traffic_sensor_data.csv')
user_travel_logs = pd.read_csv('user_travel_logs.csv')

# Convert timestamps to datetime format
public_transport_data['timestamp'] = pd.to_datetime(public_transport_data['timestamp'])
traffic_sensor_data['timestamp'] = pd.to_datetime(traffic_sensor_data['timestamp'])
user_travel_logs['start_time'] = pd.to_datetime(user_travel_logs['start_time'])

# Merge DataFrames based on the appropriate keys
# This example assumes some common keys like 'timestamp' and proximity for merging
# In practice, you may need more sophisticated spatial joins based on coordinates
merged_data = pd.merge_asof(public_transport_data.sort_values('timestamp'), 
                            traffic_sensor_data.sort_values('timestamp'), 
                            on='timestamp', direction='nearest')


# Calculate distances between coordinates
def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate the distance between two lat/lon points
    R = 6371  # Earth radius in kilometers
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c
    return distance

# Example usage to calculate distances between start and end points in user travel logs
user_travel_logs['distance_km'] = user_travel_logs.apply(lambda row: haversine(row['start_lat'], row['start_lon'], row['end_lat'], row['end_lon']), axis=1)

# Identify peak hours
user_travel_logs['hour'] = user_travel_logs['start_time'].dt.hour
peak_hours = user_travel_logs.groupby('hour').size()

# Determine popular routes
popular_routes = user_travel_logs.groupby(['start_lat', 'start_lon', 'end_lat', 'end_lon']).size().reset_index(name='counts')

# Identify congestion hotspots
congestion_hotspots = traffic_sensor_data.groupby(['sensor_id', 'location_lat', 'location_lon']).agg({'vehicle_count': 'sum', 'average_speed': 'mean'}).reset_index()

# Visualization
plt.figure(figsize=(10, 6))
sns.scatterplot(x='location_lon', y='location_lat', size='vehicle_count', hue='average_speed', data=congestion_hotspots, palette='coolwarm', sizes=(20, 200))
plt.title('Congestion Hotspots')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Average Speed')

# Correlation analysis
merged_data['public_transport_usage'] = merged_data['vehicle_id'].notna().astype(int)
correlation = merged_data[['public_transport_usage', 'vehicle_count']].corr()
print(correlation)


# Clustering user travel routes
route_coordinates = user_travel_logs[['start_lat', 'start_lon', 'end_lat', 'end_lon']]
kmeans = KMeans(n_clusters=2)  
user_travel_logs['route_cluster'] = kmeans.fit_predict(route_coordinates)

# Analyze clusters to suggest route optimizations
optimized_routes = user_travel_logs.groupby('route_cluster').agg({'start_lat': 'mean', 'start_lon': 'mean', 'end_lat': 'mean', 'end_lon': 'mean'}).reset_index()

print("Suggested new routes based on clusters:")
print(optimized_routes)
plt.show()
