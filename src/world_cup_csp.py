import copy

class WorldCupCSP:
    def __init__(self, teams, groups, debug=False):
        """
        Inicializa el problema CSP para el sorteo del Mundial.
        :param teams: Diccionario con los equipos, sus confederaciones y bombos.
        :param groups: Lista con los nombres de los grupos (A-L).
        :param debug: Booleano para activar trazas de depuración.
        """
        self.teams = teams
        self.groups = groups
        self.debug = debug

        # Las variables son los equipos.
        self.variables = list(teams.keys())

        # El dominio de cada variable inicialmente son todos los grupos.
        self.domains = {team: list(groups) for team in self.variables}

    def get_team_confederation(self, team):
        return self.teams[team]["conf"]

    def get_team_pot(self, team):
        return self.teams[team]["pot"]

    def is_valid_assignment(self, group, team, assignment):
        """
        Verifica si asignar un equipo a un grupo viola
        las restricciones de confederación o tamaño del grupo.
        """
        # Obtener equipos ya asignados a este grupo
        teams_in_group = [t for t, g in assignment.items() if g == group]

        # Restricción de tamaño del grupo (máximo 4)
        if len(teams_in_group) >= 4:
            if self.debug:
                print(f"  [REJECT] {team} -> Grupo {group}: grupo lleno ({len(teams_in_group)} equipos)")
            return False

        # Restricción de bombo: no puede haber dos equipos del mismo bombo en un grupo
        team_pot = self.get_team_pot(team)
        for t in teams_in_group:
            if self.get_team_pot(t) == team_pot:
                if self.debug:
                    print(f"  [REJECT] {team} -> Grupo {group}: mismo bombo {team_pot} que {t}")
                return False

        # Restricción de confederaciones (máximo 1 por confederación, excepto UEFA máximo 2)
        team_conf = self.get_team_confederation(team)
        conf_count = sum(1 for t in teams_in_group if self.get_team_confederation(t) == team_conf)

        if team_conf == "UEFA":
            if conf_count >= 2:
                if self.debug:
                    print(f"  [REJECT] {team} -> Grupo {group}: ya hay {conf_count} equipos UEFA")
                return False
        else:
            if conf_count >= 1:
                if self.debug:
                    print(f"  [REJECT] {team} -> Grupo {group}: ya hay {conf_count} equipo(s) de {team_conf}")
                return False

        # Restricción Playoff Intercontinental (multi-confederación)
        # Si el equipo nuevo tiene multi_conf, verificar que ningún equipo
        # del grupo pertenezca a esas confederaciones
        team_multi = self.teams[team].get("multi_conf", [])
        for mc in team_multi:
            for t in teams_in_group:
                t_conf = self.get_team_confederation(t)
                if t_conf == mc:
                    if self.debug:
                        print(f"  [REJECT] {team} -> Grupo {group}: multi_conf {mc} conflicta con {t} ({t_conf})")
                    return False

        # Si un equipo existente tiene multi_conf, verificar que la confederación
        # del nuevo equipo no esté en su lista
        for t in teams_in_group:
            t_multi = self.teams[t].get("multi_conf", [])
            if team_conf in t_multi:
                if self.debug:
                    print(f"  [REJECT] {team} -> Grupo {group}: {t} tiene multi_conf que incluye {team_conf}")
                return False

        return True

    def forward_check(self, assignment, domains):
        """
        Propagación de restricciones.
        Debe eliminar valores inconsistentes en dominios futuros.
        Retorna True si la propagación es exitosa, False si algún dominio queda vacío.
        """
        new_domains = copy.deepcopy(domains)

        for team in self.variables:
            if team in assignment:
                continue

            # Filtrar: conservar solo grupos donde la asignación sería válida
            valid_groups = [g for g in new_domains[team]
                           if self.is_valid_assignment(g, team, assignment)]
            new_domains[team] = valid_groups

            if len(valid_groups) == 0:
                if self.debug:
                    print(f"  [FC FAIL] {team}: dominio vacío tras forward checking")
                return False, new_domains

        return True, new_domains

    def select_unassigned_variable(self, assignment, domains):
        """
        Heurística MRV (Minimum Remaining Values).
        Selecciona la variable no asignada con el dominio más pequeño.
        """
        unassigned_vars = [v for v in self.variables if v not in assignment]
        if not unassigned_vars:
            return None

        selected = min(unassigned_vars, key=lambda v: len(domains[v]))

        if self.debug:
            print(f"  [MRV] Seleccionado: {selected} (dominio: {domains[selected]}, tamaño: {len(domains[selected])})")

        return selected

    def backtrack(self, assignment, domains=None):
        """
        Backtracking search para resolver el CSP.
        """
        if domains is None:
            domains = copy.deepcopy(self.domains)

        # Condición de parada: Si todas las variables están asignadas, retornamos la asignación.
        if len(assignment) == len(self.variables):
            return assignment

        # 1. Seleccionar variable con MRV
        var = self.select_unassigned_variable(assignment, domains)
        if var is None:
            return None

        if self.debug:
            print(f"\n[BT] Intentando asignar: {var} ({self.get_team_confederation(var)}, Bombo {self.get_team_pot(var)})")

        # 2. Iterar sobre los valores (grupos) posibles en el dominio
        for group in domains[var]:
            # 3. Verificar si la asignación es válida
            if self.is_valid_assignment(group, var, assignment):
                if self.debug:
                    print(f"  [ASSIGN] {var} -> Grupo {group}")

                # Hacer la asignación
                assignment[var] = group

                # Aplicar forward checking
                success, new_domains = self.forward_check(assignment, domains)

                if success:
                    # 4. Llamada recursiva
                    result = self.backtrack(assignment, new_domains)
                    if result is not None:
                        return result

                # 5. Deshacer la asignación si falla (backtrack)
                if self.debug:
                    print(f"  [BACKTRACK] Deshaciendo {var} -> Grupo {group}")
                del assignment[var]

        return None
