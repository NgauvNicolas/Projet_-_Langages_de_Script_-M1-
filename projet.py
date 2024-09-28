#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created By  : NGAUV Nicolas (M1 PluriTAL (INaLCO) 22301604)


import csv
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict, defaultdict
import pandas as pd
from scipy.stats import spearmanr






# Pour créer tous les corpus à partir de 2 textes selon les pourcentages données (contenus dans la liste pourcentages)
# Composition des différents corpus : (pourcentage_1er_texte + pourcentage_2ème_texte)
# (100% + 0%) ; (90% + 10%) ; (80% + 20%) ; (70% + 30%) ; (60% + 40%) ; 
# (50% + 50%) ; (40% + 60%) ; (30% + 70%) ; (20% + 80%) ; (90% + 10%) ; (0% + 100%)
def creation_corpus(texte1, texte2, pourcentages):
    corpus = []
    with open(texte1, 'r', encoding='utf-8') as t1, open(texte2, 'r', encoding='utf-8') as t2:
        texte_t1 = t1.read()
        texte_t2 = t2.read()
        lengths = [len(texte_t1), len(texte_t2)]
    
        for i, pourcentage in enumerate(pourcentages):
            corpus_texte1 = int(lengths[0] * pourcentage)
            corpus_texte2 = int(lengths[1] * (1 - pourcentage))

            # Si le corpus ne contient que l'un des deux textes (donc le premier et le dernier corpus produits)
            if corpus_texte1==0 or corpus_texte2==0:
                corpus.append(texte_t1[:corpus_texte1] + texte_t2[:corpus_texte2])
            else:
            # Sinon le "\n\n\n\n\n" pour que le dernier caractère capté du 1er texte ne soit pas collé au premier caractère du 2nd, afin que dans le corpus ils forment bien 2 mots distincts
                corpus.append(texte_t1[:corpus_texte1] + "\n\n\n\n\n" + texte_t2[:corpus_texte2])

            # Enregistrer chaque corpus dans un fichier texte
            nom_fichier = f"corpus_{i+1}.txt"
            with open(nom_fichier, "w+", encoding="utf-8") as fichier:
                fichier.write(corpus[-1])
            print(f"Corpus {i+1} enregistré dans {nom_fichier}")
        





# Pour obtenir les 500 mots-formes les plus fréquents des 2 textes
def motsFormes(texte1, texte2):
    corpus = ""
    global mots_formes
    mots_formes = []
    with open(texte1, 'r', encoding='utf-8') as t1, open(texte2, 'r', encoding='utf-8') as t2:
        texte_t1 = t1.read()
        texte_t2 = t2.read()

        #On veut les mots-formes les plus fréquents des 2 textes
        corpus = texte_t1 + "\n\n\n\n\n" + texte_t2

        # On considère qu'un mots en majuscule ou minuscule n'a pas le même mot-forme, puisque la représentation graphique diffère
        # Donc pas de passage des mots en bas de casse avec 
        #corpus = corpus.lower()
        # En incluant les contractions de l'anglais, on découpe en une liste de mots
        tokenizer = RegexpTokenizer("[\w']+")
        mots = tokenizer.tokenize(corpus)

        # On veut la distribution des fréquences pour tous les mots-formes
        mf = nltk.FreqDist(mots)

        # On veut garder seulement les 500 mots-formes les plus fréquents, mais on va mettre 501 car on va devoir enlever un élément de la liste
        # On obtient une liste de tuples ('mots-forme', fréquence) triée par ordre de fréquence
        liste_mots_formes = mf.most_common(501)

        # On va stocker ces mots dans une liste qui nous servira de référence pour les mots-formes des corpus
        for x in liste_mots_formes:
            mots_formes.append(x[0])
            #print(x[0])

        # Renvoie l'indice de l'élément "'" (apostrophe pour contraction de l'anglais) : 
        # pour vérifier si en voulant prendre en compte 'apostrophe pour la contraction en anglais, on a aussi gardé l'apostrophe seule... 
        # C'est le cas apparement... On obtient la position de l'élément "'" : indice 241 donc l'élément existe bel et bien dans la liste
        #print(mots_formes.index("'"))
        #print(len(mots_formes))
        # Donc on corrige en supprimant l'élément de la liste, du coup la longueur diminue de 1 et on passe de 501 à 500
        mots_formes.remove("'")
        #print(len(mots_formes))
        #print(mots_formes)





# Renvoie la liste des fréquences des mots de mots_formes trouvés dans le corpus
def freq_corpus(corpus, mots_formes):
    freq_corp =[]
    with open(corpus, 'r', encoding='utf-8') as t1:
        texte_t1 = t1.read()
        tokenizer = RegexpTokenizer("[\w']+")
        mots = tokenizer.tokenize(texte_t1)
        for x in mots_formes:
            a = mots.count(x)
            freq_corp.append(a)
    return freq_corp



# Etablit le rang de chaque mots-formes à partir de sa fréquence et de celle des autres 
# pour un corpus donné et pour les mots-formes de mots_formes 
def rang_corpus(corpus, mots_formes):
    freq_corp = freq_corpus(corpus, mots_formes)
    #print(freq_corp)

    # Créez des dictionnaires ordonnés pour le corpus avec les mots-formes comme clés
    dico_corpus = OrderedDict(zip(mots_formes, freq_corp))
    #print(dico_corpus)
    #print(mots_formes)

    # Trie en fonction de la valeur dans l'ordre décroissant
    dic_corp = sorted(dico_corpus.items(), key=lambda x: x[1], reverse=True)
    #print(dic_corp)
 
    # Crée le nouveau dictionnaire avec les rangs
    rang_corp = OrderedDict()

    # Initialise une variable pour suivre la valeur précédente
    precedente_valeur = None

    # Parcoure les données triées
    for rang, (mot, valeur) in enumerate(dic_corp, 1):
        # Si la valeur est égale à la précédente, utilise le même rang : pour faire en sorte que dans un corpus, des mots-formes qui ont la même fréquence ont le même rang
        if valeur == precedente_valeur:
            rang_corp[mot] = precedent_rang
        else:
            rang_corp[mot] = rang
            precedent_rang = rang
            precedente_valeur = valeur

    l = list(rang_corp.items())
    #print(l)
    #print(rang_corp)
    return l





# Pour ordonner une liste de tuples selon l'ordre lexicographique de chaque premier élément de chaque tuple
def ordre(liste_tuples):
    l_ordonnee = sorted(liste_tuples, key=lambda x: x[0])
    return l_ordonnee


# Compréhension de liste pour créer une nouvelle liste en ne conservant que le deuxième élément de chaque tuple d'une liste de tuples
def supprime_elt(liste_tuples):
    l = [x[1] for x in liste_tuples]
    return l

# Pour nettoyer et avoir une liste de liste de rangs de corpus que l'on pourra utiliser dans un DataFrame pour calculer le coefficient de corrélation de Spearman des rangs
def menage(liste_tuples, l_rang_corpus):
    a = ordre(liste_tuples)
    b = supprime_elt(a)
    l_rang_corpus.append(b)
    return b





# Calcul du coefficient de corrélation de Spearman à partir de 2 listes de rang de corpus propres (cf. la fonction menage(liste_tuples))
def corr_sm(liste1, liste2):
    series = {
        "texte1": liste1,
        "texte2": liste2
    }

    df = pd.DataFrame(series)
    # Pour visualiser
    #df

    #calcule le coefficient de corrélation de Spearman et la valeur p correspondante
    rho, p = spearmanr(df['texte1'], df['texte2'])
    #print(rho)
    #print(p)
    return rho





# Crée le fichier csv avec les résultats demandés
def csv_corpus(resultat_textfile, l_rang_corpus):
    with open(resultat_textfile, "w+") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for x in l_rang_corpus:
            for y in l_rang_corpus:
                if x != y:
                    a = corr_sm(x, y)
                    # indice ou position de x; indice ou position de y; coefficient de corrélation de Spearman
                    writer.writerow([l_rang_corpus.index(x), l_rang_corpus.index(y), a])
    print(f"Numéros des corpus (numérotés à partir de 0) et coefficients de corrélation de Spearman enregistrés dans {resultat_textfile}")





def main():

    pourcentages = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    creation_corpus("dracula.txt", "frankenstein.txt", pourcentages)
    motsFormes("dracula.txt", "frankenstein.txt")

    # Liste qui va contenir toutes les listes de rangs des corpus et qui va un peu plus se remplir à chaque appel de la fonction menage(liste_tuples, l_rang_corpus)
    l = []

    rang_corp1 = rang_corpus("corpus_1.txt", mots_formes)
    rang_corp1_clean = menage(rang_corp1, l)
    #print(rang_corp1_clean)
    #print(l[0])

    rang_corp2 = rang_corpus("corpus_2.txt", mots_formes)
    rang_corp2_clean = menage(rang_corp2, l)
    #print(rang_corp2_clean)
    #print(l[1])

    rang_corp3 = rang_corpus("corpus_3.txt", mots_formes)
    rang_corp3_clean = menage(rang_corp3, l)
    #print(rang_corp3_clean)
    #print(l[2])

    rang_corp4 = rang_corpus("corpus_4.txt", mots_formes)
    rang_corp4_clean = menage(rang_corp4, l)
    #print(rang_corp4_clean)
    #print(l[3])

    rang_corp5 = rang_corpus("corpus_5.txt", mots_formes)
    rang_corp5_clean = menage(rang_corp5, l)
    #print(rang_corp5_clean)
    #print(l[4])

    rang_corp6 = rang_corpus("corpus_6.txt", mots_formes)
    rang_corp6_clean = menage(rang_corp6, l)
    #print(rang_corp6_clean)
    #print(l[5])

    rang_corp7 = rang_corpus("corpus_7.txt", mots_formes)
    rang_corp7_clean = menage(rang_corp7, l)
    #print(rang_corp7_clean)
    #print(l[6])

    rang_corp8 = rang_corpus("corpus_8.txt", mots_formes)
    rang_corp8_clean = menage(rang_corp8, l)
    #print(rang_corp8_clean)
    #print(l[7])

    rang_corp9 = rang_corpus("corpus_9.txt", mots_formes)
    rang_corp9_clean = menage(rang_corp9, l)
    #print(rang_corp9_clean)
    #print(l[8])

    rang_corp10 = rang_corpus("corpus_10.txt", mots_formes)
    rang_corp10_clean = menage(rang_corp10, l)
    #print(rang_corp10_clean)
    #print(l[9])

    rang_corp11 = rang_corpus("corpus_11.txt", mots_formes)
    rang_corp11_clean = menage(rang_corp11, l)
    #print(rang_corp11_clean)
    #print(l[10])


    # Pour tester et visualiser : affiche les coefficients de corrélation correspondants sur le terminal
    #corr_sm(rang_corp1_clean, rang_corp2_clean)
    #corr_sm(rang_corp1_clean, rang_corp3_clean)
    #corr_sm(rang_corp2_clean, rang_corp3_clean)


    # Création du fichier csv
    csv_corpus("resultat.csv", l)

    



if __name__ == "__main__":
    main()


