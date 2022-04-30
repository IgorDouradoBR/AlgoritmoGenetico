#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Alunos: Hojin Ryu, Igor Dourado e Igor Vicente

import sys
from random import randint
import random
from math import factorial

ranking = []
qtdPares = None
coefMutacao = None

def embaralhar(cromossomo, trocas):
    for _ in range(trocas):
        posicao_1 = randint(0,len(cromossomo)-1)
        posicao_2 = randint(0,len(cromossomo)-1)
        valor_1 = cromossomo[posicao_1]
        while posicao_1 == posicao_2:
            posicao_2 = randint(0,len(cromossomo)-1)
        cromossomo[posicao_1] = cromossomo[posicao_2]
        cromossomo[posicao_2] = valor_1

def geraPopulacaoInicial():
    populacaoInicial = []  
    for _ in range(tamPopulacao):
        cromossomo = [random.sample(range(1,qtdPares+1), qtdPares),0]
        while cromossomo in populacaoInicial:
            cromossomo = [random.sample(range(1,qtdPares+1), qtdPares),0]
        populacaoInicial.append(cromossomo)
    return populacaoInicial

def aptidao(cromossomo):
    cont = 0.0 
    alpha = 1.0/qtdPares
    for index in range(qtdPares):
        alphaManha = alpha * (qtdPares - ranking[index].index(cromossomo[index])) # subtracao apenas para inverter o ranking
        alphaTarde = alpha * (qtdPares - ranking[(cromossomo[index]-1)+qtdPares].index(index+1))
        # aptidao para a dupla (index+1, cromossomo[index])
        cont += (alphaManha + alphaTarde)/2.0  
    
    # aptidao do cromossomo (soma da aptidao de cada par pelo numero de pares)
    return cont/qtdPares 

def selecao(populacao):
    # Elitismo: levar o melhor cromossomo da populacao atual para a proxima geracao
    cromossomo = sorted(populacao, key=lambda tup: tup[1], reverse=True)[0]
    return [cromossomo]

def reproducao(populacao, populacaoIntermediaria):  # Position Based Crossover (PBX)
    lenPopulacaoIsPar = len(populacao)%2 == 0
    if not lenPopulacaoIsPar: populacao.pop()

    for i in range(0,tamPopulacao-1,2):
        cromossomo_1 = populacao[i][0]
        cromossomo_2 = populacao[i+1][0]
        # print(cromossomo_1)
        # print(cromossomo_2)

        filho_1, filho_2 = [0] * qtdPares, [0] * qtdPares

        # print("")
        posicoesSelecionadas = random.sample(range(qtdPares), int(qtdPares/2))
        # print(posicoesSelecionadas)
        for index in posicoesSelecionadas:
            filho_1[index] = cromossomo_2[index]
            filho_2[index] = cromossomo_1[index]

        for index in range(qtdPares):
            if cromossomo_1[index] not in filho_1:
                filho_1[filho_1.index(0)] = cromossomo_1[index]

            if cromossomo_2[index] not in filho_2:
                filho_2[filho_2.index(0)] = cromossomo_2[index]
        
        # print("")
        # print(filho_1)
        # print(filho_2)
        # print("-------------")
        populacaoIntermediaria.append([filho_1,0])
        populacaoIntermediaria.append([filho_2,0])

    if lenPopulacaoIsPar: populacaoIntermediaria.pop()
    # print("len populacao intermediaria: ", len(populacaoIntermediaria))
    # for cromossomo in populacaoIntermediaria:
    #     print(cromossomo)

def mutacao(populacao):
    qtdMutar = randint(0,int((coefMutacao/100) * qtdPares)) # ira mutar nenhuma vez ou ate o numero maximo de vezes permitidos de acordo com o coeficiente de mutacao informado
    
    if qtdMutar > 0 :
        for _ in range(qtdMutar):
            indexCromossomo = randint(1,len(populacao)-1)   # escolhe o cromossomo da populacao que sera mutado
            embaralhar(populacao[indexCromossomo][0], int(0.1*qtdPares))    # faz duas inversoes em 10% dos genes do cromossomo por vez aleatoriamente
    
    return populacao

def avaliarPopulacao(populacao, ultimaAlteracao, melhorAptidao, geracao):
    maiorAptidao = 0
    melhorCromossomo = None

    for i in range(len(populacao)):
        aptidaoCalculada = aptidao(populacao[i][0])
        populacao[i][1] = aptidaoCalculada

        if aptidaoCalculada == 1:          # Criterio de parada: Solucao otima
            print(geracao,"\nCriterio de parada: Solucao otima encontrada: \n", toString(populacao[i]))
            return False

        if aptidaoCalculada > maiorAptidao: 
            maiorAptidao = aptidaoCalculada
            melhorCromossomo = populacao[i]

    if  maiorAptidao > melhorAptidao[0]:
        melhorAptidao[0] = maiorAptidao
        ultimaAlteracao[0] = 0
        print(geracao, toString(melhorCromossomo), "Array: ", melhorCromossomo[0])
    else:
        ultimaAlteracao[0] += 1

    populacaoOrdenada = sorted(populacao, key=lambda tup: tup[1], reverse=True)

    if populacao.count(populacaoOrdenada[0]) > 0.95*tamPopulacao:
        print("\nCriterio de parada: Convergencia dos valores maior que 95%\n\nTop 10:") # Criterio de parada: Convergencia
        for i in range(10):  print(toString(populacaoOrdenada[i]), "Array: ", populacaoOrdenada[i][0])  
        return False

    if ultimaAlteracao[0] > 1000:            # Criterio de parada: Muitas iteracoes sem melhora
        print("\nCriterio de parada: Muitas iteracoes sem melhora\n\nTop 10:")
        for i in range(10):  print(toString(populacaoOrdenada[i]), "Array: ", populacaoOrdenada[i][0])    
        return False
        
    return True

def toString(cromossomo):
    output = "[" + str(cromossomo[1]*100) + "%] "
    for index in range(qtdPares): output += "(" + str(index+1) + ", " + str(cromossomo[0][index]) + ") "
    return output

def main():
    file1 = open("escrita.txt", "w")
    geracao = 0
    ultimaAlteracao = [0]                               # Contabiliza a quantas iteracoes nao houve alteracao na melhor aptidao
    melhorAptidao = [0]                                 # Acompanha o valor da aptidao do melhor cromossomo
    populacao = geraPopulacaoInicial()                  # Populacao Inicial
    criterioDeParada = avaliarPopulacao(populacao, ultimaAlteracao, melhorAptidao, geracao)      # Avalia a populacao
    posicao = 1
    file1.writelines(f"Linhagem: {posicao}\n")
    for i in range(len(populacao)):
        file1.writelines(f"{str(populacao[i])}\n")
    posicao += 1
    while criterioDeParada:                             # Criterio de Parada
        geracao += 1
        populacaoIntermediaria = selecao(populacao)     # Selecao
        reproducao(populacao, populacaoIntermediaria)   # Reproducao
        populacao = mutacao(populacaoIntermediaria)     # Mutacao
        criterioDeParada = avaliarPopulacao(populacao, ultimaAlteracao, melhorAptidao, geracao)  # Avalia a populacao
        
        file1.writelines(f"Linhagem: {posicao}\n")
        for i in range(len(populacao)):
            file1.writelines(f"{str(populacao[i])}\n")
        posicao += 1

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Informe o nome do arquivo de entrada, o tamanho da populacao inicial e o coeficiente de mutacao maximo")
        exit()
    else:
        input = open(sys.argv[1])
        tamPopulacao = int(sys.argv[2])
        coefMutacao = float(sys.argv[3])
        print(sys.argv)
        if coefMutacao > 100:
            print("Coeficiente de mutacao deve ser um valor entre 0 e 100")
            exit()

        for linha in input:
            if qtdPares:
                aux = linha.strip().split(" ")
                vet = []
                for i in range(1,qtdPares+1): 
                    vet.append(int(aux[i]))
                ranking.append(vet)
            else:
                qtdPares = int(linha)
                populacaoMaxima = factorial(qtdPares)
                if tamPopulacao > populacaoMaxima: 
                    print("Populacao inicial maior que as possibilidades para o numero de pares")
                    exit()
        input.close()

    main()