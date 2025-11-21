import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix

def generar_datos_y_entrenar():
    ruta_origen = '../csv/all_matches.csv'
    ruta_csv_modelo = '../csv/datos_modelo.csv'
    ruta_modelo_pkl = '../Modelos/modelo_random_forest.pkl'
    ruta_encoder_pkl = '../Modelos/codificador_equipos.pkl'


    df = pd.read_csv(ruta_origen)
    
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'].dt.year >= 2000].copy()

    # 1: Gana Local, 2: Gana Visitante, 0: Empate
    def obtener_resultado(row):
        if row['home_score'] > row['away_score']: return 1
        elif row['away_score'] > row['home_score']: return 2
        else: return 0
    
    df['resultado'] = df.apply(obtener_resultado, axis=1)
    
    # Codificación
    le = LabelEncoder()
    equipos_unicos = pd.concat([df['home_team'], df['away_team']]).unique()
    le.fit(equipos_unicos)
    
    df['home_code'] = le.transform(df['home_team'])
    df['away_code'] = le.transform(df['away_team'])
    
    df.to_csv(ruta_csv_modelo, index=False)
    print(f"Datos filtrados guardados en: {ruta_csv_modelo}")

    X = df[['home_code', 'away_code']]
    y = df['resultado']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("2. Entrenando el modelo (Random Forest)...")
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    
    # Evaluación
    print("3. Evaluando precisión...")
    preds_train = modelo.predict(X_train)
    preds_test = modelo.predict(X_test)
    
    acc_train = accuracy_score(y_train, preds_train)
    acc_test = accuracy_score(y_test, preds_test)
    
    print(f"Precisión del modelo (Test): {acc_test:.2%}")
    
    # Guardar
    os.makedirs(os.path.dirname(ruta_modelo_pkl), exist_ok=True)
    joblib.dump(modelo, ruta_modelo_pkl)
    joblib.dump(le, ruta_encoder_pkl)
    
    print(f" El modelo se guardo en: {ruta_modelo_pkl}!")
    print(f" El encoder se guardo en: {ruta_encoder_pkl}!")

    return modelo, X_test, y_test, acc_train, acc_test

def ver_analisis_grafico(modelo, X_test, y_test):

    y_pred = modelo.predict(X_test)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=['Empate', 'Local', 'Visitante'],
                yticklabels=['Empate', 'Local', 'Visitante'])
    axes[0].set_title('Matriz de Confusión (Detalle de errores)')
    axes[0].set_xlabel('Predicción')
    axes[0].set_ylabel('Real')

    data_real = pd.DataFrame({'Resultado': y_test, 'Tipo': 'Real (Datos)'})
    data_pred = pd.DataFrame({'Resultado': y_pred, 'Tipo': 'Predicción (Modelo)'})
    data_plot = pd.concat([data_real, data_pred])

   
    sns.histplot(data=data_plot, x='Resultado', hue='Tipo', element="step", 
                 stat="count", common_norm=False, ax=axes[1], bins=[-0.5, 0.5, 1.5, 2.5])
    
    axes[1].set_xticks([0, 1, 2])
    axes[1].set_xticklabels(['Empate', 'Local', 'Visitante'])
    axes[1].set_title('Comparación: Real vs Prediccion')
    axes[1].set_ylabel('Cantidad de Partidos')
    
    plt.tight_layout()
