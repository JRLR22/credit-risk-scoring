# credit-risk-scoring

Modelo de riesgo crediticio que estima la probabilidad de impago de un cliente, propone una decisión
según el costo de cada tipo de error y explica qué variables pesaron en ella. Incluye API en FastAPI,
tablero en Streamlit, pruebas e integración continua.

**Estado:** en diseño. El plan por versiones está en [`docs/plan.md`](docs/plan.md).

## Documentación

| Documento | Contenido |
| --- | --- |
| [Requisitos](docs/requisitos.md) | Problema, requisitos, criterios de éxito y alcance |
| [Arquitectura](docs/arquitectura.md) | Componentes, flujo de datos y diseño de la API |
| [Decisiones (ADR)](docs/adr/) | Razones de las decisiones técnicas |
| [Estándares](docs/estandares.md) | Reglas de código, pruebas, seguridad y Git |
| [Plan de trabajo](docs/plan.md) | Versiones, tareas y riesgos |

## Datos

Se usa el dataset [Default of Credit Card Clients](https://doi.org/10.24432/C55S3H) de UCI Machine
Learning Repository (licencia CC BY 4.0): 30,000 clientes de tarjeta de crédito en Taiwán, 2005.

> Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive
> accuracy of probability of default of credit card clients. *Expert Systems with Applications*,
> 36(2), 2473–2480.

## Licencia

El código se distribuye bajo la licencia [MIT](LICENSE). El dataset conserva su propia licencia
(CC BY 4.0) y requiere atribución.
