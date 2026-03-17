# Universidad Rafael Landívar
## Facultad de Ingeniería — Inteligencia Artificial
### Primer Semestre 2026

---

# LABORATORIO 3
## El Sorteo de la Copa del Mundo 2026
### Problemas de Satisfacción de Restricciones (CSP)

⚽ FIFA World Cup 2026 | 48 Selecciones | 12 Grupos

| Campo | Detalle |
|-------|---------|
| 🏫 Universidad | Rafael Landívar |
| 📚 Curso | Inteligencia Artificial — Facultad de Ingeniería |
| 📅 Entrega | 13/03/2026 |

---

## Introducción

A diferencia de los problemas de búsqueda convencionales, en los Problemas de Satisfacción de Restricciones (CSPs) no buscamos una secuencia de acciones, sino una asignación de valores a variables que cumpla simultáneamente todas las restricciones del problema. Este laboratorio modela el sorteo real de la FIFA para el Mundial 2026 —el más grande de la historia, con 48 selecciones en 12 grupos de cuatro equipos— como un CSP formal, donde una asignación naive por "orden alfabético" puede producir violaciones catastróficas si no se aplican técnicas de propagación de restricciones.

El sorteo real se realizó el **5 de diciembre de 2025** en el **Kennedy Center de Washington D.C.** Las restricciones de confederación impuestas por la FIFA son exactamente las que modelaremos:

| Regla | Descripción |
|-------|-------------|
| **General** | Ningún grupo puede tener más de 1 equipo de la misma confederación (CONMEBOL, CONCACAF, AFC, CAF, OFC). |
| **Excepción UEFA** | UEFA tiene 16 clasificados. Cada grupo DEBE tener mínimo 1 y máximo 2 equipos europeos. |
| **Playoffs** | Para los 2 placeholders del Playoff Intercontinental (Bombo 4), la restricción de confederación se aplica a las 3 selecciones de cada camino del playoff. |
| **Anfitriones** | México (Grupo A), Canadá (Grupo B) y EE. UU. (Grupo D) están pre-asignados en Bombo 1. |

---

## Contexto: El Sorteo Real FIFA World Cup 2026

### Estructura del Torneo

El Mundial 2026 es la primera edición con **48 selecciones**, estructurada en **4 bombos de 12 equipos** cada uno. Los 12 grupos (A–L) se forman con 1 equipo por bombo. Los 24 clasificados de primera y segunda plaza, más los 8 mejores terceros, avanzan a un nuevo Ronda de 32.

### Distribución de Bombos (Sorteo del 5 dic 2025)

| Bombo | Equipos |
|-------|---------|
| **Bombo 1** | México, Canadá, EE. UU., España, Argentina, Francia, Inglaterra, Brasil, Portugal, Países Bajos, Bélgica, Alemania |
| **Bombo 2** | Croacia, Marruecos, Colombia, Uruguay, Suiza, Japón, Senegal, IR Irán, Corea del Sur, Ecuador, Austria, Australia |
| **Bombo 3** | Noruega, Panamá, Egipto, Argelia, Escocia, Paraguay, Túnez, Côte d'Ivoire, Uzbekistán, Qatar, Arabia Saudita, Sudáfrica |
| **Bombo 4** | Jordania, Cabo Verde, Ghana, Curazao, Haití, Nueva Zelanda, Playoff UEFA A/B/C/D, Playoff Intercontinental 1 y 2 |

### Grupos Resultantes del Sorteo Real

A continuación se muestran los 12 grupos tal como quedaron determinados el 5 de diciembre de 2025. Los equipos marcados con `*` son placeholders que se conocerán en marzo 2026 tras los playoffs.

| Grupo | Bombo 1 (Cabeza) | Bombo 2 | Bombo 3 | Bombo 4 |
|-------|-----------------|---------|---------|---------|
| **A** | México (CONCACAF) | Corea del Sur (AFC) | Sudáfrica (CAF) | Playoff UEFA-D |
| **B** | Canadá (CONCACAF) | Suiza (UEFA) | Qatar (AFC) | Playoff UEFA-A |
| **C** | Brasil (CONMEBOL) | Marruecos (CAF) | Escocia (UEFA) | Playoff UEFA-B |
| **D** | EE. UU. (CONCACAF) | Colombia (CONMEBOL) | Paraguay (CONMEBOL) | Curazao (CONCACAF) |
| **E** | Alemania (UEFA) | Japón (AFC) | Panamá (CONCACAF) | Cabo Verde (CAF) |
| **F** | Países Bajos (UEFA) | Uruguay (CONMEBOL) | Egipto (CAF) | Haití (CONCACAF) |
| **G** | Bélgica (UEFA) | Croacia (UEFA) | Argelia (CAF) | Jordania (AFC) |
| **H** | España (UEFA) | Austria (UEFA) | Arabia Saudita (AFC) | Ghana (CAF) |
| **I** | Francia (UEFA) | Senegal (CAF) | Noruega (UEFA) | Playoff Inter-1 |
| **J** | Argentina (CONMEBOL) | Ecuador (CONMEBOL) | Túnez (CAF) | Nueva Zelanda (OFC) |
| **K** | Portugal (UEFA) | IR Irán (AFC) | Uzbekistán (AFC) | Playoff Inter-2 |
| **L** | Inglaterra (UEFA) | Croacia (UEFA) | Côte d'Ivoire (CAF) | Playoff UEFA-C |

> ⚠️ **Nota sobre el Grupo K:** Irán y Uzbekistán son ambos de AFC. Esto es posible porque un placeholder de Playoff Intercontinental ocupa el 4.° lugar —las restricciones se aplican a las tres selecciones del camino del playoff, no a la AFC directamente. Esta excepción es el núcleo del caso de estudio de este laboratorio.

---

## Tarea

### Parte 1 — Implementación del WorldCupCSP

Debes completar la clase `WorldCupCSP` en el repositorio proporcionado. Tu código debe ser capaz de asignar selecciones del Bombo 3 y Bombo 4 a los espacios vacíos de los Grupos A al L, cumpliendo las restricciones reales de la FIFA.

#### Variables (X)

Los espacios vacíos en los Grupos A al L que corresponden a los Bombos 3 y 4. Dado que Bombos 1 y 2 ya están asignados tras el sorteo real, las variables son las **24 posiciones restantes** (12 del Bombo 3 + 12 del Bombo 4).

#### Dominios (D)

- **Bombo 3:** Noruega (UEFA), Panamá (CONCACAF), Egipto (CAF), Argelia (CAF), Escocia (UEFA), Paraguay (CONMEBOL), Túnez (CAF), Côte d'Ivoire (CAF), Uzbekistán (AFC), Qatar (AFC), Arabia Saudita (AFC), Sudáfrica (CAF)
- **Bombo 4:** Jordania (AFC), Cabo Verde (CAF), Ghana (CAF), Curazao (CONCACAF), Haití (CONCACAF), Nueva Zelanda (OFC), Playoff UEFA-A/B/C/D, Playoff Inter-1, Playoff Inter-2

#### Restricciones (C)

1. **Restricción Geográfica General:** Máximo 1 equipo por confederación por grupo, excepto UEFA que permite exactamente 1 ó 2.
2. **Restricción de Host Pre-asignado:** México→Grupo A, Canadá→Grupo B, EE. UU.→Grupo D (Bombo 1, ya fijado).
3. **Restricción Playoff Intercontinental:** El ganador del Playoff Inter-1 (camino: Bolivia/DR Congo/Nueva Caledonia-Jamaica) hereda las restricciones de confederación de las 3 selecciones del camino. El ganador del Playoff Inter-2 (camino: Bolivia/Surinam/Irak) hereda las confederaciones CONMEBOL, CONCACAF y AFC simultáneamente.
4. **Restricción de Balance UEFA:** 4 de los 12 grupos deben tener exactamente 2 equipos UEFA (para acomodar los 16 clasificados europeos, 4 de los cuales vienen de Playoffs en Bombo 4).
5. **Restricción Top-4 Anti-colisión (nuevo en 2026):** España y Argentina deben quedar en caminos opuestos del cuadro de eliminación directa; igual para Francia e Inglaterra. Esto ya está resuelto por el sorteo real, pero tu CSP debe validarlo.

---

### Parte 2 — Cuestionario de Comprensión

Una vez que tu código funcione, deberás ingresar al portal y responder un cuestionario de **10 preguntas**. Para responder correctamente, deberás analizar tu propia ejecución y los resultados de tu algoritmo.

Ejemplos de preguntas que encontrarás:

- En tu traza de Backtracking, ¿qué sucede inmediatamente después de intentar colocar a Uzbekistán en el Grupo I? *(Pista: Grupo I ya tiene Francia y Noruega —ambas UEFA—, ¿qué restricción viola Uzbekistán allí?)*
- ¿Cuántas veces tuvo que retroceder tu algoritmo antes de encontrar la solución correcta para el Grupo K? Explica la restricción dual AFC que complica este grupo.
- Si desactivas la Propagación de Restricciones (Forward Checking), ¿el algoritmo logra terminar el Bombo 4 o falla por inconsistencia? ¿En qué grupo falla primero?
- Explica, basado en la estructura de tu código, qué variable se seleccionó primero siguiendo la heurística MRV (Minimum Remaining Values). ¿Es el Grupo D o el Grupo K el más restrictivo al iniciar?
- ¿Qué componente de tu código impidió que Noruega fuera enviada al Grupo K antes que Uzbekistán? *(Pista: Grupo K ya tiene Portugal-UEFA e Irán-AFC.)*
- Analiza el caso especial del Grupo D (EE. UU., Colombia, Paraguay, Curazao): ¿viola la restricción general? ¿Por qué la FIFA lo permite?

---

### Parte 3 — Reporte: Análisis del Caso de Estudio del Grupo K

El producto final es un **reporte en PDF** que demuestre tu capacidad para traducir el sorteo real de la FIFA a un marco formal de CSP. El **Grupo K** (Portugal, Irán, Uzbekistán, Playoff Inter-2) es el caso de estudio central por su complejidad de restricciones.

#### Estructura requerida del reporte:

| Sección | Contenido esperado |
|---------|-------------------|
| **1. Modelado del Problema como CSP** | Definición formal de variables, dominios y restricciones aplicadas al sorteo real. Incluye la tabla de grupos resultante y la identificación de qué grupos generan conflictos (K, D, I). |
| **2. El Conflicto** | Descripción del caso específico: ¿por qué el Grupo K contiene 2 equipos de AFC (Irán + Uzbekistán) sin violar las reglas de la FIFA? ¿Cómo interactúa esto con el Playoff Inter-2? |
| **3. La Causa** | Análisis técnico: ¿qué heurística (MRV, LCV, Forward Checking) habría detectado el conflicto anticipadamente? Muestra trazas de ejecución de tu algoritmo. |
| **4. La Solución IA** | Explicación de cómo tu implementación de CSP resuelve el problema. Incluye pseudocódigo del backtracking con propagación y análisis de complejidad. |

---

## Código Base

El repositorio proporcionado contiene la estructura base de la clase `WorldCupCSP`. Debes completar los métodos marcados con `# TODO`.

```python
# world_cup_csp.py — Estructura base
class WorldCupCSP:
    def __init__(self):
        self.groups = {f'Group_{g}': [] for g in 'ABCDEFGHIJKL'}
        self.confederations = {...}  # Diccionario selección→confederación
        # Pre-asignaciones reales del sorteo:
        self._preassign_pots_1_and_2()  # Bombos 1 y 2 ya conocidos

    def is_valid_assignment(self, group, team):
        # TODO: Implementar restricción geográfica + regla UEFA
        pass

    def forward_check(self, group, team):
        # TODO: Propagación de restricciones hacia grupos no asignados
        pass

    def select_unassigned_variable(self, assignment):
        # TODO: Heurística MRV (Minimum Remaining Values)
        pass

    def backtrack(self, assignment={}):
        # TODO: Backtracking con Forward Checking
        pass
```

#### Instrucciones de ejecución y pruebas:

- Clona el repositorio proporcionado en el portal.
- Ejecuta las pruebas unitarias localmente: `pytest test_world_cup_csp.py -v`
- Si las 10 pruebas pasan, tu implementación es funcionalmente correcta y puedes proceder al cuestionario.
- Verifica que tu solución reproduzca la asignación real del Grupo K: **Portugal, Irán, Uzbekistán, Playoff Inter-2**.

---

## Entregables y Criterios de Evaluación

| Entregable | Descripción | Ponderación |
|------------|-------------|-------------|
| **1. Código en GitHub** | Implementación de WorldCupCSP verificada por commits y 10/10 pruebas pytest pasadas. | 25% |
| **2. Reporte en PDF** | Análisis formal del CSP con las 4 secciones requeridas (modelado, conflicto, causa, solución). Mínimo 4 páginas. | 35% |
| **3. Cuestionario Online** | 10 preguntas sobre la traza de ejecución de tu propio algoritmo. Requiere comprensión profunda del backtracking. | 40% |

> ⏰ **FECHA LÍMITE DE ENTREGA:** Domingo 02 de marzo de 2026, 23:59 (GMT-6)
> Entregas tardías tendrán una penalización del **20% por día**.

---

## Referencia Rápida: Confederaciones por Grupo

La siguiente tabla resume las confederaciones presentes en cada grupo tras el sorteo real. Tu implementación de CSP debe ser capaz de derivar esta asignación de forma autónoma.

| Grp | UEFA (máx. 2) | Non-UEFA (1 c/u) | Nota |
|-----|---------------|-----------------|------|
| **A** | Playoff UEFA-D (1) | CONCACAF, AFC, CAF | Anfitrión México |
| **B** | Suiza + Playoff UEFA-A (2) | CONCACAF, AFC | Anfitrión Canadá |
| **C** | Escocia + Playoff UEFA-B (2) | CONMEBOL, CAF | |
| **D** | — (0 UEFA) | 2×CONCACAF, 2×CONMEBOL | ⚠️ Excepción CONCACAF+CONMEBOL |
| **E** | Alemania (1) | AFC, CONCACAF, CAF | |
| **F** | Países Bajos (1) | CONMEBOL, CAF, CONCACAF | |
| **G** | Bélgica + Croacia (2) | CAF, AFC | |
| **H** | España + Austria (2) | AFC, CAF | |
| **I** | Francia + Noruega (2) | CAF + Playoff Inter-1 | Playoff hereda 3 confederaciones |
| **J** | — (0 UEFA) | 2×CONMEBOL, CAF, OFC | |
| **K** | Portugal (1) | 2×AFC + Playoff Inter-2 | ⚠️ Caso de estudio: 2 AFC |
| **L** | Inglaterra + Playoff UEFA-C (2) | UEFA, CAF, ?? | Grupos aún con placeholders |

El **Grupo K** es el caso de estudio central porque contiene 2 equipos de AFC (Irán del Bombo 2 y Uzbekistán del Bombo 3), aparentemente violando la regla general. La razón por la que esto es válido: el Playoff Inter-2 (Bolivia/Surinam/Irak) actúa como placeholder multi-confederación, y la restricción AFC ya se "consume" al aplicarse al camino completo del playoff. Tu algoritmo debe modelar esta excepción correctamente.

---

## Recursos y Referencias

- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4.ª ed.). Capítulo 6: Constraint Satisfaction Problems.
- FIFA (2025). *Procedures for the Final Draw — FIFA World Cup 2026*. Washington D.C.: Kennedy Center, 5 diciembre 2025.
- FIFA (2025). *Reglamento del Torneo FIFA World Cup 2026: Distribución de equipos y restricciones de la confederación.*
- URL — Departamento de Ingeniería (2026). Repositorio base del Laboratorio 3: [enlace en el portal de la asignatura].
- Documentación de pytest: https://docs.pytest.org — Para ejecutar las pruebas unitarias del laboratorio.

---

*Universidad Rafael Landívar · Facultad de Ingeniería*
*Inteligencia Artificial — Primer Semestre 2026*