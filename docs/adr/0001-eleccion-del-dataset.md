# ADR 0001: Elección del dataset

- **Estado:** aceptada
- **Fecha:** 2026-11-17

## Contexto

El proyecto necesita datos públicos de crédito con historial de pagos, una variable de impago y una
licencia que permita usarlos y citarlos en un repositorio público. También deben poder descargarse de
forma automática, sin cuentas ni pasos manuales, para que la integración continua y cualquier persona
reproduzcan los resultados.

## Opciones evaluadas

| Dataset | Registros | Licencia | Descarga automática | Observaciones |
| --- | --- | --- | --- | --- |
| Default of Credit Card Clients (UCI) | 30,000 | CC BY 4.0 | Sí | Historial de 6 meses de pagos y saldos |
| Statlog German Credit (UCI) | 1,000 | CC BY 4.0 | Sí | Muy pequeño para comparar modelos con confianza |
| Give Me Some Credit (Kaggle) | 150,000 | Reglas de la competencia | No, requiere cuenta | Redistribución restringida |
| Home Credit Default Risk (Kaggle) | 300,000+ | Reglas de la competencia | No, requiere cuenta | Varias tablas; complejidad mayor al alcance |

## Decisión

Usar **Default of Credit Card Clients** de UCI Machine Learning Repository.

- 30,000 clientes con 23 variables: límite de crédito, datos demográficos, estado de pago de los
  últimos seis meses, saldos facturados y montos pagados.
- Variable objetivo: impago en el mes siguiente (cerca de 22 % de casos positivos).
- Licencia CC BY 4.0, que permite usarlo con atribución.
- Es un dataset muy citado, lo que permite comparar los resultados con trabajos publicados.

Cita:

> Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive
> accuracy of probability of default of credit card clients. *Expert Systems with Applications*,
> 36(2), 2473–2480. Dataset: https://doi.org/10.24432/C55S3H

## Consecuencias

- Las clases están desbalanceadas (78/22): se usa validación estratificada y métricas que no dependen
  de la proporción de clases.
- Hay valores no documentados en `EDUCATION` (0, 5, 6), `MARRIAGE` (0) y en las variables de estado de
  pago (-2, 0). Se definen reglas explícitas para tratarlos y se documentan en el esquema.
- Los montos están en dólares de Taiwán y los datos son de 2005. El modelo no se presenta como
  aplicable a otro mercado sin reentrenarlo.
- Incluye sexo, edad y estado civil. No se usan como variables del modelo, pero se conservan para
  medir la equidad de sus decisiones.
