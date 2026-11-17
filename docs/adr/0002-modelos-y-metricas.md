# ADR 0002: Modelos candidatos y métricas de decisión

- **Estado:** aceptada
- **Fecha:** 2026-11-17

## Contexto

Los datos son tabulares, con unas decenas de variables y 30,000 registros. El resultado debe ser una
probabilidad confiable, explicable cliente por cliente y rápida de calcular en una API.

## Decisión

**Modelos**

1. **Regresión logística** como línea base. Es interpretable, rápida y es el estándar histórico en
   scorecards de crédito. Cualquier otro modelo debe superarla para justificarse.
2. **XGBoost** y **LightGBM**. Los modelos de árboles con gradient boosting son el estado del arte en
   datos tabulares de este tamaño y capturan relaciones no lineales sin tanta ingeniería manual.

Se descartan las redes neuronales: en datos tabulares de este tamaño no suelen superar a los árboles
y son más difíciles de explicar y calibrar.

**Métricas**

- **AUC-ROC** y **KS** para comparar la capacidad de ordenar clientes por riesgo.
- **Brier score** y curva de calibración para verificar que las probabilidades sean confiables.
- La decisión final no se toma con el umbral de 0.5, sino con el que **minimiza el costo esperado**,
  usando una matriz de costos configurable:

| | Paga | No paga |
| --- | --- | --- |
| **Aprobado** | 0 | Costo de impago (supuesto: 5) |
| **Rechazado** | Margen perdido (supuesto: 1) | 0 |

Con esa matriz, aprobar a un cliente que no paga cuesta cinco veces más que rechazar a uno que sí
paga. Los valores están en la configuración y el reporte muestra cómo cambia el umbral al variarlos.

**Explicabilidad**

SHAP (TreeExplainer para los árboles), porque da contribuciones por cliente que suman la predicción y
se pueden mostrar como motivos de la decisión.

## Consecuencias

- Hay que calibrar el modelo elegido (Platt o isotónica) porque los árboles no producen
  probabilidades calibradas por defecto.
- El umbral depende de supuestos de negocio; se reporta junto con esos supuestos.
- Se añaden dos dependencias de modelado (XGBoost y LightGBM) que deben fijarse y auditarse.
