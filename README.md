# Projet_-_Langages_de_Script
Projet du cours de Langages de Script (Python) du M1 TAL (Traitement Automatique des Langues)


NGAUV Nicolas (M1 PluriTAL (INaLCO))

COMMENTAIRES, REMARQUES ET DISCUSSIONS SUR LE PROJET





## Le rendu comprend :
- le sujet du projet
- le présent README
- les 2 textes
- le fichier de code
- les différents corpus produits à partir des 2 textes avec le code
- le fichier csv de resultat



## Pour le fichier de code :

J'ai essayé de diviser les différentes tâches en un maximum de fonctions et de commenter, pour avoir un travail clair et propre, c'est pour cela qu'il y a beaucoup de commentaires et de fonctions différentes (qui font parfois des tâches simples).
J'ai également laissé en commentaires des appels à des fonctions et différentes instructions (comme des affichages et des return) pour tester, mieux visualiser si on en a envie.

Le code entier du projet est contenu dans un unique fichier "projet.py".

Pour tester le projet : python3 projet.py
(A exécuter dans l'environnement de travail du cours : tal-ml (avec conda activate tal-ml)
Nécessite peut-être l'installation de certains packages pour pouvoir exécuter le fichier de code)
L'exécution du programme entier prend quelques secondes, merci de patienter jusqu'à la fin.

Toutes les fonctions marchent.



## Pour le fichier csv :

Comme on peut le voir, les résultats sont dans le bon format, et les différents coefficients de corrélation de Spearman des rangs obtenus prouvent bien les assertions sur la similarité entre les corpus constitués, dégagées par la méthode Known-Similarity Corpora (KSC), à quelques détails près.

En effet, certaines stratégies dans la réalisation de nos tâches amènent à des imprécisions et font que certains résultats à quelques centièmes, millièmes ou encore moins parfois, changent l'ordre auquel on peut s'attendre dans la comparaison des similarités de certains corpus avec d'autres :
- le découpage en pourcentage des 2 textes pour former les différents corpus
- la considération des majuscules et minuscules dans les mots-formes
- la prise en compte des mots-forme ne rend pas compte du contexte

Le découpage selon les pourcentage des 2 textes pour former les corpus n'a pas utilisé le mot pour unité, mais le byte (ou caractère ici).
En effet, ici on parle d'un texte en tant que document à part entière : donc un corpus composé de 80% du premier texte et de 20% du second est LITTÉRALEMENT composé de 80% du premier et de 20% du second.
Ainsi on comprend aisément que le dernier mot du premier texte ainsi que le dernier mot du dernier texte, utilisés pour former le corpus, puisse être tronqués (pas écrit en entier dans le corpus) si on atteint les 80% ou les 20% au milieu d'un mot...
Le mot étant mal coupé, son mot-forme ne sera pas le même que le mot en entier et donc influencera la valeur de la fréquence du mot-forme du mot entier du corpus, et donc possiblement le rang du mot-forme et au final la valeur du coefficient de corrélation de Spearman des rangs.

Pour ce projet, on a utilisé le concept de mot-forme.
Je suis parti du principe qu'un mot écrit en majuscule et ce même mot écrit en minuscule n'ont pas le même mot-forme, puisque leur représentation graphique était différente. C'est un choix.
Mais on aurait très bien pu partir du principe qu'un mot écrit en majuscule et en minuscule avait le même mot-forme, puisque composés des mêmes lettres et dans le même ordre...
J'ai testé cela : j'ai ajouté une instruction(ligne 65 à 67) dans le code, pour tester (passage en bas de casse, que j'ai mis en commentaire mais que vous pouvez décommenter pour tester !) et effectivement, les valeurs finales des coefficients de corrélation ne sont pas les mêmes : elles se rapprochent plus de ce qui était attendu.

La prise en compte des mots-formes et leur utilisation dans le calcul du coefficient de corrélation de Spearman ne prend pas en compte le contexte (ce qu'il y a à gauche et à droite de chaque mot, et plus généralement même l'ordre des mots dans le texte) dans l'appréciation de la similarité entre 2 corpus.
En effet, si deux corpus ont exactement les mêmes mots-formes avec les mêmes fréquences, alors ces deux corpus auront les mêmes rangs pour les mêmes mots-formes, et d'après la formule de calcul du coefficient de corrélation donnée dans le sujet, il sera égal à 1.
Similarité parfaite ? Eh bien oui et non, si on prend le contexte en compte :
- ces 2 corpus peuvent être exactement les mêmes (et donc on peut considérer qu'ils ont une similarité parfaite) si tous les mots sont écrits dans le même ordre dans ces deux corpus (c'est-à-dire même contexte);
- mais ils peuvent être très différents si les mots sont écrits dans des ordres complètement différents dans ces deux corpus (contextes différents).
Pourtant, dans ces deux cas-là, on aurait eu le même coefficient de corrélation, et ce coefficient aurait en théorie la valeur maximale (1).
