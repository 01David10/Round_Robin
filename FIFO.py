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
            "NCPU" : NCPU
        }
        datosRR.append(formato) # se agrega el objeto a la lista

    tablaProcesoFIFO = pd.DataFrame(datosRR)    # se convierte la lista en un dataframe
    print("\nDatos ingresados: ")
    print(tablaProcesoFIFO)   # se imprime el dataframe
    FIFO(tablaProcesoFIFO)

# cambiar esta funcion popr round robin
def FIFO(datos):
    colores = ["blue","red","green","cyan","brown","purple","olive","gray","orange"]
    datos = datos.sort_values(by="Tiempo llegada", ascending=True)
    print("\n--------------- DATOS ORDENADOS -----------------------------")
    print(datos)
    fig, ax = plt.subplots()
    c = 0
    for index, row in datos.iterrows():
        color = random.choice(colores)
        colores.remove(color)
        c, ax, datos = CrearGrafica(datos,index,row,ax,c,color)
        Tp = datos.at[index,"CPU Primera Vez"]
        ax.annotate("P" + str(index)  + "=" + str(row["NCPU"]), (int((Tp +c )/2), 12), fontsize=9, ha='center', color='black')

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
def CrearGrafica(datos,index,row,ax,c, color):
    tiempo_llegada = int(row["Tiempo llegada"])
    if(tiempo_llegada == 0):
        ax.broken_barh([(index, int(row["NCPU"]))], (0,10), facecolors='tab:' + color)
    else:
        if(tiempo_llegada > c):
            ax.broken_barh([(tiempo_llegada,int(row["NCPU"]))], (0,10), facecolors='tab:'+ color)
            c =  tiempo_llegada
        else:
            ax.broken_barh([(c,int(row["NCPU"]))], (0,10), facecolors='tab:'+ color)

    datos.at[index,"CPU Primera Vez"] = c
    c = c + int(row["NCPU"])
    return c,ax,datos

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