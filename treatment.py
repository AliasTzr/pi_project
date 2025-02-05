from . import pd, np, joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler


def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        return None

# Fonction pour obtenir le chemin dans l'arbre
def get_path(tree, feature_names, sample):
    node = 0
    path = []
    while tree.feature[node] != -2:  # -2 indique une feuille
        feature_name = feature_names[tree.feature[node]]
        threshold = tree.threshold[node]
        if sample[tree.feature[node]] <= threshold:
            path.append(f"{feature_name} <= {threshold}")
            node = tree.children_left[node]
        else:
            path.append(f"{feature_name} > {threshold}")
            node = tree.children_right[node]
    return path

def signature_fct(data, X_train, decision_tree_model, file_type: str):
    if data is not None:
        # Sélectionner les colonnes pertinentes
        data = data[X_train.columns]

        # Standardiser les données
        scaler = StandardScaler()
        scaler.fit(X_train)  # Pour recalculer les paramètres de standardisation
        data_scaled = scaler.transform(data)

        # Prédire les classes
        predicted_classes = decision_tree_model.predict(data_scaled)

        # Obtenir le chemin pour chaque donnée
        feature_names = X_train.columns.tolist()
        results = []
        for i, sample in enumerate(data_scaled):
            path = get_path(decision_tree_model.tree_, feature_names, sample)
            conditions = " AND ".join(path)
            results.append({"Conditions": conditions, "Classes": predicted_classes[i]})

        # Convertir les résultats en DataFrame
        results_df = pd.DataFrame(results)

        if file_type == "reste.csv":
            # Sauvegarder les résultats dans un fichier CSV
            results_df.to_csv("model_files/signature.csv", index=False)
        else:
            # Charger les signatures existantes
            try:
                existing_signatures = pd.read_csv("model_files/signature.csv")
            except FileNotFoundError:
                existing_signatures = pd.DataFrame(columns=["Conditions", "Classes"])

            # Ajouter uniquement les nouvelles signatures
            new_signatures = results_df[~results_df.apply(tuple, axis=1).isin(existing_signatures.apply(tuple, axis=1))]

            # Concaténer les nouvelles signatures avec les signatures existantes
            updated_signatures = pd.concat([existing_signatures, new_signatures], ignore_index=True)

            # Sauvegarder les résultats dans un fichier CSV
            updated_signatures.to_csv("model_files/signature.csv", index=False)
            try:
                data = pd.read_csv("signature.csv")
            except FileNotFoundError:
                print("Le fichier signature.csv n'existe pas.")
                data = pd.DataFrame(columns=["Conditions", "Classes"])

            # Supprimer les doublons
            data_cleaned = data.drop_duplicates()

            # Sauvegarder les données nettoyées dans un nouveau fichier
            data_cleaned.to_csv("model_files/signature_cleaned.csv", index=False)

            # Afficher le nombre total d'enregistrements
            total_records = len(data_cleaned)
            print(f"Le nombre total d'enregistrements après suppression des doublons est : {total_records}")

        print("Les résultats ont été enregistrés dans signature.csv")
    else:
        print("Impossible de charger les données.")


def create_model(dataset_path: str):
    data = pd.read_csv(dataset_path)
    classes = data['Sub_Cat'].unique()
    class_counts = data['Sub_Cat'].value_counts()

    major_classes = class_counts[class_counts > 30000].index
    minor_classes = class_counts[class_counts <= 30000].index

    # Créer des sous-ensembles pour chaque classe
    major_data = []
    minor_data = []

    for cls in major_classes:
        cls_data = data[data['Sub_Cat'] == cls].sample(n=30000, random_state=42)
        major_data.append(cls_data)

    for cls in minor_classes:
        cls_data = data[data['Sub_Cat'] == cls]
        minor_data.append(cls_data)

    # Concaténer les données
    balanced_data = pd.concat(major_data + minor_data)

    # Sur-échantillonnage des classes minoritaires si nécessaire
    ros = RandomOverSampler(random_state=42)
    X_res = balanced_data.drop('Sub_Cat', axis=1)
    y_res = balanced_data['Sub_Cat']
    X_res, y_res = ros.fit_resample(X_res, y_res)

    # Division en entraînement et test
    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42, stratify=y_res)

    # Concaténer les données avec les labels
    train_data = pd.concat([X_train, y_train.to_frame('Sub_Cat')], axis=1)
    test_data = pd.concat([X_test, y_test.to_frame('Sub_Cat')], axis=1)

    # Sauvegarder les données
    train_data.to_csv('model_files/new.csv', index=False)
    test_data.to_csv('model_files/reste.csv', index=False)

    train_data = pd.read_csv('model_files/new.csv')
    test_data = pd.read_csv('model_files/reste.csv')

    # Sélectionner les caractéristiques et la variable cible
    X_train = train_data[['Flow_Duration','Src_Port', 'Dst_Port', 'Init_Bwd_Win_Byts', 'Flow_IAT_Min', 'Bwd_PSH_Flags']] # Select columns as DataFrame
    y_train = train_data['Sub_Cat']

    X_test = test_data[['Flow_Duration','Src_Port', 'Dst_Port', 'Init_Bwd_Win_Byts', 'Flow_IAT_Min', 'Bwd_PSH_Flags']] # Select columns as DataFrame
    y_test = test_data['Sub_Cat']

    # Remplacer les infinis par NaN avant la standardisation
    X_train.replace([np.inf, -np.inf], np.nan, inplace=True)
    X_test.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Remplacer les NaN par la médiane
    X_train.fillna(X_train.median(), inplace=True)
    X_test.fillna(X_test.median(), inplace=True)

    # Standardisation des données
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    # Ajuster les hyperparamètres du modèle
    decision_tree_model = DecisionTreeClassifier(
        random_state=42,
        max_depth=20,  # Limiter la profondeur
        min_samples_split=2,  # Minimum d'échantillons pour diviser un nœud
        min_samples_leaf=1,  # Minimum d'échantillons par feuille
        criterion='entropy',  # Vous pouvez essayer 'entropy' également
    )

    # Réentraîner le modèle
    decision_tree_model.fit(X_train_scaled, y_train)

    # Prédictions et évaluation
    y_pred = decision_tree_model.predict(X_test_scaled)





    # Charger les données
    data = load_data('model_files/reste.csv')

    signature_fct(data=data, X_train=X_train, decision_tree_model= decision_tree_model, file_type="reste.csv")

    file_path = 'new.csv'

    # Charger les données
    data = load_data('model_files/new.csv')

    signature_fct(data=data, X_train=X_train, decision_tree_model= decision_tree_model, file_type="new.csv")


    joblib.dump(decision_tree_model, 'intrusion_detection_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(y_train.unique(), 'label_encoder.pkl')
