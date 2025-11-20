import pandas as pd

def limpiar_y_guardar(ruta_entrada, ruta_salida):
   
    df = pd.read_csv(ruta_entrada)

    #Vuelve date que es objet a fecha pa uzarla 
    df['date'] = pd.to_datetime(df['date'])

    # Filtro de copas del mundo por el año y selecionadas de tounament
    filtro_anio = (df['date'].dt.year >= 2010) & (df['date'].dt.year <= 2022)
    filtro_torneo = df['tournament'] == 'World Cup'
    df_limpio = df[filtro_anio & filtro_torneo].copy()

    # Neutral no sirve, si algo queda df_original y tambien se van nulos.
    if 'neutral' in df_limpio.columns:
        df_limpio = df_limpio.drop(columns=['neutral'])
    df_limpio = df_limpio.dropna()

    # Guardado del nuevo csv, le puse limpia, como la que necesitamos.
    df_limpio.to_csv(ruta_salida, index=False)

    print(f"¡Limpieza completada! Datos guardados en: {ruta_salida}")
    print(f"Filas resultantes: {len(df_limpio)}")