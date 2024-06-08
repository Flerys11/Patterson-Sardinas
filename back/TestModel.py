import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
from aletoire_binaire import get_donnee_verif
from Autre import find


class CodeClassifier:
    def __init__(self):
        self.model = RandomForestClassifier()

    def read_data_from_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def generate_verification_data(self, data):
        return get_donnee_verif(data)

    def result_algo(self, data):
        return find(data)

    def prepare_data(self, data):
        caracteristiques = []
        labels = []

        for entry in data:
            nombre_de_mots = entry[0]
            bit_freq = entry[1]
            info_complexity = entry[2]
            bit_density_value = entry[3]
            stats = entry[4]
            results = entry[5]

            features = [
                nombre_de_mots,
                bit_freq['0'], bit_freq['1'],
                info_complexity,
                bit_density_value,
                stats.get('ok', 0), stats.get('vide', 0)
            ]
            caracteristiques.append(features)

            labels.append(int(results))

        caracteristiques = np.array(caracteristiques)
        labels = np.array(labels)
        return caracteristiques, labels

    def train(self, file_path):
        data = self.read_data_from_file(file_path)
        X, y = self.prepare_data(data)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)
        score = accuracy_score(y_test, predictions)
        print(f"Score d'accord: {score * 100:.2f}%")

    def predict(self, new_data):
        processed_data = []

        for entry in new_data:
            nombre_de_mots = entry[0]
            bit_freq = entry[1]
            info_complexity = entry[2]
            bit_density_value = entry[3]
            stats = entry[4]

            features = [
                nombre_de_mots,
                bit_freq['0'], bit_freq['1'],
                info_complexity,
                bit_density_value,
                stats.get('ok', 0), stats.get('vide', 0)
            ]
            processed_data.append(features)

        processed_data = np.array(processed_data)
        predictions = self.model.predict(processed_data)

        return ['True' if pred else 'False' for pred in predictions]


app = Flask(__name__)

app = Flask(__name__)
CORS(app)

classifier = CodeClassifier()
file_path = 'stock_donnee.txt'
classifier.train(file_path)


@app.route('/predict', methods=['POST'])
def predict():
    request_data = request.json
    source = request_data.get('source')
    if not source:
        return jsonify({'error': 'No source provided'}), 400

    verification_data = classifier.generate_verification_data(source)
    predictions = classifier.predict(verification_data)
    return jsonify({'predictions': predictions})

@app.route('/sd', methods=['POST'])
def sd():
    request_data = request.json
    source = request_data.get('source')
    if not source:
        return jsonify({'error': 'No source provided'}), 400

    # results = classifier.verification_code(source)
    # formatted_results = classifier.format_results(results)
    formatted_results = classifier.result_algo(source)
    return jsonify({'Resultats Sardinas Patterson': formatted_results})

if __name__ == "__main__":
    app.run(debug=True)
