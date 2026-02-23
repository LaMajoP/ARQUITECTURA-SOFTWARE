import os
import copy
from typing import Optional
from domain.carrera_ingenieria import CarreraIngenieria
from infrastructure.malla_loader_factory import MallaLoaderFactory
from domain.calculadora_promedio import CalculadoraPromedio

def obtener_float_input(mensaje: str, min_val: float, max_val: float) -> float:
    while True:
        try:
            entrada = input(mensaje)
            entrada = entrada.replace(',', '.')
            valor = float(entrada)
            if min_val <= valor <= max_val:
                return valor
            else:
                print(f"Error: El valor debe estar entre {min_val} y {max_val}.")
        except ValueError:
            print("Error: Ingrese un número válido.")

def obtener_int_input(mensaje: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if min_val is not None:
                if valor < min_val:
                    print(f"Error: El valor debe ser mayor o igual a {min_val}.")
                    continue
            if max_val is not None:
                if valor > max_val:
                    print(f"Error: El valor debe ser menor o igual a {max_val}.")
                    continue
            return valor
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def main():
    print("=== Calculadora de Promedios Académicos - Facultad de Ingeniería ===")
    
    print("\nCarreras disponibles:")
    print("1. Ingeniería Informática")
    print("2. Ingeniería Civil")
    opcion_carrera = input("Seleccione una carrera (1-2): ")
    
    if opcion_carrera == "2":
        carrera = CarreraIngenieria.INGENIERIA_CIVIL
        archivo_malla = 'malla_civil.json'
    else:
        if opcion_carrera != "1":
            print("Opción no válida. Seleccionando Ingeniería Informática por defecto...")
        carrera = CarreraIngenieria.INGENIERIA_INFORMATICA
        archivo_malla = 'malla_informatica.json'
        
    print(f"\nHa seleccionado: {carrera.value}")
    
    try:
        loader = MallaLoaderFactory.get_loader('json')
        # Buscamos el archivo json de la malla en la carpeta data
        ruta_malla = os.path.join(os.path.dirname(__file__), 'data', archivo_malla)
        malla = loader.load(ruta_malla)
        print("Malla curricular cargada exitosamente.")
    except Exception as e:
        print(f"Error al cargar la malla curricular: {e}")
        return

    semestre = obtener_int_input("\nIngrese el semestre actual a cursar (1-9): ", min_val=1, max_val=9)
    
    # Se obtienen y copian las materias para simular la carga académica sin afectar la malla original
    materias_malla_semestre = malla.get_materias_por_semestre(semestre)
    carga_academica = [copy.deepcopy(m) for m in materias_malla_semestre]
    
    calculadora = CalculadoraPromedio()
    
    while True:
        print("\n" + "="*50)
        print("--- Mi Carga Académica ---")
        if not carga_academica:
            print("(No hay materias registradas en su carga académica)")
        else:
            for m in carga_academica:
                print(m)
                
        print("\n--- Resumen de Promedios ---")
        promedio_acumulado = calculadora.calcular(carga_academica)
        print(f"Promedio Ponderado Acumulado: {promedio_acumulado:.2f}")
        
        semestres_presentes = sorted(list(set(m.get_semestre() for m in carga_academica)))
        if semestres_presentes:
            print("Por semestre:")
            for sem in semestres_presentes:
                prom_semestre = calculadora.calcular_por_semestre(carga_academica, sem)
                print(f"  - Semestre {sem}: {prom_semestre:.2f}")
        print("="*50)
        
        print("\nOpciones:")
        print("1. Eliminar una materia")
        print("2. Agregar una materia de otro semestre")
        print("3. Ingresar notas de los 3 cortes para una materia")
        print("4. Agregar TODAS las materias de otro semestre")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ").strip().lower()
        
        if opcion in ['1', 'a']:
            id_eliminar = obtener_int_input("Ingrese el ID de la materia a eliminar: ")
            materia_a_eliminar = next((m for m in carga_academica if m.get_id() == id_eliminar), None)
            if materia_a_eliminar:
                carga_academica.remove(materia_a_eliminar)
                print("Materia eliminada de su carga.")
            else:
                print("Materia no encontrada en su carga académica.")
                
        elif opcion in ['2', 'b']:
            semestre_objetivo = obtener_int_input("Ingrese el número del semestre de la materia que desea agregar (1-9): ", min_val=1, max_val=9)
            materias_del_semestre = malla.get_materias_por_semestre(semestre_objetivo)
            
            if not materias_del_semestre:
                print(f"No se encontraron materias para el semestre {semestre_objetivo}.")
                continue
                
            print(f"\n--- Materias del Semestre {semestre_objetivo} ---")
            for m in materias_del_semestre:
                print(f"  ID: {m.get_id()} - {m.get_nombre()} ({m.get_creditos()} créditos)")
                
            id_agregar = obtener_int_input("\nIngrese el ID de la materia a agregar: ")
            
            if any(m.get_id() == id_agregar for m in carga_academica):
                print("Error: La materia ya está en su carga académica.")
                continue
                
            materia_en_malla = next((m for m in materias_del_semestre if m.get_id() == id_agregar), None)
            if materia_en_malla:
                carga_academica.append(copy.deepcopy(materia_en_malla))
                print(f"Materia '{materia_en_malla.get_nombre()}' agregada exitosamente.")
            else:
                print(f"Error: La materia con ID {id_agregar} no se encontró en el semestre {semestre_objetivo}.")
                
        elif opcion in ['3', 'c']:
            id_nota = obtener_int_input("Ingrese el ID de la materia a calificar: ")
            materia_a_calificar = next((m for m in carga_academica if m.get_id() == id_nota), None)
            if materia_a_calificar:
                print(f"\nIngresando notas para: {materia_a_calificar.get_nombre()}")
                corte1 = obtener_float_input("Ingrese nota Corte 1 (30%) [0-5]: ", 0.0, 5.0)
                corte2 = obtener_float_input("Ingrese nota Corte 2 (30%) [0-5]: ", 0.0, 5.0)
                corte3 = obtener_float_input("Ingrese nota Corte 3 (40%) [0-5]: ", 0.0, 5.0)
                
                nota_final = round((corte1 * 0.3) + (corte2 * 0.3) + (corte3 * 0.4), 1)
                
                try:
                    materia_a_calificar.set_notas_cortes(corte1, corte2, corte3)
                    print(f"Nota final calculada para '{materia_a_calificar.get_nombre()}': {materia_a_calificar.get_nota()}")
                except ValueError as e:
                    print(f"Error al asignar la nota: {e}")
            else:
                print("Materia no encontrada en su carga académica.")
                
        elif opcion in ['4', 'd']:
            semestre_objetivo = obtener_int_input("Ingrese el número del semestre que desea agregar completo (1-9): ", min_val=1, max_val=9)
            materias_del_semestre = malla.get_materias_por_semestre(semestre_objetivo)
            
            if not materias_del_semestre:
                print(f"No se encontraron materias para el semestre {semestre_objetivo}.")
                continue
                
            agregadas = 0
            for materia_nueva in materias_del_semestre:
                if not any(m.get_id() == materia_nueva.get_id() for m in carga_academica):
                    carga_academica.append(copy.deepcopy(materia_nueva))
                    agregadas += 1
            
            if agregadas > 0:
                print(f"Se agregaron {agregadas} materias del semestre {semestre_objetivo} a su carga académica.")
            else:
                print(f"Todas las materias del semestre {semestre_objetivo} ya estaban en su carga académica.")
                
        elif opcion in ['5', 'e']:
            print("Saliendo de la calculadora. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
