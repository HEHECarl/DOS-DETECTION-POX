from sklearn.cluster import KMeans


class KMean:
    def __init__(self):
        self.data_array = []
        self.model = KMeans(n_clusters=2, init='k-means++')

    def add_data(self, data):
        self.data_array.append(data)

    def fit(self):
        self.model.fit(self.data_array)

    def predict(self, data):
        return self.model.predict(data)