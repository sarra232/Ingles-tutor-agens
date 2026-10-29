---
name: vocabulary-manager
description: >-
  Use this skill whenever adding, editing, reviewing, or syncing English vocabulary,
  verbs with full tense conjugations, phrasal verbs, idioms, or expressions across Markdown,
  Excel CSV, and the interactive web pages (vocabulario/index.html, vocabulario/verbos.html, perfil/index.html).
---

# Vocabulary, Verbs & Profile Manager Skill

Este skill asegura que todo el vocabulario, los verbos conjugados y el perfil evolutivo de Wilson se mantengan **100% sincronizados**:

## 1. Banco General de Vocabulario (`vocabulario/vocabulario.*`)
Archivos sincronizados:
- `vocabulario/vocabulario.md`
- `vocabulario/vocabulario.csv`
- `vocabulario/index.html`

### Niveles de Confianza (Estado)
Cada palabra tiene uno de estos 3 estados basados en la confianza real de Wilson:
- `Nueva / Desconocida`: Palabra que acaba de conocer (ej. `smoothly`) y necesita familiarizarse.
- `Poca confianza`: Palabra que reconoce al leer pero aún no usa con seguridad o no sabe en qué contexto encaja (ej. `standup`).
- `Dominada`: Palabra que ya entiende, pronuncia bien y usa activamente.

## 2. Ventana Exclusiva de Verbos y Conjugaciones (`vocabulario/verbos.*`)
Cuando se agregue un **Verbo** o **Phrasal Verb**, además o en lugar de un término aislado, debe registrarse en la ventana exclusiva de verbos con **todas sus conjugaciones clave**:
- `vocabulario/verbos.md`
- `vocabulario/verbos.csv`
- `vocabulario/verbos.html`

### Campos obligatorios por cada verbo:
1. **Base / Present (`I/You/We/They`)**: ej. `Build` (`/bɪld/ - bíld`)
2. **3rd Person (`He/She/It`)**: ej. `Builds` (`/bɪldz/ - bílds`)
3. **Continuous (`-ing`)**: ej. `Building` (`/ˈbɪl.dɪŋ/ - bílding`)
4. **Past Simple (`Pasado`)**: ej. `Built` (`/bɪlt/ - bílt`)
5. **Past Participle (`Have/Has ...`)**: ej. `Built` (`/bɪlt/ - bílt`)
6. **Tipo**: `Regular` o `Irregular`
7. **Español**: Significado principal.
8. **Ejemplos en Presente, Pasado y Perfecto**: Oraciones reales del contexto de Wilson.
9. **Estado de Confianza**: `Nueva / Desconocida`, `Poca confianza`, `Dominada`.

## 3. Cómo Reporta el Estudiante Palabras Desconocidas o de Poca Confianza
1. **En el chat**: Cada vez que Wilson mencione que una palabra es nueva o que no se siente confiado usándola, el agente debe:
   - Explicar su significado exacto, cuándo usarla y cuándo **no** usarla (ej. formal vs informal, técnico vs cotidiano).
   - Registrarla o actualizar su estado a `Nueva / Desconocida` o `Poca confianza` en los archivos de vocabulario/verbos.
2. **Desde la Web (`vocabulario/index.html` o `vocabulario/verbos.html`)**:
   - El estudiante puede cambiar el estado de cualquier palabra en la web y hacer clic en **"📋 Copiar reporte para el Agente"** para pegarlo en el chat y sincronizar los archivos.
