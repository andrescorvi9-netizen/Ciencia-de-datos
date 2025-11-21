import matplotlib.pyplot as plt
import pandas as pd

def procesar_datos_col(df):
    ruta_csv='../csv/datos_modelo.csv'
    df = pd.read_csv(ruta_csv)
    df['date'] = pd.to_datetime(df['date'])
    filtro = (df['home_team'] == 'Colombia') | (df['away_team'] == 'Colombia')
    data_col = df[filtro].copy()
    
    gf_list = []
    gc_list = []
    res_list = []

    for index, row in data_col.iterrows():
        if row['home_team'] == 'Colombia':
            gf = row['home_score']
            gc = row['away_score']
        else:
            gf = row['away_score']
            gc = row['home_score']

        gf_list.append(gf)
        gc_list.append(gc)
        
        if gf > gc:
            res_list.append('Ganado')
        elif gf < gc:
            res_list.append('Perdido')
        else:
            res_list.append('Empatado')

    data_col['goles_favor'] = gf_list
    data_col['goles_contra'] = gc_list
    data_col['resultado_final'] = res_list
    data_col = data_col.sort_values('date')
    
    return data_col

def generar_grafica_col(data_col):
    if data_col.empty:
        print("Sin datos para Colombia")
        return

    fig, ax_arr = plt.subplots(1, 2, figsize=(20, 6))
    
    mapa_colores = {'Ganado': '#FCD116', 'Empatado': '#003893', 'Perdido': '#CE1126'}
    conteo_res = data_col['resultado_final'].value_counts()
    lista_colores = [mapa_colores.get(x, '#999') for x in conteo_res.index]

    ax_arr[0].pie(conteo_res, autopct='%1.1f%%', startangle=90, colors=lista_colores)
    ax_arr[0].legend(conteo_res.index, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax_arr[0].set_title('Resultados Colombia')

    datos_box = [data_col['goles_favor'], data_col['goles_contra']]
    box = ax_arr[1].boxplot(datos_box, labels=['A Favor', 'En Contra'], patch_artist=True)
    
    colores_box = ['#FCD116', '#003893']
    for patch, color in zip(box['boxes'], colores_box):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax_arr[1].set_title('Distribución de Goles (Boxplot)')
    ax_arr[1].set_ylabel('Cantidad de Goles')
    ax_arr[1].grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
