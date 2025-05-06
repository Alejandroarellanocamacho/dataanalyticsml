import pandas as pd
import glob
import os
from tqdm import tqdm

# Configuración
ruta_archivos = './pml-cancun-forecasting/descargas/*.csv'
output_file = './pml-cancun-forecasting/data/PML_CANCUN_FINAL.csv'
zona_objetivo = 'CANCUN'

def leer_archivo(archivo):
    """Lee cualquier archivo CSV sin importar su estructura"""
    try:
        # Primera pasada para encontrar encabezados
        with open(archivo, 'r', encoding='latin1') as f:
            lineas = f.readlines()
        
        # Buscar línea con encabezados
        skiprows = 0
        for i, linea in enumerate(lineas):
            if 'Fecha' in linea and any(col in linea for col in ['Hora', 'hora']):
                skiprows = i
                break
        
        # Segunda pasada para leer datos
        with open(archivo, 'r', encoding='latin1') as f:
            for _ in range(skiprows):
                next(f)
            primera_linea = f.readline()
            sep = '\t' if '\t' in primera_linea else ','
        
        # Leer datos
        df = pd.read_csv(
            archivo,
            skiprows=skiprows,
            sep=sep,
            encoding='latin1',
            engine='python',
            on_bad_lines='skip'
        )
        
        return df
    
    except Exception as e:
        print(f"Error leyendo {os.path.basename(archivo)}: {str(e)}")
        return None

def procesar_archivo(archivo):
    """Procesa un archivo individual"""
    df = leer_archivo(archivo)
    if df is None:
        return None
    
    # Normalizar nombres de columnas
    df.columns = [col.strip().upper() for col in df.columns]
    
    # Buscar columnas clave
    col_mapping = {
        'fecha': next((col for col in df.columns if 'FECHA' in col), None),
        'hora': next((col for col in df.columns if 'HORA' in col), None),
        'zona': next((col for col in df.columns if any(x in col for x in ['ZONA', 'NODO'])), None),
        'precio': next((col for col in df.columns if 'PRECIO' in col), None),
        'energia': next((col for col in df.columns if 'ENERGIA' in col), None),
        'congestion': next((col for col in df.columns if 'CONGESTION' in col), None)
    }
    
    # Verificar columnas mínimas
    if not col_mapping['fecha'] or not col_mapping['hora']:
        print(f"Archivo {os.path.basename(archivo)} no tiene columnas Fecha/Hora")
        return None
    
    # Filtrar por CANCUN si existe columna de zona
    if col_mapping['zona']:
        try:
            mask = df[col_mapping['zona']].astype(str).str.upper().str.replace('Á', 'A').str.contains(zona_objetivo.upper())
            df = df[mask]
            if df.empty:
                print(f"No hay datos de {zona_objetivo} en {os.path.basename(archivo)}")
                return None
        except:
            pass
    
    # Seleccionar columnas
    columnas = {k:v for k,v in col_mapping.items() if v is not None}
    df = df[list(columnas.values())]
    df.columns = columnas.keys()
    
    return df

def main():
    archivos = glob.glob(ruta_archivos)
    if not archivos:
        print("No se encontraron archivos CSV")
        return
    
    print(f"\n🔍 Procesando {len(archivos)} archivos...")
    
    datos = []
    for archivo in tqdm(archivos, desc="Progreso"):
        df = procesar_archivo(archivo)
        if df is not None and not df.empty:
            datos.append(df)
    
    if not datos:
        print("\n⚠️ NO SE ENCONTRARON DATOS VÁLIDOS")
        print("\n🔍 DIAGNÓSTICO FINAL:")
        print("1. Los archivos NO CONTIENEN datos para CANCUN")
        print("2. Posiblemente descargaste archivos consolidados")
        print("3. Necesitas los archivos específicos por nodo distribuido")
        print("\n💡 SOLUCIÓN INMEDIATA:")
        print("Descarga nuevamente los archivos desde:")
        print("https://www.cenace.gob.mx > SIM > Mercado de Energía > Precios > Nodos Distribuidos")
        return
    
    # Consolidar
    df_final = pd.concat(datos, ignore_index=True)
    
    # Guardar
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_final.to_csv(output_file, index=False, encoding='utf-8')
    
    # Resultados
    print(f"\n✅ ¡PROCESO TERMINADO CON ÉXITO!")
    print(f"📊 Registros totales: {len(df_final)}")
    print(f"📂 Archivo guardado en: {output_file}")
    
    if 'fecha' in df_final.columns:
        try:
            df_final['fecha'] = pd.to_datetime(df_final['fecha'])
            print(f"📅 Rango de fechas: {df_final['fecha'].min().date()} a {df_final['fecha'].max().date()}")
        except:
            pass

if __name__ == "__main__":
    main()
