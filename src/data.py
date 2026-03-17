# Datos reales del sorteo de la Copa Mundial FIFA 2026
# 48 selecciones | 12 Grupos (A-L) | 4 Bombos
# Sorteo realizado el 5 de diciembre de 2025, Kennedy Center, Washington D.C.
# Confederaciones: UEFA, CONMEBOL, CONCACAF, AFC, CAF, OFC, INTER (playoffs intercontinentales)

TEAMS = {
    # BOMBO 1 (Cabezas de serie) - Ordenados segun asignacion real del sorteo
    "Mexico": {"conf": "CONCACAF", "pot": 1},
    "Canada": {"conf": "CONCACAF", "pot": 1},
    "Brazil": {"conf": "CONMEBOL", "pot": 1},
    "USA": {"conf": "CONCACAF", "pot": 1},
    "Germany": {"conf": "UEFA", "pot": 1},
    "Netherlands": {"conf": "UEFA", "pot": 1},
    "Belgium": {"conf": "UEFA", "pot": 1},
    "Spain": {"conf": "UEFA", "pot": 1},
    "France": {"conf": "UEFA", "pot": 1},
    "Argentina": {"conf": "CONMEBOL", "pot": 1},
    "Portugal": {"conf": "UEFA", "pot": 1},
    "England": {"conf": "UEFA", "pot": 1},

    # BOMBO 2
    "South Korea": {"conf": "AFC", "pot": 2},
    "Switzerland": {"conf": "UEFA", "pot": 2},
    "Morocco": {"conf": "CAF", "pot": 2},
    "Colombia": {"conf": "CONMEBOL", "pot": 2},
    "Japan": {"conf": "AFC", "pot": 2},
    "Uruguay": {"conf": "CONMEBOL", "pot": 2},
    "Croatia": {"conf": "UEFA", "pot": 2},
    "Austria": {"conf": "UEFA", "pot": 2},
    "Senegal": {"conf": "CAF", "pot": 2},
    "Iran": {"conf": "AFC", "pot": 2},
    "Ecuador": {"conf": "CONMEBOL", "pot": 2},
    "Australia": {"conf": "AFC", "pot": 2},

    # BOMBO 3
    "South Africa": {"conf": "CAF", "pot": 3},
    "Qatar": {"conf": "AFC", "pot": 3},
    "Scotland": {"conf": "UEFA", "pot": 3},
    "Paraguay": {"conf": "CONMEBOL", "pot": 3},
    "Panama": {"conf": "CONCACAF", "pot": 3},
    "Egypt": {"conf": "CAF", "pot": 3},
    "Algeria": {"conf": "CAF", "pot": 3},
    "Saudi Arabia": {"conf": "AFC", "pot": 3},
    "Norway": {"conf": "UEFA", "pot": 3},
    "Tunisia": {"conf": "CAF", "pot": 3},
    "Uzbekistan": {"conf": "AFC", "pot": 3},
    "Cote d'Ivoire": {"conf": "CAF", "pot": 3},

    # BOMBO 4
    "Playoff UEFA-D": {"conf": "UEFA", "pot": 4},
    "Playoff UEFA-A": {"conf": "UEFA", "pot": 4},
    "Playoff UEFA-B": {"conf": "UEFA", "pot": 4},
    "Curacao": {"conf": "CONCACAF", "pot": 4},
    "Cape Verde": {"conf": "CAF", "pot": 4},
    "Haiti": {"conf": "CONCACAF", "pot": 4},
    "Jordan": {"conf": "AFC", "pot": 4},
    "Ghana": {"conf": "CAF", "pot": 4},
    "Playoff Inter-1": {"conf": "INTER", "pot": 4,
                        "multi_conf": ["CONMEBOL", "CAF", "OFC", "CONCACAF"]},
    "New Zealand": {"conf": "OFC", "pot": 4},
    "Playoff Inter-2": {"conf": "INTER", "pot": 4,
                        "multi_conf": ["CONMEBOL", "CONCACAF", "AFC"]},
    "Playoff UEFA-C": {"conf": "UEFA", "pot": 4},
}

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
