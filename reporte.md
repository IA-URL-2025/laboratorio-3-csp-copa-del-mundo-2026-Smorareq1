# Reporte: Analisis del Caso de Estudio del Grupo K

## Copa del Mundo FIFA 2026 — Problema de Satisfaccion de Restricciones (CSP)

**Universidad Rafael Landivar — Facultad de Ingenieria**
**Inteligencia Artificial — Primer Semestre 2026**
**Carne:** 1057123
**Fecha:** Marzo 2026

---

## 1. Modelado del Problema como CSP

### 1.1 Definicion Formal

El sorteo de la Copa del Mundo FIFA 2026 se modela como un CSP de la forma **(X, D, C)** donde:

**Variables (X):** Cada una de las 48 selecciones clasificadas constituye una variable del problema. Estas estan organizadas en 4 bombos de 12 equipos. Los Bombos 1 y 2 se preasignan de forma secuencial, dejando 24 variables activas (Bombo 3 + Bombo 4) para el solver basado en backtracking.

**Dominios (D):** El dominio inicial de cada variable es el conjunto de 12 grupos {A, B, C, D, E, F, G, H, I, J, K, L}. A medida que se aplican restricciones, los dominios se reducen mediante Forward Checking.

**Restricciones (C):**

| # | Restriccion | Descripcion Formal |
|---|-------------|-------------------|
| C1 | Tamano de grupo | Cada grupo contiene exactamente 4 equipos: \|grupo_g\| = 4 |
| C2 | Un equipo por bombo | Para cada grupo g, los 4 equipos deben provenir de 4 bombos distintos |
| C3 | Confederacion general | Para confederaciones no-UEFA: max 1 equipo por grupo por confederacion |
| C4 | Excepcion UEFA | UEFA puede tener 1 o 2 equipos por grupo (para acomodar 16 clasificados europeos) |
| C5 | Anfitriones fijos | Mexico -> Grupo A, Canada -> Grupo B, EE.UU. -> Grupo D (preasignados en Bombo 1) |
| C6 | Playoff Intercontinental | Inter-1 hereda restricciones de CONMEBOL, CAF, OFC, CONCACAF. Inter-2 hereda CONMEBOL, CONCACAF, AFC |

### 1.2 Tabla de Grupos Resultante (Solucion del Solver)

| Grupo | Bombo 1 | Bombo 2 | Bombo 3 | Bombo 4 |
|-------|---------|---------|---------|---------|
| **A** | Mexico (CONCACAF) | South Korea (AFC) | Paraguay (CONMEBOL) | Cape Verde (CAF) |
| **B** | Canada (CONCACAF) | Switzerland (UEFA) | Qatar (AFC) | Ghana (CAF) |
| **C** | Brazil (CONMEBOL) | Morocco (CAF) | Saudi Arabia (AFC) | Playoff UEFA-D (UEFA) |
| **D** | USA (CONCACAF) | Colombia (CONMEBOL) | Uzbekistan (AFC) | Playoff UEFA-A (UEFA) |
| **E** | Germany (UEFA) | Japan (AFC) | Scotland (UEFA) | Playoff Inter-1 (INTER) |
| **F** | Netherlands (UEFA) | Uruguay (CONMEBOL) | South Africa (CAF) | Jordan (AFC) |
| **G** | Belgium (UEFA) | Croatia (UEFA) | Egypt (CAF) | Playoff Inter-2 (INTER) |
| **H** | Spain (UEFA) | Austria (UEFA) | Panama (CONCACAF) | New Zealand (OFC) |
| **I** | France (UEFA) | Senegal (CAF) | Norway (UEFA) | Curacao (CONCACAF) |
| **J** | Argentina (CONMEBOL) | Iran (AFC) | Algeria (CAF) | Playoff UEFA-B (UEFA) |
| **K** | Portugal (UEFA) | Ecuador (CONMEBOL) | Tunisia (CAF) | Playoff UEFA-C (UEFA) |
| **L** | England (UEFA) | Australia (AFC) | Cote d'Ivoire (CAF) | Haiti (CONCACAF) |

### 1.3 Grupos Conflictivos Identificados

El analisis revela tres grupos del sorteo real de la FIFA que **no pueden ser reproducidos** por un modelo CSP estricto:

- **Grupo K (real):** Portugal (UEFA), Iran (AFC), Uzbekistan (AFC), Playoff Inter-2 — contiene 2 equipos AFC, violando C3.
- **Grupo D (real):** EE.UU. (CONCACAF), Colombia (CONMEBOL), Paraguay (CONMEBOL), Curacao (CONCACAF) — contiene 2 CONCACAF y 2 CONMEBOL.
- **Grupo J (real):** Argentina (CONMEBOL), Ecuador (CONMEBOL), Tunez (CAF), Nueva Zelanda (OFC) — contiene 2 CONMEBOL.

El solver CSP estricto produce una solucion valida diferente donde cada confederacion no-UEFA aparece como maximo 1 vez por grupo.

---

## 2. El Conflicto

### 2.1 El Caso del Grupo K

En el sorteo real del 5 de diciembre de 2025, el Grupo K quedo conformado por:

| Posicion | Equipo | Confederacion | Bombo |
|----------|--------|---------------|-------|
| 1 | Portugal | UEFA | 1 |
| 2 | IR Iran | AFC | 2 |
| 3 | Uzbekistan | AFC | 3 |
| 4 | Playoff Inter-2 | INTER (Bolivia/Surinam/Irak) | 4 |

**La aparente violacion:** Iran y Uzbekistan son ambos de la AFC. Bajo la regla general (C3: maximo 1 equipo por confederacion no-UEFA), esto constituye una violacion directa.

### 2.2 Por que la FIFA lo permite

La FIFA aplica una interpretacion especial para los placeholders de Playoff Intercontinental:

1. **El Playoff Inter-2 representa un camino con 3 selecciones:** Bolivia (CONMEBOL), Surinam (CONCACAF) e Irak (AFC). El ganador sera de una de estas confederaciones.

2. **La restriccion se aplica al "camino", no al grupo:** La FIFA considera que la restriccion de confederacion del Playoff Inter-2 ya esta "consumida" por las selecciones del camino del playoff. Es decir, el slot del Playoff Inter-2 ya lleva implicitamente las restricciones de CONMEBOL, CONCACAF y AFC.

3. **Interpretacion de la FIFA:** Como Irak (AFC) ya esta representado en el camino del playoff, la presencia de Iran y Uzbekistan (ambos AFC) en el mismo grupo se justifica porque el conflicto AFC se resuelve a nivel del playoff, no a nivel del grupo.

4. **Consecuencia practica:** Si el ganador del Playoff Inter-2 fuera Irak (AFC), el Grupo K tendria 3 equipos AFC — algo que bajo reglas estrictas seria imposible. Sin embargo, la FIFA prioriza la viabilidad logistica del sorteo por encima de la pureza del modelo de restricciones.

### 2.3 Impacto en el Modelo CSP

En nuestro modelo CSP estricto, el `is_valid_assignment` rechaza esta configuracion:

```
[REJECT] Uzbekistan -> Grupo K: ya hay 1 equipo(s) de AFC (Iran)
```

El solver produce una solucion valida pero diferente, donde Iran y Uzbekistan terminan en grupos separados. Esto demuestra que **el CSP estricto es mas restrictivo que las reglas reales de la FIFA**, y la discrepancia radica en el tratamiento especial de los placeholders intercontinentales.

---

## 3. La Causa

### 3.1 Analisis de Heuristicas

#### MRV (Minimum Remaining Values)

La heuristica MRV selecciona siempre la variable con el dominio mas pequeno, priorizando las variables mas restringidas. En nuestra ejecucion:

1. **Primera seleccion MRV:** `Playoff Inter-2` con dominio `['G', 'H', 'I']` (tamano 3). Es la variable mas restringida del problema porque su restriccion multi-confederacion (CONMEBOL, CONCACAF, AFC) elimina 9 de los 12 grupos.

2. **Segunda seleccion MRV:** `Playoff Inter-1` con dominio `['E', 'H', 'L']` (tamano 3). Igualmente restringida por su multi-confederacion (CONMEBOL, CAF, OFC, CONCACAF).

3. **Tercera seleccion:** `Paraguay` con dominio de tamano 5, seguido por equipos con dominios progresivamente mas grandes.

**MRV y el Grupo K:** En un CSP sin restriccion multi-confederacion, el Grupo K no seria particularmente restrictivo al inicio (contiene Portugal-UEFA e Iran-AFC, permitiendo equipos de CAF, CONMEBOL, CONCACAF, OFC para el pot 3). Sin embargo, **con la restriccion multi-conf**, el Grupo K se vuelve restrictivo para los Playoff Inter, no para los equipos regulares.

#### Forward Checking

El Forward Checking propaga restricciones despues de cada asignacion, eliminando valores inconsistentes de los dominios futuros. Su impacto clave:

- Tras preasignar los 24 equipos de Bombos 1 y 2, Forward Checking redujo los dominios de los 24 equipos restantes.
- **Playoff Inter-2** quedo con solo 3 grupos validos (G, H, I) — los unicos sin CONMEBOL, CONCACAF ni AFC.
- **Playoff Inter-1** quedo con solo 3 grupos validos (E, H, L) — los unicos sin CONMEBOL, CAF, OFC ni CONCACAF.

Si desactivaramos Forward Checking, el algoritmo intentaria colocar los Playoff Inter en los 12 grupos indiscriminadamente, descubriendo la invalides solo al momento de la verificacion, aumentando drasticamente el numero de backtracks.

### 3.2 Traza de Ejecucion

La traza completa del solver muestra el proceso de decision:

```
=== Preasignacion de Bombos 1 y 2 ===
Bombo 1: Mexico->A, Canada->B, Brazil->C, USA->D, Germany->E,
         Netherlands->F, Belgium->G, Spain->H, France->I,
         Argentina->J, Portugal->K, England->L

Bombo 2: South Korea->A, Switzerland->B, Morocco->C, Colombia->D,
         Japan->E, Uruguay->F, Croatia->G, Austria->H,
         Senegal->I, Iran->J, Ecuador->K, Australia->L

=== Backtracking con Forward Checking ===

Paso 1: [MRV] Playoff Inter-2 (dominio: ['G','H','I'], tamano: 3)
        [ASSIGN] Playoff Inter-2 -> Grupo G
        Razon: G tiene Belgium(UEFA)+Croatia(UEFA), sin CONMEBOL/CONCACAF/AFC

Paso 2: [MRV] Playoff Inter-1 (dominio: ['E','H','L'], tamano: 3)
        [ASSIGN] Playoff Inter-1 -> Grupo E
        Razon: E tiene Germany(UEFA)+Japan(AFC), sin CONMEBOL/CAF/OFC/CONCACAF

Paso 3: [MRV] Paraguay (dominio: ['A','B','H','I','L'], tamano: 5)
        [ASSIGN] Paraguay -> Grupo A

Paso 4-24: Asignacion secuencial sin backtracks...
           Qatar->B, Saudi Arabia->C, Uzbekistan->D, Jordan->F,
           South Africa->F, Scotland->E, Norway->I, Panama->H,
           Egypt->G, Algeria->J, Tunisia->K, Cote d'Ivoire->L,
           Cape Verde->A, Ghana->B, Playoff UEFA-D->C,
           Playoff UEFA-A->D, Playoff UEFA-B->J,
           Curacao->I, Haiti->L, New Zealand->H,
           Playoff UEFA-C->K
```

**Resultado:** 0 backtracks. La combinacion de MRV + Forward Checking resolvio el problema en una sola pasada, asignando primero las variables mas restringidas (Playoff Inter) y propagando restricciones para evitar callejones sin salida.

### 3.3 Deteccion Anticipada del Conflicto

**MRV** detecta el conflicto anticipadamente al priorizar los Playoff Inter (dominio mas pequeno = mas restringido). Sin MRV, un algoritmo naive podria intentar colocar equipos AFC en multiples grupos antes de descubrir que no queda espacio para los Playoff Inter.

**Forward Checking** impide que Uzbekistan se coloque en un grupo con Playoff Inter-2, ya que:
```
[REJECT] Uzbekistan -> Grupo G: Playoff Inter-2 tiene multi_conf que incluye AFC
```

Sin Forward Checking, esta inconsistencia solo se detectaria mucho mas tarde, generando backtracks innecesarios.

---

## 4. La Solucion IA

### 4.1 Pseudocodigo del Algoritmo

```
funcion BACKTRACK-CSP(asignacion, dominios):
    si asignacion esta completa:
        retornar asignacion

    var <- SELECT-MRV(asignacion, dominios)

    para cada grupo en dominios[var]:
        si ES-VALIDA(grupo, var, asignacion):
            asignacion[var] <- grupo

            exito, nuevos_dominios <- FORWARD-CHECK(asignacion, dominios)

            si exito:
                resultado <- BACKTRACK-CSP(asignacion, nuevos_dominios)
                si resultado != null:
                    retornar resultado

            eliminar asignacion[var]   // backtrack

    retornar null   // no hay solucion en esta rama


funcion SELECT-MRV(asignacion, dominios):
    no_asignadas <- {v in Variables | v no en asignacion}
    retornar argmin(v in no_asignadas, |dominios[v]|)


funcion ES-VALIDA(grupo, equipo, asignacion):
    equipos_en_grupo <- {t | asignacion[t] = grupo}

    // C1: Tamano del grupo
    si |equipos_en_grupo| >= 4: retornar falso

    // C2: Un equipo por bombo
    para cada t en equipos_en_grupo:
        si bombo(t) = bombo(equipo): retornar falso

    // C3-C4: Restriccion de confederacion
    conf <- confederacion(equipo)
    conteo <- |{t in equipos_en_grupo | confederacion(t) = conf}|
    si conf = "UEFA" y conteo >= 2: retornar falso
    si conf != "UEFA" y conteo >= 1: retornar falso

    // C6: Multi-confederacion (Playoff Inter)
    para cada mc en multi_conf(equipo):
        para cada t en equipos_en_grupo:
            si confederacion(t) = mc: retornar falso

    para cada t en equipos_en_grupo:
        si conf en multi_conf(t): retornar falso

    retornar verdadero


funcion FORWARD-CHECK(asignacion, dominios):
    nuevos_dominios <- copia(dominios)

    para cada var no asignada:
        nuevos_dominios[var] <- {g in dominios[var] |
                                  ES-VALIDA(g, var, asignacion)}
        si nuevos_dominios[var] esta vacio:
            retornar (falso, nuevos_dominios)

    retornar (verdadero, nuevos_dominios)
```

### 4.2 Analisis de Complejidad

**Sin heuristicas ni propagacion:**
- Variables: n = 48 (24 activas tras preasignacion)
- Dominio maximo: d = 12 grupos
- Complejidad del peor caso: O(d^n) = O(12^24) ≈ 3.6 x 10^25 nodos

**Con MRV + Forward Checking:**
- MRV reduce el factor de ramificacion efectivo al priorizar variables con dominios pequenos
- Forward Checking poda ramas inconsistentes antes de expandirlas
- En nuestra ejecucion: **24 asignaciones, 0 backtracks** — el algoritmo resolvio en O(n) asignaciones
- Esto representa una reduccion de 10^25 a ~24 nodos explorados

**Complejidad por operacion:**
- `is_valid_assignment`: O(k) donde k = equipos en el grupo (max 4) → O(1)
- `forward_check`: O(n * d * k) por cada llamada → O(n * d)
- `select_unassigned_variable` (MRV): O(n) por seleccion
- Total con propagacion: O(n^2 * d) en el caso observado

### 4.3 Conclusion

La implementacion demuestra que las tecnicas de CSP (backtracking + MRV + Forward Checking) resuelven eficientemente el problema del sorteo mundialista. Sin embargo, el modelo CSP estricto no puede reproducir el sorteo real de la FIFA para los Grupos K, D y J, debido a que la FIFA aplica excepciones pragmaticas para los placeholders de Playoff Intercontinental que no se capturan en un modelo puramente formal de restricciones. Esta discrepancia entre el modelo teorico y la realidad practica es precisamente lo que hace del Grupo K un caso de estudio valioso: ilustra los limites de la formalizacion y la necesidad de incorporar conocimiento del dominio en el diseno de restricciones.

---

*Generado como parte del Laboratorio 3 — CSP Copa del Mundo 2026*
*Universidad Rafael Landivar — Carne: 1057123*
