import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def preparar_datos_colombia(df):
    # pa saber si es visitante o local 
    filtro = (df['home_team'] == 'Colombia') | (df['away_team'] == 'Colombia')
    df_col = df[filtro].copy()

    # Listas pa nuevas columnas
    goles_favor = []
    resultados = []

    for index, row in df_col.iterrows():
       
        if row['home_team'] == 'Colombia':
            gf = row['home_score']
            gc = row['away_score']
        else:
            gf = row['away_score']
            gc = row['home_score']

        goles_favor.append(gf)
        if gf > gc:
            resultados.append('Ganado')
        elif gf < gc:
            resultados.append('Perdido')
        else:
            resultados.append('Empatado')

    # las susodichas columnas y orden por fecha
    df_col['goles_favor'] = goles_favor
    df_col['resultado'] = resultados
    df_col = df_col.sort_values('date')
    
    return df_col


def graficar_rendimiento(df_col):

    fig, axs = plt.subplots(1, 2, figsize=(22, 6))  
    plt.suptitle('Análisis de Rendimiento: Colombia (Mundiales 2010-2022)', fontsize=20)

    # este es el circular
    conteo = df_col['resultado'].value_counts()
    colores = {'Ganado': '#4CAF50', 'Empatado': '#FFC107', 'Perdido': '#F44336'}
    colores_grafica = [colores.get(x, '#999') for x in conteo.index]
    
    axs[0].pie(conteo, labels=conteo.index, autopct='%1.1f%%', startangle=90, colors=colores_grafica)
    axs[0].set_title('Resultados', fontsize=14)

    #Dispersión de goles
    axs[1].scatter(df_col['date'], df_col['goles_favor'], color='purple', s=100, alpha=0.7)
    
    axs[1].plot(df_col['date'], df_col['goles_favor'], color='gray', linestyle='--', alpha=0.3)
    axs[1].set_title('Evolucion de Goles (2010-2022)', fontsize=14)
    axs[1].set_xlabel('Año')
    axs[1].set_ylabel('Goles Marcados')
    axs[1].tick_params(axis='x', rotation=45)

    plt.subplots_adjust(wspace=0.4, top=0.85)