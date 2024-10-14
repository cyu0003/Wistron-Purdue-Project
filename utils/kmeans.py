import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def make_df(data):
    return pd.DataFrame(data)

def normalize_df(df):
    return (df-df.mean())/df.std()

def kmeans(df, c):
    kmeans = KMeans(n_clusters=c, init='k-means++', max_iter=500, random_state=0)
    kmeans.fit(df.values)
    df['cluster'] = kmeans.labels_
    return df

def visualize(df, c):
    pca = PCA(2)
    pca_res = pca.fit_transform(df)
    df['x'] = pca_res[:, 0]
    df['y'] = pca_res[:, 1]

    for i in range(0, c):
        cluster = df[df['cluster'] == i]
        plt.scatter(cluster['x'], cluster['y'], label=f'Cluster {i}')

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()