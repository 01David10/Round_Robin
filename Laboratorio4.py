import pandas as pd
import matplotlib.pyplot as plt
import random

# funcion para el menu de inicio
def MenuInicio():
    print("Round Robin:")

    datosRR = []    # lista para almacenar los datos de los procesos
    n_procesos = ValidarDato("Cantidad de procesos: ",1)

    for i in range(n_procesos):
        tiempo_llegada = ValidarDato(f"Tiempo de llegada para P{i}: ",0)
        NCPU = ValidarDato(f"NCPU para P{i}: ",1)
        formato = {     # estructura del objeto
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

    quantum = ValidarDato("Ingrese el quantum: ", 1)  # preguntar cuantos Q tiene cada proceso
    switch_time = ValidarDato("Ingrese el tiempo de intercambio: ", 1)  # preguntar cuantos quantum dura el intercambio
    round_robin(tablaProcesoRR, quantum, switch_time)

# cambiar esta funcion por round robin
def round_robin(datos, quantum, switch_time):
    colores_originales = ["blue","red","green","cyan","brown","purple","olive","gray","orange"]
    colores = colores_originales.copy()
    datos = datos.sort_values(by="Tiempo llegada", ascending=True)
    print("\n--------------- DATOS ORDENADOS -----------------------------")
    print(datos)
    fig, ax = plt.subplots()
    c = 0
    queue = list(range(len(datos)))
    while queue:
        print("Cola de procesos:", [datos.iloc[process]["Proceso"] for process in queue])  # imprimir la cola de procesos
        i = queue.pop(0)
        row = datos.iloc[i]
        color = random.choice(colores)
        colores.remove(color)
        if not colores:  # If colores is empty
            colores = colores_originales.copy()  # Reset colores to its original state
        if row["NCPU"] > quantum:
            c, ax, datos = CrearGrafica(datos, i, row, ax, c, color, quantum, switch_time)
            datos.at[i, "NCPU"] -= quantum
            queue.append(i)        
        else:
            c, ax, datos = CrearGrafica(datos, i, row, ax, c, color, row["NCPU"], switch_time)
        Tp = datos.at[i, "CPU Primera Vez"]
        ax.annotate("P" + str(i)  + "=" + str(row["NCPU"]), (int((Tp +c )/2), 12), fontsize=9, ha='center', color='black')

    ax.set_ylim(0, 50)
    ax.set_xlim(0, )
    ax.set_xlabel('Quantums')
    ax.set_yticks([10], labels=['Procesos'])
    ax.grid(False)
    plt.show()
    CalcularDatos(datos)
    print(datos)
    print("Tiempo vuelta en promedio: %s" % datos["Tiempo vuelta"].mean())
    print("Tiempo vuelta en espera: %s" % datos["Tiempo espera"].mean())

# modificarla para que quede con los intercambios
def CrearGrafica(datos, index, row, ax, c, color, quantum, switch_time):
    tiempo_llegada = int(row["Tiempo llegada"])
    if tiempo_llegada > c:
        c = tiempo_llegada
    ax.broken_barh([(c, quantum)], (10*index, 9), facecolors=color)
    c += quantum
    c += switch_time
    if pd.isna(row["CPU Primera Vez"]) or row["CPU Primera Vez"] is None:  # Add this condition
        datos.at[index, "CPU Primera Vez"] = c
    datos.at[index, "CPU Ultima Vez"] = c
    return c, ax, datos

# funcion para calcular los tiempos de vuelta y espera
def CalcularDatos(datos):
    for index, row in datos.iterrows():
        datos.at[index,"Tiempo vuelta"] =  (int(row["CPU Primera Vez"]) +int(row["NCPU"])) - 0 - row["Tiempo llegada"]
        datos.at[index,"Tiempo espera"] = row["CPU Primera Vez"] - row["Tiempo llegada"]
    return datos

# funcion para visualizar la cola de prioridad
def ColaPrioridad(datos):
    pass

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