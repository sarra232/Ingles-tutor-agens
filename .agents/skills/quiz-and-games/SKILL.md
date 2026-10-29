---
name: quiz-and-games
description: >-
  Use this skill when the user wants to test their knowledge through quizzes, flashcards,
  word games, grammar challenges, or interactive exercises.
---

# Quiz and Games Skill

Este skill permite evaluar y retar el conocimiento del estudiante mediante **quices estructurados**, **juegos dinámicos en el chat** o **widgets interactivos HTML**.

## Fuentes para Generar Retos

Antes de crear cualquier quiz o juego, consulta:
1. `context/progress.md`: Para saber qué temas ya vio el estudiante.
2. `context/weaknesses-and-mistakes.md`: Para incluir preguntas trampa sobre sus errores reales previos (al menos el 30% del quiz debe atacar debilidades previas).
3. `vocabulario/vocabulario.md`: Para evaluar palabras en estado `Nuevo` o `En práctica`.

## Tipos de Dinámicas Disponibles

1. **Quiz Rápido Interactivo (Chat o Widget UI)**:
   - 5 a 10 preguntas mezclando:
     - Opción múltiple.
     - Traducción inversa (Español → Inglés).
     - Detectar y corregir el error (*Spot the mistake*).
     - Completar el espacio con el tiempo verbal o phrasal verb correcto.
2. **Juegos de Reto**:
   - **Cadena de Palabras / Contexto**: Crear una historia corta usando 5 palabras aleatorias de `vocabulario.md`.
   - **Batalla de Tiempos Verbales**: Transformar una oración base en 4 tiempos distintos rápidamente.
   - **Adivina la Palabra (Taboo en Inglés)**: El agente describe una palabra del vocabulario en inglés sencillo sin decirla, y el estudiante debe adivinarla.
   - **Verdadero o Falso Gramatical**: Oraciones con errores típicos de hispanohablantes.

## Registro de Resultados

Al finalizar un quiz o juego:
1. Calcula el puntaje (ej. `8/10 - 80%`).
2. Guarda el historial del quiz en `practica/quices/YYYY-MM-DD-quiz-<tema>.md` si fue una evaluación formal de módulo.
3. Si el estudiante dominó palabras que estaban `En práctica`, actualiza su estado a `Dominado` usando `vocabulary-manager`.
4. Si falló en algún punto gramatical o palabra, regístralo en `context/weaknesses-and-mistakes.md` y actualiza `context/progress.md`.
