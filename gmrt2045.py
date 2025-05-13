# -*- coding: utf-8 -*-
"""
Created on Tue May 13 13:23:25 2025

@author: CENADIF

Script para procesar pruebas de freno y cotejarlas con los parámetros
establecidos en la norma ingles GMRT-2045
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 

#.Ruta del excel de Resultado_NINF.xlsx
datos_path = sys.argv[1] if len(sys.argv) > 1 else None

#.....................................................................................................................................................#
#....................................................IMPORTAR DATOS DE LAS PRUEBAS....................................................................#
#.....................................................................................................................................................#

# Crea un diccionario para almacenar los DataFrames de cada hoja
velocidades_EB,distancias_EB,velocidades_B7,distancias_B7 = {},{},{},{}

# Itera a través de todos los archivos en la carpeta especificada
for filename in os.listdir(datos_path):
    if filename.endswith(".csv"):  # Nos aseguramos de que solo procesamos archivos CSV
        filepath = os.path.join(datos_path, filename)
        try:
            # Lee el archivo CSV y su nombre
            nombre_archivo_sin_extension = os.path.splitext(filename)[0]
            df=pd.read_csv(filepath, sep=';',encoding='latin1',header=0,skiprows=[1])
            for col in df.columns:
                    # Verificar si la columna contiene objetos (lo más probable es que sean strings si hay comas)
                    if df[col].dtype == 'object':
                        try:
                            # Intentar reemplazar las comas por puntos
                            df[col] = df[col].str.replace(',', '.', regex=False)
                        except AttributeError:
                            # Si la columna no tiene el atributo 'str' (no es de tipo string), omitir
                            pass
            
            # Ahora intenta convertir todas las columnas a numérico (donde sea posible)
            df_numerico = df.apply(pd.to_numeric, errors='coerce')
            
            # Elimina los duplicados de la columna 'Tiempo Pulsador'
            df_recortado = df_numerico.drop_duplicates(subset=['Tiempo Pulsador'], keep='first')
            
            if len(df_recortado) > 1:
                v_inicial = df_recortado['Velocity'].iloc[1]
                dist_frenado = df_recortado['Distancia'].max()
                p_max=df_recortado['CIL KPA'].max()
            if p_max>250:
                velocidades_EB[nombre_archivo_sin_extension] = v_inicial
                distancias_EB[nombre_archivo_sin_extension] = dist_frenado
            else:
                velocidades_B7[nombre_archivo_sin_extension] = v_inicial
                distancias_B7[nombre_archivo_sin_extension] = dist_frenado
        except Exception as e:
            print(f"Error al leer el archivo {filename} con codificación Latin-1: {e}")
            
#.....................................................................................................................................................#
#....................................................PREPROCESAMIENTO ESTADÍSTICO.....................................................................#
#.....................................................................................................................................................# 
df_B7 = pd.DataFrame({'velocidad': velocidades_B7, 'distancia': distancias_B7})
df_EB = pd.DataFrame({'velocidad': velocidades_EB, 'distancia': distancias_EB})
# Definimos las velocidades de referencia del ensayo
velocidades_ref = np.array([30, 40, 60, 80, 90])  # Se puede ajustar según el ensayo

def asignar_velocidad_grupo(vel):
    # Devuelve la velocidad de referencia más cercana
    return velocidades_ref[np.argmin(np.abs(velocidades_ref - vel))]

# Aplicarlo a tu DataFrame
df_B7['velocidad_grupo'] = df_B7['velocidad'].apply(asignar_velocidad_grupo)
df_EB['velocidad_grupo'] = df_EB['velocidad'].apply(asignar_velocidad_grupo)

# 2. Calcular promedio de distancia por grupo
media_distancia_B7 = df_B7.groupby('velocidad_grupo')['distancia'].mean()
media_v0_B7 = df_B7.groupby('velocidad_grupo')['velocidad'].mean()
media_distancia_EB = df_EB.groupby('velocidad_grupo')['distancia'].mean()
media_v0_EB = df_EB.groupby('velocidad_grupo')['velocidad'].mean()

# 3. Calcular dispersión
def scatter_percent(row, media_distancia):
    media = media_distancia.loc[row['velocidad_grupo']]
    return abs(row['distancia'] - media) / media * 100
    
#.Calculo dispersion
df_B7['scatter'] = df_B7.apply(scatter_percent, axis=1,media_distancia=media_distancia_B7)
df_EB['scatter'] = df_EB.apply(scatter_percent, axis=1,media_distancia=media_distancia_EB)

# 4. Evaluar cumplimiento
cumple_scatter_EB = (df_EB['scatter'] <= 15).all()  # todos los datos deben estar dentro de ±15%
cumple_scatter_B7 = (df_B7['scatter'] <= 15).all()  # todos los datos deben estar dentro de ±15%

#.....................................................................................................................................................#
#....................................................GRAFICOS SEGUN NORMA GMRT2045....................................................................#
#.....................................................................................................................................................#

#.Funcion de velocidades y distancias objetivo
def brake_targets(a_mean,tol=0):
    target_v=np.linspace(0,160,300)
    target_dist=(1+tol)*(target_v/3.6)**2/(2*a_mean)
    return target_dist,target_v

#.Calculo para B7 con tolerancias
x_B7,v_B7 = brake_targets(1.0,tol=0)
x_B7_tol,v_B7_tol = brake_targets(1.0,tol=0.15)
x_B7_adm,v_B7_adm = brake_targets(1.0,tol=-0.1)
#.Calculo para EB con tolerancias
x_EB,v_EB = brake_targets(1.2,tol=0)
x_EB_tol,v_EB_tol = brake_targets(1.2,tol=0.15)
x_EB_adm,v_EB_adm = brake_targets(1.2,tol=-0.1)

#.Hacemos los graficos de la norma
fig,ax=plt.subplots(nrows=1,ncols=2,figsize=(15,5),dpi=250)
ax[0].plot(x_B7,v_B7,color='k',label='Objetivo',linestyle='-',linewidth=3,zorder=1)
ax[0].plot(x_B7_tol,v_B7_tol,color='k',label='Tolerancia=+15%',linestyle='--',linewidth=2,zorder=1)
ax[0].plot(x_B7_adm,v_B7_adm,color='k',label='Tolerancia=-10%',linestyle='--',linewidth=2,zorder=1)
ax[0].fill_between(x_B7_tol,v_B7_tol,color='tab:red',alpha=0.2,zorder=0)
ax[0].fill_between(x_B7_tol,v_B7_adm,np.interp(x_B7_tol,x_B7_adm,v_B7_adm), color='tab:green', alpha=0.2,zorder=0)
ax[0].fill_between(x_B7_adm, v_B7_adm,120, color='yellow', alpha=0.2,zorder=0)
ax[0].set_xlabel('Distancia de frenado [m]',fontsize=14,fontfamily='Cambria')
ax[0].set_ylabel('Velocidad inicial [km/h]',fontsize=14,fontfamily='Cambria')
ax[0].set_xlim(0,550)
ax[0].set_ylim(0,120)
ax[0].set_title('Freno B7',fontsize=18,fontfamily='Cambria',fontweight='bold')
#.Coloco las pruebas B7 como valores
ax[0].scatter(media_distancia_B7,media_v0_B7,color='m',marker='X',label='Prom. Ensayos',zorder=2)
ax[0].legend(fontsize=14,prop={'family': 'Cambria'})
ax[0].grid(True, which='both', linestyle='--', alpha=0.5)


ax[1].plot(x_EB,v_EB,color='k',label='Objetivo',linestyle='-',linewidth=3,zorder=1)
ax[1].plot(x_EB_tol,v_EB_tol,color='k',label='Tolerancia=+15%',linestyle='--',linewidth=2,zorder=1)
ax[1].plot(x_EB_adm,v_EB_adm,color='k',label='Tolerancia=-10%',linestyle='--',linewidth=2,zorder=1)
ax[1].fill_between(x_EB_tol,v_EB_tol,color='tab:red',alpha=0.2,zorder=0)
ax[1].fill_between(x_EB_tol,v_EB_adm,np.interp(x_EB_tol,x_EB_adm,v_EB_adm), color='tab:green', alpha=0.2,zorder=0)
ax[1].fill_between(x_EB_adm, v_EB_adm,120, color='yellow', alpha=0.2,zorder=0)
ax[1].set_xlabel('Distancia de frenado [m]',fontsize=14,fontfamily='Cambria')
ax[1].set_ylabel('Velocidad inicial [km/h]',fontsize=14,fontfamily='Cambria')
ax[1].set_title('Freno EB',fontsize=18,fontfamily='Cambria',fontweight='bold')
ax[1].set_xlim(0,550)
ax[1].set_ylim(0,120)
#.Coloco las pruebas EB como valores
ax[1].scatter(media_distancia_EB,media_v0_EB,color='m',marker='X',label='Prom. Ensayos',zorder=2)
ax[1].legend(fontsize=14,prop={'family': 'Cambria'})
ax[1].grid(True, which='both', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(datos_path,'GMRT2045_plot.png'),dpi=300)