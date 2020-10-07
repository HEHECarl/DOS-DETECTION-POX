from sklearn.neighbors import KNeighborsClassifier


class KNN:
    def __init__(self):
        self.data_array = []
        self.class_array = []
        self.model = KNeighborsClassifier(n_neighbors=5)

    def add_data(self, data, cls):
        self.data_array.append(data)
        self.class_array.append(cls)

    def import_Data(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        for line in lines:
            self.add_data([int(line.split()[0]), int(line.split()[1])], int(line.split()[2]))

    def fit(self):
        self.model.fit(self.data_array, self.class_array)

    def predict(self, data):
        return self.model.predict(data)
