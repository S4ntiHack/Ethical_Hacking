import itertools
import argparse
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import re
import os
import sys
from time import sleep

SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
LEET_DICT = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"}
VERSION = "2.1"
DEFAULT_MAX_LENGTH = 10

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(f"""
    ██████╗██████╗  █████╗  ██████╗██╗  ██╗██████╗ ██╗ ██████╗████████╗
   ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██║██╔════╝╚══██╔══╝
   ██║     ██████╔╝███████║██║     █████╔╝ ██║  ██║██║██║        ██║   
   ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██║  ██║██║██║        ██║   
   ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗██████╔╝██║╚██████╗   ██║   
    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝ ╚═════╝   ╚═╝   
                                                                    
                    Versión {VERSION} - Generador de Diccionarios
    """)

def apply_leet(text, leet=False):
    if not leet:
        return [text]
    leet_variants = [text]
    for char, replacement in LEET_DICT.items():
        new_variants = []
        for variant in leet_variants:
            if char in variant:
                new_variants.append(variant.replace(char, replacement))
        leet_variants += new_variants
    return list(set(leet_variants))

def generar_combinaciones(args):
    dato, simbolos, numeros, leet, exclude, max_length = args
    combinaciones = []
    variants = apply_leet(dato, leet)
    
    for variant in variants:
        if len(variant) > max_length:
            continue
            
        if not exclude or not re.search(exclude, variant):
            combinaciones.append(variant)
        
        if numeros:
            for num_length in range(1, min(4, max_length - len(variant) + 1)):
                for num in itertools.product(numeros, repeat=num_length):
                    combo = f"{variant}{''.join(num)}"
                    if len(combo) <= max_length and (not exclude or not re.search(exclude, combo)):
                        combinaciones.append(combo)
        
        if simbolos:
            for simbolo in simbolos:
                combo = f"{variant}{simbolo}"
                if len(combo) <= max_length and (not exclude or not re.search(exclude, combo)):
                    combinaciones.append(combo)
                if numeros:
                    for num_length in range(1, min(3, max_length - len(combo)) + 1):
                        for num in itertools.product(numeros, repeat=num_length):
                            combo_num = f"{combo}{''.join(num)}"
                            if len(combo_num) <= max_length and (not exclude or not re.search(exclude, combo_num)):
                                combinaciones.append(combo_num)
    return combinaciones

def generar_diccionario_automatico(datos, archivo_salida, special=False, leet=False, exclude=None, threads=4, max_length=DEFAULT_MAX_LENGTH):
    simbolos = SYMBOLS if special else ""
    numeros = "0123456789"
    
    print(f"\n[+] Configuración:")
    print(f"    - Palabras base: {len(datos)}")
    print(f"    - Símbolos: {'Activado' if special else 'Desactivado'}")
    print(f"    - Leet: {'Activado' if leet else 'Desactivado'}")
    print(f"    - Exclusión: '{exclude if exclude else 'Ninguna'}'")
    print(f"    - Hilos: {threads}")
    print(f"    - Longitud máxima: {max_length} caracteres")
    print(f"    - Archivo de salida: {archivo_salida}\n")
    
    total_palabras = sum(len(apply_leet(d, leet)) for d in datos)
    print(f"[+] Estimación inicial: ~{total_palabras * 100:,} posibles combinaciones (hasta {max_length} caracteres)")
    
    with open(archivo_salida, 'w') as f:
        with Pool(threads) as pool:
            args = [(dato, simbolos, numeros, leet, exclude, max_length) for dato in datos]
            for combinaciones in tqdm(pool.imap(generar_combinaciones, args), 
                                   total=len(datos), 
                                   desc="Generando",
                                   unit="palabra"):
                for combo in combinaciones:
                    f.write(combo + '\n')

def generar_diccionario_manual(caracteres, longitud_min, longitud_max, archivo_salida, special=False, leet=False, exclude=None):
    if special:
        caracteres += SYMBOLS
    
    total_combinaciones = sum(len(caracteres)**i for i in range(longitud_min, longitud_max + 1))
    print(f"\n[+] Configuración:")
    print(f"    - Caracteres: {len(caracteres)} distintos")
    print(f"    - Longitud: {longitud_min} a {longitud_max} caracteres")
    print(f"    - Leet: {'Activado' if leet else 'Desactivado'}")
    print(f"    - Exclusión: '{exclude if exclude else 'Ninguna'}'")
    print(f"    - Archivo de salida: {archivo_salida}")
    print(f"\n[+] Estimación: {total_combinaciones:,} combinaciones posibles")
    
    with open(archivo_salida, 'w') as f:
        for longitud in tqdm(range(longitud_min, longitud_max + 1), 
                           desc="Progreso", 
                           unit="longitud"):
            for combinacion in itertools.product(caracteres, repeat=longitud):
                password = ''.join(combinacion)
                if not exclude or not re.search(exclude, password):
                    if leet:
                        for variant in apply_leet(password, leet=True):
                            if len(variant) <= longitud_max:
                                f.write(variant + '\n')
                    else:
                        f.write(password + '\n')

def menu_principal():
    clear_screen()
    show_banner()
    
    print("  [1] Modo Automático (basado en palabras clave)")
    print("  [2] Modo Manual (combinación de caracteres)")
    print("  [3] Acerca de CrackDict")
    print("  [4] Salir\n")
    
    while True:
        try:
            opcion = int(input("Seleccione una opción (1-4): "))
            if 1 <= opcion <= 4:
                return opcion
            print("Error: Ingrese un número entre 1 y 4")
        except ValueError:
            print("Error: Ingrese un número válido")

def configurar_automatico():
    clear_screen()
    print("\n[ CONFIGURACIÓN - MODO AUTOMÁTICO ]")
    print("-----------------------------------")
    
    datos = input("\nIngrese palabras clave (separadas por espacios): ").split()
    if not datos:
        print("\n[!] Debe ingresar al menos una palabra clave")
        sleep(2)
        return None
    
    archivo = input("Nombre del archivo de salida [diccionario.txt]: ") or "diccionario.txt"
    special = input("¿Incluir símbolos especiales? (s/n) [n]: ").lower() == 's'
    leet = input("¿Aplicar transformación leet? (s/n) [n]: ").lower() == 's'
    exclude = input("Patrón a excluir (ej: '123|abc', dejar vacío para ninguno): ") or None
    
    try:
        max_length = int(input(f"Longitud máxima de contraseñas [{DEFAULT_MAX_LENGTH}]: ") or DEFAULT_MAX_LENGTH)
        max_length = max(1, min(max_length, 50))
    except ValueError:
        max_length = DEFAULT_MAX_LENGTH
        print(f"Usando valor por defecto: {max_length} caracteres")
    
    try:
        threads = int(input(f"Número de hilos a usar [1-{cpu_count()}]: ") or cpu_count())
        threads = max(1, min(threads, cpu_count()))
    except ValueError:
        threads = cpu_count()
        print(f"Usando valor por defecto: {threads} hilos")
    
    return {
        'datos': datos,
        'archivo': archivo,
        'special': special,
        'leet': leet,
        'exclude': exclude,
        'threads': threads,
        'max_length': max_length
    }

def configurar_manual():
    clear_screen()
    print("\n[ CONFIGURACIÓN - MODO MANUAL ]")
    print("--------------------------------")
    
    caracteres = input("\nCaracteres a combinar (ej: abc123): ") or "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    while True:
        try:
            min_len = int(input(f"Longitud mínima [1]: ") or 1)
            max_len = int(input(f"Longitud máxima [{DEFAULT_MAX_LENGTH}]: ") or DEFAULT_MAX_LENGTH)
            if min_len <= 0 or max_len <= 0:
                print("Las longitudes deben ser mayores a 0")
            elif min_len > max_len:
                print("La longitud mínima no puede ser mayor que la máxima")
            elif max_len > 50:
                print("¡Advertencia! Longitudes mayores a 50 pueden generar archivos enormes")
                confirm = input("¿Continuar? (s/n): ").lower()
                if confirm != 's':
                    continue
            else:
                break
        except ValueError:
            print("Ingrese números válidos")
    
    archivo = input("Nombre del archivo de salida [diccionario.txt]: ") or "diccionario.txt"
    special = input("¿Incluir símbolos especiales? (s/n) [n]: ").lower() == 's'
    leet = input("¿Aplicar transformación leet? (s/n) [n]: ").lower() == 's'
    exclude = input("Patrón a excluir (ej: '123|abc', dejar vacío para ninguno): ") or None
    
    return {
        'caracteres': caracteres,
        'min_len': min_len,
        'max_len': max_len,
        'archivo': archivo,
        'special': special,
        'leet': leet,
        'exclude': exclude
    }

def main():
    while True:
        opcion = menu_principal()
        
        if opcion == 1:
            config = configurar_automatico()
            if config:
                print("\n[+] Iniciando generación...")
                try:
                    generar_diccionario_automatico(
                        config['datos'],
                        config['archivo'],
                        config['special'],
                        config['leet'],
                        config['exclude'],
                        config['threads'],
                        config['max_length']
                    )
                    print(f"\n[+] Diccionario generado exitosamente en {config['archivo']}")
                    print(f"[+] Longitud máxima de contraseñas: {config['max_length']} caracteres")
                except Exception as e:
                    print(f"\n[!] Error: {str(e)}")
                input("\nPresione Enter para continuar...")
        
        elif opcion == 2:
            config = configurar_manual()
            print("\n[+] Iniciando generación...")
            try:
                generar_diccionario_manual(
                    config['caracteres'],
                    config['min_len'],
                    config['max_len'],
                    config['archivo'],
                    config['special'],
                    config['leet'],
                    config['exclude']
                )
                print(f"\n[+] Diccionario generado exitosamente en {config['archivo']}")
                print(f"[+] Rango de longitudes: {config['min_len']}-{config['max_len']} caracteres")
            except Exception as e:
                print(f"\n[!] Error: {str(e)}")
            input("\nPresione Enter para continuar...")
        
        elif opcion == 3:
            clear_screen()
            show_banner()
            print("\nCRACKDICT - Generador Avanzado de Diccionarios")
            print("------------------------------------------------")
            print(f"Versión: {VERSION}")
            print("Autor: Santiago Montenegro")
            print(f"\nCaracterísticas:")
            print(f"- Generación automática basada en palabras clave (hasta {DEFAULT_MAX_LENGTH} caracteres por defecto)")
            print("- Generación manual por combinación de caracteres")
            print("- Transformación leet (a→4, e→3, etc.)")
            print("- Exclusión de patrones no deseados")
            print("- Multiprocesamiento para mayor velocidad")
            print("- Estimación de combinaciones antes de generar")
            input("\nPresione Enter para volver al menú...")
        
        elif opcion == 4:
            print("\n¡Gracias por usar CrackDict!")
            sleep(1)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Operación cancelada por el usuario")
        sys.exit(1)
