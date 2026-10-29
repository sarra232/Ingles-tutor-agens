---
name: curriculum-planner
description: >-
  Use this skill when designing, updating, or reviewing the English learning roadmap (ruta),
  study plan (plan de estudio), or creating structured study materials in the material/ directory.
  Also use it when updating student progress in context/progress.md after completing a module or lesson.
---

# Curriculum Planner Skill

Este skill guía la creación y mantenimiento de la **Ruta de Aprendizaje**, el **Plan de Estudio** y el **Material Didáctico** del estudiante.

## Procedimiento Paso a Paso

1. **Verificar Contexto**:
   - Lee `context/profile.md` y `context/progress.md` para conocer el nivel actual, metas y disponibilidad de tiempo del estudiante.
2. **Diseño o Actualización de la Ruta (`ruta-y-plan/roadmap.md`)**:
   - Estructura la ruta en fases claras (ej. Fase 1: Supervivencia y Base A1-A2, Fase 2: Independencia Conversacional B1, Fase 3: Fluidez Operativa B2+).
   - Cada módulo debe especificar:
     - **Objetivo comunicativo** (¿Qué podrá hacer el estudiante en la vida real?).
     - **Gramática clave**.
     - **Vocabulario meta**.
     - **Hito de validación** (quiz o charla necesaria para darlo por superado).
3. **Creación de Material de Estudio (`material/`)**:
   - Ubica el archivo en la subcarpeta correspondiente:
     - `material/01-fundamentos/`
     - `material/02-gramatica/`
     - `material/03-lecturas-y-dialogos/`
     - `material/04-pronunciacion-y-listening/`
   - Usa siempre la siguiente estructura en cada documento de material:
     1. **Resumen Ejecutivo (¿Para qué sirve y cuándo se usa?)**
     2. **Fórmula / Estructura Visual** (en bloques de código o tablas para fácil lectura y copia)
     3. **Ejemplos Prácticos** (Inglés | Pronunciación aproximada | Español)
     4. **Errores Comunes a Evitar** (especialmente para hispanohablantes)
     5. **Mini-Ejercicio de Práctica Rápida**
4. **Registro de Progreso**:
   - Al crear nuevo material o completar un tema, actualiza `context/progress.md` y añade la entrada en `context/session-log.md`.
