import multiprocessing
from py3270 import Emulator
import sys, os, time

terminate = False

def emulador():
    global e, terminate
    # Main
    host = "155.210.152.51"
    port = "3270"
    mylogin = 'GRUPO_03'
    mypass = 'secreto6'
    delay=20
    delayScreen=0.5
    
    e = Emulator(visible=True)
    e.connect(host + ':' + port)

    # Patalla inicio
    time.sleep(delayScreen)
    e.send_enter()

    # Pantalla Login
    time.sleep(delayScreen)
    ## Usuario
    e.wait_for_field()
    e.send_string(mylogin)
    e.send_enter()
    ## Contraseña
    e.wait_for_field()
    e.send_string(mypass)
    e.send_enter()

    # Pantalla previa a comandos
    time.sleep(delayScreen)
    e.wait_for_field()
    e.send_enter()
    time.sleep(delayScreen)
    e.wait_for_field()
    e.send_string('PA1')
    e.send_enter()

    # Pantalla comandos
    time.sleep(delayScreen)
    e.wait_for_field()
    e.send_string('tareas.c')
    e.send_enter()

# Guardar lo que se lee por pantalla en un fichero 
def pantalla(filename="pantalla.txt"):
    time.sleep(0.5)
    screen_content = ''
    for row in range(1, 43 + 1):
        line = e.string_get(row, 1, 79)
        screen_content += line + '\n'
    archivo = open(filename, "w")
    archivo.write(screen_content)
    archivo.close()

# Opción ASSIGN TASKS
def assign_tasks(tipo, fecha, desc, nombre):
    e.send_string("1")
    e.send_enter()

    if tipo=="General":
        e.send_string("1")
        e.send_enter()
        e.send_string(fecha)
        e.send_enter()
        e.send_string(desc)
        e.send_enter()

    elif tipo=="Especifico":
        e.send_string("2")
        e.send_enter()
        e.send_string(fecha)
        e.send_enter()
        e.send_string(nombre)
        e.send_enter()
        e.send_string(desc)
        e.send_enter()
    
    e.send_string("3")
    e.send_enter()

def read_line(line, file="pantalla.txt"):
    # Abre el archivo en modo lectura
    with open(file, "r") as archivo:
        lineas = archivo.readlines()  # Lee todas las líneas del archivo

        if 0 <= line < len(lineas):
            linea_deseada = lineas[line]
            return linea_deseada.strip()  # strip() elimina los caracteres de nueva línea
        else:
            return 0

def get_tasks_general():
    resultado = []
    for num_line in range(1, 43 + 1):
        line=read_line(num_line,"./sl-pr-2/pantalla.txt")
        print(line)
        if line!=0:
            if line.find("TOTAL TASK")!=-1:
                return resultado
            else:
                partes = line.split(" ")
                temp = {"fecha":partes[4],"descripcion":partes[6]}
                resultado.append(temp)

def get_tasks_specific():
    resultado = []
    for num_line in range(1, 43 + 1):
        line=read_line(num_line,"./sl-pr-2/pantalla.txt")
        print(line)
        if line!=0:
            if line.find("TOTAL TASK")!=-1:
                return resultado
            else:
                partes = line.split(" ")
                temp = {"fecha":partes[4],"nombre":partes[5],"descripcion":partes[6]}
                resultado.append(temp)

# Opción VIEW TASKS
def view_tasks():
    resultado=[]
    e.send_string("2")
    e.send_enter()
    e.exec_command(b"Clear")
    e.send_string("1")
    e.send_enter()
    pantalla()
    resultado = resultado.append(get_tasks_general())
    e.exec_command(b"Clear")
    e.send_string("2")
    e.send_enter()
    pantalla()
    resultado = resultado.append(get_tasks_specific())
    return resultado

# Opción EXIT TASKS
def exit_tasks():
    global terminate
    e.send_string("3")
    e.send_enter()
    terminate=True

if __name__ == '__main__':
    while not terminate:
        time.sleep(1)
    e.terminate()