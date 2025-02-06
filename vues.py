from flask import request, jsonify, send_file, make_response
import joblib
import os
import zipfile
import csv, json
from .treatment import create_model
from . import app, db, pd
from .models import Signatures



X_train_columns = ["Flow_Duration","Src_Port", "Dst_Port", "Init_Bwd_Win_Byts", "Flow_IAT_Min", "Bwd_PSH_Flags"]

# Fonctions pour vérifier les conditions
def is_condition_satisfied(condition, sample, feature_names):
    feature, operator, threshold = condition.split(" ")
    threshold = float(threshold)

    try:
        feature_index = feature_names.index(feature)
    except ValueError:
        return False

    if operator == "<=":
        return sample[feature_index] <= threshold
    elif operator == ">":
        return sample[feature_index] > threshold
    return False

def is_signature_satisfied(signature, sample, feature_names):
    conditions = signature["Conditions"].split(" AND ")
    return all(is_condition_satisfied(condition, sample, feature_names) for condition in conditions)


    
def check_signature(sample, feature_names, signatures):
    if signatures is not None:
        for index, signature in signatures.iterrows():
            if is_signature_satisfied(signature, sample, feature_names):
                return signature["condition"], signature["Classes"]
    return None, None

@app.route('/')  # Définir la route racine
def home():
    return jsonify({"message": "Hello-world"}), 200

@app.route('/init-model', methods=["GET"])
def init():
    # Chemin du fichier ZIP
    zip_path = "dataset/dataset.zip"
    # Décompresser le fichier ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('dataset')
    if os.path.exists("dataset/dataset.csv"):
        create_model("dataset/dataset.csv")
        os.remove("dataset/dataset.csv")
        if os.path.exists("dataset/reste.csv"):
            with open("dataset/reste.csv", mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                # Convertir les lignes CSV en une liste de dictionnaires
                rows = list(csv_reader)
            # Sauvegarder la liste en fichier JSON
            with open("dataset/fichier_test.json", mode='w', encoding='utf-8') as json_file:
                json.dump(rows, json_file, indent=4)
            return send_file("dataset/fichier_test.json", as_attachment=True)
        else:
            return jsonify({"message": "Le fichier reste.csv n'existe pas"}), 400

@app.route('/predict', methods=["POST"])
def predict():
    try:
        signatures = pd.read_csv("model_files/signature_cleaned.csv")
    except FileNotFoundError:
        print("Le fichier signature_cleaned.csv n'existe pas.")
        signatures = pd.DataFrame(columns=["Conditions", "Classes"])

    try:
        decision_tree_model = joblib.load('model_files/intrusion_detection_model.pkl')
        scaler = joblib.load('model_files/scaler.pkl')
    except FileNotFoundError:
        print("Les fichiers du modèle ou du scaler n'existent pas.")
        decision_tree_model = None
        scaler = None
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Les données doivent être une liste"}), 400
        for row in data:
            data_frame = pd.DataFrame([row])[X_train_columns]
            new_data_scaled = scaler.transform(data_frame)
            sample = new_data_scaled[0]
            condition, signature_class = check_signature(sample, X_train_columns, signatures)
            signtre = Signatures(
                classe = str(signature_class),
                condition = str(condition),
                data = str(data_frame.to_dict(orient="records")[0])
            )
            db.session.add(signtre)
            db.session.commit()
        return jsonify({
            "message": "Analyse terminé"
        }), 201
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500
    