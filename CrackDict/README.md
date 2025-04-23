# CrackDict

CrackDict es una herramienta avanzada para la generación de diccionarios personalizables, útil para pruebas de penetración, análisis de contraseñas y otros fines relacionados con ciberseguridad y automatización.

## Características

- **Modo Automático**: genera combinaciones a partir de palabras clave.
- **Modo Manual**: genera combinaciones a partir de un conjunto de caracteres.
- **Transformación Leet**: sustituciones tipo a→4, e→3, i→1, etc.
- **Exclusión de patrones**: evita palabras o secuencias no deseadas mediante expresiones regulares.
- **Multiprocesamiento**: aprovecha varios núcleos del procesador para mayor velocidad.
- **Control de longitud y complejidad**: define mínimo, máximo y símbolos a incluir.
- **Salida limpia**: genera archivos `.txt` listos para herramientas como Hydra, John the Ripper, etc.

## Instalación y uso

Clona el repositorio y ejecuta el script:

```bash
git clone https://github.com/S4ntiHack/Ethical_Hacking/CrackDict
cd CrackDict
python3 CrackDict.py
