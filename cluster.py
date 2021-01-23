from sklearn.cluster import KMeans


def cluster(X, clust_num):
    km = KMeans(
        n_clusters=clust_num, init='random',
        n_init=10, max_iter=300, 
        tol=1e-04, random_state=0
    )
    km.fit(X)

    return km.labels_