# Requisitos

## Problema

Una empresa que otorga crédito al consumo necesita decidir a qué solicitantes aprobar. Aprobar a un
cliente que no paga genera una pérdida directa; rechazar a uno que sí habría pagado es una venta
perdida. Hoy esa decisión depende de reglas fijas que no se ajustan al comportamiento real de los
clientes.

El proyecto construye un modelo que estima la **probabilidad de impago** de cada cliente a partir de
su historial de pagos y saldos, propone una decisión (aprobar o revisar) y explica qué variables
pesaron en ella, de forma que un analista pueda justificarla.

## Usuarios

| Usuario | Necesidad |
| --- | --- |
| Analista de crédito | Consultar el riesgo de un cliente y entender los motivos antes de decidir |
| Sistema de originación | Pedir una calificación por API como parte de un flujo automático |
| Área de riesgos | Revisar el desempeño del modelo, su calibración y posibles sesgos |

## Requisitos funcionales

- **RF-01.** Descargar el dataset desde su fuente oficial y verificar su integridad.
- **RF-02.** Validar el esquema de los datos (tipos, rangos y categorías) antes de usarlos.
- **RF-03.** Entrenar y comparar al menos tres modelos: regresión logística como línea base,
  XGBoost y LightGBM.
- **RF-04.** Calcular la probabilidad de impago calibrada para un cliente.
- **RF-05.** Proponer una decisión con un umbral elegido según el costo de cada tipo de error.
- **RF-06.** Devolver las variables que más contribuyeron a la calificación de cada cliente.
- **RF-07.** Exponer la calificación mediante una API REST.
- **RF-08.** Ofrecer un tablero web para probar el modelo y ver sus métricas.
- **RF-09.** Generar un reporte de evaluación con métricas, curvas y análisis de equidad.

## Requisitos no funcionales

- **RNF-01. Reproducibilidad.** El mismo código y los mismos datos producen las mismas métricas
  (dependencias fijadas y semillas controladas).
- **RNF-02. Rendimiento.** La API responde en menos de 200 ms (p95) por solicitud en un equipo de
  desarrollo.
- **RNF-03. Seguridad.** Sin secretos en el repositorio, entradas validadas, autenticación por API key
  y dependencias auditadas en cada cambio.
- **RNF-04. Calidad.** Cobertura de pruebas de al menos 80 % en `src/`, sin errores de lint ni de tipos.
- **RNF-05. Mantenibilidad.** Código modular, configuración separada del código y decisiones
  técnicas documentadas.
- **RNF-06. Portabilidad.** El proyecto completo se levanta con Docker en un solo comando.

## Criterios de éxito del modelo

Se fijan antes de entrenar, para evaluar el modelo contra un objetivo y no ajustar el objetivo al
resultado. Se miden sobre un conjunto de prueba que no se usa en ninguna otra etapa.

| Métrica | Mínimo aceptable | Motivo |
| --- | --- | --- |
| AUC-ROC | 0.75 | Capacidad de ordenar clientes de menor a mayor riesgo |
| Estadístico KS | 0.35 | Métrica estándar en la industria de crédito para separación de clases |
| Brier score | Menor que el de la línea base | Las probabilidades deben ser confiables, no solo el orden |
| Mejora sobre la línea base | AUC al menos 0.01 mayor | Un modelo complejo solo se justifica si supera al simple |

Si ningún modelo alcanza los mínimos, se documenta el resultado y sus causas en lugar de cambiar los
umbrales.

## Alcance

**Incluye**

- Pipeline completo: datos, entrenamiento, evaluación, explicación y servicio.
- Análisis de equidad por sexo, edad y estado civil.
- Documentación técnica y del modelo (model card).

**No incluye**

- Datos de clientes reales ni datos personales identificables.
- Despliegue productivo, monitoreo en línea o reentrenamiento automático.
- Decisiones de crédito reales: el modelo es un ejercicio de ingeniería y analítica.

## Supuestos y restricciones

- Los datos provienen de clientes de tarjeta de crédito en Taiwán (2005). Los patrones pueden no
  trasladarse a otro país ni a otra época; se documenta como limitación.
- Los costos de error (aprobar a un cliente que no paga frente a rechazar a uno que sí paga) son
  supuestos configurables, no cifras de una empresa real.
- Sexo, edad y estado civil no se usan como variables del modelo; se conservan solo para medir si el
  modelo trata de forma distinta a cada grupo.
