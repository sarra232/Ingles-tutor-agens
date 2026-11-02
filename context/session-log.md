# Historial de Sesiones (`session-log.md`)

Registro cronológico de sesiones para mantener trazabilidad completa entre diferentes días y dispositivos.

---

## 2026-10-28 — Sesión 1: Ambiente, GitHub Pages, Diagnóstico, Perfil Evolutivo, Ventana de Verbos y Mini-Reto 1.1
- **Actividad**:
  - Configuración completa del ambiente (`AGENTS.md`, `.agents/skills/`, `.agents/agents/`, `context/`).
  - Inicialización de repositorio Git y portal para **GitHub Pages** (`index.html` + `.github/workflows/deploy-pages.yml`).
  - Creación de **Ruta (`ruta-y-plan/roadmap.md`)** y **Plan de Estudio 1-2h/día (`ruta-y-plan/plan-estudio.md`)**.
  - Aplicación y calificación del **Examen Diagnóstico Integral** (`practica/quices/01-examen-diagnostico.md`) — Puntaje: **7.2 / 10**.
  - Creación de la página **Mi Perfil y Presentación Evolutiva** (`perfil/index.html` y `perfil/mi-presentacion.md`).
  - Creación de la **Ventana Exclusiva de Verbos y Conjugaciones** (`vocabulario/verbos.html`, `verbos.md`, `verbos.csv`) con 15 verbos clave en 5 formas verbales y audio 🔊.
  - Ajuste del motor de voz en las 3 páginas web para forzar voces nativas en inglés (`en-US` / `en-GB`) con selector de voz.
  - Realización del **Mini-Reto de 5 frases de la Lección 1.1** — Puntaje: **8.5 / 10** (Corrigió con éxito `systems engineer`, `live in a town`, `its landscapes`, `wonderful`, `quiet`, `finish building`, `attend` y `teammates`).
- **Próximo paso**: Roleplay #1 de presentación o Lección 1.2 (Estructura Maestra de la Oración y Conectores).

---

## 2026-10-29 — Sesión 2: Roleplay #1, Lección 1.2 y Estudio React en Vivo con Google AI Studio
- **Actividad**:
  - Realización del **Mini-Roleplay #1 con Alex** (`practica/charlas/2026-10-29-welcome-call-alex.md`) — Puntaje: **8.8 / 10**.
  - Creación de la **Lección 1.2: Estructura Maestra de la Oración y Conectores** (`material/01-fundamentos/02-estructura-maestra-y-conectores.md`).
  - Construcción de **Orus React Live English Studio** (`practica/voz/index.html` + `practica/voz/voice_server.py` + `practica/voz/live_state.json`) conectado a **Google AI Studio (`GEMINI_API_KEY` en `.env`)** y voz femenina neural (`edge-tts` — `Jenny Neural`).
  - Configuración de `.gitignore` y `.env.example` para proteger la variable de ambiente `GEMINI_API_KEY`.
  - Ajuste del estilo del tutor a **informal, directo, concreto y sin adulaciones** (`context/profile.md` y `voice_server.py`).
  - **Práctica Hablada por Micrófono en Edge (Puntaje: 9.2 / 10)**:
    - Pronunció con 92% de precisión: `surrounded by nature`, `feels so alive`, `enjoy hiking with my dogs`, `As for my hobbies, I am a very active person`, `different projects`, `fix it`, y `help our teammates`.
    - Nuevos puntos detectados en habla espontánea para practicar: `make a mistake` (no *do a mistake*) y `I prefer to continue practicing vocabulary` (no *prefer continue practice*).
- **Próximo paso**: Sincronizar vocabulario/verbos/perfil v1.1 y practicar verbos encadenados (`prefer to + verb`, `continue + -ing`, `make vs do`).

---

## 2026-10-30 — Sesión 3: Sincronización v1.1, Calentamiento de Verbos/Collocations y Módulo 2.1 (Pasado Simple y Daily Standup)
- **Actividad**:
  - Sincronización de `vocabulario/vocabulario.*` (31 términos), `vocabulario/verbos.*` (21 verbos) y `perfil/*` (v1.1).
  - Creación de la **Lección 2.1: Hablar del Pasado sin Trabarse (Pasado Simple, Verbos Clave y Daily Standup)** (`material/02-gramatica/01-pasado-simple-y-daily-standup.md`).
  - Inicio del servidor de voz (`localhost:8090`) y carga de los nuevos slides, retos y escena de Daily Standup en `practica/voz/live_state.json`.
