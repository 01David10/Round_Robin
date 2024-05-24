import pandas as pd
import matplotlib.pyplot as plt

# funcion para el menu de inicio
def MenuInicio():
    print("Round Robin")

    datosRR = []    # lista para almacenar los datos de los procesos
    n_procesos = ValidarDato("Cantidad de procesos: ",1)

    for i in range(n_procesos):
        tiempo_llegada = ValidarDato(f"Tiempo de llegada para P{i}: ",0)
        tiempo_llegada = tiempo_llegada*50 # se convierte a milisegundos
        NCPU = ValidarDato(f"NCPU para P{i}: ",1)
        NCPU = NCPU*50 # se convierte a milisegundos

        # E/S
        num_io = ValidarDato(f"Cantidad de E/S para P{i}: ", 0)
        duracion_io = []
        ncpu_post_io = []

        for j in range(num_io):
            duracion_es = ValidarDato(f"Ingrese la duracion de la E/S {j+1} para P{i}: ",1) * 50
            ncpu_post_es = ValidarDato(f"Ingrese NCPU despues de la E/S {j+1} para p{i}: ",1) * 50
            duracion_io.append(duracion_es)
            ncpu_post_io.append(ncpu_post_es)

        # estructura del objeto
        formato = {     
            "Proceso": f"P{i}",
            "Tiempo llegada": tiempo_llegada,
            "NCPU": NCPU,
            "CPU Primera Vez": None,  
            "CPU Ultima Vez": None,    
            "Duracion E/S": duracion_io,
            "NCPU Post E/S": ncpu_post_io,
            "E/S actual": 0, # para llevar el control de la E/S actual
            "NCPU Restante" : NCPU  # para llevar el control del NCPU restante
        }
        datosRR.append(formato) # se agrega el objeto a la lista

    tablaProcesoRR = pd.DataFrame(datosRR)    # se convierte la lista en un dataframe

    print("\nDatos ingresados: ")
    print(tablaProcesoRR)   # se imprime el dataframe

    quantum = 50 # cada Q equivale a 50 milisegundos
    switch_time = 10    # tiempo de intercambio (milisegundos)
    round_robin(tablaProcesoRR, quantum, switch_time)

def round_robin(datos, quantum, switch_time):
    colores = ["blue", "red", "green", "cyan", "brown", "purple", "olive", "gray", "orange"]
    color_map = {process: color for process, color in zip(datos["Proceso"], colores)}
    datos = datos.sort_values(by="Tiempo llegada", ascending=True)
    fig, ax = plt.subplots()
    c = 0
    queue = []
    es_queue = []  # inicializar la cola de procesos en E/S
    arrived = set()
    current_time = 0

    print("\nCola de procesos:")
    while len(queue) > 0 or len(arrived) < len(datos):
        # Añadir nuevos procesos a la cola que han llegado hasta el current_time
        for i in range(len(datos)):
            if datos.iloc[i]["Tiempo llegada"] <= current_time and i not in arrived:
                queue.append(i)
                arrived.add(i)

        # Manejo de procesos en E/S
        for es_process, es_end_time in es_queue[:]:
            if current_time >= es_end_time:
                queue.append(es_process)
                es_queue.remove((es_process, es_end_time))

        if not queue:
            current_time += 1
            continue

        i = queue.pop(0)
        row = datos.iloc[i]
        color = color_map[datos.iloc[i]["Proceso"]]

        # añadir etiquetas
        if pd.isna(row["CPU Primera Vez"]) or row["CPU Primera Vez"] is None:
            ax.annotate("P" + str(i), (c, 15), fontsize=9, ha='left', color=color)
            datos.at[i, "CPU Primera Vez"] = current_time

        ncpu_restante = datos.at[i, "NCPU Restante"]

        if ncpu_restante > quantum:
            c, ax, datos = CrearGrafica(datos, i, row, ax, c, color, quantum, switch_time)
            datos.at[i, "NCPU Restante"] -= quantum
            queue.append(i)
            current_time += quantum + switch_time
        else:
            c, ax, datos = CrearGrafica(datos, i, row, ax, c, color, ncpu_restante, switch_time)
            current_time += ncpu_restante + switch_time
            datos.at[i, "NCPU Restante"] = 0  # Proceso ha completado su NCPU actual

            # Manejo de E/S si el proceso ha completado su NCPU actual
            current_es = datos.at[i, "E/S actual"]
            es_durations = datos.at[i, "Duracion E/S"]
            quanta_after_es = datos.at[i, "NCPU Post E/S"]
            if current_es < len(es_durations):
                es_time = es_durations[current_es]
                post_es_quantum = quanta_after_es[current_es]
                datos.at[i, "NCPU Restante"] = post_es_quantum
                datos.at[i, "E/S actual"] += 1
                es_queue.append((i, current_time + es_time))

                # Añadir la E/S a la gráfica
                ax.broken_barh([(c, es_time)], (0, 9), facecolors='yellow')  # Agregar la duración de E/S a la gráfica
                c += es_time
                current_time += es_time
            else:
                datos.at[i, "NCPU Restante"] = 0  # Proceso terminado

    ax.set_ylim(0, 50)
    ax.set_xlim(0, current_time)
    ax.set_xlabel('ms')
    ax.set_yticks([10], labels=['Procesos'])
    ax.grid(False)
    plt.show()
    CalcularDatos(datos)
    print("\nDatos de cada proceso:")
    print(datos)
    print("\nPromedios:")
    print("Promedio del tiempo de vuelta: %s" % datos["Tiempo vuelta"].mean())
    print("Promedio del tiempo de espera: %s" % datos["Tiempo espera"].mean())
    print("Tiempo total CPU: %s" % current_time)

def CrearGrafica(datos, index, row, ax, c, color, quantum, switch_time):
    tiempo_llegada = int(row["Tiempo llegada"])
    if tiempo_llegada > c:
        c = tiempo_llegada
    ax.broken_barh([(c, quantum)], (0, 9), facecolors=color)
    if pd.isna(row["CPU Primera Vez"]) or row["CPU Primera Vez"] is None:  
        datos.at[index, "CPU Primera Vez"] = c
    
    c += quantum
    c += switch_time
    datos.at[index, "CPU Ultima Vez"] = c
    return c, ax, datos

# funcion para calcular los tiempos de vuelta y espera
def CalcularDatos(datos):
    for index, row in datos.iterrows(): 
        datos.at[index,"Tiempo vuelta"] = row["CPU Ultima Vez"] - row["Tiempo llegada"]
        datos.at[index,"Tiempo espera"] = row["CPU Primera Vez"] - row["Tiempo llegada"]
    return datos

# funcion para validar los datos de entrada
def ValidarDato(mensaje,opcion):
    while True:
        try:
            dato = int(input(mensaje))
            if(opcion == 1):    # para el ncpu, cantidad de procesos, duracion de E/S y ncpu E/S
                if(dato > 0):
                    return dato
                else:
                    print("El dato debe ser mayor 0")
            else:   # para el tiempo de llegada
                if(dato >=0):
                    return dato
                else:
                    print("El dato debe ser mayor o igual 0")
        except ValueError:
            print("Por favor ingrese un valor numerico")

if __name__ == "__main__":
    MenuInicio()