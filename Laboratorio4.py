import pandas as pd
import matplotlib.pyplot as plt
import random

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
        # estructura del objeto
        formato = {     
            "Proceso" : f"P{i}",
            "Tiempo llegada" : tiempo_llegada,
            "NCPU" : NCPU,
            "CPU Primera Vez": None,  
            "CPU Ultima Vez": None    
        }
        datosRR.append(formato) # se agrega el objeto a la lista

    tablaProcesoRR = pd.DataFrame(datosRR)    # se convierte la lista en un dataframe

    print("\nDatos ingresados: ")
    print(tablaProcesoRR)   # se imprime el dataframe

    quantum = 50 # cada Q equivale a 50 milisegundos
    switch_time = 10    # tiempo de intercambio (milisegundos)
    round_robin(tablaProcesoRR, quantum, switch_time)

# cambiar esta funcion por round robin
def round_robin(datos, quantum, switch_time):
    colores = ["blue","red","green","cyan","brown","purple","olive","gray","orange"]
    color_map = {process: color for process, color in zip(datos["Proceso"], colores)}   # diccionario para asignar colores a los procesos
    datos = datos.sort_values(by="Tiempo llegada", ascending=True)
    fig, ax = plt.subplots()
    c = 0
    queue = list(range(len(datos))) # creacion cola de procesos
    added_to_graph = [False] * len(datos)  # lista para verificar que proceso ha sido añadido a la grafica (para las etiquetas)

    print("\nCola de procesos:")
    while queue:
        print([datos.iloc[process]["Proceso"] for process in queue])  # imprimir la cola de procesos
        i = queue.pop(0)
        row = datos.iloc[i]
        color = color_map[datos.iloc[i]["Proceso"]] # Asignar color al proceso, tomando en cuenta el diccionario

        # añadir etiquetas
        if not added_to_graph[i]:  # verifica si el proceso no ha sido añadido a la grafica antes (para no repetir etiquetas)
            ax.annotate("P" + str(i), (c, 15), fontsize=9, ha='left', color=color)  # añade la etiqueta al proceso
            added_to_graph[i] = True  # marca el proceso como añadido

        if row["NCPU"] > quantum:
            c, ax, datos = CrearGrafica(datos, i, row, ax, c, color, quantum, switch_time)
            datos.at[i, "NCPU"] -= quantum
            queue.append(i)        
        else:
            c, ax, datos = CrearGrafica(datos, i, row, ax, c, color, row["NCPU"], switch_time)
        Tp = datos.at[i, "CPU Primera Vez"]

    ax.set_ylim(0, 50)
    ax.set_xlim(0, )
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

# modificarla para que quede con los intercambios
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
        datos.at[index,"Tiempo vuelta"] = (int(row["CPU Primera Vez"]) +int(row["NCPU"])) - 0 - row["Tiempo llegada"]
        datos.at[index,"Tiempo espera"] = row["CPU Primera Vez"] - row["Tiempo llegada"]
    return datos

# funcion para validar los datos de entrada
def ValidarDato(mensaje,opcion):
    while True:
        try:
            dato = int(input(mensaje))
            if(opcion == 1):
                if(dato > 0):
                    return dato
                else:
                    print("Tiempo de llegada y cantidad de procesos debe ser mayor 0")
            else:
                if(dato >=0):
                    return dato
                else:
                    print("NCPU debe ser positivo, mayor o igual 0")
        except ValueError:
            print("Por favor ingrese un valor numerico")

if __name__ == "__main__":
    MenuInicio()