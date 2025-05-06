import os

folders = [
    "pml-cancun-forecasting/data",
    "pml-cancun-forecasting/notebooks",
    "pml-cancun-forecasting/src",
    "pml-cancun-forecasting/powerbi",
    "pml-cancun-forecasting/docs",
    "pml-cancun-forecasting/descargas"
    
]

files = [
    "pml-cancun-forecasting/notebooks/1_EDA_PML.ipynb",
    "pml-cancun-forecasting/notebooks/2_Prediccion_Diaria.ipynb",
    "pml-cancun-forecasting/notebooks/3_Prediccion_Anual.ipynb",  
    "pml-cancun-forecasting/src/data_cleaning.py",
    "pml-cancun-forecasting/src/models.py",
    "pml-cancun-forecasting/powerbi/prediccion_diaria.pbix",
    "pml-cancun-forecasting/powerbi/proyeccion_anual.pbix",
    "pml-cancun-forecasting/docs/reporte_final.md",
    "pml-cancun-forecasting/README.md"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    
for file in files:
    with open(file, "w") as f:
        f.write("# Placeholder\n")