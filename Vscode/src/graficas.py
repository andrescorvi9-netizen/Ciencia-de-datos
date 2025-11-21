import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def preparar_datos_colombia(df):

    filtro = (df['home_team'] == 'Colombia') | (df['away_team'] == 'Colombia')
    df_col = df[filtro].copy()


    goles_favor = []
    goles_contra = [] 
    resultados = []

    for index, row in df_col.iterrows():
        
        if row['home_team'] == 'Colombia':
            gf = row['home_score']
            gc = row['away_score']
        else:
            gf = row['away_score']
            gc = row['home_score']

        goles_favor.append(gf)
        goles_contra.append(gc)
        if gf > gc:
            resultados.append('Ganado')
        elif gf < gc:
            resultados.append('Perdido')
        else:
            resultados.append('Empatado')

   
    df_col['goles_favor'] = goles_favor
    df_col['goles_contra'] = goles_contra 
    df_col['resultado'] = resultados
    df_col = df_col.sort_values('date')
    
    return df_col


def graficar_rendimiento(df_col):

    fig, axs = plt.subplots(1, 2, figsize=(22, 6))  
    plt.suptitle('Análisis de Rendimiento: Colombia (Mundiales 2010-2022)', fontsize=20)


    colores_colombia = {'Ganado': '#FCD116', 'Empatado': '#003893', 'Perdido': '#CE1126'} 
    conteo = df_col['resultado'].value_counts()
    colores_grafica = [colores_colombia.get(x, '#999') for x in conteo.index]

    wedges, texts, autotexts = axs[0].pie(
        conteo, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colores_grafica,
        wedgeprops={'edgecolor': 'black'}
    )
    

    axs[0].legend(
        wedges, 
        conteo.index, 
        title="Resultados",
        loc="center left", 
        bbox_to_anchor=(1, 0, 0.5, 1) 
    )
    
    axs[0].set_title('Distribución de Resultados', fontsize=14)
    axs[0].axis('equal') 

    axs[1].plot(df_col['date'], df_col['goles_favor'], 
                color='#FCD116', 
                marker='o',
                label='Goles a Favor',
                linewidth=2,
                alpha=0.9)
    
  
    axs[1].plot(df_col['date'], df_col['goles_contra'], 
                color='#003893', 
                marker='x', 
                linestyle='--', 
                label='Goles en Contra',
                linewidth=2,
                alpha=0.9)
    
    axs[1].set_title('Evolucion de Goles (2010-2022)', fontsize=14)
    axs[1].set_xlabel('Fecha') 
    axs[1].set_ylabel('Goles')
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].legend() 
    axs[1].grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.subplots_adjust(wspace=0.4, top=0.85)

    plt.show()