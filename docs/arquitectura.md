# Arquitectura

## Visión general

```
 Fuente oficial         Validación y           Entrenamiento          Evaluación
 (UCI)           ──►    limpieza       ──►     logística       ──►    AUC, KS, Brier,
 descarga con           (esquema,              XGBoost                calibración,
 checksum               variables)             LightGBM               umbral por costo
                                                   │
                                                   ▼
                        Explicación      ◄──   Modelo elegido
                        (SHAP)                 + metadatos
                            │                      │
                            ▼                      ▼
                     Tablero Streamlit        API FastAPI
                                              POST /v1/score
```

El entrenamiento y el servicio están separados: el entrenamiento produce un artefacto versionado
(modelo, metadatos y métricas) y la API solo lo carga. La API no entrena ni accede a los datos crudos.

## Estructura del repositorio

```
credit-risk-scoring/
├── src/credit_risk/        paquete principal
│   ├── config.py           configuración (rutas, semillas, costos)
│   ├── data.py             descarga, verificación y carga
│   ├── schema.py           validación del esquema de datos
│   ├── features.py         variables derivadas
│   ├── train.py            entrenamiento y validación cruzada
│   ├── evaluate.py         métricas, calibración y umbral
│   ├── explain.py          explicaciones con SHAP
│   └── registry.py         guardado y carga de modelos con metadatos
├── api/                    servicio FastAPI
├── app/                    tablero Streamlit
├── notebooks/              análisis exploratorio (solo lectura de resultados)
├── tests/                  pruebas unitarias, de API y de modelo
├── docs/                   requisitos, arquitectura, ADR, model card
├── data/                   datos descargados (fuera de git)
├── models/                 artefactos entrenados (fuera de git)
└── reports/                métricas y figuras generadas
```

La lógica vive en `src/`. Los notebooks importan desde ahí y no contienen código que el resto del
proyecto necesite; así todo lo importante queda probado.

## Flujo de datos

1. `data.py` descarga el archivo, compara su SHA-256 con el valor registrado y lo guarda en `data/raw/`.
2. `schema.py` valida tipos, rangos y categorías; los valores fuera de lo documentado se reportan y
   se tratan con una regla explícita.
3. Se separa un **conjunto de prueba (20 %, estratificado)** antes de cualquier análisis. Solo se usa
   en la evaluación final.
4. `features.py` crea variables a partir del historial (por ejemplo, meses con atraso, utilización de
   la línea de crédito). Las transformaciones se ajustan solo con datos de entrenamiento.
5. `train.py` compara modelos con validación cruzada estratificada de 5 particiones.
6. `evaluate.py` calibra el modelo elegido, calcula métricas en prueba y elige el umbral que minimiza
   el costo esperado.
7. `registry.py` guarda el modelo con su versión, fecha, métricas, hash de los datos y versiones de
   librerías.

## API

Versionada bajo `/v1`. Toda petición, salvo `/health`, requiere el encabezado `X-API-Key`.

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/health` | Estado del servicio |
| `GET` | `/v1/model` | Versión, fecha de entrenamiento y métricas del modelo cargado |
| `POST` | `/v1/score` | Calificación de un cliente |

Ejemplo de respuesta de `/v1/score`:

```json
{
  "probability_of_default": 0.27,
  "decision": "review",
  "threshold": 0.35,
  "top_factors": [
    {"feature": "months_delayed_last_6", "impact": 0.12},
    {"feature": "credit_utilization", "impact": 0.05}
  ],
  "model_version": "1.0.0"
}
```

Errores:

| Código | Caso |
| --- | --- |
| `401` | API key ausente o inválida |
| `422` | Datos de entrada inválidos (tipo, rango o campo faltante) |
| `429` | Límite de peticiones excedido |
| `500` | Error interno; la respuesta no incluye detalles de la implementación |

## Tecnologías

| Área | Herramienta |
| --- | --- |
| Lenguaje | Python 3.11 |
| Datos | pandas, pandera |
| Modelos | scikit-learn, XGBoost, LightGBM |
| Explicabilidad | SHAP |
| API | FastAPI, Pydantic, Uvicorn |
| Tablero | Streamlit |
| Calidad | Ruff, mypy, pytest, pytest-cov, pre-commit |
| Seguridad | pip-audit, gitleaks, Dependabot |
| Entrega | Docker, GitHub Actions |

Las razones de las decisiones principales están en [`docs/adr/`](adr/).
