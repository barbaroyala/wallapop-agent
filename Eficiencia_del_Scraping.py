import time

TIMER = {}

def iniciar_temporizador(etapa):
    TIMER[etapa] = time.time()

def terminar_temporizador(etapa):
    if etapa in TIMER:
        duracion = time.time() - TIMER[etapa]
        print(f"⏱️ Duración de '{etapa}': {duracion:.2f} segundos")
        return duracion
    else:
        print(f"⚠️ Etapa '{etapa}' no fue iniciada.")
        return None
