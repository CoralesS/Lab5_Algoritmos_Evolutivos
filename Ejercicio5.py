import pandas as pd
import random

# Leer disponibilidad
df = pd.read_csv('tesistas.csv', delimiter=';')
tesistas = df['TesistaID'].tolist()
franjas = df.columns[1:].tolist()  # F1, F2, ..., F6
num_salas = 6

# Convertir disponibilidad a dict {TesistaID: [1/0,...]}
disp = {row['TesistaID']: row[1:].tolist() for _, row in df.iterrows()}

# Solución: dict {tesista: (sala, franja_index)}
# Heurística inicial: asignar secuencial, buscando primer sala/franja libre y disponible

def asignacion_inicial():
    asignacion = {}
    # Estructura para saber uso por sala y franja
    uso = [[None]*len(franjas) for _ in range(num_salas)]  # None o tesista
    
    for t in tesistas:
        franjas_disp = disp[t]
        asignado = False
        for f_idx, disponible in enumerate(franjas_disp):
            if disponible == 1:
                for s in range(num_salas):
                    # Si sala libre en franja
                    if uso[s][f_idx] is None:
                        asignacion[t] = (s, f_idx)
                        uso[s][f_idx] = t
                        asignado = True
                        break
            if asignado:
                break
        # Si no asignado, poner (-1, -1)
        if not asignado:
            asignacion[t] = (-1, -1)
    return asignacion, uso

# Función para calcular métricas:
# Huecos: franjas libres entre franjas ocupadas en una sala
# Solapamientos: cantidad de tesistas asignados a la misma sala y franja (debería ser 0)
def calcular_metricas(asignacion):
    # Construir matriz sala x franjas con lista de tesistas
    uso = [[[] for _ in franjas] for _ in range(num_salas)]
    for t, (s, f_idx) in asignacion.items():
        if s >= 0 and f_idx >= 0:
            uso[s][f_idx].append(t)
    
    solapamientos = 0
    huecos = 0
    # Revisar solapamientos
    for s in range(num_salas):
        franjas_ocupadas = []
        for f_idx in range(len(franjas)):
            if len(uso[s][f_idx]) > 1:
                solapamientos += len(uso[s][f_idx]) - 1
            if len(uso[s][f_idx]) > 0:
                franjas_ocupadas.append(f_idx)
        # Calcular huecos: franjas vacías entre primer y último ocupado
        if franjas_ocupadas:
            primer = min(franjas_ocupadas)
            ultimo = max(franjas_ocupadas)
            for f_idx in range(primer, ultimo+1):
                if len(uso[s][f_idx]) == 0:
                    huecos += 1
            # Verificar horas continuas no exceden 4
            # Contar bloques continuos >4
            max_continuas = 0
            count = 0
            for f_idx in range(primer, ultimo+1):
                if len(uso[s][f_idx]) > 0:
                    count += 1
                    max_continuas = max(max_continuas, count)
                else:
                    count = 0
            if max_continuas > 4:
                # Penalizamos con huecos extra para forzar solución
                huecos += (max_continuas - 4) * 10
    return solapamientos, huecos

# Vecindad: mover 1 tesista a otra sala/franja disponible y libre
def obtener_vecinos(asignacion):
    vecinos = []
    for t in tesistas:
        s_actual, f_actual = asignacion[t]
        for s in range(num_salas):
            for f_idx in range(len(franjas)):
                if disp[t][f_idx] == 1 and (s != s_actual or f_idx != f_actual):
                    # Verificar que no haya solapamiento en vecino
                    ocupado = False
                    for ot, (os, of) in asignacion.items():
                        if ot != t and os == s and of == f_idx:
                            ocupado = True
                            break
                    if not ocupado:
                        vecino = asignacion.copy()
                        vecino[t] = (s, f_idx)
                        vecinos.append(vecino)
    return vecinos

def hill_climbing(iteraciones=500):
    actual, _ = asignacion_inicial()
    mejor = actual
    solap, huecos = calcular_metricas(mejor)
    mejor_costo = solap*100 + huecos  # Peso mayor a solapamiento
    
    for _ in range(iteraciones):
        vecinos = obtener_vecinos(actual)
        mejor_vecino = None
        mejor_costo_vecino = mejor_costo
        
        for vecino in vecinos:
            solap_v, huecos_v = calcular_metricas(vecino)
            costo_v = solap_v*100 + huecos_v
            if costo_v < mejor_costo_vecino:
                mejor_vecino = vecino
                mejor_costo_vecino = costo_v
        
        if mejor_vecino is None:
            break
        else:
            actual = mejor_vecino
            mejor_costo = mejor_costo_vecino
            mejor = mejor_vecino
    
    return mejor, calcular_metricas(mejor)

# Ejecutar hill climbing
solucion_final, (solap_final, huecos_final) = hill_climbing()

# Mostrar calendario
print("Calendario final (tesista -> sala, franja):")
for t in tesistas:
    s, f_idx = solucion_final[t]
    if s >= 0 and f_idx >= 0:
        print(f"{t}: Sala {s+1}, Franja {franjas[f_idx]}")
    else:
        print(f"{t}: No asignado")

print(f"\nSolapamientos: {solap_final}")
print(f"Huecos totales: {huecos_final}")

