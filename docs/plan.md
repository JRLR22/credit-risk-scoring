# Plan de trabajo

El proyecto avanza por versiones. Cada versión es un milestone en GitHub y cada tarea es un issue;
los pull requests cierran los issues que resuelven.

| Versión | Objetivo |
| --- | --- |
| v0.1.0 | Base del proyecto: estructura, calidad de código y CI |
| v0.2.0 | Datos: descarga, validación y análisis exploratorio |
| v0.3.0 | Modelado: línea base, modelos candidatos, calibración y umbral |
| v0.4.0 | Explicabilidad y equidad |
| v0.5.0 | Servicio: API y tablero |
| v1.0.0 | Entrega: Docker, seguridad, documentación final y release |

## v0.1.0: Base del proyecto

- Configurar el paquete con `pyproject.toml` y dependencias fijadas.
- Configurar Ruff, mypy y pytest con cobertura.
- Configurar pre-commit con Ruff y gitleaks.
- Agregar Makefile con las tareas comunes (`install`, `lint`, `test`, `train`, `serve`).
- Crear la CI en GitHub Actions: lint, tipos, pruebas y auditoría de dependencias.
- Agregar módulo de configuración y logging.

## v0.2.0: Datos

- Descargar el dataset desde UCI con verificación SHA-256.
- Definir y probar el esquema de datos con pandera, incluidas las reglas para valores no documentados.
- Separar el conjunto de prueba estratificado y guardarlo de forma reproducible.
- Análisis exploratorio en notebook: distribución de clases, variables clave, correlaciones.
- Implementar variables derivadas del historial de pagos con pruebas.

## v0.3.0: Modelado

- Entrenar la regresión logística como línea base con validación cruzada.
- Entrenar XGBoost y LightGBM con búsqueda de hiperparámetros acotada.
- Calibrar el modelo elegido y comparar curvas de calibración.
- Seleccionar el umbral por costo esperado y documentar la sensibilidad a los supuestos.
- Guardar el modelo con metadatos y verificación de hash.
- Generar el reporte de evaluación (métricas, ROC, KS, calibración).

## v0.4.0: Explicabilidad y equidad

- Calcular explicaciones SHAP globales y por cliente.
- Medir diferencias de aprobación y error entre grupos de sexo, edad y estado civil.
- Redactar la model card.

## v0.5.0: Servicio

- Implementar la API con FastAPI: `/health`, `/v1/model` y `/v1/score`.
- Agregar autenticación por API key, límite de peticiones y CORS configurable.
- Pruebas de la API: casos válidos, inválidos, autenticación y errores.
- Medir la latencia y documentarla.
- Implementar el tablero en Streamlit.

## v1.0.0: Entrega

- Dockerfile en varias etapas con usuario sin privilegios y `docker-compose.yml`.
- Construcción de la imagen en la CI.
- README final en español e inglés con resultados y limitaciones.
- Publicar el release v1.0.0 con notas de versión.

## Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Fuga de información del conjunto de prueba al entrenamiento | Separar la prueba primero; transformaciones dentro de `Pipeline`; prueba automatizada que lo verifica |
| Modelo sesgado contra un grupo | Excluir variables sensibles del modelo y medir diferencias por grupo |
| Probabilidades mal calibradas | Calibración explícita y Brier score como criterio |
| Fuente de datos no disponible | Verificación por hash y documentación de la fuente alterna |
| Dependencias con vulnerabilidades | pip-audit en la CI y Dependabot |
