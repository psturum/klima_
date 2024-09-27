import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from sklearn.covariance import EllipticEnvelope
from sklearn.cluster import KMeans

# Create the figure with the specified size
fig = plt.figure(figsize=(18, 12))

# Create the map using PlateCarree projection and set extent
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-70, 40, 40, 70])

# Put a background image on for nice sea rendering
ax.stock_img()

# Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

# Add land, coastline, and states features
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(states_provinces, edgecolor='gray')

# Adjust the position of the plot area to reduce whitespace
ax.set_position([0, 0, 1, 1])  # [left, bottom, width, height]

# Save the figure without any whitespace around the map
plt.savefig('foo.png', bbox_inches='tight', pad_inches=0)

# Display the map without whitespace
plt.show()

df = pd.read_csv("co2_data.txt", delimiter=";")

# # Filter rows based on specified conditions
eu = df[(df['lon'] >= -70) & (df['lon'] <= 40) & (df['lat'] >= 40) & (df['lat'] <= 70)]

down_sampled = eu.sample(n=5000, random_state=42)
down_sampled.to_csv('filename.csv', index=False)
# # Extract relevant columns for clustering
data_for_clustering = down_sampled[['emission']]

# # Specify the number of clusters (5 in your case)
num_clusters = 5

# # Perform K-means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
down_sampled['cluster'] = kmeans.fit_predict(data_for_clustering)

# # Use EllipticEnvelope for outlier removal based on 'emission'
envelope = EllipticEnvelope(contamination=0.05)  # Adjust contamination based on your data
envelope.fit(down_sampled[['emission']])
outliers = envelope.predict(down_sampled[['emission']])

# # Filter out outliers
down_sampled_filtered = down_sampled[outliers == 1]

# Extract relevant columns for clustering
data_for_clustering = down_sampled_filtered[['emission']]

# # Specify the number of clusters (5 in your case)
num_clusters = 5

# # Perform K-means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
down_sampled_filtered['cluster'] = kmeans.fit_predict(data_for_clustering)

# # Calculate mean emission for each cluster and sort them
cluster_means = down_sampled_filtered.groupby('cluster')['emission'].mean().sort_values().index

# # Create a mapping from original cluster labels to sorted labels
label_mapping = {cluster: new_label for new_label, cluster in enumerate(cluster_means)}

# # Apply the sorted labels to the 'cluster' column
down_sampled_filtered['cluster_ordered'] = down_sampled_filtered['cluster'].map(label_mapping)
# print(down_sampled_filtered)
# # Create a scatter plot with color-coded points

plt.figure(figsize=(10, 6))

# scatter = plt.scatter([0] * len(df), df['emission'], c=df['cluster_ordered'], cmap='viridis')

# # Set axis labels
plt.xlabel('Constant X-coordinate')
plt.ylabel('Emission')

# # Create legend handles and labels in the correct order
unique_labels = sorted(df['cluster_ordered'].unique())

legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plt.cm.viridis(i / 5), markersize=10) for i in unique_labels]
legend_labels = [f'Cluster {label}' for label in unique_labels]

# # Add legend
plt.legend(legend_handles, legend_labels, title='Cluster')

# # Show the plot
plt.title('Clustering Based on Emission Values (Outliers Removed)')
plt.show()
