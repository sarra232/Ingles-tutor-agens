# Sistema de Aprendizaje de Inglés — Definición, Alcance y Reglas Maestras

Este repositorio es un **ecosistema de aprendizaje de inglés personalizado, persistente y multi-dispositivo**. Su objetivo es garantizar que cualquier sesión con el agente (sin importar el día, la hora, la conversación o la máquina) retome exactamente el contexto, progreso, vocabulario y necesidades del estudiante.

---

## 1. Protocolo de Persistencia de Contexto (Obligatorio en cada sesión)

Al iniciar cualquier conversación o tarea en este proyecto, el agente **DEBE**:

1. **Leer el estado actual del estudiante** antes de proponer contenido o evaluar:
   - `context/profile.md`: Nivel actual, objetivos, estilo de aprendizaje y disponibilidad.
   - `context/progress.md`: Ruta activa, módulo/tema actual, temas dominados y próximo paso sugerido.
   - `context/weaknesses-and-mistakes.md`: Errores frecuentes y puntos débiles a reforzar.
2. **Actualizar el contexto al avanzar**:
   - Cada vez que se complete una lección, quiz, charla o bloque de vocabulario, actualizar `context/progress.md` y registrar el resumen en `context/session-log.md`.
   - Si se detectan errores recurrentes (gramática, falsos amigos, estructura, pronunciación), anotarlos en `context/weaknesses-and-mistakes.md`.

---

## 2. Alcance del Sistema (Scope)

El sistema cubre cuatro pilares integrados:

1. **Ruta y Plan de Estudio (`ruta-y-plan/`)**:
   - Diseño progresivo por niveles (MCER: A1 → A2 → B1 → B2 → C1) adaptado a las metas del estudiante.
   - Objetivos medibles por módulo y criterios de dominio para avanzar.
2. **Material de Estudio (`material/`)**:
   - Documentos Markdown claros, estructurados para **ver, leer, copiar y practicar**.
   - Incluye tablas comparativas, ejemplos reales con traducción y notas de pronunciación figurada/IPA.
3. **Sistema de Vocabulario y Verbos (`vocabulario/` y `perfil/`)**:
   - **Vocabulario General (`vocabulario/`)**:
     - `vocabulario/vocabulario.md`: Tablas organizadas para lectura rápida y copia.
     - `vocabulario/vocabulario.csv`: Archivo compatible con **Excel**.
     - `vocabulario/index.html`: **Página web interactiva** con buscador, filtros por nivel de confianza (`Nueva / Desconocida`, `Poca confianza`, `Dominada`), modo Flashcards, pronunciación por voz (🔊) y botón para exportar cambios al agente.
   - **Ventana Exclusiva de Verbos y Conjugaciones (`vocabulario/verbos.*`)**:
     - `vocabulario/verbos.md`, `vocabulario/verbos.csv` y `vocabulario/verbos.html`: Tabla y aplicación web dedicada exclusivamente a los verbos con sus tiempos (**Infinitivo/Base**, **3ra Persona Presente (`-s`)**, **Gerundio (`-ing`)**, **Pasado Simple**, **Participio Pasado (`have/has + ...`)**, pronunciación y audio 🔊 por cada conjugación).
   - **Página Evolutiva de Perfil y Presentación (`perfil/`)**:
     - `perfil/mi-presentacion.md` y `perfil/index.html`: Página web y documento vivo donde se almacena el discurso personal y profesional de Wilson (quién es, dónde vive, personalidad, ambiciones, rutina como Java Dev, proyectos, etc.), con audio por frase y por bloque para practicar e ir expandiéndolo a medida que su nivel crece.
4. **Práctica Activa y Evaluación (`practica/`)**:
   - **Quices (`practica/quices/`)**: Evaluaciones diagnósticas y por módulo.
   - **Juegos (`practica/juegos/`)**: Retos de memoria, completar frases, asociación y widgets interactivos.
   - **Charlas (`practica/charlas/`)**: Sesiones de roleplay y conversación guiada con retroalimentación correctiva.

---

## 3. Arquitectura de Skills y Agentes Especializados

### Skills Disponibles (`.agents/skills/`)
- **`curriculum-planner`**: Creación y ajuste de la ruta de aprendizaje, planes de estudio y guías de estudio en `material/`.
- **`english-tutor`**: Explicaciones pedagógicas, sesiones de conversación (`charlas`), roleplays y corrección constructiva de errores.
- **`vocabulary-manager`**: Gestión y sincronización del vocabulario en Markdown (`vocabulario.md`), Excel (`vocabulario.csv`) y Web (`index.html`).
- **`quiz-and-games`**: Generación de quices interactivos, juegos de vocabulario/gramática y retos basados en repetición espaciada (SRS).

### Definiciones de Agentes / Roles (`.agents/agents/`)
- **`architect-planner.md`**: Arquitecto curricular encargado de estructurar rutas, módulos y métricas de avance.
- **`conversation-coach.md`**: Compañero de charla y roleplay que adapta su nivel de inglés al del estudiante y entrega feedback detallado.
- **`quiz-master.md`**: Evaluador gamificado que diseña retos basados en el historial de errores (`weaknesses-and-mistakes.md`) y el vocabulario activo.
- **`lexicon-keeper.md`**: Curador de vocabulario, phrasal verbs, idioms y collocations.

---

## 4. Reglas Pedagógicas y de Formato

- **Claridad y Copiabilidad**: Todo material en `material/` debe incluir bloques de ejemplos fáciles de copiar, estructuras tipo fórmula (ej. `Subject + Auxiliary + Verb + Object`) y pronunciación aproximada además de IPA cuando sea útil.
- **Enfoque Práctico (80/20)**: Priorizar el inglés de alto impacto (estructuras frecuentes, vocabulario cotidiano/profesional y fluidez comunicativa) sobre teoría gramatical abstracta.
- **Feedback Constructivo**: Durante charlas o quices, siempre mostrar:
  1. Lo que el estudiante dijo/escribió.
  2. La versión corregida natural.
  3. Una breve explicación del *porqué* en español.
