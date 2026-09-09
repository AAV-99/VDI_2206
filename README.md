# VDI 2206 — Framework Multi-Agente para Revisión de Diseño Mecatrónico

Framework basado en **CrewAI Flows** y modelos de lenguaje **Google Gemini** para automatizar el ciclo de diseño conceptual mecatrónico bajo la norma **VDI 2206**. El sistema ejecuta una tripulación de 4 agentes especializados por disciplina —Integración/Requerimientos, Mecánica, Electrónica/Instrumentación y Control/Automatización— para generar reportes individuales por disciplina y un dossier técnico consolidado, a partir de un **único contexto de proyecto** provisto por el usuario.

---

## 📑 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Guía Paso a Paso (Windows)](#-guía-paso-a-paso)
- [Estructura de Archivos de Configuración](#-estructura-de-archivos-de-configuración)
- [Archivos de Salida](#-archivos-de-salida-output)
- [Visualización de Entregables](#-visualización-de-entregables-markdown-en-vs-code)

---

## Requisitos Previos

- Sistema operativo Windows
- Cuenta de Google (para la API key de Gemini)
- Conexión a internet para descargar dependencias

---

## 📋 Guía Paso a Paso

Sigue esta secuencia de pasos para configurar el entorno desde cero en un sistema Windows recién formateado o sin herramientas previas.

### 1. Instalar Software Base

- **Git for Windows:** necesario para clonar el proyecto. Descarga e instala desde la [Guía de Instalación Oficial de Git](https://git-scm.com/download/win).
- **Visual Studio Code:** editor de código recomendado. Descarga e instala desde la [Guía de Instalación Oficial de VS Code](https://code.visualstudio.com/docs/setup/windows).

### 2. Obtener API Key de Google Gemini

1. Accede a [Google AI Studio](https://aistudio.google.com/) e inicia sesión con tu cuenta de Google.
2. Genera una nueva clave en la sección **Get API Key**. Consulta la [Documentación Oficial de Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key) para más detalles sobre cuotas y permisos.

### 3. Instalar `uv` (Administrador de Entornos y Python)

**uv** se encarga de descargar Python y gestionar dependencias automáticamente.

1. Abre **PowerShell** en tu equipo.
2. Ejecuta el comando de instalación oficial (consulta la [Guía de Instalación Oficial de uv](https://docs.astral.sh/uv/getting-started/installation/)):

```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> ⚠️ **Importante:** una vez terminada la instalación, **cierra y vuelve a abrir PowerShell** para que los comandos queden registrados en las variables de sistema.

### 4. Verificar Git y uv

Antes de continuar, confirma que Git y `uv` quedaron correctamente instalados y accesibles desde la terminal. Cierra y vuelve a abrir PowerShell si acabas de instalar algo, y ejecuta:

```powershell
git --version
uv --version
```

Deberías obtener una salida similar a esta (los números de versión pueden variar):

```
git version 2.45.1.windows.1
uv 0.4.29
```

| Comando | Qué verifica | Si falla |
|---|---|---|
| `git --version` | Git for Windows quedó instalado y en el `PATH` | Reinstala Git marcando la opción "Add to PATH" durante la instalación, o reinicia la terminal |
| `uv --version` | `uv` quedó instalado correctamente | Reinicia PowerShell; si persiste, vuelve a ejecutar el comando de instalación del paso 3 |

> ⚠️ Si alguno de estos comandos no es reconocido (`no se reconoce como un comando interno o externo...`), **no continúes** con los siguientes pasos — el resto de la guía asume que estas herramientas ya responden correctamente. Revisa la instalación correspondiente antes de seguir.

### 5. Clonar el Repositorio y Abrir en VS Code

1. En PowerShell, navega a la carpeta donde guardarás tus proyectos (por ejemplo, el Escritorio):

```powershell
   cd ~\Desktop
```

2. Clona el repositorio:

```powershell
   git clone https://github.com/AAV-99/VDI_2206
```

3. Abre VS Code y, desde el menú **Archivo > Abrir carpeta...** (`File > Open Folder...`), selecciona la carpeta del proyecto clonado (`vdi`).

### 6. Sincronizar el Entorno Local y Crear la API Key

1. Abre la terminal integrada de VS Code (`Ctrl + ~` o menú **Terminal > Nueva Terminal**).
2. Ejecuta el siguiente comando para crear el entorno virtual e instalar CrewAI y todas las librerías necesarias definidas en `pyproject.toml` (más información en la [Guía de Inicio Rápido de CrewAI](https://docs.crewai.com/installation)):

```powershell
   uv sync
```

3. Verifica que CrewAI quedó instalado correctamente dentro del entorno del proyecto:

```powershell
   uv run crewai --version
```

   Deberías obtener una salida similar a esta (el número de versión puede variar):

```
   crewai, version 1.15.17
```

   Si el comando falla o no reconoce `crewai`, vuelve a ejecutar `uv sync` dentro de la carpeta raíz del proyecto (junto a `pyproject.toml`) y reintenta.

4. En la raíz del proyecto (junto al archivo `pyproject.toml`), crea un nuevo archivo llamado `.env`.
5. Agrega tu clave de API de Gemini dentro del archivo `.env`:

```env
   GEMINI_API_KEY="tu_api_key_aqui"
```

### 7. Configurar el Caso de Estudio (Contexto y Agentes)

A diferencia de versiones anteriores, el proyecto ya **no** se configura editando directamente el código Python. En su lugar, debes crear/editar tres archivos de texto plano en las rutas indicadas. Si alguno no existe todavía en tu copia del repositorio, créalo manualmente en esa ruta exacta.

| Archivo | Ruta | Qué contiene |
|---|---|---|
| `contexto.txt` | `src/vdi/contexto.txt` | El caso de estudio completo (texto libre, sin formato especial) |
| `agents.yaml` | `src/vdi/crews/vdicrew/config/agents.yaml` | Definición de los agentes (rol, objetivo, backstory) |
| `tasks.yaml` | `src/vdi/crews/vdicrew/config/tasks.yaml` | Definición de las tareas que ejecuta cada agente |

**a) `contexto.txt` — el caso de estudio**

Pega aquí, en texto plano y sin ninguna sintaxis especial, la descripción completa de tu proyecto: objetivos, requerimientos técnicos, restricciones de costo, normativas aplicables, etc. Este archivo se inyecta completo como la variable `{contexto}` en `agents.yaml` y `tasks.yaml`.

```text
Diseño mecatrónico de un efector final (gripper) liviano (< 1.5 kg) para acople directo
a la brida ISO 9409-1-50-4-M6 del cobot Universal Robots UR5.

Objetivo: tomar láminas planas de acero AISI/SAE 1020 de 250x250x2 mm (~0.98 kg)
provenientes de una estación de corte láser y alimentarlas a una celda de doblado o soldadura.

Requerimientos principales:
- Masa total del gripper <= 1.5 kg.
- Tiempo de ciclo pick-and-place <= 4.0 s.
- Sensado de verificación de agarre seguro ("pieza sujeta") antes de mover el robot.
- Alimentación y control compatible con Tool I/O 24V DC del UR5.
- Cumplimiento de seguridad colaborativa bajo ISO/TS 15066.

Costo objetivo de fabricación: <= 1000 USD.
```

> No uses YAML aquí — es texto plano. Puedes pegar documentos largos (varias páginas, listas, tablas en texto) sin preocuparte por indentación ni caracteres especiales.

**b) `agents.yaml` — quiénes ejecutan el análisis**

```yaml
team_lead:
  role: >
    Lead System & Requirements Engineer
  goal: >
    A partir del {contexto}, levantar los requerimientos del sistema y consolidar el
    expediente técnico final.
  backstory: >
    Eres un especialista en ingeniería de sistemas responsable de traducir las
    necesidades del proyecto en requerimientos claros y de integrar los aportes
    de cada disciplina en un dossier coherente.

mecanico:
  role: >
    Senior Mechanical Engineer
  goal: >
    Diseñar el subsistema mecánico/estructural según el {contexto} y generar un BOM
    preliminar de materiales y componentes mecánicos.
  backstory: >
    Eres un ingeniero mecánico senior experto en diseño de mecanismos y estructuras.

electronico:
  role: >
    Senior Electronics & Instrumentation Engineer
  goal: >
    Diseñar la arquitectura de sensórica, actuación y potencia según el {contexto} y
    generar un BOM electrónico preliminar.
  backstory: >
    Eres un especialista en hardware electrónico, sensores y sistemas de control/potencia.

software:
  role: >
    Automation & Control Architect
  goal: >
    Definir la arquitectura conceptual de control/software necesaria para cumplir el
    {contexto}. QUEDA ESTRICTAMENTE PROHIBIDO GENERAR CÓDIGO DE PROGRAMACIÓN.
  backstory: >
    Eres un arquitecto de sistemas de control y automatización industrial.
```

> Este es un **placeholder de ejemplo**. Ajusta roles, `goal` y `backstory` según el dominio real de tu caso de estudio (por ejemplo, si tu proyecto no tiene componente eléctrico, puedes reemplazar `electronico` por otra disciplina relevante).

**c) `tasks.yaml` — qué debe producir cada agente**

```yaml
requirements_ingestion_task:
  description: >
    Analizar el {contexto} y establecer los requerimientos funcionales, restricciones
    operativas y presupuesto aplicable.
  expected_output: >
    Un informe con la matriz de requerimientos funcionales y restricciones.
  agent: team_lead
  output_file: output/01_requirements_and_system.md

mechanical_subsystem_design_task:
  description: >
    Desarrollar la propuesta del subsistema mecánico según el {contexto} y generar la
    tabla de BOM preliminar mecánico.
  expected_output: >
    Un reporte técnico del subsistema mecánico con su BOM preliminar.
  agent: mecanico
  output_file: output/02_mechanical_subsystem.md

electronic_subsystem_design_task:
  description: >
    Desarrollar la propuesta del subsistema electrónico según el {contexto} y generar
    la tabla de BOM preliminar electrónico.
  expected_output: >
    Un reporte técnico del subsistema electrónico con su BOM preliminar.
  agent: electronico
  output_file: output/03_electronic_subsystem.md

software_subsystem_design_task:
  description: >
    Definir la arquitectura conceptual de control/software según el {contexto}.
    NO INCLUIR NINGÚN BLOQUE DE CÓDIGO.
  expected_output: >
    Un documento conceptual de arquitectura de control, sin código.
  agent: software
  output_file: output/04_control_automation_architecture.md

design_board_integration_task:
  description: >
    Consolidar los aportes de todas las disciplinas en el Dossier de Diseño Conceptual
    VDI 2206 final, verificando cumplimiento presupuestal y de requerimientos según el
    {contexto}.
  expected_output: >
    El expediente final consolidado en formato Markdown.
  agent: team_lead
  output_file: output/00_vdi2206_consolidated_dossier.md
```

> Cada `agent:` en `tasks.yaml` debe coincidir exactamente con una clave definida en `agents.yaml`. Puedes agregar, quitar o renombrar agentes y tareas según la disciplina de tu proyecto — solo asegúrate de mantener `{contexto}` como variable en cada `description`/`goal` donde el agente necesite conocer el caso de estudio.

### 8. Ejecutar

En la terminal integrada de VS Code, inicia la ejecución del flujo de agentes:

```powershell
crewai run
```

*(También puedes ejecutarlo con `uv run kickoff`).*

---

## 📁 Estructura de Archivos de Configuración

```
vdi/
├── .env
├── pyproject.toml
└── src/
    └── vdi/
        ├── main.py
        ├── contexto.txt          ← Caso de estudio (texto plano)
        └── crews/
            └── vdicrew/
                ├── vdicrew.py
                └── config/
                    ├── agents.yaml   ← Definición de agentes
                    └── tasks.yaml    ← Definición de tareas
```

---

## 📁 Archivos de Salida (`/output`)

Toda la documentación generada por los agentes se guarda de forma independiente en la carpeta `output/` (excluida del control de versiones mediante `.gitignore`):

| Archivo | Contenido |
|---|---|
| `output/01_requirements_and_system.md` | Matriz de Requerimientos e Integración VDI 2206 |
| `output/02_mechanical_subsystem.md` | Concepto Mecánico/Mecanismos + **BOM Preliminar de Materiales** |
| `output/03_electronic_subsystem.md` | Hardware de Instrumentación/Control + **BOM Electrónico** |
| `output/04_control_automation_architecture.md` | Arquitectura Conceptual de Control/Automatización **sin código** |
| `output/00_vdi2206_consolidated_dossier.md` | **Expediente Final Consolidado VDI 2206** |

Los nombres de estos archivos deben coincidir con el campo `output_file` que definas en `tasks.yaml`; si agregas o renombras tareas, actualiza esta tabla en consecuencia.

---

## 📊 Visualización de Entregables Markdown en VS Code

Para leer y revisar los informes formateados dentro de VS Code:

1. Abre cualquier archivo dentro de la carpeta `output/`.
2. Presiona la combinación de teclas **`Ctrl + K`** y luego **`V`** (o haz clic en el botón de vista previa dividida en la esquina superior derecha).