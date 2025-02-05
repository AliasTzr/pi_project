import csv, os, json
import pandas as pd

# zip_path = "dataset/dataset.zip"
#     # Décompresser le fichier ZIP
# with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#     zip_ref.extractall('dataset')
# print(os.path.join("dataset", "dataset.csv"))
# os.remove("dataset/dataset.csv")

# if os.path.exists("dataset/reste.csv"):
#     with open("dataset/reste.csv", mode='r', encoding='utf-8') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         # Convertir les lignes CSV en une liste de dictionnaires
#         rows = list(csv_reader)
#     # Sauvegarder la liste en fichier JSON
#     with open("dataset/fichier_test.json", mode='w', encoding='utf-8') as json_file:
#         json.dump(rows, json_file, indent=4)

# print("done")

data = {
    "Flow_ID": "192.168.0.13-111.107.169.216-554-6297-6",
    "Src_IP": "111.107.169.216",
    "Src_Port": "6297",
    "Dst_IP": "192.168.0.13",
    "Dst_Port": "554",
    "Protocol": "6",
    "Timestamp": "26/05/2019 10:20:33 PM",
    "Flow_Duration": "2717",
    "Tot_Fwd_Pkts": "0",
    "Tot_Bwd_Pkts": "2",
    "TotLen_Fwd_Pkts": "0.0",
    "TotLen_Bwd_Pkts": "0.0",
    "Fwd_Pkt_Len_Max": "0.0",
    "Fwd_Pkt_Len_Min": "0.0",
    "Fwd_Pkt_Len_Mean": "0.0",
    "Fwd_Pkt_Len_Std": "0.0",
    "Bwd_Pkt_Len_Max": "0.0",
    "Bwd_Pkt_Len_Min": "0.0",
    "Bwd_Pkt_Len_Mean": "0.0",
    "Bwd_Pkt_Len_Std": "0.0",
    "Flow_Byts/s": "0.0",
    "Flow_Pkts/s": "736.1059992638942",
    "Flow_IAT_Mean": "2717.0",
    "Flow_IAT_Std": "0.0",
    "Flow_IAT_Max": "2717.0",
    "Flow_IAT_Min": "2717.0",
    "Fwd_IAT_Tot": "0.0",
    "Fwd_IAT_Mean": "0.0",
    "Fwd_IAT_Std": "0.0",
    "Fwd_IAT_Max": "0.0",
    "Fwd_IAT_Min": "0.0",
    "Bwd_IAT_Tot": "2717.0",
    "Bwd_IAT_Mean": "2717.0",
    "Bwd_IAT_Std": "0.0",
    "Bwd_IAT_Max": "2717.0",
    "Bwd_IAT_Min": "2717.0",
    "Fwd_PSH_Flags": "0",
    "Bwd_PSH_Flags": "0",
    "Fwd_URG_Flags": "0",
    "Bwd_URG_Flags": "0",
    "Fwd_Header_Len": "0",
    "Bwd_Header_Len": "44",
    "Fwd_Pkts/s": "0.0",
    "Bwd_Pkts/s": "736.1059992638942",
    "Pkt_Len_Min": "0.0",
    "Pkt_Len_Max": "0.0",
    "Pkt_Len_Mean": "0.0",
    "Pkt_Len_Std": "0.0",
    "Pkt_Len_Var": "0.0",
    "FIN_Flag_Cnt": "0",
    "SYN_Flag_Cnt": "1",
    "RST_Flag_Cnt": "0",
    "PSH_Flag_Cnt": "0",
    "ACK_Flag_Cnt": "0",
    "URG_Flag_Cnt": "0",
    "CWE_Flag_Count": "0",
    "ECE_Flag_Cnt": "0",
    "Down/Up_Ratio": "0.0",
    "Pkt_Size_Avg": "0.0",
    "Fwd_Seg_Size_Avg": "0.0",
    "Bwd_Seg_Size_Avg": "0.0",
    "Fwd_Byts/b_Avg": "0",
    "Fwd_Pkts/b_Avg": "0",
    "Fwd_Blk_Rate_Avg": "0",
    "Bwd_Byts/b_Avg": "0",
    "Bwd_Pkts/b_Avg": "0",
    "Bwd_Blk_Rate_Avg": "0",
    "Subflow_Fwd_Pkts": "0",
    "Subflow_Fwd_Byts": "0",
    "Subflow_Bwd_Pkts": "2",
    "Subflow_Bwd_Byts": "0",
    "Init_Fwd_Win_Byts": "-1",
    "Init_Bwd_Win_Byts": "14600",
    "Fwd_Act_Data_Pkts": "0",
    "Fwd_Seg_Size_Min": "0",
    "Active_Mean": "0.0",
    "Active_Std": "0.0",
    "Active_Max": "0.0",
    "Active_Min": "0.0",
    "Idle_Mean": "2717.0",
    "Idle_Std": "0.0",
    "Idle_Max": "2717.0",
    "Idle_Min": "2717.0",
    "Label": "Anomaly",
    "Cat": "DoS",
    "Sub_Cat": "DoS-Synflooding"
}

with open("dataset/fichier_test.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)  # Liste de dictionnaires

# Définir les colonnes à comparer
columns_to_check = ["Flow_Duration", "Src_Port", "Dst_Port", "Init_Bwd_Win_Byts", "Flow_IAT_Min", "Bwd_PSH_Flags"]

# Extraire uniquement les colonnes d'intérêt
data_frame = pd.DataFrame([data])[columns_to_check]

# Convertir en dictionnaire (une seule ligne)
json_data = data_frame.to_dict(orient="records")[0]
print(len(str(json_data)))

# Compter les occurrences dans le fichier JSON
count = sum(1 for item in data_list if all(item.get(key) == value for key, value in json_data.items()))

# Afficher le résultat
print(f"Nombre d'occurrences trouvées : {count}")

# Afficher la longueur de la chaîne
