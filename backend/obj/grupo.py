from random import randint
from .time import Time
import operator

class Grupo:
    def __init__(self):
        self.times = []
    
    def partida_grupo_interno(self):
        l = []
        # Todos do grupo contra todos do grupo
        for i in range(5):
            for j in range(i + 1, 5):
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
                            t1 = 16
                            t2 = randint(1, 15)
                        else:
                            t2 = 16
                            t1 = randint(1, 15)
                
                # Salvando saldo de rounds para desempate
                self.times[0][i].rounds += t1
                self.times[0][j].rounds += t2

                aux_t1 = Time(self.times[0][i].nome)
                aux_t2 = Time(self.times[0][j].nome)
                aux_t1.rounds = t1
                aux_t2.rounds = t2
                
                
                if t1 == 16:
                    self.times[0][i].pontos += 1
                    aux_t1.pontos = self.times[0][i].pontos
                    aux_t2.pontos = self.times[0][j].pontos
                    l.append([aux_t1, aux_t2])
                else:
                    self.times[0][j].pontos += 1
                    aux_t1.pontos = self.times[0][i].pontos
                    aux_t2.pontos = self.times[0][j].pontos
                    l.append([aux_t2, aux_t1])

        return l
                

    def classificados(self, n):
        c = []

        # Ordenando os time de cada grupo por pontuação e por rounds ganhos
        aux = sorted(self.times[0], key = operator.attrgetter('rounds'), reverse = True)
        aux = sorted(aux, key = operator.attrgetter('pontos'), reverse = True)

        c.append(aux[0]) # Time 1 do grupo
        c.append(aux[1]) # Time 2 do grupo
        
        return c, self.times[0]