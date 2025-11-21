import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def preparar_datos_espana(df):

    equipo = 'Spain'
    
    # Filtrar partidos de España
    filtro = (df['home_team'] == equipo) | (df['away_team'] == equipo)
    df_espana = df[filtro].copy()

    if df_espana.empty:
        print(f"Advertencia: No se encontraron datos para {equipo}.")
        return df_espana

    goles_favor = []
    goles_contra = []
    resultados = []

    for index, row in df_espana.iterrows():
        if row['home_team'] == equipo:
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

    df_espana['goles_favor'] = goles_favor
    df_espana['goles_contra'] = goles_contra
    df_espana['resultado'] = resultados
    
    df_espana = df_espana.sort_values('date')
    
    return df_espana

def graficar_rendimiento_espana(df_espana):

    if df_espana.empty:
        print("No hay datos de España para graficar.")
        return


    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    conteo = df_espana['resultado'].value_counts().reindex(['Ganado', 'Empatado', 'Perdido'], fill_value=0)
    

    colores_res = {'Ganado': '#C60B1E', 'Empatado': '#FFC400', 'Perdido': '#808080'}

 
    wedges, texts, autotexts = axes[0].pie(
        conteo, 
        autopct='%1.1f%%', 
        startangle=90,     
        colors=[colores_res[k] for k in conteo.index],
        wedgeprops={'edgecolor': 'black'}
    ) 
    axes[0].legend(
        wedges, 
        conteo.index, 
        title="Resultados",
        loc="center left", 
        bbox_to_anchor=(1, 0, 0.5, 1) 
    )
    axes[0].set_title('Resultados de España en Mundiales', fontsize=14, fontweight='bold')
    axes[0].axis('equal') 
    fechas = df_espana['date'].dt.strftime('%Y-%m')
    x = range(len(fechas))
    

    axes[1].plot(x, df_espana['goles_favor'], marker='o', label='A Favor', color='#C60B1E', linewidth=2)
    axes[1].plot(x, df_espana['goles_contra'], marker='x', label='En Contra', color='#FFC400', linewidth=2, linestyle='--')
    
    axes[1].set_title('Evolución de Goles - España', fontsize=14, fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(fechas, rotation=45, ha='right', fontsize=9)
    axes[1].set_ylabel('Goles')
    axes[1].legend()
    axes[1].grid(True, linestyle='--', alpha=0.3)

    plt.tight_layout()
