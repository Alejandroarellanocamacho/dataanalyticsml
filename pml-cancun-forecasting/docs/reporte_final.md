# Reporte: Pronóstico de Precios de Energía con SARIMA

## Análisis Exploratorio de Datos (EDA)
El análisis exploratorio inicial de los datos del Precio Marginal Local (PML) en el nodo CANCUN reveló varias tendencias y características importantes:

Tendencias Horarias de Congestión: Se identificó una mayor congestión durante las tardes, lo que sugiere una posible correlación con los picos de demanda eléctrica a lo largo del día. Esta congestión podría ser un factor influyente en el comportamiento del PML.

Variación Mensual: El PML promedio mostró su valor más alto durante el mes de agosto, lo que podría estar relacionado con factores estacionales como el aumento en el uso de aire acondicionado debido a las altas temperaturas en la región de Cancún.

Identificación de Outliers: Mediante el análisis de cuartiles y el rango intercuartílico, se identificaron valores atípicos (outliers) en la distribución del PML. La Figura 1 muestra la distribución del precio con los límites inferior y superior para la detección de outliers. Se observa una concentración significativa de precios en rangos bajos, con la presencia de valores extremos superiores que alcanzan niveles considerablemente altos. Estos picos podrían estar asociados a eventos específicos de alta demanda o restricciones en la red de transmisión.

![Outliers](./images/output.png)

Relación entre Congestión y PML: Un análisis de mapa de calor sugirió una relación positiva entre la congestión en la red y el PML promedio, lo que refuerza la hipótesis de que la congestión es un factor relevante que impacta el precio de la energía en el nodo CANCUN.

##  Resumen Ejecutivo
- **Objetivo**: Predecir precios horarios para 1, 3 y 5 años
- **Resultado clave**: Los precios mostrarán patrones estacionales diarios con [tendencia ascendente/descendente]

## Metodología
```python
# Generar pronósticos
    horas_pronostico = {
        '1 año': 24 * 365,
        '3 años': 24 * 365 * 3,
        '5 años': 24 * 365 * 5
    }
    predicciones_sarima = {}
modelo = auto_arima(df, seasonal=True, m=24)
```

## Hallazgos
- **Patrón diario**: [La aplicación del modelo SARIMA con órdenes fijos (1,0,1)[24] resultó en una proyección del PML que se mantiene relativamente constante a lo largo de los horizontes de 1, 3 y 5 años (ver Figura X). Esto sugiere que, con la configuración actual del modelo, no se identifican tendencias significativas a largo plazo ni una estacionalidad anual marcada. El modelo tiende a predecir una continuación del nivel de precios observado en el período reciente.]


## Dashboard Proyeccion Precio Anual
|![Captura del dashboard Anual](./images/Panel_Anual.PNG)|
|![Captura](./images/Proyeccion_1_3_5_años.PNG)|
|![Proyeccion SARIMA](./mages/Proyeccion_sarima.PNG)|

---

# Dashboard Predicioón Diaria
|![Captura Por año Comparación temporal](./images/predicion_por_año_comp_temp.PNG)|
|![Grafico de Dispersión](./images/predicion_por_año_dispersion.PNG)|
|![Mapa de calor](./images/predicion_por_año_heatmap.PNG)|



## 🔍 ¿Qué significa ARIMA?

**ARIMA** es un acrónimo que representa:

AR (AutoRegresivo): El modelo usa valores pasados de la serie para predecir valores futuros

I (Integrado): Se aplican diferencias a los datos para hacerlos estacionarios (eliminar tendencias)

MA (Media Móvil): El modelo considera errores de predicción pasados



"La aplicación del modelo SARIMA con órdenes fijos ([insertar órdenes que usaste]) resultó en una proyección del PML que se mantiene relativamente constante a lo largo de los horizontes de 1, 3 y 5 años (ver Figura X). Esto sugiere que, con la configuración actual del modelo, no se identifican tendencias significativas a largo plazo ni una estacionalidad anual marcada. El modelo tiende a predecir una continuación del nivel de precios observado en el período reciente."

# 📈 Proyecto de Predicción de Precios con SARIMA

## 🧠 Objetivo

Desarrollar un modelo de series de tiempo que permita **predecir el comportamiento futuro del precio por hora** a partir de un histórico de aproximadamente 5 años. El objetivo principal es obtener una **proyección anual (y también a 3 y 5 años)** con base en un modelo SARIMA ajustado automáticamente.

---

## 📅 Datos

- **Fuente de datos:** archivo local con columnas `fecha_hora` y `precio`.
- **Frecuencia:** datos horarios.
- **Duración del histórico:** ~5 años.
- **Preprocesamiento realizado:**
  - Conversión de `fecha_hora` a índice de tipo `datetime`.
  - Eliminación de duplicados.
  - Alineación a frecuencia horaria (`asfreq('H')`).
  - Relleno de valores faltantes mediante forward fill (`ffill`).

---

## ⚙️ Modelo SARIMA

Se utilizó la librería `pmdarima` para determinar automáticamente los mejores parámetros para el modelo SARIMA mediante `auto_arima()`:

```python
auto_arima(df_sarima, seasonal=True, m=24)
```

- `m=24`: se consideró una estacionalidad diaria (24 horas).
- Se encontraron los siguientes parámetros óptimos:
  - `order = (p, d, q)`
  - `seasonal_order = (P, D, Q, m)`

> Estos valores se aplicaron al modelo `SARIMAX` de `statsmodels`.

---

## 📊 Resultados de la Proyección

Se realizaron proyecciones para los siguientes horizontes:

| Horizonte | Horas proyectadas |
|-----------|-------------------|
| 1 año     | 8,760 horas       |
| 3 años    | 26,280 horas      |
| 5 años    | 43,800 horas      |

### Ejemplo de visualización:

![Gráfica SARIMA](./images/output_SARIMA.png)

---

## 📤 Exportación

Se exportaron los archivos `.csv` con las proyecciones para cada horizonte:

- `proyeccion_sarima_1_año.csv`
- `proyeccion_sarima_3_años.csv`
- `proyeccion_sarima_5_años.csv`

---

## ✅ Conclusiones

- El modelo SARIMA se ajustó correctamente a los datos.
- Las proyecciones permiten tener una visión futura útil para la toma de decisiones.
- Se recomienda revisar y actualizar el modelo con nuevos datos cada cierto tiempo para mantener su precisión.

---

## 🔧 Requerimientos técnicos

- Python 3.12
- Librerías:
  - pandas
  - numpy
  - matplotlib
  - statsmodels
  - pmdarima


