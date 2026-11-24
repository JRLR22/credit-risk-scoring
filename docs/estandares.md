# Estándares de desarrollo

Reglas que sigue todo cambio en el repositorio. La integración continua verifica las que se pueden
automatizar; el resto se revisa en cada pull request.

## Código

- Python 3.11. Nombres de módulos, funciones y variables en inglés; documentación y mensajes de
  commit en español.
- Formato y lint con **Ruff**; tipos revisados con **mypy** en modo estricto sobre `src/` y `api/`.
- Anotaciones de tipo en todas las funciones públicas.
- Funciones con una sola responsabilidad. Si una función necesita un comentario para explicar qué
  hace, probablemente debe dividirse o renombrarse.
- Los comentarios explican el porqué de una decisión, no lo que el código ya dice.
- Sin valores fijos en el código: rutas, semillas, umbrales y costos viven en `config.py` o en
  variables de entorno.
- `logging` en lugar de `print`. Los logs nunca incluyen datos de clientes ni secretos.

## Datos y modelos

- El conjunto de prueba se separa antes de cualquier análisis y solo se usa en la evaluación final.
- Toda transformación que aprende de los datos (escalado, imputación, codificación) se ajusta solo con
  datos de entrenamiento, dentro de un `Pipeline`.
- Semillas fijas en todo proceso aleatorio.
- Los criterios de éxito se definen antes de entrenar ([requisitos](requisitos.md)) y no se cambian
  para que un modelo los cumpla.
- Cada modelo guardado incluye versión, fecha, métricas, hash de los datos y versiones de librerías.
- Los modelos se cargan solo desde rutas del proyecto y se verifica su hash antes de usarlos, porque
  los archivos serializados pueden ejecutar código.

## Pruebas

- **pytest**, con cobertura mínima de 80 % en `src/`.
- Todo cambio de comportamiento incluye pruebas nuevas o actualizadas.
- Tipos de prueba:
  - Unitarias: limpieza, variables derivadas, métricas, umbral.
  - De datos: el esquema rechaza valores inválidos.
  - De modelo: AUC mínimo en un conjunto fijo y relaciones esperadas (más meses de atraso no
    reduce el riesgo).
  - De API: respuestas correctas, validación de entradas, autenticación y errores.
- Las pruebas no descargan datos ni dependen de la red; usan datos sintéticos pequeños.

## Seguridad

- Ningún secreto en el repositorio. La configuración sensible se lee de variables de entorno;
  `.env.example` documenta cuáles existen sin valores reales.
- **gitleaks** en pre-commit y en la CI para detectar secretos.
- **pip-audit** en la CI para detectar dependencias con vulnerabilidades conocidas; **Dependabot**
  propone actualizaciones.
- La API valida toda entrada con Pydantic (tipos, rangos, campos obligatorios), exige API key, limita
  la tasa de peticiones y el tamaño del cuerpo, y restringe CORS a orígenes configurados.
- Los errores devueltos al cliente no incluyen trazas, rutas ni versiones.
- La imagen Docker se construye en varias etapas, sobre una base ligera, y se ejecuta con un usuario
  sin privilegios.

## Git y revisiones

- `main` siempre está en un estado funcional y protegida: solo recibe cambios por pull request con la
  CI en verde.
- Ramas con prefijo según el tipo de cambio:

| Prefijo | Uso |
| --- | --- |
| `feature/` | Funcionalidad nueva |
| `fix/` | Corrección de un error |
| `refactor/` | Cambio interno sin alterar el comportamiento |
| `docs/` | Documentación |
| `chore/` | Mantenimiento: dependencias, configuración, limpieza |
| `test/` | Pruebas |

- Mensajes de commit en español, en infinitivo y con una primera línea de máximo 72 caracteres:
  `Agregar validación del esquema de datos`. El cuerpo explica el porqué si no es evidente.
- Un pull request por tema, enlazado a su issue (`Closes #12`), integrado con **Squash and merge**.
- Versiones con [Semantic Versioning](https://semver.org/lang/es/) y registro en
  [`CHANGELOG.md`](../CHANGELOG.md).

## Documentación

- Las decisiones técnicas relevantes se registran como ADR en [`docs/adr/`](adr/).
- El README explica el problema, los resultados, cómo ejecutar el proyecto y sus limitaciones.
- El modelo final se documenta en una model card: datos, métricas, equidad, usos previstos y usos no
  recomendados.

## Definición de terminado

Un cambio está terminado cuando:

1. La CI pasa: lint, tipos, pruebas, cobertura y auditoría de seguridad.
2. Incluye pruebas para el comportamiento nuevo.
3. La documentación afectada está actualizada.
4. El pull request describe qué cambia, por qué y cómo se probó.
