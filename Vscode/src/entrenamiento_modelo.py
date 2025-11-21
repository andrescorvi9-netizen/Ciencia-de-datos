import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

def generar_datos_y_entrenar():

    ruta_origen = '../csv/all_matches.csv'
    ruta_csv_modelo = '../csv/datos_modelo.csv'
    ruta_modelo_pkl = '../Modelos/modelo_random_forest.pkl'
    ruta_encoder_pkl = '../Modelos/codificador_equipos.pkl'

    df = pd.read_csv(ruta_origen)
    
 
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'].dt.year >= 2000].copy()
    

    #Gana Local, 2: Gana Visitante, 0: Empate
    def obtener_resultado(row):
        if row['home_score'] > row['away_score']: return 1
        elif row['away_score'] > row['home_score']: return 2
        else: return 0
    
    df['resultado'] = df.apply(obtener_resultado, axis=1)
    

    le = LabelEncoder()
    equipos_unicos = pd.concat([df['home_team'], df['away_team']]).unique()
    le.fit(equipos_unicos)
    
    df['home_code'] = le.transform(df['home_team'])
    df['away_code'] = le.transform(df['away_team'])
    
    df.to_csv(ruta_csv_modelo, index=False)
    print(f"Datos filtrados guardados en: {ruta_csv_modelo}")


    X = df[['home_code', 'away_code']]
    y = df['resultado']
    
  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("2. Entrenando el modelo (Random Forest)...")
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
   
    print("3. Evaluando precisión...")
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo (Accuracy): {acc:.2%}")
    
 
    os.makedirs(os.path.dirname(ruta_modelo_pkl), exist_ok=True)
    
    joblib.dump(modelo, ruta_modelo_pkl)
    joblib.dump(le, ruta_encoder_pkl)
    
    print(f" El modelo se guardo en: {ruta_modelo_pkl}!")

    print(f" El encoder se guardo en: {ruta_encoder_pkl}!")
