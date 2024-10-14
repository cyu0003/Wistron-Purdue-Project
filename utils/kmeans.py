import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def make_df(data):
    df = pd.DataFrame(data)
    return df.drop('id', axis='columns')

def normalize_df(df):
    return (df-df.mean())/df.std()

def kmeans(df, c):
    kmeans = KMeans(n_clusters=c, init='k-means++', max_iter=500, random_state=0)
    kmeans.fit(df.values)
    df['cluster'] = kmeans.labels_
    return df

def visualize(df):
    pca = PCA(2)
    pca_res = pca.fit_transform(df)
    df['x'] = pca_res[:, 0]
    df['y'] = pca_res[:, 1]

    cluster0 = df[df['cluster'] == 0]
    cluster1 = df[df['cluster'] == 1]
    cluster2 = df[df['cluster'] == 2]

    plt.scatter(cluster0['x'], cluster0['y'], label = 'C 0')
    plt.scatter(cluster1['x'], cluster1['y'], label = 'C 1')
    plt.scatter(cluster2['x'], cluster2['y'], label = 'C 2')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()