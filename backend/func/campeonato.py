import sys
import pymongo
sys.path.append('..')
from random import randint
from obj.time import Time
from obj.grupo import Grupo

# Gera 5 times e adiciona a lista
def gera_time(nome):
    lista_times = []

    for i in range(5):
        lista_times.append(Time(nome))
        nome += 1

    return nome, lista_times

# Gera os 16 grupos, totalizando 80 times
def gera_grupos():
    lista_grupo, j = [], 1

    for i in range(16):
        g = Grupo()
        j, times = gera_time(j)
        g.times.append(times)
        lista_grupo.append(g)
    
    return lista_grupo

# Forma a chave A e a chave B randomicamente
def forma_chave(l):
    A, B = [], []

    for i in l:
        n = randint(1, 2)

        if n == 1:
            if len(A) != 16:
                A.append(i)
            else:
                B.append(i)
        else:
            if len(B) != 16:
                B.append(i)
            else:
                A.append(i)
    
    return A, B

def partida(l):
    t1 = 0
    t2 = 0

    # Gerando o vencedor randomicamente
    while t1 == t2:
        t1 = randint(1, 100)
        t2 = randint(1, 100)

        if t1 == t2:
            pass
        else:
            if t1 > t2:
                l[0].rounds = 16
                l[1].rounds = randint(1, 15)
            else:
                l[1].rounds = 16
                l[0].rounds = randint(1, 15)

    winner = None
    loser = None

    if l[0].rounds == 16:
        winner = l[0]
        loser = l[1]
        del l[1]
    else:
        winner = l[1]
        loser = l[0]
        del l[0]
        
    return loser, winner, l

def partida_final(A, B):
    t1 = 0
    t2 = 0

    # Gerando o vencedor randomicamente
    while t1 == t2:
        t1 = randint(1, 100)
        t2 = randint(1, 100)

        if t1 == t2:
            pass
        else:
            if t1 > t2:
                A.rounds = 16
                B.rounds = randint(1, 15)
            else:
                A.rounds = 16
                B.rounds = randint(1, 15)

    if A.rounds == 16:
        return A, B
    else:
        return B, A

def playoffs(times):
    l, historico, cont = [], [], 1

    # Formando uma única lista
    for i in times:
        l += i
    
    A, B = forma_chave(l)
    winner = None

    # Enquanto não tiver um vencedor
    while not winner:
        # Se a chave A e a chave B ainda não tiver somente um time
        if len(A) != 1 and len(B) != 1:
            loser, time, A = partida(A)
            historico.append([time, loser])
            cont += 1

            loser, time, B = partida(B)
            historico.append([time, loser])
            cont += 1
        else:
            winner, loser = partida_final(A[0], B[0])

    historico.append([winner, loser])

    return historico

def simula():
    grupos, cont, classificados, partidas_fase_grupos, historico_grupos_final = gera_grupos(), 1, [], [], []

    for i in grupos:
        partidas_fase_grupos += i.partida_grupo_interno()
        c, partidas_grupo_resultado_final = i.classificados(cont)
        classificados.append(c)
        historico_grupos_final += partidas_grupo_resultado_final
        cont += 1
        
    return partidas_fase_grupos, historico_grupos_final, playoffs(classificados)