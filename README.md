# 🇬🇧 Centro Personal de Aprendizaje de Inglés

Este repositorio contiene toda la estructura, memoria persistente, skills, agentes, materiales y banco de vocabulario para aprender y practicar inglés de manera continua desde cualquier lugar, hora o máquina.

---

## 📁 Estructura del Proyecto

```text
Ingles/
├── AGENTS.md                        # Reglas maestras (se cargan automáticamente en cada sesión)
├── .agents/
│   ├── skills/                      # Procedimientos especializados del sistema
│   │   ├── curriculum-planner/      # Diseño de ruta, plan de estudio y material
│   │   ├── english-tutor/           # Tutoría, explicaciones y charlas (roleplay)
│   │   ├── vocabulary-manager/      # Sincronización triple de vocabulario (MD, Excel, Web)
│   │   └── quiz-and-games/          # Generación de quices, juegos y retos
│   └── agents/                      # Definiciones y alcance de cada rol de agente
│       ├── architect-planner.md
│       ├── conversation-coach.md
│       ├── quiz-master.md
│       └── lexicon-keeper.md
├── context/                         # 🧠 Memoria persistente del estudiante
│   ├── profile.md                   # Nivel, objetivos y preferencias
│   ├── progress.md                  # Estado actual, módulo activo y métricas
│   ├── session-log.md               # Historial de sesiones fecha por fecha
│   └── weaknesses-and-mistakes.md   # Errores frecuentes a reforzar en quices/charlas
├── ruta-y-plan/                     # 🗺️ Ruta de aprendizaje y plan de estudio
├── material/                        # 📖 Documentos para ver, leer, copiar y practicar
│   ├── 01-fundamentos/
│   ├── 02-gramatica/
│   ├── 03-lecturas-y-dialogos/
│   └── 04-pronunciacion-y-listening/
├── vocabulario/                     # 🔤 Sistema Triple de Vocabulario
│   ├── vocabulario.md               # Tabla Markdown para lectura y copia rápida
│   ├── vocabulario.csv              # Archivo compatible con Excel / Google Sheets
│   └── index.html                   # App web interactiva con audio (🔊) y Flashcards
└── practica/                        # 🎯 Evaluaciones y práctica activa
    ├── quices/
    ├── juegos/
    └── charlas/
```

---

## 🔄 ¿Cómo funciona la persistencia entre días, horas o máquinas?

1. **Regla Automática (`AGENTS.md`)**: Siempre que abras esta carpeta en Antigravity, el agente lee automáticamente `AGENTS.md`, que le ordena consultar `context/profile.md`, `context/progress.md` y `context/weaknesses-and-mistakes.md`.
2. **Portabilidad Total**: Todos los datos viven en archivos planos dentro de esta carpeta. Si sincronizas esta carpeta con **Git / GitHub**, Google Drive o OneDrive, cualquier máquina tendrá exactamente el mismo progreso, vocabulario y contexto al instante.
