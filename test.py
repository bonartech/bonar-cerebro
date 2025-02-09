from CEREBRO.cerebro import encadenamiento_de_pensamiento, mostrar_grafo, procesar_texto_y_construir_grafo

print('test el leon es un mamifero grande')
procesar_texto_y_construir_grafo("El león es un mamífero grande.")
mostrar_grafo()

print("test tigre", "león")
encadenamiento_de_pensamiento("tigre", "león")
mostrar_grafo()


print('test El sol es una estrella brillante en el cielo')
procesar_texto_y_construir_grafo("El sol es una estrella brillante en el cielo.")
mostrar_grafo()
encadenamiento_de_pensamiento("sol", "mamífero")
