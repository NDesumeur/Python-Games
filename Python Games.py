import random
from random import randint, choice, sample
import time
import pygame
import pygame.mixer


###############################################################################################################################################################################################################################
def creer_grille():
    return [['O' for i in range(10)] for i in range(10)]


def afficher_grille(grille):
    print("    |A|B|C|D|E|F|G|H|I|J|")

    for i, ligne in enumerate(grille):
        if i + 1 != 10:
            print(" | " + f"{i + 1}" + "|" + f"{' '.join(ligne)}" + "|")
        elif i + 1 == 10:
            print(" |" + f"{i + 1}" + "|" + f"{' '.join(ligne)}" + "|")
    print("=========================")


def verifier_victoire(grille1, grille2):
    N = 0
    T = 0
    for ligne in range(len(grille1)):
        for case in range(len(grille1[ligne])):
            if grille1[ligne][case] == "N":
                N = N + 1
            if grille2[ligne][case] == "T":
                T = T + 1
    if T == N:
        return True
    return False


def case_occupee(grille, row, col):
    return case_valide(row, col) and grille[row][col] != 'O'


def case_valide(row, col):
    return 0 <= row < 10 and 0 <= col < 10


def cases_valides_disponibles(grille, cases):
    for row, col in cases:
        if not case_valide(row, col) or case_occupee(grille, row, col):
            return False
    return True


def verifier_coule(grille, coordonnees_bateau):
    for coord in coordonnees_bateau:
        row, col = coord
        if grille[row][col] != 'T':
            return False
    return True


def placer_navires(grille, navires):
    coordonnees_navires = {}
    for navire, taille in navires.items():
        if taille == 1:
            print(f"\nPlacement du {navire} ({taille} case)")
            afficher_grille(grille)

            print(f"Entrez les coordonnées de la case occupée par le {navire}.")
            print("Les coordonnées doivent être au format colonne + ligne (par exemple, A1).")
            print("Les colonnes sont représentées par des lettres de A à J, et les lignes par des chiffres de 1 à 10.")

            while True:
                coord = input(f"Coordonnées de la case du {navire} : ")
                try:
                    col = ord(coord[0].upper()) - ord('A')
                    row = int(coord[1:]) - 1
                    if not case_valide(row, col):
                        print("Coordonnées hors de la grille !")
                        continue
                    if case_occupee(grille, row, col):
                        print("Emplacement déjà occupé !")
                        continue
                    grille[row][col] = 'N'
                    coordonnees_navires[navire] = [(row, col)]
                    break
                except (IndexError, ValueError):
                    print("Coordonnées invalides !")

        else:
            print(f"\nPlacement du {navire} ({taille} cases)")
            afficher_grille(grille)

            while True:
                print(f"Entrez les coordonnées de la première case et la dernière case occupées par le {navire}.")
                print("Les coordonnées doivent être au format colonne + ligne (par exemple, A1).")
                print(
                    "Les colonnes sont représentées par des lettres de A à J, et les lignes par des chiffres de 1 à 10.")

                while True:
                    try:
                        coord1 = input(f"Coordonnées de la première case du {navire} : ")
                        col1 = ord(coord1[0].upper()) - ord('A')
                        row1 = int(coord1[1:]) - 1
                        if not case_valide(row1, col1):
                            print("Coordonnées hors de la grille !")
                            continue
                        break
                    except (IndexError, ValueError):
                        print("Coordonnées invalides !")

                while True:
                    try:
                        coord2 = input(f"Coordonnées de la dernière case du {navire} : ")
                        col2 = ord(coord2[0].upper()) - ord('A')
                        row2 = int(coord2[1:]) - 1
                        if not case_valide(row2, col2):
                            print("Coordonnées hors de la grille !")
                            continue
                        break
                    except (IndexError, ValueError):
                        print("Coordonnées invalides !")

                if row1 == row2:
                    if col1 < col2:
                        cases = [(row1, col) for col in range(col1, col2 + 1)]
                    else:
                        cases = [(row1, col) for col in range(col2, col1 + 1)]
                elif col1 == col2:
                    if row1 < row2:
                        cases = [(row, col1) for row in range(row1, row2 + 1)]
                    else:
                        cases = [(row, col1) for row in range(row2, row1 + 1)]
                else:
                    print("Coordonnées invalides !")
                    continue

                if len(cases) != taille:
                    print("Nombre de cases incorrect !")
                    continue

                if not cases_valides_disponibles(grille, cases):
                    print("Emplacement déjà occupé ou invalide !")
                    continue

                for row, col in cases:
                    grille[row][col] = 'N'
                coordonnees_navires[navire] = cases
                break

        afficher_grille(grille)
    return coordonnees_navires


def bataille_navale():
    print("=== Bataille Navale ===")
    print("1. Jouer")
    print("2. Description du jeu")

    ch = input("Choisissez une option (1-2) : ")

    if ch == '2':
        print("\nLa Bataille Navale est un jeu de stratégie classique pour deux joueurs.")
        print("\nLe but du jeu est de localiser et de couler tous les navires de l'adversaire.")
        print("\nLes joueurs placent leurs navires sur leur grille de jeu en choisissant les positions.")
        print("\nLes navires peuvent être placés horizontalement ou verticalement, sans se chevaucher.")
        print("\nLes joueurs s'alternent pour attaquer les positions sur la grille de l'adversaire.")
        print("\nUne attaque réussie est un 'touché', et un navire entièrement touché est 'coulé'.")
        print("\nLorsqu'un joueur touche un navire adverse il peut rejouer.")
        print("\nLe premier joueur à couler tous les navires adverses remporte la partie.\n\n\n")
        return bataille_navale()

    grille_joueur1 = creer_grille()
    grille_joueur2 = creer_grille()
    grille_joueur1_cachee = creer_grille()
    grille_joueur2_cachee = creer_grille()

    joueur1 = input("Entrez le nom du joueur 1: ")
    joueur2 = input("Entrez le nom du joueur 2: ")
    print("Bon match " + joueur1 + " et " + joueur2 + ' ! ')
    print('\n \nVeuillez choisir les navires : ')
    print("composition 1 : un navire de 5 cases, un de 4 cases, deux de 3 cases et un de 2 cases.")
    print(
        "composition 2 : un navire de 4 cases, deux navires de 3 cases, trois navires de 2 cases, quatre navires de 1 cases.")
    choix = 0
    while choix != 1 and choix != 2:
        choix = int(input("Choissisez une composition pour jouer (1-2) : "))
    if choix == 1:
        navires = {'Porte-avions': 5, 'Croiseur': 4, 'Contre-torpilleur 1': 3, 'Contre-torpilleur 2': 3,
                   'Torpilleur': 2}
    else:
        navires = {'Cuirassé': 4, 'Croiseur 1': 3, 'Croisseur 2': 3, "Torpilleur 1": 2, 'Torpilleur 2': 2,
                   "Torpilleur 3": 2, 'Sous-marin 1': 1, 'Sous-marin 2': 1, 'Sous-marin 3': 1, 'Sous-marin 4': 1}
    for i in range(1000):
        print('\n')
    print(f"{joueur1}, placez vos navires :")
    navires_joueur1 = placer_navires(grille_joueur1, navires)
    print("On passe des lignes.")
    for i in range(1000):
        print("\n")
    input(f"Appuyez sur Entrée pour passer au tour de {joueur2}")

    print(f"{joueur2}, placez vos navires :")
    navires_joueur2 = placer_navires(grille_joueur2, navires)
    print("On passe des lignes.")
    for i in range(1000):
        print("\n")
    joueur_actuel = joueur1
    adversaire = joueur2
    joueur_actuel_grille = grille_joueur2_cachee
    adversaire_grille = grille_joueur2
    navires_adversaire = navires_joueur2
    win = False

    while not win:
        pas_touche = 0
        while pas_touche == 0 or not win:
            for i in range(30):
                print("\n")
            print(f"\n   ===== tour de {joueur_actuel}  =====")
            afficher_grille(joueur_actuel_grille)
            coord = input("Entrez les coordonnées pour tirer : ")
            try:
                col = ord(coord[0].upper()) - ord('A')
                row = int(coord[1:]) - 1

                if not case_valide(row, col):
                    print("Coordonnées hors de la grille !")

                if case_occupee(adversaire_grille, row, col) and joueur_actuel_grille[row][col] != 'T':
                    print("Touché !")
                    joueur_actuel_grille[row][col] = 'T'
                    for nav in navires.keys():
                        print('a')
                        if verifier_coule(joueur_actuel_grille, navires_adversaire[nav]):
                            print(f"Le navire {nav}({navires[nav]} cases) de {adversaire} a été coulé !")
                    if verifier_victoire(adversaire_grille, joueur_actuel_grille):
                        print(f"{joueur_actuel} a coulé tous les navires. Victoire du {joueur_actuel}!")
                        win = True
                        return "Fin du jeu !"

                elif not case_occupee(adversaire_grille, row, col) and case_valide(row, col):
                    print("Dans l'eau !")
                    joueur_actuel_grille[row][col] = 'X'
                    pas_touche = 1
                    joueur_actuel, adversaire = adversaire, joueur_actuel
                    if joueur_actuel == f"{joueur1}":
                        joueur_actuel_grille = grille_joueur2_cachee
                        adversaire_grille = grille_joueur2
                        navires_adversaire = navires_joueur2
                    elif joueur_actuel == f"{joueur2}":
                        joueur_actuel_grille = grille_joueur1_cachee
                        adversaire_grille = grille_joueur1
                        navires_adversaire = navires_joueur1
            except (IndexError, ValueError):
                print("Coordonnées invalides !")


#################################################################################################################################################################################################################################


def afficher_grille_taquin(grille):
    taille = len(grille)
    separateur = "+{}+".format("-" * (5 * taille))

    print(separateur)
    for ligne in grille:
        ligne_grille = "|"
        for case in ligne:
            if case == taille ** 2:
                ligne_grille += "    |"
            else:
                ligne_grille += " {:2d} |".format(case)
        print(ligne_grille)
        print(separateur)


def grille_resolue_taquin(grille):
    taille = len(grille)
    numero_case = 1
    for i in range(taille):
        for j in range(taille):
            if i == taille - 1 and j == taille - 1:
                if grille[i][j] != taille ** 2:
                    return False
            elif grille[i][j] != numero_case:
                return False
            numero_case += 1
    return True


def echanger_cases_taquin(grille, case1, case2):
    taille = len(grille)
    for i in range(taille):
        for j in range(taille):
            if grille[i][j] == case1:
                grille[i][j] = case2
            elif grille[i][j] == case2:
                grille[i][j] = case1
    return grille


def melanger_grille_taquin(grille):
    taille = len(grille)
    case_vide = taille ** 2

    nb_mouvements = random.randint(taille ** 2 * 5, taille ** 2 * 10)

    for _ in range(nb_mouvements):
        cases_valides = []
        i, j = None, None
        for k in range(taille):
            for l in range(taille):
                if grille[k][l] == case_vide:
                    i, j = k, l
                cases_valides.append((k, l))
        mouvement = random.choice([(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)])
        if mouvement in cases_valides:
            grille = echanger_cases_taquin(grille, grille[i][j], grille[mouvement[0]][mouvement[1]])
    return grille


def jouer_taquin():
    taille = 0
    while True:
        try:
            taille = int(input("Entrez la taille du jeu Taquin (par exemple, 3 pour un jeu 3x3) : "))
            if taille < 3 or taille >= 10:
                print("La taille de la grille doit être supérieure ou égale à 3 et inférieure à 10.")
            else:
                break
        except ValueError:
            print("Veuillez entrer un nombre entier.")

    grille = [[i + j * taille + 1 for i in range(taille)] for j in range(taille)]
    grille[taille - 1][taille - 1] = taille ** 2
    grille = melanger_grille_taquin(grille)

    largeur_case = len(str(taille ** 2))

    while not grille_resolue_taquin(grille):
        afficher_grille_taquin(grille)

        case_vide = taille ** 2
        mouvement = input("Entrez le numéro de la case à déplacer (1 à {}): ".format(taille ** 2 - 1))

        try:
            case = int(mouvement)
            if case < 1 or case > taille ** 2 or case == case_vide:
                print("Mouvement invalide !")
                continue
        except ValueError:
            print("Veuillez entrer un nombre entier.")
            continue

        i, j = None, None
        for k in range(taille):
            for l in range(taille):
                if grille[k][l] == case:
                    i, j = k, l
                    break
            if i is not None:
                break

        cases_voisines = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        case_vide = None
        for voisin in cases_voisines:
            if 0 <= voisin[0] < taille and 0 <= voisin[1] < taille and grille[voisin[0]][voisin[1]] == taille ** 2:
                case_vide = voisin
                break

        if case_vide is None:
            print("Mouvement invalide !")
            continue

        grille = echanger_cases_taquin(grille, grille[i][j], grille[case_vide[0]][case_vide[1]])
        for i in range(100):
            print("\n")

    print("Félicitations ! Vous avez résolu le jeu Taquin !")


def afficher_description_taquin():
    description = """
    Le Taquin est un jeu de puzzle dans lequel le joueur doit réorganiser des nombres ou des images mélangés sur une grille afin de les remettre dans un ordre numérique ou logique spécifique.

    Le jeu se joue sur une grille de taille variable. La grille est remplie de cases numérotées ou avec des images, sauf une case qui est vide. Le but du jeu est de déplacer les cases adjacents à la case vide pour réorganiser les numéros ou les images et les replacer dans l'ordre souhaité.

    Pour jouer au Taquin, vous devez entrer la taille de la grille (par exemple, 3 pour un jeu 3x3). Vous serez ensuite invité à entrer le numéro de la case que vous souhaitez déplacer. Les cases adjacentes à la case vide peuvent être déplacées en entrant leur numéro correspondant.

    Le jeu continue jusqu'à ce que vous réussissiez à réorganiser les numéros ou les images dans l'ordre correct. Une fois que vous avez terminé, vous recevrez un message de félicitations.

    Amusez-vous bien !
    """

    print(description)


def jeu_taquin():
    c = 0
    while c == 0:
        print("=== Bienvenue au Taquin ! ===")
        choix = input("Choisissez une option :\n1. Jouer au Taquin\n2. Description du jeu\n\n> ")
        if choix == "1":
            c = 1
            for i in range(100):
                print("\n")
            jouer_taquin()
        elif choix == "2":
            print("\n\n\n\n\n\n\n\n")
            afficher_description_taquin()
        else:
            print("Option invalide. Veuillez choisir une option valide.")


#################################################################################################################################################################################################################################

def initialiser_grille_2048():
    grille = [[0] * 4 for _ in range(4)]
    ajouter_case_2048(grille)
    ajouter_case_2048(grille)
    return grille


def afficher_grille_2048(grille):
    print("-----------------------------")
    for ligne in grille:
        print("|", end=" ")
        for case in ligne:
            if case != 0:
                print(f"{case:4}", end=" |")
            else:
                print("    ", end=" |")
        print("\n-----------------------------")


def ajouter_case_2048(grille):
    cases_libres = []
    for i in range(4):
        for j in range(4):
            if grille[i][j] == 0:
                cases_libres.append((i, j))
    if cases_libres:
        i, j = random.choice(cases_libres)
        grille[i][j] = random.choice([2, 4])


def deplacer_gauche_2048(grille):
    nouvelle_grille = [ligne.copy() for ligne in grille]
    for i in range(4):
        nouvelle_ligne = []
        for j in range(4):
            if nouvelle_grille[i][j] != 0:
                nouvelle_ligne.append(nouvelle_grille[i][j])
        nouvelle_ligne += [0] * (4 - len(nouvelle_ligne))

        for j in range(3):
            if nouvelle_ligne[j] == nouvelle_ligne[j + 1]:
                nouvelle_ligne[j] *= 2
                nouvelle_ligne[j + 1] = 0

        nouvelle_grille[i] = nouvelle_ligne

    return nouvelle_grille


def deplacer_droite_2048(grille):
    nouvelle_grille = [ligne[::-1] for ligne in grille]
    nouvelle_grille = deplacer_gauche_2048(nouvelle_grille)
    nouvelle_grille = [ligne[::-1] for ligne in nouvelle_grille]
    return nouvelle_grille


def deplacer_haut_2048(grille):
    nouvelle_grille = [list(colonne) for colonne in zip(*grille)]
    nouvelle_grille = deplacer_gauche_2048(nouvelle_grille)
    nouvelle_grille = [list(colonne) for colonne in zip(*nouvelle_grille)]
    return nouvelle_grille


def deplacer_bas_2048(grille):
    nouvelle_grille = [list(colonne) for colonne in zip(*grille)]
    nouvelle_grille = deplacer_droite_2048(nouvelle_grille)
    nouvelle_grille = [list(colonne) for colonne in zip(*nouvelle_grille)]
    return nouvelle_grille


def jeu_termine_2048(grille):
    for i in range(4):
        for j in range(4):
            if grille[i][j] == 2048:
                return True
            if grille[i][j] == 0:
                return False
            if j < 3 and grille[i][j] == grille[i][j + 1]:
                return False
            if i < 3 and grille[i][j] == grille[i + 1][j]:
                return False
    return True


def calculer_score_2048(grille):
    return max(max(ligne) for ligne in grille)


def jouer_2048():
    grille = initialiser_grille_2048()
    score = 0
    while True:
        print("Score:", score)
        afficher_grille_2048(grille)
        if jeu_termine_2048(grille) or score == 2048:
            print("Jeu terminé !")
            break
        print("\n\n\n\n")
        direction = input("Utilisez les touches 'z' pour haut , 's' pour bas , 'q' pour gauche, 'd' pour droite : ")
        if direction.lower() == 'z':
            grille = deplacer_haut_2048(grille)
        elif direction.lower() == 'q':
            grille = deplacer_gauche_2048(grille)
        elif direction.lower() == 's':
            grille = deplacer_bas_2048(grille)
        elif direction.lower() == 'd':
            grille = deplacer_droite_2048(grille)
        else:
            for i in range(100):
                print("\n")
            print("Vous devez entrer une direction valide !")
            continue
        for i in range(100):
            print("\n")
        ajouter_case_2048(grille)
        score = calculer_score_2048(grille)


def afficher_description_2048():
    description = """
    Le jeu 2048 est un jeu de puzzle dans lequel vous combinez des nombres pour atteindre le nombre 2048.
    Les règles du jeu sont simples :
    - Utilisez les touches 'z', 's', 'q', 'd' pour déplacer les cases vers le haut, le bas, la gauche ou la droite.
    - Chaque déplacement fusionne les cases de même valeur en une seule case contenant la somme des deux cases d'origine.
    - Après chaque déplacement, une nouvelle case contenant un 2 ou un 4 apparaît de manière aléatoire.
    - L'objectif est d'obtenir une case contenant la valeur 2048.
    - Le jeu se termine lorsque vous atteignez une case de valeur 2048 ou lorsque vous ne pouvez plus faire de mouvement.

    Bonne chance et amusez-vous bien !
    """
    print(description)


def jouer_2048_final():
    while True:
        print("=== Bienvenue au jeu 2048 ! ===")
        print("\n")
        print("Choisissez une option : (1) Jouer | (2) Description du jeu | (q) Quitter\n")
        choix = input("> ")
        if choix == '1':
            for i in range(100):
                print("\n")
            jouer_2048()
        elif choix == '2':
            print("\n\n\n\n")
            afficher_description_2048()
            input("Appuyez sur Entrée")
        elif choix.lower() == 'q':
            print("Au revoir !")
            break
        else:
            print("Veuillez choisir une option valide !")


#################################################################################################################################################################################################################################

def Jeu_des_allumettes():
    end = False
    allumettes = randint(15, 35)
    joueur1 = input("Entrez le nom du joueur 1: ")
    joueur2 = input("Entrez le nom du joueur 2: ")
    print("\n\n")
    joueurs = [joueur1, joueur2]
    joueur = choice(joueurs)
    joueurs.remove(joueur)
    joueur_adverse = joueurs[0]
    print(f"Le joueur qui commence est: {joueur} ! ")

    while not end:
        print("\n\n\n")
        print(f"=== Tour de {joueur} ===")
        print(f"Il reste {allumettes} allumettes !")

        nombre = 0
        while nombre == 0:
            try:
                nbr = int(input("Veuillez choisir entre 1, 2 ou 3 allumettes à enlever : "))
                if nbr in [1, 2, 3]:
                    if allumettes < nbr:
                        print(f"Vous ne pouvez pas enlever {nbr} allumettes, il n'en reste que {allumettes} !")
                    else:
                        allumettes -= nbr
                        print(f"Le joueur {joueur} a enlevé {nbr} allumettes !")

                        if allumettes == 0:
                            for i in range(5):
                                print("\n")
                            print(f"{joueur} a enlevé la dernière allumette...")
                            print(f"{joueur} a perdu et {joueur_adverse} a gagné !")
                            end = True

                        joueur, joueur_adverse = joueur_adverse, joueur
                        nombre = 1
                else:
                    print("Veuillez entrer un nombre entre 1 et 3.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")


def lancer_jeu_des_allumettes():
    try:
        print("===Jeu des allumettes===")
        print("1. Jouer")
        print("2. Description du jeu")
        ch = int(input("Choisissez une option (1-2) : "))
        if ch == 1:
            Jeu_des_allumettes()
        elif ch == 2:
            print("Le jeu des allumettes est un jeu simple et divertissant pour deux joueurs.")
            print("Au début du jeu, un nombre aléatoire (entre 15 et 35) d'allumettes est placé sur la table.")
            print("Les joueurs se relaient pour enlever 1, 2 ou 3 allumettes à chaque tour.")
            print("Le joueur qui enlève la dernière allumette perd la partie.")
            print("Le joueur qui commence est choisi au hasard.")
            print("Le jeu se poursuit jusqu'à ce qu'un joueur enlève la dernière allumette.")
            lancer_jeu_des_allumettes()
        else:
            lancer_jeu_des_allumettes()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


################################################################################################################################################################################################################################


def Jeu_des_allumettesIA():
    end = False
    allumettes = randint(15, 35)
    joueur1 = input("Entrez le nom du joueur : ")
    joueur2 = "IA"
    print("\n\n")
    joueurs = [joueur1, joueur2]
    joueur = choice(joueurs)
    joueurs.remove(joueur)
    joueur_adverse = joueurs[0]
    print(f"Le joueur qui commence est: {joueur} ! ")

    def choisir_coup_Allumettes_IA():
        if allumettes == 1:
            return 1
        elif allumettes <= 4:
            return allumettes - 1
        elif allumettes % 4 == 0:
            return randint(1, 3)
        else:
            return allumettes % 4

    while not end:
        print("\n\n\n")
        print(f"=== Tour de {joueur} ===")
        print(f"Il reste {allumettes} allumettes !")

        if joueur == "IA":
            nombre = choisir_coup_Allumettes_IA()
            print(f"L'IA a enlevé {nombre} allumettes !")
        else:
            nombre = 0
            while nombre == 0:
                try:
                    nbr = int(input("Veuillez choisir entre 1, 2 ou 3 allumettes à enlever : "))
                    if nbr in [1, 2, 3]:
                        if allumettes < nbr:
                            print(f"Vous ne pouvez pas enlever {nbr} allumettes, il n'en reste que {allumettes} !")
                        else:
                            nombre = nbr
                            print(f"Le joueur {joueur} a enlevé {nombre} allumettes !")
                    else:
                        print("Veuillez entrer un nombre entre 1 et 3.")
                except ValueError:
                    print("Veuillez entrer un nombre valide.")

        allumettes -= nombre

        if allumettes == 0:
            for i in range(5):
                print("\n")
            print(f"{joueur} a enlevé la dernière allumette...")
            print(f"{joueur} a perdu et {joueur_adverse} a gagné !")
            end = True

        joueur, joueur_adverse = joueur_adverse, joueur

    return joueur_adverse


def lancer_jeu_des_allumettesIA():
    try:
        print("=== Jeu des allumettes ===")
        print("1. Jouer")
        print("2. Description du jeu")
        ch = int(input("Choisissez une option (1-2) : "))
        if ch == 1:
            joueur_gagnant = Jeu_des_allumettesIA()
            print(f"\nLe joueur {joueur_gagnant} a gagné la partie !")
            relance = False
            while not relance:
                rejouer = input("Voulez-vous rejouer ? (Oui/Non) : ")
                if rejouer.lower() == "oui":
                    relance = True
                    Jeu_des_allumettesIA()
                elif rejouer.lower() == "non":
                    relance = True
                    print("Merci d'avoir joué !")
        elif ch == 2:
            print("Le jeu des allumettes est un jeu simple et divertissant pour deux joueurs.")
            print("Au début du jeu, un nombre aléatoire (entre 15 et 35) d'allumettes est placé sur la table.")
            print("Les joueurs se relaient pour enlever 1, 2 ou 3 allumettes à chaque tour.")
            print("Le joueur qui enlève la dernière allumette perd la partie.")
            print("Le joueur qui commence est choisi au hasard.")
            print("Le jeu se poursuit jusqu'à ce qu'un joueur enlève la dernière allumette.")
            lancer_jeu_des_allumettesIA()
        else:
            lancer_jeu_des_allumettesIA()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


################################################################################################################################################################################################################################

def demander_informations_joueurs():
    joueur1 = input("Nom du joueur 1 : ")
    symbole1 = input(f"Symbole de {joueur1} (X ou O) : ")
    while symbole1.upper() not in ["X", "O"]:
        print("Le symbole doit être X ou O.")
        symbole1 = input(f"Symbole de {joueur1} (X ou O) : ")
    joueur2 = input("Nom du joueur 2 : ")
    symbole2 = "X" if symbole1.upper() == "O" else "O"
    for i in range(1000):
        print("\n")
    return joueur1, symbole1.upper(), joueur2, symbole2


def designer_joueur_depart(joueur1, joueur2):
    joueurs = [joueur1, joueur2]
    joueur = random.choice(joueurs)
    return joueur


def creer_grille_P4():
    grille = []
    for _ in range(6):
        ligne = []
        for _ in range(7):
            ligne.append(" ")
        grille.append(ligne)
    return grille


def afficher_grille_P4(grille):
    print("+---+---+---+---+---+---+---+")
    print("| 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
    print("+---+---+---+---+---+---+---+")
    for ligne in grille:
        print("| " + " | ".join(ligne) + " |")
        print("+---+---+---+---+---+---+---+")


def inserer_jeton(grille, colonne, symbole):
    for i in range(5, -1, -1):
        if grille[i][colonne] == " ":
            grille[i][colonne] = symbole
            return True
    return False


def verifier_victoire_P4(grille, symbole):
    for ligne in grille:
        for i in range(4):
            if ligne[i] == ligne[i + 1] == ligne[i + 2] == ligne[i + 3] == symbole:
                return True

    for i in range(7):
        for j in range(3):
            if grille[j][i] == grille[j + 1][i] == grille[j + 2][i] == grille[j + 3][i] == symbole:
                return True

    for i in range(3, 6):
        for j in range(4):
            if grille[i][j] == grille[i - 1][j + 1] == grille[i - 2][j + 2] == grille[i - 3][j + 3] == symbole:
                return True

    for i in range(3):
        for j in range(4):
            if grille[i][j] == grille[i + 1][j + 1] == grille[i + 2][j + 2] == grille[i + 3][j + 3] == symbole:
                return True

    return False


def jouer_puissance4():
    joueur1, symbole1, joueur2, symbole2 = demander_informations_joueurs()

    while True:
        joueur_actuel = designer_joueur_depart(joueur1, joueur2)
        symbole_actuel = symbole1 if joueur_actuel == joueur1 else symbole2

        grille = creer_grille_P4()

        while True:
            print("\n\n\n\n\n")
            print("================================")
            print("C'est au tour du joueur", joueur_actuel, "(", symbole_actuel, ")")
            afficher_grille_P4(grille)
            print("================================")
            colonne = input("Entrez le numéro de colonne pour insérer le jeton : ")

            if not colonne.isdigit():
                print("Entrée invalide. Veuillez entrer un numéro de colonne valide.")
                continue

            colonne = int(colonne) - 1

            if colonne < 0 or colonne > 6:
                print("Numéro de colonne invalide. Veuillez réessayer.")
                continue

            if inserer_jeton(grille, colonne, symbole_actuel):
                if verifier_victoire_P4(grille, symbole_actuel):
                    afficher_grille_P4(grille)
                    print("Félicitations ! Le joueur", joueur_actuel, "a gagné !")
                    break
                elif " " not in grille[0]:
                    afficher_grille_P4(grille)
                    print("La grille est pleine. Match nul !")
                    break
                else:
                    joueur_actuel = joueur2 if joueur_actuel == joueur1 else joueur1
                    symbole_actuel = symbole1 if joueur_actuel == joueur1 else symbole2
            else:
                print("Colonne pleine. Veuillez réessayer.")
        rejoue = 0
        while rejoue == 0:
            choix = input("Voulez-vous rejouer ? (Oui/Non) : ")
            print("\n\n\n\n\n\n")
            if choix.lower() == "non":
                rejoue = 1
            elif choix.lower() == "oui":
                rejoue = 2
                symbole1 = input(f"Symbole de {joueur1} (X ou O) : ")
                while symbole1.upper() not in ["X", "O"]:
                    print("Le symbole doit être X ou O.")
                    symbole1 = input(f"Symbole de {joueur1} (X ou O) : ")
                symbole2 = "X" if symbole1.upper() == "O" else "O"
        if rejoue == 1:
            break
        if rejoue == 2:
            continue


def description_puissance_4():
    try:
        print("=== Bienvenue au jeu Puissance 4! ===")
        print("1. Jouer en mode Duo")
        print("2. Jouer en mode Solo contre IA")
        print("3. Description du jeu")
        choix = int(input("Choisissez une option (1-3) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
                return jouer_puissance4()
        elif choix == 2:
            jouer_puissance4_ia()
        elif choix == 3:
            for i in range(10):
                print("\n")
                print("Le Puissance 4 est un jeu de stratégie classique où deux joueurs s'affrontent.\n")
                print(
                    "Le but du jeu est d'aligner 4 jetons de sa couleur (X ou O) horizontalement, verticalement ou en diagonale.\n")
                print("Chaque joueur joue à tour de rôle en insérant son jeton dans l'une des colonnes de la grille.\n")
                print("Le joueur qui réussit à aligner 4 jetons de sa couleur en premier remporte la partie.\n")
                print(
                    "Si la grille est entièrement remplie sans qu'aucun joueur ne parvienne à aligner 4 jetons, la partie est déclarée nulle.\n\n")
                print("Amusez-vous bien et que le meilleur joueur gagne !")
                print("\n\n\n")
                return description_puissance_4()
        else:
            return description_puissance_4()
    except ValueError:
        print("Veuillez entrer un nombre valide.")


################################################################################################################################################################################################################################

def demander_informations_joueurs_IAP4(chiffre, joueur):
    if chiffre == 0:
        joueur1 = input("Entrez votre nom : ")
        symbole1 = input(f"Symbole de {joueur1} (X ou O) : ")
        while symbole1.upper() not in ["X", "O"]:
            print("Le symbole doit être X ou O.")
            symbole1 = input(f"Symbole de {joueur1} (X ou O) : ")
        joueur2 = "IA"
        symbole2 = "X" if symbole1.upper() == "O" else "O"
        for i in range(1000):
            print("\n")
        return joueur1, symbole1.upper(), joueur2, symbole2
    elif chiffre == 1:
        joueur1 = joueur
        symbole1 = input(f"Symbole de {joueur1} (X ou O) : ")
        while symbole1.upper() not in ["X", "O"]:
            print("Le symbole doit être X ou O.")
            symbole1 = input(f"Symbole de {joueur1} (X ou O) : ")
        joueur2 = "IA"
        symbole2 = "X" if symbole1.upper() == "O" else "O"
        for i in range(1000):
            print("\n")
        return joueur1, symbole1.upper(), joueur2, symbole2


def designer_joueur_depart_IAP4(joueur1, joueur2):
    joueurs = [joueur1, joueur2]
    choix = random.choice(joueurs)
    return choix


def creer_grilleIAP4():
    grille = []
    for _ in range(6):
        ligne = []
        for _ in range(7):
            ligne.append(" ")
        grille.append(ligne)
    return grille


def afficher_grilleIAP4(grille):
    print("+---+---+---+---+---+---+---+")
    print("| 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
    print("+---+---+---+---+---+---+---+")
    for ligne in grille:
        print("| " + " | ".join(ligne) + " |")
        print("+---+---+---+---+---+---+---+")


def inserer_jeton_IAP4(grille, colonne, symbole):
    for i in range(5, -1, -1):
        if grille[i][colonne] == " ":
            grille[i][colonne] = symbole
            return True
    return False


def verifier_victoireIAP4(grille, symbole):
    for ligne in grille:
        for i in range(4):
            if ligne[i] == ligne[i + 1] == ligne[i + 2] == ligne[i + 3] == symbole:
                return True

    for i in range(7):
        for j in range(3):
            if grille[j][i] == grille[j + 1][i] == grille[j + 2][i] == grille[j + 3][i] == symbole:
                return True

    for i in range(3, 6):
        for j in range(4):
            if grille[i][j] == grille[i - 1][j + 1] == grille[i - 2][j + 2] == grille[i - 3][j + 3] == symbole:
                return True

    for i in range(3):
        for j in range(4):
            if grille[i][j] == grille[i + 1][j + 1] == grille[i + 2][j + 2] == grille[i + 3][j + 3] == symbole:
                return True

    return False


def choisir_colonne_iaP4(grille, symbole):
    coup_gagnant = trouver_coup_gagnantP4(grille, symbole)
    if coup_gagnant is not None:
        return coup_gagnant

    coup_bloquant = trouver_coup_gagnantP4(grille, "X" if symbole == "O" else "O")
    if coup_bloquant is not None:
        return coup_bloquant

    return choisir_meilleur_coupIAP4(grille, symbole)


def trouver_coup_gagnantP4(grille, symbole):
    for colonne in range(7):
        copie_grille = [ligne.copy() for ligne in grille]
        if inserer_jeton_IAP4(copie_grille, colonne, symbole):
            if verifier_victoireIAP4(copie_grille, symbole):
                return colonne
    return None


def evaluer_positionP4(grille, symbole):
    score = 0

    for ligne in grille:
        for i in range(4):
            fenetre = ligne[i:i + 4]
            score += evaluer_fenetreP4(fenetre, symbole)

    for i in range(7):
        colonne = [grille[j][i] for j in range(6)]
        for j in range(3):
            fenetre = colonne[j:j + 4]
            score += evaluer_fenetreP4(fenetre, symbole)

    for i in range(3, 6):
        for j in range(4):
            fenetre = [grille[i - k][j + k] for k in range(4)]
            score += evaluer_fenetreP4(fenetre, symbole)

    for i in range(3):
        for j in range(4):
            fenetre = [grille[i + k][j + k] for k in range(4)]
            score += evaluer_fenetreP4(fenetre, symbole)

    return score


def evaluer_fenetreP4(fenetre, symbole):
    score = 0
    symbole_ia = "X" if symbole == "O" else "O"
    if fenetre.count(symbole) == 4:
        score += 100
    elif fenetre.count(symbole) == 3 and fenetre.count(" ") == 1:
        score += 5
    elif fenetre.count(symbole) == 2 and fenetre.count(" ") == 2:
        score += 2

    if fenetre.count(symbole_ia) == 3 and fenetre.count(" ") == 1:
        score -= 4

    return score


def choisir_meilleur_coupIAP4(grille, symbole):
    coups_possibles = [colonne for colonne in range(7) if grille[0][colonne] == " "]
    meilleur_score = float("-inf")
    meilleur_coup = random.choice(coups_possibles)

    for coup in coups_possibles:
        copie_grille = [ligne.copy() for ligne in grille]
        inserer_jeton_IAP4(copie_grille, coup, symbole)
        score = minimax_P4(copie_grille, 5, False, symbole)
        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = coup

    return meilleur_coup


def minimax_P4(grille, profondeur, maximisant, symbole):
    scores = {
        "X": -1,
        "O": 1,
        "match_nul": 0
    }

    if verifier_victoireIAP4(grille, "X"):
        return scores["X"]
    if verifier_victoireIAP4(grille, "O"):
        return scores["O"]
    if " " not in grille[0]:
        return scores["match_nul"]

    if profondeur == 0:
        return evaluer_positionP4(grille, symbole)

    if maximisant:
        meilleur_score = float("-inf")
        for colonne in range(7):
            if grille[0][colonne] == " ":
                copie_grille = [ligne.copy() for ligne in grille]
                inserer_jeton_IAP4(copie_grille, colonne, symbole)
                score = minimax_P4(copie_grille, profondeur - 1, False, symbole)
                meilleur_score = max(meilleur_score, score)
        return meilleur_score

    else:
        meilleur_score = float("inf")
        for colonne in range(7):
            if grille[0][colonne] == " ":
                copie_grille = [ligne.copy() for ligne in grille]
                inserer_jeton_IAP4(copie_grille, colonne, "X" if symbole == "O" else "O")
                score = minimax_P4(copie_grille, profondeur - 1, True, symbole)
                meilleur_score = min(meilleur_score, score)
        return meilleur_score


def jouer_puissance4_ia():
    d = 0
    j = ""
    while True:
        joueur1, symbole1, joueur2, symbole2 = demander_informations_joueurs_IAP4(d, j)
        joueur_actuel = designer_joueur_depart_IAP4(joueur1, joueur2)
        symbole_actuel = symbole1 if joueur_actuel == joueur1 else symbole2

        grille = creer_grilleIAP4()

        while True:
            print("\n\n\n\n\n")
            print("================================")
            print("C'est au tour du joueur", joueur_actuel, "(", symbole_actuel, ")")
            afficher_grilleIAP4(grille)
            print("================================")
            if joueur_actuel == "IA":
                colonne = choisir_colonne_iaP4(grille, symbole_actuel)
            else:
                colonne = input("Entrez le numéro de colonne pour insérer le jeton : ")

                if not colonne.isdigit():
                    print("Entrée invalide. Veuillez entrer un numéro de colonne valide.")
                    continue

                colonne = int(colonne) - 1

                if colonne < 0 or colonne > 6:
                    print("Numéro de colonne invalide. Veuillez réessayer.")
                    continue

            if inserer_jeton_IAP4(grille, colonne, symbole_actuel):
                if verifier_victoireIAP4(grille, symbole_actuel):
                    print("\n\n\n\n\n")
                    print("================================")
                    print("Le joueur", joueur_actuel, "a gagné !")
                    afficher_grilleIAP4(grille)
                    print("================================")
                    break
                elif " " not in grille[0]:
                    print("\n\n\n\n\n")
                    print("================================")
                    print("La partie est un match nul.")
                    afficher_grilleIAP4(grille)
                    print("================================")
                    break
                else:
                    joueur_actuel = joueur1 if joueur_actuel == joueur2 else joueur2
                    symbole_actuel = symbole1 if symbole_actuel == symbole2 else symbole2
            else:
                print("\n\n\n\n\n")
                print("================================")
                print("La colonne est pleine. Veuillez choisir une autre colonne.")
                print("================================")
        continuer = 0
        while continuer == 0:
            rejouer = input("Voulez-vous rejouer ? (oui/non) : ")
            if rejouer.lower() == "non":
                return "Au revoir !"
            elif rejouer.lower() == "oui":
                d = 1
                j = joueur1
                continuer = 1


###################################################################################################################################################################################################################################################


symbole_joueur1_morpion = ""
symbole_joueur2_morpion = ""


def afficher_grille_morpion_IA(grille):
    print("-------------")
    for i in range(3):
        for j in range(3):
            print("|", grille[i][j], end=" ")
        print("|")
        print("-------------")


def verifier_victoire_morpion_IA(grille, joueur):
    for i in range(3):
        if grille[i][0] == grille[i][1] == grille[i][2] == joueur:
            return True

    for j in range(3):
        if grille[0][j] == grille[1][j] == grille[2][j] == joueur:
            return True

    if grille[0][0] == grille[1][1] == grille[2][2] == joueur:
        return True
    if grille[0][2] == grille[1][1] == grille[2][0] == joueur:
        return True

    return False


def choisir_symboles_morpion_IA(joueur1, joueur2):
    global symbole_joueur1_morpion, symbole_joueur2_morpion

    symboles = ["X", "O"]
    symbole_joueur1_morpion = input(f"{joueur1}, choisissez un symbole (X ou O) : ")
    while symbole_joueur1_morpion not in symboles:
        symbole_joueur1_morpion = input("Veuillez choisir un symbole valide (X ou O) : ")

    symbole_joueur2_morpion = symboles[1 - symboles.index(symbole_joueur1_morpion)]


def tour_morpion_IA(grille, symbole_IA):
    _, coup = minimax_morpion_IA(grille, symbole_IA, symbole_IA, symbole_joueur1_morpion)
    grille[coup[0]][coup[1]] = symbole_IA


def minimax_morpion_IA(grille, joueur_actuel, symbole_IA, symbole_joueur):
    if verifier_victoire_morpion_IA(grille, symbole_IA):
        return 1, None
    elif verifier_victoire_morpion_IA(grille, symbole_joueur):
        return -1, None
    elif all(grille[i][j] != " " for i in range(3) for j in range(3)):
        return 0, None

    coups = []
    for i in range(3):
        for j in range(3):
            if grille[i][j] == " ":
                coups.append((i, j))

    if joueur_actuel == symbole_IA:
        meilleur_score = float("-inf")
        meilleur_coup = None
        for coup in coups:
            nouvelle_grille = [ligne[:] for ligne in grille]
            nouvelle_grille[coup[0]][coup[1]] = joueur_actuel
            score, _ = minimax_morpion_IA(nouvelle_grille, symbole_joueur, symbole_IA, symbole_joueur)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = coup
        return meilleur_score, meilleur_coup
    else:
        meilleur_score = float("inf")
        meilleur_coup = None
        for coup in coups:
            nouvelle_grille = [ligne[:] for ligne in grille]
            nouvelle_grille[coup[0]][coup[1]] = joueur_actuel
            score, _ = minimax_morpion_IA(nouvelle_grille, symbole_IA, symbole_IA, symbole_joueur)
            if score < meilleur_score:
                meilleur_score = score
                meilleur_coup = coup
        return meilleur_score, meilleur_coup


def jouer_morpion_IA():
    global symbole_joueur1_morpion, symbole_joueur2_morpion

    joueur1 = input("Entrez votre nom : ")
    continuer = True
    while continuer:
        grille = [[" " for i in range(3)] for i in range(3)]

        if symbole_joueur1_morpion == "" or symbole_joueur2_morpion == "":
            choisir_symboles_morpion_IA(joueur1, "IA")

        print(f"{joueur1} jouera avec le symbole '{symbole_joueur1_morpion}'")
        print(f"IA jouera avec le symbole '{symbole_joueur2_morpion}'")

        joueurs = [(joueur1, symbole_joueur1_morpion), ("IA", symbole_joueur2_morpion)]
        random.shuffle(joueurs)
        joueur_courant = joueurs[0]

        print(f"{joueur_courant[0]} commence !")

        while True:
            afficher_grille_morpion_IA(grille)

            if joueur_courant[0] == "IA":
                tour_morpion_IA(grille, symbole_joueur2_morpion)
            else:
                while True:
                    try:
                        ligne = int(input(f"{joueur_courant[0]}, choisissez une ligne (1-3) : "))
                        colonne = int(input(f"{joueur_courant[0]}, choisissez une colonne (1-3) : "))

                        if ligne < 1 or ligne > 3 or colonne < 1 or colonne > 3:
                            raise ValueError
                        if grille[ligne - 1][colonne - 1] != " ":
                            raise ValueError

                        break

                    except ValueError:
                        print("Veuillez entrer des coordonnées valides (1-3) pour une case libre.")

                grille[ligne - 1][colonne - 1] = joueur_courant[1]

            if verifier_victoire_morpion_IA(grille, joueur_courant[1]):
                afficher_grille_morpion_IA(grille)
                if joueur_courant[0] == "IA":
                    print("IA a gagné !")
                else:
                    print(f"Bravo {joueur_courant[0]} ! Vous avez gagné !")
                break
            elif all(grille[i][j] != " " for i in range(3) for j in range(3)):
                afficher_grille_morpion_IA(grille)
                print("Match nul !")
                break

            joueur_courant = joueurs[1] if joueur_courant == joueurs[0] else joueurs[0]

            print("\n" * 5)  # Espacement entre les tours

        choix = input("Voulez-vous rejouer ? (1: Oui, 2: Non) : ")
        while choix != "1" and choix != "2":
            choix = input("Veuillez entrer 1 pour rejouer ou 2 pour arrêter : ")

        if choix == "1":
            for i in range(1000):
                print("\n")

        if choix == "2":
            continuer = False


def description_jeu_morpion_IA():
    try:
        print("=== Bienvenue au jeu Morpion ! ===")
        print("1. Jouer au morpion (solo vs IA)")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
            jouer_morpion_IA()
        elif choix == 2:
            for i in range(100):
                print("\n")
            print("\n\n\nLe Morpion est un jeu de plateau pour deux joueurs.\n")
            print("Le plateau de jeu est une grille de 3x3 cases.\n")
            print("Chaque joueur choisit un symbole, soit 'X' soit 'O'.\n")
            print("Les joueurs alternent ensuite pour placer leur symbole sur une case vide du plateau.\n")
            print(
                "Le premier joueur à aligner trois de ses symboles horizontalement, verticalement ou en diagonale gagne la partie.\n")
            print(
                "Si toutes les cases sont remplies sans qu'un joueur n'ait aligné trois symboles, la partie est déclarée nulle.\n\n")
            print("Amusez-vous bien !\n\n\n")
            return description_jeu_morpion_IA()
        else:
            return description_jeu_morpion_IA()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################


def create_grille(PROBA):
    grille = []
    grille_cachee = []
    colonnes = 0
    nbr_voltorb_colonne = [0] * 5
    nbr_points_colonne = [0] * 5

    for _ in range(5):
        l = random.sample(PROBA, 5)
        nbr_voltorb_ligne = l.count(0)
        nbr_points_ligne = sum([i for i in l if i != 0])

        for j in range(5):
            if l[j] == 0:
                nbr_voltorb_colonne[j] += 1
            else:
                nbr_points_colonne[j] += l[j]

        grille.append(l)
        grille_cachee.append([nbr_voltorb_ligne, nbr_points_ligne, "?", "?", "?", "?", "?"])
        colonnes = nbr_voltorb_colonne, nbr_points_colonne

    return grille, grille_cachee, colonnes


def print_grille(grille, colonnes):
    liste_colonnes = []
    Voltorbs = "|"
    points = "|"
    for v in colonnes[0]:
        Voltorbs = Voltorbs + str(v) + "|"
    for p in colonnes[1]:
        points = points + str(p) + "|"
    liste_colonnes.append(Voltorbs)
    liste_colonnes.append(points)

    for ligne in grille:
        grille_str = " " + " ".join(str(element) for element in ligne[2:]) + " |" + str(ligne[0]) + "|" + str(
            ligne[1]) + "|"

        print(grille_str)
    for colonnes in liste_colonnes:
        print(colonnes)


def check_Voltorb(grille, v, score):
    if grille[v[0]][v[1]] == 0:
        print("La case était un Voltorb !")
        return True
    else:
        print("La case était un", grille[v[0]][v[1]], ".")
        print("Votre score actuel sur ce niveau est de: " + str(score) + " jetons.")
        return False


def check_game_over(grille):
    for ligne in grille:
        for case in ligne:
            if case == 2 or case == 3:
                return False
    return True


def Niveau_actuel(niveau):
    PROBA = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 0, 0, 0]
    if niveau == 2:
        PROBA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0]
    if niveau == 3:
        PROBA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if niveau == 4:
        PROBA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if niveau == 5:
        PROBA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0]
    return PROBA


def Voltorbataille():
    scorefinal = 0
    level = 1
    perdu = False
    gagne = False
    PROBA = Niveau_actuel(level)
    grille, grille_cachee, colonnes = create_grille(PROBA)
    score = 1
    while not level == 5:
        if check_game_over(grille):
            PROBA = Niveau_actuel(level)
            grille, grille_cachee, colonnes = create_grille(PROBA)

        print("Grille :")
        print_grille(grille_cachee, colonnes)
        verif = False
        ligne = 0
        colonne = 0
        while not verif:
            ligne = int(input("Entrez le numéro de la ligne que vous voulez choisir: ")) - 1
            colonne = int(input("Entrez le numéro de la colonne que vous voulez choisir: ")) - 1
            if 0 <= ligne <= 4 and 0 <= colonne <= 4:
                verif = True
            else:
                print("La valeur n'est pas comprise entre 1 et 5.")
        check = check_Voltorb(grille, (ligne, colonne), score)

        if check:
            perdu = True
            print("Grille :")
            grille_cachee[ligne][colonne + 2] = "V"
            print_grille(grille_cachee, colonnes)
            print("Le niveau est terminé. \nVous avez perdu...")
            print("Votre score actuel est de : " + str(scorefinal) + " jetons.")
            if level != 1:
                level = level - 1
                print(f"Vous redescendez au niveau {level}.")
            else:
                PROBA = Niveau_actuel(level)
                print("Vous restez au niveau 1.")
                grille, grille_cachee, colonnes = create_grille(PROBA)
        else:
            if grille[ligne][colonne] != "!":
                score *= grille[ligne][colonne]
                grille_cachee[ligne][colonne + 2] = grille[ligne][colonne]
                grille[ligne][colonne] = "!"
            if check_game_over(grille):
                print_grille(grille_cachee, colonnes)
                level = level + 1
                if level > 5:
                    scorefinal = scorefinal + score
                    gagne = True
                    print("Votre score final est de : " + str(scorefinal) + " jetons !")
                    print("Le jeu est terminé. \nVous avez gagné !!")

                else:
                    scorefinal = scorefinal + score
                    print("Votre score est de : " + str(scorefinal) + " jetons !\nVous avez gagné " + str(
                        score) + ' jetons grâce à ce niveau')
                    score = 1
                    print(f"Le niveau est terminé. \nVous passez au niveau {level} .")


def description_jeu_Voltorbe():
    print("\n=== Bienvenue dans Voltorbataille ! ===\n")
    val = int(input("Entrez 1 pour jouer à la Voltorbataille et 2 pour avoir une description du jeu : "))

    if val == 1:
        for i in range(100):
            print("\n")
        Voltorbataille()
    elif val == 2:
        print("\n" + "-" * 200)
        print("\nLa Voltorbataille est un minijeu issu de l'univers Pokémon, inspiré du jeu classique Démineur.")
        print(
            "Vous vous retrouverez face à une grille de 5x5 tuiles retournées.\nChaque tuile peut révéler soit un nombre, représentant les points que vous pouvez gagner, soit un Voltorbe, ce qui entraînera une fin de partie.\n Votre objectif est de réussir les niveaux sans découvrir de voltorbe.")
        print("Les tuiles retournées sont représentées par des points d'interrogation.")
        print(
            "Les chiffres sur les tuiles indiquent le nombre total de Voltorbes présents dans la ligne ou la colonne.")
        print(
            "Par exemple, si une ligne affiche un 3, cela signifie qu'il y a trois Voltorbes dans cette ligne, tandis qu'un 0 indique l'absence de Voltorbes.")
        print("Le nombre de Voltorbes est suivi du nombre de points disponibles dans chaque ligne.")
        print(
            "Votre objectif est de terminer le niveau 5 en progressant à chaque niveau réussi et en redescendant d'un niveau en cas d'échec.")
        print("N'oubliez pas de garder un œil sur votre score, qui vous donne une indication de votre performance.")
        print("\n" + "-" * 200 + "\n")
        description_jeu_Voltorbe()
    else:
        description_jeu_Voltorbe()


###################################################################################################################################################################################################################################################

def afficher_menu_pong(fenetre, LARGEUR, HAUTEUR, NOIR, VIOLET, VIOLETclair):
    fenetre.fill(NOIR)
    police_menu = pygame.font.Font(None, 72)
    texte_titre = police_menu.render("Pong", True, VIOLET)
    position_titre = texte_titre.get_rect(center=(LARGEUR / 2, 100))
    fenetre.blit(texte_titre, position_titre)

    texte_jouer = police_menu.render("Jouer", True, VIOLETclair)
    position_jouer = texte_jouer.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 + 50))
    fenetre.blit(texte_jouer, position_jouer)

    texte_quitter = police_menu.render("Quitter", True, VIOLETclair)
    position_quitter = texte_quitter.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 + 150))
    fenetre.blit(texte_quitter, position_quitter)

    pygame.display.flip()

    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                return
            elif evenement.type == pygame.MOUSEBUTTONDOWN:
                if position_jouer.collidepoint(evenement.pos):
                    jouer_pong(fenetre, LARGEUR, HAUTEUR, NOIR, VIOLET, VIOLETclair)
                elif position_quitter.collidepoint(evenement.pos):
                    pygame.quit()
                    return


def jouer_pong(fenetre, LARGEUR, HAUTEUR, NOIR, VIOLET, VIOLETclair):
    j = False
    if j:
        pygame.quit()

    horloge = pygame.time.Clock()

    LARGEUR_PADDLE = 10
    HAUTEUR_PADDLE = 80
    paddle_gauche = pygame.Rect(50, HAUTEUR / 2 - HAUTEUR_PADDLE / 2, LARGEUR_PADDLE, HAUTEUR_PADDLE)
    paddle_droite = pygame.Rect(LARGEUR - 50 - LARGEUR_PADDLE, HAUTEUR / 2 - HAUTEUR_PADDLE / 2, LARGEUR_PADDLE,
                                HAUTEUR_PADDLE)

    balle = pygame.Rect(LARGEUR / 2 - 10, HAUTEUR / 2 - 10, 20, 20)
    vitesse_balle_x = 3 * random.choice((1, -1))
    vitesse_balle_y = 3 * random.choice((1, -1))

    score_joueur1 = 0
    score_joueur2 = 0
    POINTS_VICTOIRE = 5
    niveau = 1
    touches_balle = 0
    en_cours = True

    vitesse_paddle = 5
    temps_restant = 3
    police_compteur = pygame.font.Font(None, 72)

    while temps_restant > 0:
        fenetre.fill(NOIR)
        texte_compteur = police_compteur.render(str(temps_restant), True, VIOLET)
        position_compteur = texte_compteur.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))
        fenetre.blit(texte_compteur, position_compteur)
        pygame.display.flip()
        pygame.time.wait(1000)
        temps_restant -= 1

    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False

        touches = pygame.key.get_pressed()
        if touches[pygame.K_z] and paddle_gauche.y > 0:
            paddle_gauche.y -= vitesse_paddle
        if touches[pygame.K_s] and paddle_gauche.y < HAUTEUR - HAUTEUR_PADDLE:
            paddle_gauche.y += vitesse_paddle
        if touches[pygame.K_UP] and paddle_droite.y > 0:
            paddle_droite.y -= vitesse_paddle
        if touches[pygame.K_DOWN] and paddle_droite.y < HAUTEUR - HAUTEUR_PADDLE:
            paddle_droite.y += vitesse_paddle

        balle.x += vitesse_balle_x
        balle.y += vitesse_balle_y

        if balle.y <= 0 or balle.y >= HAUTEUR - 20:
            vitesse_balle_y *= -1

        if balle.colliderect(paddle_gauche) or balle.colliderect(paddle_droite):
            vitesse_balle_x *= -1
            touches_balle += 1

        if balle.x <= 0:
            score_joueur2 += 1
            balle.center = (LARGEUR / 2, HAUTEUR / 2)
            vitesse_balle_x = 3 * random.choice((1, -1))
            vitesse_balle_y = 3 * random.choice((1, -1))
            touches_balle = 0
            if score_joueur2 == POINTS_VICTOIRE:
                fenetre.fill(NOIR)
                police_resultat = pygame.font.Font(None, 48)
                texte_resultat = police_resultat.render("Joueur 2 a gagné !", True, VIOLET)
                position_resultat = texte_resultat.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))
                fenetre.blit(texte_resultat, position_resultat)
                pygame.display.flip()
                pygame.time.wait(5000)
                en_cours = False
            else:
                niveau += 1
                if touches_balle >= 5:
                    touches_balle = 0
                    vitesse_balle_x *= 2
                    vitesse_balle_y *= 2
                niveau_vitesse = min(niveau, 9) / 2
                vitesse_balle_x = abs(vitesse_balle_x) + niveau_vitesse
                vitesse_balle_y = abs(vitesse_balle_y) + niveau_vitesse
                if niveau_vitesse == niveau:
                    vitesse_paddle = 5 + niveau_vitesse

        elif balle.x >= LARGEUR - 20:
            score_joueur1 += 1
            balle.center = (LARGEUR / 2, HAUTEUR / 2)
            vitesse_balle_x = 3 * random.choice((1, -1))
            vitesse_balle_y = 3 * random.choice((1, -1))
            touches_balle = 0
            if score_joueur1 == POINTS_VICTOIRE:
                fenetre.fill(NOIR)
                police_resultat = pygame.font.Font(None, 48)
                texte_resultat = police_resultat.render("Joueur 1 a gagné !", True, VIOLET)
                position_resultat = texte_resultat.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))
                fenetre.blit(texte_resultat, position_resultat)
                pygame.display.flip()
                pygame.time.wait(5000)
                en_cours = False

            else:
                niveau += 1
                if touches_balle >= 5:
                    touches_balle = 0
                    vitesse_balle_x *= 2
                    vitesse_balle_y *= 2
                niveau_vitesse = min(niveau, 9) / 2
                vitesse_balle_x = -abs(vitesse_balle_x) - niveau_vitesse
                vitesse_balle_y = abs(vitesse_balle_y) + niveau_vitesse
                if niveau_vitesse == niveau:
                    vitesse_paddle = 5 + niveau_vitesse
        if en_cours:
            fenetre.fill(NOIR)
            pygame.draw.rect(fenetre, VIOLETclair, paddle_gauche)
            pygame.draw.rect(fenetre, VIOLETclair, paddle_droite)
            pygame.draw.ellipse(fenetre, VIOLETclair, balle)

            police_score = pygame.font.Font(None, 36)
            texte_score = police_score.render(f"{score_joueur1} | {score_joueur2}", True, VIOLET)
            position_score = texte_score.get_rect(center=(LARGEUR / 2, 30))
            fenetre.blit(texte_score, position_score)

            pygame.display.flip()
            horloge.tick(60)
        if not en_cours:
            j = True
            break


def main_pong():
    pygame.init()
    LARGEUR = 1000
    HAUTEUR = 600
    NOIR = (0, 0, 0)
    VIOLET = (136, 46, 114)
    VIOLETclair = (218, 112, 214)

    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Pong")

    afficher_menu_pong(fenetre, LARGEUR, HAUTEUR, NOIR, VIOLET, VIOLETclair)


def description_Pong_JEU():
    try:
        print("=== Bienvenue au jeu Pong ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
                return main_pong()
        elif choix == 2:
            for i in range(10):
                print("\n")
                print("""
Le jeu Pong est un jeu classique où deux joueurs s'affrontent sur un terrain de jeu divisé en deux côtés.

Chaque joueur contrôle une raquette, et le but du jeu est de marquer des points en faisant rebondir une balle sur le mur de l'adversaire.

Les joueurs peuvent déplacer leur raquette verticalement le long de leur moitié du terrain pour intercepter la balle.

Pour le joueur 1, les touches "Z" et "S" permettent de déplacer la raquette vers le haut et vers le bas respectivement.

Quant au joueur 2, il utilise les touches fléchées "haut" et "bas" pour déplacer sa raquette dans la même direction.

Lorsque la balle est en mouvement, les joueurs doivent anticiper sa trajectoire et ajuster rapidement la position de leur raquette pour la frapper.

Si un joueur réussit à faire rebondir la balle sur la raquette de l'adversaire de telle sorte qu'elle dépasse cette dernière et ne puisse pas être renvoyée,

il marque un point. Le premier joueur à atteindre 5 points remporte la partie.



                     Bonne chance et bon jeu !


                """)
                print("\n\n\n")
                return description_Pong_JEU()
        else:
            return description_Pong_JEU()
    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################

def attendre_appui_touche():
    print("Appuyez sur la touche 'Entrée' pour jouer !")
    input()


def jouer_jeu_memoire():
    print("Bienvenue dans le Jeu de Mémoire !")
    print("Je vais afficher une séquence de couleurs. À vous de la reproduire.")
    attendre_appui_touche()
    niveau = 1
    temps_affichage = 2
    score = 0
    nombre_vie = 3
    if niveau <= 3:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune"}

    elif niveau <= 5:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris"}

    elif niveau <= 8:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris", "O": "orange"}

    else:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris", "O": "orange", "M": "marron"}

    while True:
        if niveau == 16:
            print("Bravo ! vous avez réussi le dernier niveau !")
            return rejouer_jeu_couleur(1)
        print("\n    Niveau", niveau)
        print("=================")
        print("\n")
        if niveau <= 3:
            temps_affichage = random.randint(2, 4)
        elif niveau <= 5:
            temps_affichage = 2
        elif niveau <= 8:
            temps_affichage = randint(1, 2)
        else:
            temps_affichage = 0.5
        sequence = generer_sequence(niveau)
        afficher_sequence(sequence, temps_affichage, niveau)
        joueur_sequence = saisir_sequence(len(sequence), niveau)

        if joueur_sequence == sequence:
            print("Bravo ! Vous avez reproduit la séquence correctement.")
            print("======================================================")
            score += len(sequence)
            niveau += 1
        else:
            nombre_vie = nombre_vie - 1
            if nombre_vie == 0:
                print("Dommage ! Vous n'avez plus de vie !")
                print("Vous avez perdu...")
                print("Votre score final est de", score)
                print("======================================")
                print("\n\n\n")
                return rejouer_jeu_couleur(1)
            else:
                if nombre_vie == 1:
                    print("Vous vous êtes trompé, vous perdez une vie !")
                    print(f"il vous reste {nombre_vie} vie. ")
                    print("=============================================")
                    print("\n\n\n")
                else:
                    print("Vous vous êtes trompé, vous perdez une vie !")
                    print(f"il vous reste {nombre_vie} vie(s). ")
                    print("=============================================")
                    print("\n\n\n")


def rejouer_jeu_couleur(r):
    try:
        if r == 1:
            print("Voulez vous rejouer ?")
            print("1) rejouer")
            print("2) quitter")
            choix = int(input("choisissez une option (1-2): "))
            if choix == 1:
                return jouer_jeu_memoire()
            elif choix == 2:
                return
            else:
                return rejouer_jeu_couleur(1)
        elif r == 0:
            print("=== Bienvenue au jeu RememberTheColors ! ===")
            print("1. Jouer")
            print("2. Description du jeu")
            choix = int(input("Choisissez une option (1-2) : "))
            if choix == 1:
                for i in range(100):
                    print("\n")
                return jouer_jeu_memoire()
            elif choix == 2:
                print(
                    "=====================================================================================================================================")
                print("\n\n\nLe jeu RememberTheColors est un jeu de mémoire.\n")
                print("Des couleurs s'affichent à l'écran et vous devez les mémoriser dans l'ordre.\n")
                print("Vous devez ensuite les réecrire dans le même ordre.\n")
                print("Si vous avez toutes les bonnes couleurs vous passez au niveau suivant.\n")
                print("Sinon vous restez au même niveau et vous perdez une vie.\n")
                print("Au début du jeu vous avez 3 vies et il y a 15 niveaux.\n")
                print("Attention la difficulté s'intensifie rapidement !\n")
                print("Bonne chance !\n\n\n\n\n")
                return rejouer_jeu_couleur(0)

            else:
                return rejouer_jeu_couleur(0)
        else:
            rejouer_jeu_couleur(0)

    except ValueError:
        print("Veuillez entrer un nombre valide.")


def generer_sequence(niveau):
    if niveau <= 3:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune"}
    elif niveau <= 5:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris"}
    elif niveau <= 8:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris", "O": "orange"}
    else:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris", "O": "orange", "M": "marron"}
    sequence = []
    longueur = niveau
    if niveau > 10:
        longueur = 10
    if niveau >= 13:
        longueur = 11

    for _ in range(longueur):
        couleur = random.choice(list(couleurs.keys()))
        sequence.append(couleur)
    return sequence


def afficher_sequence(sequence, temps_affichage, niveau):
    if niveau <= 3:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune"}

    elif niveau <= 5:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris"}

    elif niveau <= 8:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris", "O": "orange"}

    else:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris", "O": "orange", "M": "marron"}

    for couleur in sequence:
        afficher_couleur(couleurs[couleur])
        time.sleep(temps_affichage)
    effacer_console()


def saisir_sequence(longueur, niveau):
    start_time = time.time()

    if niveau <= 3:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune"}
        print(
            "Entrez: | R > \033[91m██\033[0m | B > \033[94m██\033[0m | J > \033[93m██\033[0m | V > \033[92m██\033[0m |")
        print("==============================================")
    elif niveau <= 5:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris"}
        print(
            "Entrez: | R > \033[91m██\033[0m | B > \033[94m██\033[0m | J > \033[93m██\033[0m | V > \033[92m██\033[0m | G > \033[90m██\033[0m |")
        print("=======================================================")
    elif niveau <= 8:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris", "O": "orange"}
        print(
            "Entrez: | R > \033[91m██\033[0m | B > \033[94m██\033[0m | J > \033[93m██\033[0m | V > \033[92m██\033[0m | G > \033[90m██\033[0m | O > \033[38;5;208m██\033[0m |")
        print("================================================================")
    else:
        couleurs = {"B": "bleu", "V": "vert", "R": "rouge", "J": "jaune", "G": "gris", "O": "orange", "M": "marron"}
        print(
            "Entrez: | R > \033[91m██\033[0m | B > \033[94m██\033[0m | J > \033[93m██\033[0m | V > \033[92m██\033[0m | G > \033[90m██\033[0m | O > \033[38;5;208m██\033[0m | M > \033[38;5;94m██\033[0m |")
        print("=========================================================================")

    joueur_sequence = []
    couleurs_disponibles = ", ".join([couleurs[c] for c in couleurs])

    for _ in range(longueur):
        sequence = input(f"Reproduisez la couleur {_ + 1} : ")
        ecoule_time = time.time() - start_time

        if ecoule_time > 7:
            print("Temps dépassé.")
            return None

        joueur_sequence.append(sequence.upper())

    effacer_console()
    return joueur_sequence


def afficher_couleur(couleur):
    if couleur == "bleu":
        print("\033[94m██\033[0m")
        print("\n")
    elif couleur == "vert":
        print("\033[92m██\033[0m")
        print("\n")
    elif couleur == "rouge":
        print("\033[91m██\033[0m")
        print("\n")
    elif couleur == "jaune":
        print("\033[93m██\033[0m")
        print("\n")
    elif couleur == "gris":
        print("\033[90m██\033[0m")
        print("\n")
    elif couleur == "orange":
        print("\033[38;5;208m██\033[0m")
        print("\n")
    elif couleur == "marron":
        print("\033[38;5;94m██\033[0m")
        print("\n")


def effacer_console():
    for i in range(1000):
        print("\n")


###################################################################################################################################################################################################################################################

def afficher_pendu(tentatives):
    stages = [
        '''
           --------
           |      
           |
           |
           |
           |
           -
        ''',
        '''
           --------
           |      |
           |
           |
           |
           |
           -
        ''',
        '''
           --------
           |      |
           |      O
           |
           |
           |
           -
        ''',
        '''
           --------
           |      |
           |      O
           |      |
           |
           |
           -
        ''',
        '''
           --------
           |      |
           |      O
           |     /|
           |
           |
           -
        ''',
        '''
           --------
           |      |
           |      O
           |     /|\\
           |
           |
           -
        ''',
        '''
           --------
           |      |
           |      O
           |     /|\\
           |     /
           |
           -
        ''',
        '''
           --------
           |      |
           |      O
           |     /|\\
           |     / \\
           |
           -
        '''
    ]
    return stages[tentatives]


def jeu_pendu():
    mots_francais = [
        "abaissement", "abasourdi", "abat-jour", "abattoir", "abdomen", "abeille", "abeillon", "aboiement",
        "abondance", "abonné", "abordage", "aboutir", "abrasif", "abreuvoir", "abriter", "absolu", "absurde",
        "abuser", "abysse", "abyssin", "acacia", "accent", "accessoire", "accident", "acclamer", "accolade",
        "accompli", "accord", "accoster", "accrocher", "accueil", "acheté", "acide", "acier", "acompte",
        "acquérir", "acrobate", "activité", "actuel", "acuité", "adapté", "addictif", "addition", "adhésif",
        "adieu", "adjoint", "admiration", "adopter", "adorable", "adoucir", "adresse", "adroit", "adulte",
        "adversaire", "aérien", "affecter", "affiche", "affoler", "affrété", "affûtage", "afghan", "africain",
        "agaçant", "agencer", "aggraver", "agile", "agiter", "agonie", "agrandir", "agréable", "agricole",
        "ahurissant", "ailier", "aimable", "aîné", "aire", "aisance", "ajouter", "alambic", "alarmer",
        "album", "alchimie", "alerte", "algèbre", "alibi", "alliance", "allocution", "allumer", "allure",
        "alourdir", "alpin", "alsacien", "altérer", "alvéole", "amadouer", "amarrer", "amateur", "ambassade",
        "ambiance", "ambigu", "ambroisie", "amené", "amertume", "amical", "amidon", "amiral", "amour",
        "ampoule", "amusement", "analogie", "ancien", "anémie", "ange", "anglais", "angoisse",
        "animation", "annexe", "annonce", "annuel", "anodin", "anomalie", "antenne", "antidote", "anxiété",
        "apaiser", "apéritif", "aplanir", "apogée", "apôtre", "appareil", "appeler", "applaudir", "appoint",
        "apporter", "apprendre", "approche", "approuver", "appuyer", "arbitre", "arbuste", "archer", "ardoise",
        "argent", "aride", "armée", "armoire", "armure", "aromate", "arracher", "arrêter", "arriver",
        "artisan", "ascenseur", "asile", "aspirer", "assaut", "asseoir", "assiette", "associer", "assurer",
        "astuce", "atelier", "atout", "atroce", "attacher", "attaque", "attente", "attirer", "attraper",
        "aubaine", "auberge", "audace", "auditeur", "augmenter", "aurore", "automne", "autoriser", "avalanche",
        "avancer", "avenir", "averse", "aveugle", "avide", "avion", "aviser", "avocat", "avouer",
        "axial", "axiome", "azimut", "azur", "babiller", "bacchus", "bague", "baignade", "balancer",
        "balcon", "balise", "bambou", "banane", "banc", "bandage", "banjo", "banlieue", "bannière",
        "banquet", "barbare", "barbe", "baril", "baron", "barque", "barrage", "barreau", "baryton",
        "bascule", "basilic", "bassin", "bastingage", "bataille", "bateau", "bâton", "battre", "bavard",
        "baver", "bavoir", "beau", "bébé", "bec", "belge", "belle", "béquille", "berceau",
        "berger", "berline", "bermuda", "besace", "besoin", "beurre", "biais", "bibelot", "biberon",
        "biceps", "bidule", "bijou", "bille", "binette", "biologie", "biopsie", "biplan", "biscuit",
        "bison", "bistouri", "bitume", "bizarre", "blâmer", "blanc", "blason", "bleu", "blond",
        "bocal", "bœuf", "boire", "boisson", "boîte", "bolide", "bonbon", "bondir", "bonheur",
        "bonjour", "bord", "borne", "bosse", "boucle", "boue", "bougie", "boulon", "bouquet",
        "bourgeon", "boussole", "boutique", "boxeur", "branche", "bras", "brave", "brebis", "brèche",
        "breton", "brève", "brider", "brigade", "briller", "brique", "brise", "brochure", "broder",
        "bronze", "brosser", "brouter", "bruit", "brûler", "brume", "brusque", "brutal", "bruyant",
        "bûcher", "buffle", "bulle", "bureau", "burin", "buse", "butiner", "butoir", "cabane",
        "cabine", "câble", "cache", "cadeau", "cadre", "café", "cage", "caillou", "caisson",
        "calcul", "caleçon", "calibre", "calin", "calme", "calomnie", "calvaire", "camarade", "caméra",
        "campagne", "campeur", "canal", "canard", "candide", "canette", "cannibale", "canon", "canot",
        "cantique", "capable", "caporal", "caprice", "capsule", "capter", "capuche", "carabine", "caractère",
        "carburant", "cardinal", "carie", "carillon", "carlin", "carnage", "carotte", "carreau", "cartable",
        "carte", "casier", "casque", "casser", "castor", "catastrophe", "catégorie", "cause", "caution",
        "cavité", "ceinture", "céleste", "cellule", "cendre", "censure", "centrale", "cerise", "cerner",
        "certitude", "cerveau", "cesser", "chacal", "chagrin", "chaîne", "chair", "chaleur", "chambre",
        "chamois", "chanson", "chantage", "chaos", "chapeau", "chapon", "charbon", "chardon", "charge",
        "charme", "charnière", "chasse", "chat", "chaud", "chausson", "chavirer", "chemin", "chenille",
        "cheval", "chèvre", "chez", "chiffre", "chimère", "chiot", "chirurgie", "chlore", "choc",
        "choisir", "chose", "chou", "choyer", "chrétien", "chrome", "chuchoter", "chuter", "cigare",
        "cigogne", "cime", "cimetière", "cinéma", "cintrer", "cirque", "citer", "citoyen", "citron",
        "civil", "clair", "clameur", "clan", "clapet", "classe", "clavier", "client", "cligner",
        "climat", "cloche", "cloner", "cloporte", "cobalt", "cobra", "cocasse", "cocon", "cocotte",
        "coffre", "cogner", "cohabiter", "cohésion", "coiffer", "coincer", "colère", "colibri", "colline",
        "colmater", "colonel", "combat", "comédie", "comète", "commande", "commencer", "commodité", "commune",
        "compact", "compas", "compter", "concave", "conclure", "conduire", "confier", "congeler", "congrès",
        "conifère", "connaître", "conquérir", "consoler", "conte", "continuer", "contrat", "convexe", "copain",
        "copie", "corail", "corbeau", "cordage", "corniche", "corps", "cosmos", "coton", "coude",
        "coupure", "cour", "couteau", "couvrir", "coyote", "crabe", "crainte", "crâne", "cravate",
        "crayon", "créature", "crédit", "creuser", "crevette", "crible", "crinière", "cristal", "critère",
        "croire", "croquer", "crotale", "crucial", "cruel", "crypte", "cube", "cuisiner", "cuivre",
        "culotte", "cumulus", "cure", "curieux", "cuve", "cyanure", "cycle", "cyclone", "cylindre",
        "cynique", "dactylo", "damier", "danger", "danse", "dard", "date", "dauphin", "débattre",
        "début", "décembre", "déchirer", "décider", "déclarer", "décorer", "décrire", "défaire", "défiler",
        "défrayer", "dégager", "dégivrer", "déglutir", "déguster", "déjeuner", "délice", "déluge", "demain",
        "demander", "demeurer", "demi", "démon", "dénicher", "départ", "dépenser", "déployer", "déposer",
        "déranger", "dernier", "dérober", "dérouler", "désastre", "descendre", "désert", "désigner", "désirer",
        "désordre", "dessiner", "destin", "détacher", "détester", "détour", "détruire", "devancer", "devenir",
        "deviner", "devoir", "diable", "dialogue", "diamant", "dicter", "dieu", "différer", "digestion",
        "digne", "diluer", "dimanche", "dîner", "diode", "diorama", "direct", "diriger", "discours",
        "disposer", "distance", "divertir", "diviser", "docile", "docteur", "dogme", "doigt", "dominer",
        "donation", "donjon", "donner", "dopamine", "dortoir", "dose", "douane", "double", "douceur",
        "douter", "douze", "dragon", "draper", "dresser", "dribbler", "droit", "duper", "durant",
        "durcir", "durer", "éblouir", "écarter", "échapper", "éclair", "éclipse", "éclore", "écluse",
        "école", "économie", "écouter", "écran", "écrire", "écrivain", "écurie", "éden", "édifice",
        "éditer", "édition", "éducation", "effacer", "effectif", "effort", "effrayant", "effusion", "égal",
        "égarer", "église", "égout", "éjaculer", "élaborer", "élancer", "élargir", "électron", "élégant",
        "éléphant", "élève", "éliminer", "élixir", "elle", "éloge", "élu", "émaner", "emballer",
        "embarquer", "embryon", "émeraude", "émission", "emmener", "émotion", "empereur", "employer", "emporter",
        "emprise", "énergie", "enfance", "enfermer", "enfiler", "enfler", "enfouir", "enfreindre", "enfuir",
        "engager", "engloutir", "engrais", "enivrer", "enjamber", "enjeu", "enlever", "ennemi", "ennuyeux",
        "enquête", "enrichir", "enrouler", "enseigne", "entasser", "entendre", "entier", "entourer", "entraver",
        "entre", "envelopper", "envie", "envoyer", "épais", "épaule", "épicer", "épisode", "épitaphe",
        "époque", "épreuve", "éprouver", "épuiser", "équateur", "équipage", "équipe", "équiper", "erreur",
        "ériger", "escalier", "escargot", "espace", "espèce", "espiègle", "espoir", "esprit", "essayer",
        "essence", "essuyer", "estime", "estrade", "établir", "étage", "étaler", "état", "étendre",
        "éternel", "éthique", "étincelle", "étiquette", "étoile", "étonnant", "étourdir", "étrange", "étroit",
        "étude", "euphorie", "évaluer", "évasion", "éventail", "évidence", "éviter", "évolutif", "évoquer",
        "exact", "exagérer", "exaucer", "exceller", "exciter", "exécuter", "exemple", "exercer", "exiger",
        "exil", "exister", "exode", "explorer", "exposer", "exprimer", "exquis", "extase", "extension",
        "extérieur", "exutoire", "fable", "fabuleux", "facette", "facile", "facteur", "faction", "facture",
        "faire", "falloir", "famille", "fanfare", "fantôme", "farce", "farine", "farouche", "fasciner",
        "fatal", "fatigue", "faucon", "faune", "faute", "faux", "favori", "fax", "fée",
        "félin", "femme", "fenêtre", "ferme", "féroce", "fertiliser", "ferveur", "festival", "feuille",
        "feutre", "fiable", "fibre", "ficeler", "fiche", "fiction", "fidèle", "fier", "figer",
        "figure", "filet", "fille", "film", "filtre", "final", "finesse", "finir", "fiole",
        "firme", "fixer", "flairer", "flamme", "flanc", "flâner", "flaque", "fleur", "flexion",
        "flocon", "flore", "flot", "flou", "fluide", "flûte", "flux", "focus", "foin",
        "foire", "fois", "fonction", "fond", "force", "forêt", "forger", "forme", "formule",
        "fort", "fortune", "forum", "fossé", "foudre", "fouet", "fougue", "fouiller", "foulure",
        "four", "foyer", "frais", "franc", "frapper", "frayeur", "frégate", "freiner", "frelon",
        "frémir", "frénésie", "frère", "friable", "friche", "frimeur", "friser", "frisson", "frivole",
        "froid", "fromage", "front", "frotter", "fruit", "fugue", "fuir", "fuite", "fumer",
        "fureur", "furieux", "furtif", "fusion", "futé", "futur", "gabarit", "gâcher", "gagner",
        "gain", "gala", "galet", "galop", "gamme", "gant", "garage", "garde", "garçon",
        "garnir", "gâteau", "gauche", "gaufre", "gaule", "gaver", "gazon", "géant", "gélatine",
        "geler", "générer", "genou", "gentil", "geste", "geyser", "gibier", "gicler", "gigot",
        "gilet", "girafe", "givre", "glace", "glaçon", "glisser", "globe", "gloire", "gluant",
        "gober", "gobelin", "goéland", "golfe", "gomme", "gonfler", "gorge", "gorille", "goudron",
        "gouffre", "goulot", "goupille", "gourmand", "goutte", "graduel", "grain", "gramme", "grand",
        "grappin", "gratuit", "gravir", "grenat", "griffure", "griller", "grimper", "grogner", "gronder",
        "grotte", "groupe", "gruger", "grutier", "gruyère", "guépard", "guerrier", "guetter", "guider",
        "guirlande", "guitare", "gustatif", "gymnaste", "gyrostat", "habiter", "hache", "haïr", "halte",
        "hameau", "hangar", "hanter", "haricot", "harmonie", "harpon", "hasard", "haut", "havre",
        "herbe", "heureux", "hiberner", "hibou", "hilarant", "histoire", "hiver", "homme", "honneur",
        "honte", "horde", "horizon", "horloge", "hormone", "horrible", "houle", "housse", "hublot",
        "huile", "huit", "humain", "humble", "humide", "humour", "hurler", "hybride", "hydrater",
        "hyène", "hypnose", "idée", "idiot", "ignorer", "iguane", "illicite", "illusion", "image",
        "imaginer", "imiter", "immense", "immobile", "immuable", "impact", "implorer", "imposer", "impression",
        "imprimer", "imputer", "incapable", "incendie", "incident", "incliner", "incolore", "index", "indiquer",
        "induction", "indulger", "inédit", "infime", "infliger", "informer", "infusion", "ingérer", "inhaler",
        "inhiber", "injecter", "injure", "innocent", "inoculer", "inonder", "inscrire", "insecte", "insigne",
        "insister", "institut", "insulter", "intact", "intense", "intention", "intégrer", "intégral", "intérieur",
        "interne", "intime", "intrigue", "intuitif", "inutile", "invasion", "inventer", "inviter", "iode",
        "iris", "issue", "ivre", "jade", "jadis", "jamais", "jambe", "janvier", "jardin",
        "jauger", "jaune", "javelot", "jeté", "jeudi", "jeunesse", "joie", "joindre", "joli",
        "joueur", "journal", "jovial", "joyau", "jubiler", "jugement", "junior", "jupon", "jurer",
        "jusque", "juste", "juteux", "kayak", "kimono", "kiosque", "label", "labial", "labourer",
        "lacérer", "lacet", "laine", "laisser", "lait", "lama", "lambeau", "lampe", "lance",
        "lanterne", "lapin", "large", "larme", "laurier", "lavabo", "laver", "laxatif", "lecture",
        "légal", "légende", "légume", "lessive", "lettre", "levé", "levier", "lévrier", "libérer",
        "libre", "licence", "licorne", "liège", "lier", "limace", "limer", "limite", "lingot",
        "lion", "lire", "lisser", "liste", "litre", "livre", "lobe", "local", "locomotive",
        "logique", "loin", "loisir", "lombric", "lotus", "louche", "loup", "lourd", "louve",
        "loyal", "lubie", "lucide", "lueur", "luge", "luire", "lundi", "lune", "lunette",
        "lutin", "lutte", "luxe", "machine", "magasin", "magenta", "magie", "magnifique", "magot",
        "maigre", "main", "mairie", "maison", "majorer", "malaxer", "malgré", "malice", "maman",
        "mammouth", "manche", "manger", "maniéré", "manoir", "manquer", "manteau", "manuel", "marathon",
        "marbre", "marche", "mardi", "marge", "mariage", "marier", "marque", "marron", "mars",
        "masque", "massif", "mastique", "matériel", "matin", "mauvais", "maximal", "méchant", "médecin",
        "méditer", "méduse", "méfier", "mégot", "mélange", "mêler", "mélodie", "melon", "membre",
        "même", "mémoire", "menacer", "mener", "menhir", "mensonge", "mentor", "mercredi", "mère",
        "merle", "messager", "mesure", "métal", "météore", "méthode", "métier", "métro", "meuble",
        "meurtre", "meute", "miauler", "microbe", "midi", "miel", "mieux", "milieu", "mille",
        "mimer", "mince", "mineur", "ministre", "minute", "miracle", "miroir", "missile", "mixte",
        "mobile", "mode", "module", "moelleux", "moins", "mois", "moment", "monde", "moniteur",
        "monnaie", "monotone", "monstre", "montagne", "monument", "moquer", "moral", "mordre", "morose",
        "morse", "mortier", "morue", "motif", "mouche", "moufle", "moulin", "mourir", "mousse",
        "mouton", "mouvement", "moyen", "mûr", "muqueuse", "muraille", "muret", "muse", "musique",
        "muter", "mutuel", "myriade", "mystère", "mythique", "nageur", "nappe", "narval", "naseau",
        "natif", "nature", "navire", "nébuleux", "nécessaire", "négatif", "neige", "nerveux", "nettoyer",
        "neuf", "neuron", "neutre", "neutron", "nez", "nièce", "niveau", "noble", "noce",
        "nocif", "noir", "nomade", "nombre", "nommer", "nord", "norme", "notaire", "noter",
        "nounours", "nourrir", "nouveau", "novice", "noyade", "noyer", "nuage", "nuancer", "nuire",
        "nuit", "nuptial", "nuque", "oasis", "obéir", "objectif", "obliger", "obscur", "observer",
        "obstacle", "obtenir", "obus", "occasion", "occuper", "ocre", "octobre", "octroyer", "odeur",
        "odorat", "offense", "officier", "offrir", "ogive", "oiseau", "olive", "ombre", "onctueux",
        "onduler", "ongle", "onze", "opter", "optique", "orageux", "orange", "orbite", "ordonner",
        "oreille", "organe", "orgueil", "orifice", "ornement", "orteil", "ortie", "osciller", "osmose",
        "ossature", "otage", "otarie", "ouate", "oublier", "ouest", "ours", "outil", "outre",
        "ouvert", "ouvrir", "ovale", "ozone", "pacifier", "pacte", "pagaie", "page", "paille",
        "pain", "paire", "paix", "palace", "palmarès", "palpiter", "panda", "panier", "panneau",
        "panorama", "pantalon", "papayer", "papier", "papoter", "papyrus", "parc", "parfum", "parler",
        "parmi", "parole", "partager", "parvenir", "passer", "pastèque", "paternel", "patience", "patron",
        "paume", "pause", "pauvre", "paver", "pavot", "payer", "paysage", "peau", "pécher",
        "pécule", "pédaler", "pédant", "peigne", "peinture", "pelage", "pelote", "peluche", "pendant",
        "péniche", "pénombre", "penser", "pente", "pépite", "percer", "perdu", "perle", "permettre",
        "persil", "perte", "peser", "pétale", "petit", "pétrir", "pétrole", "peuple", "pharaon",
        "phobie", "phoque", "photon", "phrase", "physique", "piano", "pied", "pierre", "pieu",
        "pile", "pilier", "pilote", "pinceau", "pincette", "pingouin", "pinson", "pinte", "pion",
        "piquer", "pirate", "pire", "pirogue", "piscine", "piston", "pivoter", "pixel", "pizza",
        "placard", "plafond", "plaisir", "plan", "plaque", "plastron", "plateau", "plein", "pleurer",
        "pliage", "plier", "plonger", "plot", "pluie", "plume", "plus", "pochette", "poche",
        "poème", "poésie", "poète", "pointe", "poire", "poison", "poitrine", "poivre", "police",
        "pollen", "polygone", "pomme", "pompier", "poncer", "pondre", "pont", "population", "porc",
        "port", "porter", "positif", "possible", "poste", "potager", "potin", "pouce", "poudre",
        "poulet", "poupée", "pour", "pourquoi", "pourrir", "poursuivre", "pousser", "poutre", "pouvoir",
        "prairie", "pratique", "précieux", "prédire", "préfixe", "préparer", "présence", "président", "presser",
        "prêt", "preuve", "prier", "primeur", "prince", "prison", "priver", "prix", "problème",
        "processus", "prochain", "produire", "profond", "proie", "projet", "promener", "prononcer", "propre",
        "prospère", "protéger", "prouver", "provoquer", "prudence", "prune", "public", "puceron", "pudding",
        "puéril", "puiser", "pulluler", "pulpe", "pulsar", "punir", "purifier", "puzzle", "pyramide",
        "quand", "quartier", "quasi", "quête", "question", "qui", "quitter", "quoique", "quota",
        "racine", "raconter", "radieux", "ragondin", "raideur", "raison", "ramasser", "ramener", "rampant",
        "ramure", "ranch", "rang", "rapide", "rappel", "rare", "rasage", "ratisser", "ravager",
        "ravir", "rayer", "rayon", "réagir", "réaliser", "réanimer", "recevoir", "récolter", "recruter",
        "reculer", "recycler", "réduire", "réfléchir", "refuser", "regarder", "regretter", "rein", "rejeter",
        "rejoindre", "relation", "relever", "religion", "remarquer", "remédier", "remonter", "remplacer", "remuer",
        "rencontre", "rendre", "renfort", "renifler", "renoncer", "rentrer", "renverser", "repas", "replier",
        "répondre", "reposer", "reproche", "requin", "résoudre", "respect", "rester", "résultat", "retard",
        "retenir", "retirer", "retour", "retrouver", "réunion", "réussir", "revanche", "réveil", "réviser",
        "revoir", "revue", "richesse", "rideau", "ridicule", "rien", "rigide", "rigoler", "rincer",
        "rire", "risque", "rituel", "rival", "rivière", "robe", "robot", "roche", "rodeur",
        "rogner", "roman", "rompre", "ronce", "rond", "rose", "rosée", "rosette", "rosir",
        "rotation", "rotule", "roue", "rouge", "rouler", "route", "ruban", "rubis", "ruche",
        "rude", "rugir", "ruine", "ruisseau", "rumeur", "rural", "ruse", "rustique", "rythme",
        "sabler", "sabot", "sabre", "sac", "sachet", "sacoche", "safari", "sagesse", "saisir",
        "salade", "salive", "salle", "salon", "salto", "salut", "samedi", "sanction", "sang",
        "sarcasme", "sardine", "saturer", "saugrenu", "saumon", "sauter", "sauver", "savoir", "savon",
        "scalpel", "sceller", "scénario", "sceptre", "schéma", "science", "scinder", "score", "second",
        "seigneur", "sein", "séjour", "sel", "sélection", "selle", "selon", "semaine", "sembler",
        "semence", "séminaire", "sensuel", "sentir", "séparer", "séquence", "serein", "sergent", "sérieux",
        "serrure", "sertir", "service", "sésame", "seuil", "seul", "sevrage", "siècle", "siège",
        "siffler", "sigle", "signal", "silence", "silo", "simple", "singe", "sinon", "sinus",
        "sirop", "site", "situer", "skier", "snob", "sobre", "social", "socle", "sodium",
        "soigner", "soirée", "soixante", "solde", "soleil", "solide", "solo", "solvant", "sombre",
        "somme", "somnoler", "sonde", "songeur", "sonner", "sorte", "sosie", "sottise", "souci",
        "soudain", "souffle", "souhait", "soulever", "soupape", "source", "soutirer", "souvenir", "spacieux",
        "spatial", "spécial", "sphère", "spider", "spirale", "sport", "stade", "stagiaire", "stand",
        "star", "statue", "stock", "strident", "studieux", "stupide", "style", "subir", "subtil",
        "subvenir", "succès", "sucre", "suer", "suffire", "suivre", "sujet", "sulfite", "supposer",
        "surprendre", "surtout", "surveiller", "table", "tabou", "tache", "tacler", "tacot", "tact",
        "taie", "taille", "taire", "talon", "talus", "tandem", "tard", "tarte", "tâter",
        "tatouage", "taupe", "taureau", "taxer", "téléviser", "témoigner", "tempête", "temple", "temporel",
        "tenaille", "tendre", "tenir", "tension", "terminer", "terne", "terrible", "tête", "texte",
        "thé", "thème", "théorie", "tigre", "timide", "tissu", "titre", "toast", "toboggan",
        "toc", "toge", "toilette", "toit", "tolérer", "tomate", "tonneau", "tordre", "tornade",
        "torse", "tortue", "totem", "toucher", "tournage", "tousser", "tout", "toux", "trace",
        "traduire", "trahir", "train", "trancher", "travail", "trèfle", "tremper", "trésor", "treuil",
        "triage", "tribu", "trier", "trio", "tripe", "triste", "troc", "trois", "trombone",
        "tronc", "trop", "trotter", "trouer", "truc", "truite", "tuba", "tuer", "tuile",
        "turbo", "tutu", "tuyau", "type", "union", "unique", "unité", "univers", "urbain",
        "urchin", "urgent", "urne", "usage", "user", "usiner", "usure", "utile", "vacarme",
        "vaccin", "vagabond", "vague", "vaincre", "vaisseau", "valable", "valise", "vallon", "valoir",
        "valser", "valseur", "vampire", "vanille", "vapeur", "varier", "vasque", "vaste", "veau",
        "veille", "veine", "velcro", "vélo", "vendre", "vénérer", "venger", "venir", "vent",
        "venue", "verbe", "verdict", "verger", "verglas", "vernis", "verre", "vers", "vert",
        "veste", "vétérin", "vexer", "viande", "victime", "vide", "vie", "vieux", "vif",
        "vigie", "vigne", "ville", "vingt", "violon", "virus", "visage", "vite", "vive",
        "vivre", "vocation", "voici", "voie", "voile", "voir", "voisin", "voiture", "volaille",
        "volcan", "voler", "volt", "volume", "vorace", "vote", "vouloir", "vous", "voyage",
        "voyou", "vrac", "vrai", "yacht", "yeti", "yeux", "yoga", "zénith", "zeste",
        "zoologie", "zut"
    ]
    mots_anglais = [
        "abandon", "ability", "absence", "abuse", "academy", "accent", "access", "accident",
        "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act", "action",
        "actor", "actress", "actual", "adapt", "add", "addict", "address", "adjust", "admit",
        "adult", "advance", "advice", "aerobic", "affair", "afford", "afraid", "again", "age",
        "agent", "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
        "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone", "alpha",
        "already", "also", "alter", "always", "amateur", "amazing", "among", "amount", "amused",
        "analyst", "anchor", "ancient", "anger", "angle", "angry", "animal", "ankle", "announce",
        "annual", "another", "answer", "antenna", "antique", "anxiety", "any", "apart", "apology",
        "appear", "apple", "approve", "april", "arch", "arctic", "area", "arena", "argue",
        "arm", "armed", "armor", "army", "around", "arrange", "arrest", "arrive", "arrow",
        "art", "artefact", "artist", "artwork", "ask", "aspect", "assault", "asset", "assist",
        "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction",
        "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado", "avoid",
        "awake", "aware", "away", "awesome", "awful", "awkward", "axis", "baby", "bachelor",
        "bacon", "badge", "bag", "balance", "balcony", "ball", "bamboo", "banana", "banner",
        "bar", "barely", "bargain", "barrel", "base", "basic", "basket", "battle", "beach",
        "bean", "beauty", "because", "become", "beef", "before", "begin", "behave", "behind",
        "believe", "below", "belt", "bench", "benefit", "best", "betray", "better", "between",
        "beyond", "bicycle", "bid", "bike", "bind", "biology", "bird", "birth", "bitter",
        "black", "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood",
        "blossom", "blouse", "blue", "blur", "blush", "board", "boat", "body", "boil",
        "bomb", "bone", "bonus", "book", "boost", "border", "boring", "borrow", "boss",
        "bottom", "bounce", "box", "boy", "bracket", "brain", "brand", "brass", "brave",
        "bread", "breeze", "brick", "bridge", "brief", "bright", "bring", "brisk", "broccoli",
        "broken", "bronze", "broom", "brother", "brown", "brush", "bubble", "buddy", "budget",
        "buffalo", "build", "bulb", "bulk", "bullet", "bundle", "bunker", "burden", "burger",
        "burst", "bus", "business", "busy", "butter", "buyer", "buzz", "cabbage", "cabin",
        "cable", "cactus", "cage", "cake", "call", "calm", "camera", "camp", "can",
        "canal", "cancel", "candy", "cannon", "canoe", "canvas", "canyon", "capable", "capital",
        "captain", "car", "carbon", "card", "cargo", "carpet", "carry", "cart", "case",
        "cash", "casino", "castle", "casual", "cat", "catalog", "catch", "category", "cattle",
        "caught", "cause", "caution", "cave", "ceiling", "celery", "cement", "census", "century",
        "cereal", "certain", "chair", "chalk", "champion", "change", "chaos", "chapter", "charge",
        "chase", "chat", "cheap", "check", "cheese", "chef", "cherry", "chest", "chicken",
        "chief", "child", "chimney", "choice", "choose", "chronic", "chuckle", "chunk", "churn",
        "cigar", "cinnamon", "circle", "citizen", "city", "civil", "claim", "clap", "clarify",
        "claw", "clay", "clean", "clerk", "clever", "click", "client", "cliff", "climb",
        "clinic", "clip", "clock", "clog", "close", "cloth", "cloud", "clown", "club",
        "clump", "cluster", "clutch", "coach", "coast", "coconut", "code", "coffee", "coil",
        "coin", "collect", "color", "column", "combine", "come", "comfort", "comic", "common",
        "company", "concert", "conduct", "confirm", "congress", "connect", "consider", "control", "convince",
        "cook", "cool", "copper", "copy", "coral", "core", "corn", "correct", "cost",
        "cotton", "couch", "country", "couple", "course", "cousin", "cover", "coyote", "crack",
        "cradle", "craft", "cram", "crane", "crash", "crater", "crawl", "crazy", "cream",
        "credit", "creek", "crew", "cricket", "crime", "crisp", "critic", "crop", "cross",
        "crouch", "crowd", "crucial", "cruel", "cruise", "crumble", "crunch", "crush", "cry",
        "crystal", "cube", "culture", "cup", "cupboard", "curious", "current", "curtain", "curve",
        "cushion", "custom", "cute", "cycle", "dad", "damage", "damp", "dance", "danger",
        "daring", "dash", "daughter", "dawn", "day", "deal", "debate", "debris", "decade",
        "december", "decide", "decline", "decorate", "decrease", "deer", "defense", "define", "defy",
        "degree", "delay", "deliver", "demand", "demise", "denial", "dentist", "deny", "depart",
        "depend", "deposit", "depth", "deputy", "derive", "describe", "desert", "design", "desk",
        "despair", "destroy", "detail", "detect", "develop", "device", "devote", "diagram", "dial",
        "diamond", "diary", "dice", "diesel", "diet", "differ", "digital", "dignity", "dilemma",
        "dinner", "dinosaur", "direct", "dirt", "disagree", "discover", "disease", "dish", "dismiss",
        "disorder", "display", "distance", "divert", "divide", "divorce", "dizzy", "doctor", "document",
        "dog", "doll", "dolphin", "domain", "donate", "donkey", "donor", "door", "dose",
        "double", "dove", "draft", "dragon", "drama", "drastic", "draw", "dream", "dress",
        "drift", "drill", "drink", "drip", "drive", "drop", "drum", "dry", "duck",
        "dumb", "dune", "during", "dust", "dutch", "duty", "dwarf", "dynamic", "eager",
        "eagle", "early", "earn", "earth", "easily", "east", "easy", "echo", "ecology",
        "economy", "edge", "edit", "educate", "effort", "egg", "eight", "either", "elbow",
        "elder", "electric", "elegant", "element", "elephant", "elevator", "elite", "else", "embark",
        "embody", "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable", "enact",
        "end", "endless", "endorse", "enemy", "energy", "enforce", "engage", "engine", "enhance",
        "enjoy", "enlist", "enough", "enrich", "enroll", "ensure", "enter", "entire", "entry",
        "envelope", "episode", "equal", "equip", "era", "erase", "erode", "erosion", "error",
        "erupt", "escape", "essay", "essence", "estate", "eternal", "ethics", "evidence", "evil",
        "evoke", "evolve", "exact", "example", "excess", "exchange", "excite", "exclude", "excuse",
        "execute", "exercise", "exhaust", "exhibit", "exile", "exist", "exit", "exotic", "expand",
        "expect", "expire", "explain", "expose", "express", "extend", "extra", "eye", "eyebrow",
        "fabric", "face", "faculty", "fade", "faint", "faith", "fall", "false", "fame",
        "family", "famous", "fan", "fancy", "fantasy", "farm", "fashion", "fat", "fatal",
        "father", "fatigue", "fault", "favorite", "feature", "february", "federal", "fee", "feed",
        "feel", "female", "fence", "festival", "fetch", "fever", "few", "fiber", "fiction",
        "field", "figure", "file", "film", "filter", "final", "find", "fine", "finger",
        "finish", "fire", "firm", "first", "fiscal", "fish", "fit", "fitness", "fix",
        "flag", "flame", "flash", "flat", "flavor", "flee", "flight", "flip", "float",
        "flock", "floor", "flower", "fluid", "flush", "fly", "foam", "focus", "fog",
        "foil", "fold", "follow", "food", "foot", "force", "forest", "forget", "fork",
        "fortune", "forum", "forward", "fossil", "foster", "found", "fox", "fragile", "frame",
        "frequent", "fresh", "friend", "fringe", "frog", "front", "frost", "frown", "frozen",
        "fruit", "fuel", "fun", "funny", "furnace", "fury", "future", "gadget", "gain",
        "galaxy", "gallery", "game", "gap", "garage", "garbage", "garden", "garlic", "garment",
        "gas", "gasp", "gate", "gather", "gauge", "gaze", "general", "genius", "genre",
        "gentle", "genuine", "gesture", "ghost", "giant", "gift", "giggle", "ginger", "giraffe",
        "girl", "give", "glad", "glance", "glare", "glass", "glide", "glimpse", "globe",
        "gloom", "glory", "glove", "glow", "glue", "goat", "goddess", "gold", "good",
        "goose", "gorilla", "gospel", "gossip", "govern", "gown", "grab", "grace", "grain",
        "grant", "grape", "grass", "gravity", "great", "green", "grid", "grief", "grit",
        "grocery", "group", "grow", "grunt", "guard", "guess", "guide", "guilt", "guitar",
        "gun", "gym", "habit", "hair", "half", "hammer", "hamster", "hand", "happy",
        "harbor", "hard", "harsh", "harvest", "hat", "have", "hawk", "hazard", "head",
        "health", "heart", "heavy", "hedgehog", "height", "hello", "helmet", "help", "hen",
        "hero", "hidden", "high", "hill", "hint", "hip", "hire", "history", "hobby",
        "hockey", "hold", "hole", "holiday", "hollow", "home", "honey", "hood", "hope",
        "horn", "horror", "horse", "hospital", "host", "hotel", "hour", "hover", "hub",
        "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurdle", "hurry",
        "hurt", "husband", "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore",
        "ill", "illegal", "illness", "image", "imitate", "immense", "immune", "impact", "impose",
        "improve", "impulse", "inch", "include", "income", "increase", "index", "indicate", "indoor",
        "industry", "infant", "inflict", "inform", "inhale", "inherit", "initial", "inject", "injury",
        "inmate", "inner", "innocent", "input", "inquiry", "insane", "insect", "inside", "inspire",
        "install", "intact", "interest", "into", "invest", "invite", "involve", "iron", "island",
        "isolate", "issue", "item", "ivory", "jacket", "jaguar", "jar", "jazz", "jealous",
        "jeans", "jelly", "jewel", "job", "join", "joke", "journey", "joy", "judge",
        "juice", "jump", "jungle", "junior", "junk", "just", "kangaroo", "keen", "keep",
        "ketchup", "key", "kick", "kid", "kidney", "kind", "kingdom", "kiss", "kit",
        "kitchen", "kite", "kitten", "kiwi", "knee", "knife", "knock", "know", "lab",
        "label", "labor", "ladder", "lady", "lake", "lamp", "language", "laptop", "large",
        "later", "latin", "laugh", "laundry", "lava", "law", "lawn", "lawsuit", "layer",
        "lazy", "leader", "leaf", "learn", "leave", "lecture", "left", "leg", "legal",
        "legend", "leisure", "lemon", "lend", "length", "lens", "leopard", "lesson", "letter",
        "level", "liar", "liberty", "library", "license", "life", "lift", "light", "like",
        "limb", "limit", "link", "lion", "liquid", "list", "little", "live", "lizard",
        "load", "loan", "lobster", "local", "lock", "logic", "lonely", "long", "loop",
        "lottery", "loud", "lounge", "love", "loyal", "lucky", "luggage", "lumber", "lunar",
        "lunch", "luxury", "lyrics", "machine", "mad", "magic", "magnet", "maid", "mail",
        "main", "major", "make", "mammal", "man", "manage", "mandate", "mango", "mansion",
        "manual", "maple", "marble", "march", "margin", "marine", "market", "marriage", "mask",
        "mass", "master", "match", "material", "math", "matrix", "matter", "maximum", "maze",
        "meadow", "mean", "measure", "meat", "mechanic", "medal", "media", "melody", "melt",
        "member", "memory", "mention", "menu", "mercy", "merge", "merit", "merry", "mesh",
        "message", "metal", "method", "middle", "midnight", "milk", "million", "mimic", "mind",
        "minimum", "minor", "minute", "miracle", "mirror", "misery", "miss", "mistake", "mix",
        "mixed", "mixture", "mobile", "model", "modify", "mom", "moment", "monitor", "monkey",
        "monster", "month", "moon", "moral", "more", "morning", "mosquito", "mother", "motion",
        "motor", "mountain", "mouse", "move", "movie", "much", "muffin", "mule", "multiply",
        "muscle", "museum", "mushroom", "music", "must", "mutual", "myself", "mystery", "myth",
        "naive", "name", "napkin", "narrow", "nasty", "nation", "nature", "near", "neck",
        "need", "negative", "neglect", "neither", "nephew", "nerve", "nest", "net", "network",
        "neutral", "never", "news", "next", "nice", "night", "noble", "noise", "nominee",
        "noodle", "normal", "north", "nose", "notable", "note", "nothing", "notice", "novel",
        "now", "nuclear", "number", "nurse", "nut", "oak", "obey", "object", "oblige",
        "obscure", "observe", "obtain", "obvious", "occur", "ocean", "october", "odor", "off",
        "offer", "office", "often", "oil", "okay", "old", "olive", "olympic", "omit",
        "once", "one", "onion", "online", "only", "open", "opera", "opinion", "oppose",
        "option", "orange", "orbit", "orchard", "order", "ordinary", "organ", "orient", "original",
        "orphan", "ostrich", "other", "outdoor", "outer", "output", "outside", "oval", "oven",
        "over", "own", "owner", "oxygen", "oyster", "ozone", "pact", "paddle", "page",
        "pair", "palace", "palm", "panda", "panel", "panic", "panther", "paper", "parade",
        "parent", "park", "parrot", "party", "pass", "patch", "path", "patient", "patrol",
        "pattern", "pause", "pave", "payment", "peace", "peanut", "pear", "peasant", "pelican",
        "pen", "penalty", "pencil", "people", "pepper", "perfect", "permit", "person", "pet",
        "phone", "photo", "phrase", "physical", "piano", "picnic", "picture", "piece", "pig",
        "pigeon", "pill", "pilot", "pink", "pioneer", "pipe", "pistol", "pitch", "pizza",
        "place", "planet", "plastic", "plate", "play", "please", "pledge", "pluck", "plug",
        "plunge", "poem", "poet", "point", "polar", "pole", "police", "pond", "pony",
        "pool", "popular", "portion", "position", "possible", "post", "potato", "pottery", "poverty",
        "powder", "power", "practice", "praise", "predict", "prefer", "prepare", "present", "pretty",
        "prevent", "price", "pride", "primary", "print", "priority", "prison", "private", "prize",
        "problem", "process", "produce", "profit", "program", "project", "promote", "proof", "property",
        "prosper", "protect", "proud", "provide", "public", "pudding", "pull", "pulp", "pulse",
        "pumpkin", "punch", "pupil", "puppy", "purchase", "purity", "purpose", "purse", "push",
        "put", "puzzle", "pyramid", "quality", "quantum", "quarter", "question", "quick", "quit",
        "quiz", "quote", "rabbit", "raccoon", "race", "rack", "radar", "radio", "rail",
        "rain", "raise", "rally", "ramp", "ranch", "random", "range", "rapid", "rare",
        "rate", "rather", "raven", "raw", "razor", "ready", "real", "reason", "rebel",
        "rebuild", "recall", "receive", "recipe", "record", "recycle", "reduce", "reflect", "reform",
        "refuse", "region", "regret", "regular", "reject", "relax", "release", "relief", "rely",
        "remain", "remember", "remind", "remove", "render", "renew", "rent", "reopen", "repair",
        "repeat", "replace", "report", "require", "rescue", "resemble", "resist", "resource", "response",
        "result", "retire", "retreat", "return", "reunion", "reveal", "review", "reward", "rhythm",
        "rib", "ribbon", "rice", "rich", "ride", "ridge", "rifle", "right", "rigid",
        "ring", "riot", "ripple", "risk", "ritual", "rival", "river", "road", "roast",
        "robot", "robust", "rocket", "romance", "roof", "rookie", "room", "rose", "rotate",
        "rough", "round", "route", "royal", "rubber", "rude", "rug", "rule", "run",
        "runway", "rural", "sad", "saddle", "sadness", "safe", "sail", "salad", "salmon",
        "salon", "salt", "salute", "same", "sample", "sand", "satisfy", "satoshi", "sauce",
        "sausage", "save", "say", "scale", "scan", "scare", "scatter", "scene", "scheme",
        "school", "science", "scissors", "scorpion", "scout", "scrap", "screen", "script", "scrub",
        "sea", "search", "season", "seat", "second", "secret", "section", "security", "seed",
        "seek", "segment", "select", "sell", "seminar", "senior", "sense", "sentence", "series",
        "service", "session", "settle", "setup", "seven", "shadow", "shaft", "shallow", "share",
        "shed", "shell", "sheriff", "shield", "shift", "shine", "ship", "shiver", "shock",
        "shoe", "shoot", "shop", "short", "shoulder", "shove", "shrimp", "shrug", "shuffle",
        "shy", "sibling", "sick", "side", "siege", "sight", "sign", "silent", "silk",
        "silly", "silver", "similar", "simple", "since", "sing", "siren", "sister", "situate",
        "six", "size", "skate", "sketch", "ski", "skill", "skin", "skirt", "skull",
        "slab", "slam", "sleep", "slender", "slice", "slide", "slight", "slim", "slogan",
        "slot", "slow", "slush", "small", "smart", "smile", "smoke", "smooth", "snack",
        "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock", "soda",
        "soft", "solar", "soldier", "solid", "solution", "solve", "someone", "song", "soon",
        "sorry", "sort", "soul", "sound", "soup", "source", "south", "space", "spare",
        "spatial", "spawn", "speak", "special", "speed", "spell", "spend", "sphere", "spice",
        "spider", "spike", "spin", "spirit", "split", "spoil", "sponsor", "spoon", "sport",
        "spot", "spray", "spread", "spring", "spy", "square", "squeeze", "squirrel", "stable",
        "stadium", "staff", "stage", "stairs", "stamp", "stand", "start", "state", "stay",
        "steak", "steel", "stem", "step", "stereo", "stick", "still", "sting", "stock",
        "stomach", "stone", "stool", "story", "stove", "strategy", "street", "strike", "strong",
        "struggle", "student", "stuff", "stumble", "style", "subject", "submit", "subway", "success",
        "such", "sudden", "suffer", "sugar", "suggest", "suit", "summer", "sun", "sunny",
        "sunset", "super", "supply", "supreme", "sure", "surface", "surge", "surprise", "surround",
        "survey", "suspect", "sustain", "swallow", "swamp", "swap", "swarm", "swear", "sweet",
        "swift", "swim", "swing", "switch", "sword", "symbol", "symptom", "syrup", "system",
        "table", "tackle", "tag", "tail", "talent", "talk", "tank", "tape", "target",
        "task", "taste", "tattoo", "taxi", "teach", "team", "tell", "ten", "tenant",
        "tennis", "tent", "term", "test", "text", "thank", "that", "theme", "then",
        "theory", "there", "they", "thing", "this", "thought", "three", "thrive", "throw",
        "thumb", "thunder", "ticket", "tide", "tiger", "tilt", "timber", "time", "tiny",
        "tip", "tired", "tissue", "title", "toast", "tobacco", "today", "toddler", "toe",
        "together", "toilet", "token", "tomato", "tomorrow", "tone", "tongue", "tonight", "tool",
        "tooth", "top", "topic", "topple", "torch", "tornado", "tortoise", "toss", "total",
        "tourist", "toward", "tower", "town", "toy", "track", "trade", "traffic", "tragic",
        "train", "transfer", "trap", "trash", "travel", "tray", "treat", "tree", "trend",
        "trial", "tribe", "trick", "trigger", "trim", "trip", "trophy", "trouble", "truck",
        "true", "truly", "trumpet", "trust", "truth", "try", "tube", "tuition", "tumble",
        "tuna", "tunnel", "turkey", "turn", "turtle", "twelve", "twenty", "twice", "twin",
        "twist", "two", "type", "typical", "ugly", "umbrella", "unable", "unaware", "uncle",
        "uncover", "under", "undo", "unfair", "unfold", "unhappy", "uniform", "unique", "unit",
        "universe", "unknown", "unlock", "until", "unusual", "unveil", "update", "upgrade", "uphold",
        "upon", "upper", "upset", "urban", "urge", "usage", "use", "used", "useful",
        "useless", "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve",
        "van", "vanish", "vapor", "various", "vast", "vault", "vehicle", "velvet", "vendor",
        "venture", "venue", "verb", "verify", "version", "very", "vessel", "veteran", "viable",
        "vibrant", "vicious", "victory", "video", "view", "village", "vintage", "violin", "virtual",
        "virus", "visa", "visit", "visual", "vital", "vivid", "vocal", "voice", "void",
        "volcano", "volume", "vote", "voyage", "wage", "wagon", "wait", "walk", "wall",
        "walnut", "want", "warfare", "warm", "warrior", "wash", "wasp", "waste", "water",
        "wave", "way", "wealth", "weapon", "wear", "weasel", "weather", "web", "wedding",
        "week", "weird", "welcome", "west", "wet", "whale", "what", "wheat", "wheel",
        "when", "where", "whip", "whisper", "wide", "width", "wife", "wild", "will",
        "win", "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom",
        "wise", "wish", "witness", "wolf", "woman", "wonder", "wood", "wool", "word",
        "work", "world", "worry", "worth", "wrap", "wreck", "wrestle", "wrist", "write",
        "wrong", "yard", "year", "yellow", "you", "young", "youth", "zebra", "zero",
        "zone", "zoo"
    ]
    choisi = False
    mot_choisi = ""

    while not choisi:
        print("A quel mode voulez-vous jouer ? ")
        print("1) Mot français aléatoire")
        print("2) Mot anglais aléatoire")
        print("3) Mot aléatoire anglais ou français")
        print("4) Deux joueurs, un entre le mot et l'autre devine")
        print("Choisissez une option (1-4)")
        print("===================================================")

        try:
            ModeDeJeu = int(input("> "))

            if ModeDeJeu not in [1, 2, 3, 4]:
                print("Veuillez choisir une option valide (1-4).")
                continue
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue

        print("\n\n\n\n\n\n\n")

        if ModeDeJeu == 1:
            print("=== Mode de jeu mot français ===")
            mot_choisi = random.choice(mots_francais).lower()
            choisi = True
        elif ModeDeJeu == 2:
            print("=== Mode de jeu mot anglais ===")
            mot_choisi = random.choice(mots_anglais).lower()
            choisi = True
        elif ModeDeJeu == 3:
            print("=== Mode de jeu langue aléatoire ===")
            liste = ["anglais", "français"]
            langue = random.choice(liste)

            if langue == "français":
                print(f"Mot de langue {langue} !")
                mot_choisi = random.choice(mots_francais).lower()
                choisi = True
            elif langue == "anglais":
                print(f"Mot de langue {langue} !")
                mot_choisi = random.choice(mots_anglais).lower()
                choisi = True
        elif ModeDeJeu == 4:
            print("=== Mode de jeu duo ===")
            print("Le joueur 1 va choisir le mot et le joueur")

            while True:
                langue = input("Entrez la langue du mot: ")
                langues = ["invention", "anglais", "chinois", "hindi", "espagnol", "français", "arabe", "bengali",
                           "russe", "portugais", "indonésien", "ourdou", "allemand", "japonais", "swahili", "telugu",
                           "marathi", "turc", "tamoul", "vietnamien", "coréen", "italien", "yoruba", "oriya", "kannada",
                           "gujarati", "polonais", "ouzbek", "bhojpuri", "pendjabi", "malais", "hausa", "tamazight",
                           "kurde", "serbe", "néerlandais", "roumain", "cingalais", "népalais", "zoulou", "tchèque",
                           "birman", "kinyarwanda", "amharique", "oromo", "afrikaans", "somali", "bulgarie", "hongrois",
                           "slovaque", "lingala", "grec", "télougou", "bengali", "malayalam", "farsi", "maltais",
                           "akan", "azerbaijanais", "georgien", "bosniaque", "kiswahili", "catalan", "esperanto",
                           "tigrinya", "mongol", "sindhi", "latvian", "kazakh", "ukrainien", "quechua", "bielorusse",
                           "tatar", "gujarati", "bambara", "macedonien", "islandais", "kurde", "malais", "bulgare",
                           "hebreu", "twi", "fulfulde", "kirundi", "luxembourgeois", "ouïgour", "inuktitut",
                           "mazandarani", "wolof", "xhosa", "yoruba", "assamais", "cebuano", "khmer",
                           "tamazight", "mossi", "shona", "géorgien"]

                if langue.lower() not in langues:
                    print("Veuillez entrer une langue valide.")
                    print(f"Voici les langues disponibles : {langues}")
                    continue

                break

            while True:
                mot_choisi = input("Entrez le mot choisi : ").lower()

                if not mot_choisi.isalpha():
                    print("Veuillez entrer un mot valide (lettres uniquement).")
                    continue

                break

            for i in range(1000):
                print("\n")
            if langue != "invention":
                print(f"Le mot choisi est de langue {langue} ! ")
                choisi = True
            elif langue == "invention":
                print("Le mot choisi est d'une langue inventée ou qui n'est pas dans la liste ! ")
                choisi = True

    mot_trouve = [mot_choisi[0]] + ["_"] * (len(mot_choisi) - 1)
    tentatives_max = 7
    tentatives = 0
    lettres_proposees = []

    print("Bienvenue dans le jeu Pendu !")
    print("Le mot à deviner contient", len(mot_choisi), "lettres.")

    while True:
        print(afficher_pendu(tentatives))
        print("Mot actuel:", " ".join(mot_trouve))
        proposition = input("Proposez une lettre : ").lower()

        if len(proposition) != 1 or not proposition.isalpha():
            print("Veuillez entrer une lettre.")
            continue

        if proposition in lettres_proposees:
            print("Vous avez déjà proposé cette lettre.")
            continue

        lettres_proposees.append(proposition)

        if proposition in mot_choisi:
            for i in range(len(mot_choisi)):
                if mot_choisi[i] == proposition:
                    mot_trouve[i] = proposition
            if "_" not in mot_trouve:
                print("Mot actuel:", " ".join(mot_trouve))
                print("Félicitations ! Vous avez deviné le mot :", "".join(mot_trouve))
                print("\n\n")
                print("Voulez-vous rejouer ?")
                print("1) Oui")
                print("2) Non")
                print("\n\n\n")
                c = 0
                while True:
                    try:
                        c = int(input("> "))

                        if c not in [1, 2]:
                            print("Veuillez choisir une option valide (1-2).")
                            continue
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                        continue

                    break

                if c == 1:
                    jeu_pendu()
                elif c == 2:
                    break
        else:
            tentatives += 1
            print("La lettre proposée n'est pas présente dans le mot.")

        print("Tentatives restantes :", tentatives_max - tentatives)

        if tentatives == tentatives_max:
            print(afficher_pendu(tentatives))
            print("Dommage ! Vous avez épuisé toutes vos tentatives.")
            print("Le mot à deviner était :", mot_choisi)
            print("\n\n")
            print("Voulez-vous rejouer ?")
            print("1) Oui")
            print("2) Non")
            print("\n\n\n")
            c = 0

            while True:
                try:
                    c = int(input("> "))

                    if c not in [1, 2]:
                        print("Veuillez choisir une option valide (1-2).")
                        continue
                except ValueError:
                    print("Veuillez entrer un nombre valide.")
                    continue

                break

            if c == 1:
                jeu_pendu()
            elif c == 2:
                break

        if tentatives > tentatives_max:
            print("Erreur : Le nombre de tentatives a dépassé la limite maximale.")
            break


def description_jeu_pendu():
    try:
        print("=== Bienvenue dans le jeu Pendu ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
                jeu_pendu()
        elif choix == 2:
            print("Le but du jeu est de deviner un mot en proposant des lettres.\n")
            print("Vous pouvez choisir parmi plusieurs modes de jeu :")
            print("1) Mot français aléatoire")
            print("2) Mot anglais aléatoire")
            print("3) Mot aléatoire anglais ou français")
            print("4) Deux joueurs, un entre le mot et l'autre devine\n\n")
            print("Dans les modes 1 à 3, un mot sera choisi aléatoirement selon les critères spécifiés.")
            print("Dans le mode 4, le joueur 1 choisit le mot et le joueur 2 tente de le deviner.\n")
            print("Vous avez un nombre limité de tentatives pour deviner le mot.")
            print("Si vous devinez toutes les lettres du mot, vous gagnez.")
            print("Sinon, si vous épuisez toutes vos tentatives, vous perdez.\n")
            print("Amusez-vous bien et bonne chance !\n\n\n\n\n")
            description_jeu_pendu()
        else:
            description_jeu_pendu()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################

symbole_joueur1 = ""
symbole_joueur2 = ""


def afficher_grille_morpion(grille):
    print("-------------")
    for i in range(3):
        for j in range(3):
            print("|", grille[i][j], end=" ")
        print("|")
        print("-------------")


def verifier_victoire_morpion(grille, joueur):
    for i in range(3):
        if grille[i][0] == grille[i][1] == grille[i][2] == joueur:
            return True

    for j in range(3):
        if grille[0][j] == grille[1][j] == grille[2][j] == joueur:
            return True

    if grille[0][0] == grille[1][1] == grille[2][2] == joueur:
        return True
    if grille[0][2] == grille[1][1] == grille[2][0] == joueur:
        return True

    return False


def choisir_symboles(joueur1, joueur2):
    global symbole_joueur1, symbole_joueur2

    symboles = ["X", "O"]
    symbole_joueur1 = input(f"{joueur1}, choisissez un symbole (X ou O) : ")
    while symbole_joueur1 not in symboles:
        symbole_joueur1 = input("Veuillez choisir un symbole valide (X ou O) : ")

    symbole_joueur2 = symboles[1 - symboles.index(symbole_joueur1)]


def jouer_morpion():
    global symbole_joueur1, symbole_joueur2

    joueur1 = input("Entrez le nom du Joueur 1 : ")
    joueur2 = input("Entrez le nom du Joueur 2 : ")
    continuer = True
    while continuer:
        grille = [[" " for _ in range(3)] for _ in range(3)]

        if symbole_joueur1 == "" or symbole_joueur2 == "":
            choisir_symboles(joueur1, joueur2)

        print(f"{joueur1} jouera avec le symbole '{symbole_joueur1}'")
        print(f"{joueur2} jouera avec le symbole '{symbole_joueur2}'")

        joueurs = [(joueur1, symbole_joueur1), (joueur2, symbole_joueur2)]
        random.shuffle(joueurs)
        joueur_courant = joueurs[0]

        print(f"{joueur_courant[0]} commence !")

        while True:
            afficher_grille_morpion(grille)

            while True:
                try:
                    ligne = int(input(f"{joueur_courant[0]}, choisissez une ligne (1-3) : "))
                    colonne = int(input(f"{joueur_courant[0]}, choisissez une colonne (1-3) : "))

                    if ligne < 1 or ligne > 3 or colonne < 1 or colonne > 3:
                        raise ValueError
                    if grille[ligne - 1][colonne - 1] != " ":
                        raise ValueError

                    break

                except ValueError:
                    print("Veuillez entrer des coordonnées valides (1-3) pour une case libre.")

            grille[ligne - 1][colonne - 1] = joueur_courant[1]

            if verifier_victoire_morpion(grille, joueur_courant[1]):
                afficher_grille_morpion(grille)
                print(f"Bravo {joueur_courant[0]} ! Vous avez gagné !")
                break
            elif all(grille[i][j] != " " for i in range(3) for j in range(3)):
                afficher_grille_morpion(grille)
                print("Match nul !")
                break

            joueur_courant = joueurs[1] if joueur_courant == joueurs[0] else joueurs[0]

            print("\n" * 5)

        choix = input("Voulez-vous rejouer ? (1: Oui, 2: Non) : ")
        while choix != "1" and choix != "2":
            choix = input("Veuillez entrer 1 pour rejouer ou 2 pour arrêter : ")

        if choix == "1":
            for i in range(1000):
                print("\n")

        if choix == "2":
            continuer = False


def description_jeu_morpion():
    try:
        print("=== Bienvenue au jeu Morpion ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
            jouer_morpion()
        elif choix == 2:
            for i in range(100):
                print("\n")
            print("\n\n\nLe Morpion est un jeu de plateau pour deux joueurs.\n")
            print("Le plateau de jeu est une grille de 3x3 cases.\n")
            print("Chaque joueur choisit un symbole, soit 'X' soit 'O'.\n")
            print("Les joueurs alternent ensuite pour placer leur symbole sur une case vide du plateau.\n")
            print(
                "Le premier joueur à aligner trois de ses symboles horizontalement, verticalement ou en diagonale gagne la partie.\n")
            print(
                "Si toutes les cases sont remplies sans qu'un joueur n'ait aligné trois symboles, la partie est déclarée nulle.\n\n")
            print("Amusez-vous bien !\n\n\n")
            return description_jeu_morpion()
        else:
            return description_jeu_morpion()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 20
INVINCIBILITY_TIME = 3000


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH // 2 - self.rect.width // 2
        self.rect.y = WINDOW_HEIGHT - self.rect.height
        self.invincible = False
        self.last_collision_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        current_time = pygame.time.get_ticks()
        if self.invincible or current_time - self.last_collision_time < INVINCIBILITY_TIME:
            self.image.fill(GREEN)
        else:
            self.image.fill(PURPLE)

    def reset(self):
        self.invincible = False
        self.last_collision_time = 0

    def handle_collision(self):
        self.last_collision_time = pygame.time.get_ticks()


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.color = random.choice([BLUE, RED, GREEN, YELLOW])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        liste = [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 4,
                 4, 4, 2, 3, 4, 5, 5, 5, 6, 6, 7, 2, 3, 7, 7, 5, 5, 5]
        self.speed_y = random.choice(liste)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = -BLOCK_HEIGHT
            self.rect.x = random.randint(0, WINDOW_WIDTH - BLOCK_WIDTH)
            self.color = random.choice([BLUE, RED, GREEN, YELLOW])
            self.image.fill(self.color)


def jouer_Color_game():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for _ in range(25):
        x = random.randint(0, WINDOW_WIDTH - BLOCK_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        block = Block(x, y)
        all_sprites.add(block)
        blocks.add(block)

    score = 0
    score_timer = pygame.time.get_ticks()

    menu_font = pygame.font.Font(None, 48)
    menu_text = menu_font.render("Dodger's Rush", True, BLUE)

    play_font = pygame.font.Font(None, 36)
    play_text = play_font.render("Jouer", True, WHITE)

    quit_font = pygame.font.Font(None, 36)
    quit_text = quit_font.render("Quitter", True, WHITE)

    menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    play_rect = play_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
    quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))

    menu_active = True
    playing = False

    running = True
    start_time = 0
    current_time = 0
    while running:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_active:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_rect.collidepoint(mouse_pos):
                        menu_active = False
                        playing = True
                    elif quit_rect.collidepoint(mouse_pos):
                        running = False
                elif not playing:
                    menu_active = True

        if menu_active:
            score = 0
            current_time = current_time - start_time
            start_time = pygame.time.get_ticks()
            window.fill(BLACK)
            window.blit(menu_text, menu_rect)
            window.blit(play_text, play_rect)
            window.blit(quit_text, quit_rect)
            pygame.display.flip()
            continue

        if playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            player.reset()

            all_sprites.update()

            collisions = pygame.sprite.spritecollide(player, blocks, False)
            if collisions:
                current_time = pygame.time.get_ticks()
                if current_time - player.last_collision_time >= INVINCIBILITY_TIME:
                    playing = False
                for block in collisions:
                    block.rect.y = -BLOCK_HEIGHT
                    player.handle_collision()

            current_time = pygame.time.get_ticks()

            if current_time - score_timer >= 1000 and current_time > 3000:
                score += 1
                score_timer = current_time

            window.fill(BLACK)
            all_sprites.draw(window)
            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(score), True, WHITE)
            window.blit(score_text, (10, 10))
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()


def description_jeu_Dodgers_Rush():
    try:
        print("=== Bienvenue sur le jeu Dodger's Rush ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
            jouer_Color_game()
        elif choix == 2:
            for i in range(100):
                print("\n")
            print("""
Le jeu auquel vous jouez est une version simplifiée du jeu "Dodger's Rush". Dans ce jeu, vous contrôlez un personnage représenté par un carré violet et votre objectif est d'éviter les blocs qui tombent du haut de l'écran.

Si votre personnage entre en collision avec l'un des blocs, vous perdez la partie. Le jeu se termine et vous devez recommencer depuis le début pour essayer d'obtenir un meilleur score.

Pour déplacer votre personnage, vous pouvez utiliser les touches gauche et droite du clavier. Vous pouvez déplacer votre personnage vers la gauche en appuyant sur la touche gauche et vers la droite en appuyant sur la touche droite.
"""
                  )
            print("Amusez-vous bien !\n\n\n")
            return description_jeu_Dodgers_Rush()
        else:
            return description_jeu_Dodgers_Rush()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################


YELLOW2 = (255, 255, 98)
BLUE2 = (135, 206, 235)
DARK_BLUE = (0, 0, 102)
BROWN = (179, 139, 109)
SCREEN_WIDTH_space = 800
SCREEN_HEIGHT_space = 600
NUM_LEVELS_space = 11
NUM_CLOUDS_PER_LEVEL_space = 5
CLOUD_SPEED_INCREMENT_space = 1
CLOUD_WIDTH_space = 70
CLOUD_HEIGHT_space = 50
CLOUD_MIN_SPEED_space = 3
CLOUD_MAX_SPEED_space = 8
CLOUD_GAP_space = 200
CLOUD_VERTICAL_MARGIN_space = 150
PLAYER_WIDTH_space = 30
PLAYER_HEIGHT_space = 30
PLAYER_SPEED_space = 5
END_SCREEN_SPEED_MULTIPLIER_space = 1.3


def draw_text_Space_Lost_Bird(text, font, color, x, y, screen):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def show_menu_Space_Lost_Bird(screen, clock):
    menu_running = True

    jouer_button_rect = pygame.Rect(
        SCREEN_WIDTH_space // 2 - 50, SCREEN_HEIGHT_space // 2, 100, 50)
    quitter_button_rect = pygame.Rect(
        SCREEN_WIDTH_space // 2 - 50, SCREEN_HEIGHT_space // 2 + 50, 100, 50)

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if jouer_button_rect.collidepoint(mouse_pos):
                    return True
                elif quitter_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

        screen.fill(DARK_BLUE)
        font = pygame.font.Font(None, 36)
        draw_text_Space_Lost_Bird("Space Lost Bird", pygame.font.Font(None, 50), YELLOW2, SCREEN_WIDTH_space // 2 - 130,
                                  SCREEN_HEIGHT_space // 2 - 70, screen)
        pygame.draw.rect(screen, DARK_BLUE, jouer_button_rect)
        pygame.draw.rect(screen, DARK_BLUE, quitter_button_rect)
        draw_text_Space_Lost_Bird("Jouer", font, BLUE2, SCREEN_WIDTH_space // 2 - 35, SCREEN_HEIGHT_space // 2 + 10,
                                  screen)
        draw_text_Space_Lost_Bird("Quitter", font, BLUE2, SCREEN_WIDTH_space // 2 - 50, SCREEN_HEIGHT_space // 2 + 60,
                                  screen)

        pygame.display.update()
        clock.tick(60)


def run_level_Space_Lost_Bird(level, total_score, PLAYER_START_X, PLAYER_START_Y, screen, clock):
    player_x = PLAYER_START_X
    player_y = PLAYER_START_Y
    player_dy = 0

    clouds = []
    nombre = NUM_CLOUDS_PER_LEVEL_space
    if level >= 8:
        nombre = 6
    for _ in range(nombre):
        cloud_speed = random.randint(CLOUD_MIN_SPEED_space + (CLOUD_SPEED_INCREMENT_space * (level - 1)),
                                     CLOUD_MAX_SPEED_space + (CLOUD_SPEED_INCREMENT_space * (level - 1)))
        cloud_direction = random.choice([-1, 1])

        if cloud_direction == -1:
            cloud_x = SCREEN_WIDTH_space
        else:
            cloud_x = -CLOUD_WIDTH_space

        cloud_y = random.randint(CLOUD_VERTICAL_MARGIN_space,
                                 SCREEN_HEIGHT_space - CLOUD_HEIGHT_space - CLOUD_VERTICAL_MARGIN_space)

        clouds.append([cloud_x, cloud_y, cloud_speed, cloud_direction])

    score = 0

    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_dy = -10
        if level <= 5:
            screen.fill(BLUE2)
        else:
            screen.fill(DARK_BLUE)

        player_y += player_dy
        player_dy += 1

        if player_y >= SCREEN_HEIGHT_space - PLAYER_HEIGHT_space:
            player_y = SCREEN_HEIGHT_space - PLAYER_HEIGHT_space
            player_dy = 0

        pygame.draw.rect(screen, YELLOW2, (player_x, player_y, PLAYER_WIDTH_space, PLAYER_HEIGHT_space))

        for cloud in clouds:
            cloud_x, cloud_y, cloud_speed, cloud_direction = cloud

            if cloud_direction == -1:
                cloud_x -= cloud_speed
                if cloud_x < -CLOUD_WIDTH_space:
                    cloud_x = SCREEN_WIDTH_space
                    cloud_y = random.randint(CLOUD_VERTICAL_MARGIN_space,
                                             SCREEN_HEIGHT_space - CLOUD_HEIGHT_space - CLOUD_VERTICAL_MARGIN_space)
            else:
                cloud_x += cloud_speed
                if cloud_x > SCREEN_WIDTH_space:
                    cloud_x = -CLOUD_WIDTH_space
                    cloud_y = random.randint(CLOUD_VERTICAL_MARGIN_space,
                                             SCREEN_HEIGHT_space - CLOUD_HEIGHT_space - CLOUD_VERTICAL_MARGIN_space)

            cloud[0] = cloud_x
            if level <= 5:
                pygame.draw.rect(screen, WHITE, (cloud_x, cloud_y, CLOUD_WIDTH_space, CLOUD_HEIGHT_space))
            else:
                pygame.draw.rect(screen, BROWN, (cloud_x, cloud_y, CLOUD_WIDTH_space, CLOUD_HEIGHT_space))

            if (
                    player_x + PLAYER_WIDTH_space > cloud_x
                    and player_x < cloud_x + CLOUD_WIDTH_space
                    and player_y + PLAYER_HEIGHT_space > cloud_y
                    and player_y < cloud_y + CLOUD_HEIGHT_space
            ):
                return -1, total_score

        font = pygame.font.Font(None, 30)
        draw_text_Space_Lost_Bird("Niveau: {}".format(level), font, WHITE, 10, 10, screen)
        draw_text_Space_Lost_Bird("Temps (ms): {}".format(total_score + score), font, WHITE, 10, 40, screen)

        pygame.display.update()
        clock.tick(60)

        if player_y <= 0:
            return score, total_score + score

        score += 1

    return -1, total_score


def end_level_screen_Space_Lost_Bird(level, total_score, clock, screen):
    end_screen_running = True

    while end_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        if level <= 5:
            screen.fill(BLUE2)
        else:
            screen.fill(DARK_BLUE)
        font = pygame.font.Font(None, 36)
        score_s = str(ms_to_seconds(int(total_score))) + " secondes"
        if level != 5 and level != 10:
            draw_text_Space_Lost_Bird("Niveau {} terminé !".format(level), font, WHITE, SCREEN_WIDTH_space // 2 - 150,
                                      SCREEN_HEIGHT_space // 2 - 50,
                                      screen)
            draw_text_Space_Lost_Bird("Temps actuel: {}".format(score_s), font, WHITE, SCREEN_WIDTH_space // 2 - 100,
                                      SCREEN_HEIGHT_space // 2,
                                      screen)
            draw_text_Space_Lost_Bird("Appuyez sur Entrée pour passer au niveau suivant", font, WHITE,
                                      SCREEN_WIDTH_space // 2 - 300,
                                      SCREEN_HEIGHT_space // 2 + 50, screen)
        elif level == 5:
            draw_text_Space_Lost_Bird("Niveau {} terminé !".format(level), font, WHITE, SCREEN_WIDTH_space // 2 - 150,
                                      SCREEN_HEIGHT_space // 2 - 50,
                                      screen)
            draw_text_Space_Lost_Bird("Temps actuel: {}".format(score_s), font, WHITE, SCREEN_WIDTH_space // 2 - 100,
                                      SCREEN_HEIGHT_space // 2,
                                      screen)
            draw_text_Space_Lost_Bird("Appuyez sur Entrée pour passer au niveau suivant", font, WHITE,
                                      SCREEN_WIDTH_space // 2 - 300,
                                      SCREEN_HEIGHT_space // 2 + 50, screen)
            draw_text_Space_Lost_Bird(f"Bravo vous avez atteint l'espace !", pygame.font.Font(None, 48), DARK_BLUE,
                                      SCREEN_WIDTH_space - 680,
                                      SCREEN_HEIGHT_space - 400, screen)
        elif level == 10:
            draw_text_Space_Lost_Bird(f"Vous avez terminé tous les niveaux, avec un temps de {score_s} !",
                                      pygame.font.Font(None, 30),
                                      WHITE, SCREEN_WIDTH_space - 750,
                                      SCREEN_HEIGHT_space - 550, screen)

            draw_text_Space_Lost_Bird(f"Bravo, l'oiseau peut rentrer chez lui !", pygame.font.Font(None, 48), YELLOW2,
                                      SCREEN_WIDTH_space - 680,
                                      SCREEN_HEIGHT_space // 2 + 50, screen)
            draw_text_Space_Lost_Bird(
                "Appuyez sur Entrée pour revenir à l'accueil et enregistrer votre temps au classement",
                pygame.font.Font(None, 20), WHITE, SCREEN_WIDTH_space // 2 - 250, SCREEN_HEIGHT_space // 2, screen)

        pygame.display.update()
        clock.tick(60)


def lancer_Space_Lost_Bird(player_name):
    pygame.init()
    pygame.mixer.init()

    PLAYER_START_X = SCREEN_WIDTH_space // 2 - PLAYER_WIDTH_space // 2
    PLAYER_START_Y = SCREEN_HEIGHT_space - PLAYER_HEIGHT_space
    screen = pygame.display.set_mode((SCREEN_WIDTH_space, SCREEN_HEIGHT_space))
    pygame.display.set_caption("Space Lost Bird")

    clock = pygame.time.Clock()

    while True:
        total_score = 10
        if show_menu_Space_Lost_Bird(screen, clock):
            current_level = 1
            game_over = False
            pygame.mixer.music.load("Eterna_Forest.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.01)
            while current_level <= NUM_LEVELS_space and not game_over:
                score, total_score = run_level_Space_Lost_Bird(current_level, total_score, PLAYER_START_X,
                                                               PLAYER_START_X, screen, clock)

                if score == -1:
                    game_over = True
                    total_score = 0
                    break
                end_level_screen_Space_Lost_Bird(current_level, total_score, clock, screen)
                current_level += 1

                if current_level == 6:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("dark_theme.mp3")
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.01)

                if current_level == 11:
                    score_final = total_score
                    with open("classement_Space_Lost_Bird.txt", "a") as file:
                        file.write("{}: {}\n".format(player_name, total_score))
                    game_over = True
                    total_score = 0
                    break


def ms_to_seconds(milliseconds):
    seconds = milliseconds / 1000
    return seconds


def description_Space_Lost_Bird():
    try:
        print("=== Bienvenue sur le jeu Space Lost Bird ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        print("3. Classement des meilleures performances")
        choix = int(input("Choisissez une option (1-3) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
            username = input("Entrez votre nom de joueur: ")
            lancer_Space_Lost_Bird(username)
        elif choix == 2:
            for i in range(100):
                print("\n")
            print("""
Dans Space Lost Bird, tu incarnes un jeune oiseau venu d'une autre planète qui s'est retrouvé sur la Terre.

Ton objectif est de l'aider à rejoindre l'espace et sa planète d'origine en évitant les obstacles sur son chemin.

Le jeu se déroule sur plusieurs niveaux. À chaque niveau, tu te retrouves dans un paysage rempli de d'obstacles.

Des nuages néfastes de différentes formes et tailles se déplacent horizontalement à des vitesses variables dans les 5 premiers niveaux.

Puis des astéroïdes encore plus rapides seront présent dans les 5 derniers niveaux.

Tu dois contrôler l'oiseau en utilisant la barre d'espace pour sauter et éviter les obstacles.

Si tu entres en collision avec un obstacles, tu perds.

Au fur et à mesure que tu progresses dans les niveaux, la vitesse des obtacles augmente, rendant le jeu plus difficile. Tu dois être rapide et agile pour sauter au bon moment et éviter les obstacles.

Chaque fois que tu atteins le sommet de l'écran, tu passes au niveau suivant.

 À la fin de chaque niveau, tu obtiens ton temps actuel. Si tu réussis à terminer tous les niveaux, tu atteins enfin l'espace et ta planète d'origine, réalisant ainsi ton objectif ultime.

"Reach The Space" est un jeu d'adresse et de réflexes qui mettra à l'épreuve ta coordination et ta capacité à anticiper les mouvements des obstacles.


2Prêt à guider cet oiseau interplanétaire vers son destin cosmique ?


Amuse-toi bien et bonne chance dans ton voyage vers l'espace !"""
                  )
            print("\n\n\n")
            return description_Space_Lost_Bird()
        elif choix == 3:
            with open("classement_Space_Lost_Bird.txt", "r") as file:
                lines = file.readlines()
            print("\n\n\n=== Leaderboard ===\n\n\n")
            data = []
            for line in lines:
                parts = line.strip().split(
                    ": ")
                if len(parts) == 2:
                    player_name = parts[0]
                    total_score = ms_to_seconds(int(parts[1]))
                    data.append((player_name, total_score))
            sorted_data = sorted(data, key=lambda x: x[1], reverse=False)
            top_players = sorted_data[:5]
            place = 1
            for player in top_players:
                print(f"{place})", player[0], "temps: ", player[1], " secondes")
                place += 1

            print("\n\n\n\n")
            description_Space_Lost_Bird()
        else:
            return description_Space_Lost_Bird()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################

SCREEN_WIDTH_flappy = 288
SCREEN_HEIGHT_flappy = 512

BIRD_WIDTH = 40
BIRD_HEIGHT = 40

MENU_flappy = 0
PLAYING_flappy = 1
GAME_OVER_flappy = 2


def load_image_safe(filename, width=None, height=None, default_color=(100, 100, 100)):
    """Charge une image avec gestion d'erreur. Crée une surface colorée si l'image n'existe pas."""
    try:
        img = pygame.image.load(filename)
        if width and height:
            img = pygame.transform.scale(img, (width, height))
        return img
    except (pygame.error, FileNotFoundError):
        print(f"Attention: Image '{filename}' introuvable. Utilisation d'une image de remplacement.")
        if width and height:
            surface = pygame.Surface((width, height))
        else:
            surface = pygame.Surface((100, 100))
        surface.fill(default_color)
        return surface


# Chargement des images
background_img_flappy = load_image_safe("flapp.png", SCREEN_WIDTH_flappy, SCREEN_HEIGHT_flappy, (135, 206, 235))
top_pipe_img = load_image_safe("top_pipe.png", 52, 320, (0, 200, 0))
bottom_pipe_img = load_image_safe("bottom_pipe.png", 52, 320, (0, 200, 0))


def choix_oiseau():
    try:
        print(
            "Veuillez choisir votre oiseau : \n1) Flappy bird\n2) Doge bird\n3) Nyan bird\n4) Cool bird\n5) Weird bird\n6) Angry bird")
        choix = int(input("> "))
        if choix == 1:
            bird_img = load_image_safe("flappy-bird.png", BIRD_WIDTH, BIRD_HEIGHT, (255, 255, 0))
            return bird_img
        elif choix == 2:
            bird_img = load_image_safe("flappy_bird.png", BIRD_WIDTH, BIRD_HEIGHT, (255, 200, 100))
            return bird_img
        elif choix == 3:
            bird_img = load_image_safe("nyan_bird.png", BIRD_WIDTH, BIRD_HEIGHT, (255, 105, 180))
            return bird_img
        elif choix == 4:
            bird_img = load_image_safe("cool_bird.png", BIRD_WIDTH, BIRD_HEIGHT, (0, 191, 255))
            return bird_img
        elif choix == 5:
            bird_img = load_image_safe("weird_bird.png", BIRD_WIDTH, BIRD_HEIGHT, (128, 0, 128))
            return bird_img
        elif choix == 6:
            bird_img = load_image_safe("angry-bird.png", BIRD_WIDTH, BIRD_HEIGHT, (255, 0, 0))
            return bird_img
        else:
            choix_oiseau()

    except ValueError:
        print("Veuillez entrer un nombre valide !")


class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT_flappy // 2
        self.velocity = 0
        self.gravity = 0.25
        self.jump_power = 4
        self.screen = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = -self.jump_power

    def draw(self, screen, bird_img):
        screen.blit(bird_img, (self.x, self.y))


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, 350)
        self.passed = False

    def update(self):
        self.x -= 2

    def draw(self, screen):
        screen.blit(top_pipe_img, (self.x, self.height - top_pipe_img.get_height()))
        screen.blit(bottom_pipe_img, (self.x, self.height + 100))

    def collision(self, bird):
        if bird.y < self.height or bird.y > self.height + 100:
            if self.x < bird.x < self.x + top_pipe_img.get_width():
                return True
        return False


def initialize_game_Flying_Birdies():
    pygame.init()
    return pygame.display.set_mode((SCREEN_WIDTH_flappy, SCREEN_HEIGHT_flappy))


def main_Flying_Birdies(bird_img):
    screen = initialize_game_Flying_Birdies()
    pygame.mixer.music.load("How_about_a_song_Jubilife_city.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.01)
    Bird.screen = screen
    clock = pygame.time.Clock()

    score = 0
    pipe_gap = 150
    pipe_frequency = 120
    pipe_counter = pipe_frequency
    pipes = []

    bird = Bird()

    game_state = MENU_flappy

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state == MENU_flappy:
                    if event.key == pygame.K_RETURN:
                        game_state = PLAYING_flappy
                elif game_state == PLAYING_flappy:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                elif game_state == GAME_OVER_flappy:
                    if event.key == pygame.K_RETURN:
                        score = 0
                        pipes.clear()
                        bird = Bird()
                        game_state = MENU_flappy

        screen.blit(background_img_flappy, (0, 0))

        if game_state == MENU_flappy:
            font = pygame.font.Font(None, 36)
            title = font.render("Flappy Bird", True, (255, 255, 255))
            subtitle = pygame.font.Font(None, 20).render("Appuyez sur Entrée pour jouer", True, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH_flappy // 2 - title.get_width() // 2, 200))
            screen.blit(subtitle, (SCREEN_WIDTH_flappy // 2 - subtitle.get_width() // 2, 250))
        elif game_state == PLAYING_flappy:
            pipe_counter -= 1
            if pipe_counter <= 0:
                pipe_height = random.randint(100, 300)
                pipes.append(Pipe(SCREEN_WIDTH_flappy))
                pipe_counter = pipe_frequency

            for pipe in pipes:
                if pipe.collision(bird):
                    game_state = GAME_OVER_flappy

                if not pipe.passed and pipe.x + top_pipe_img.get_width() < bird.x:
                    pipe.passed = True
                    score += 1

                pipe.update()
                pipe.draw(screen)

                if pipe.x < -top_pipe_img.get_width():
                    pipes.remove(pipe)

            bird.update()
            bird.draw(screen, bird_img)
            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(score), True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
        elif game_state == GAME_OVER_flappy:
            font = pygame.font.Font(None, 36)
            game_over_text = font.render("Game Over", True, (255, 255, 255))
            score_text = font.render("Score: " + str(score), True, (255, 255, 255))
            restart_text = font.render("Appuyez sur Entrée pour rejouer", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH_flappy // 2 - game_over_text.get_width() // 2, 200))
            screen.blit(score_text, (SCREEN_WIDTH_flappy // 2 - score_text.get_width() // 2, 250))
            screen.blit(restart_text, (SCREEN_WIDTH_flappy // 2 - restart_text.get_width() // 2, 300))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


def description_Flying_birdies():
    try:
        print("=== Flying Birdies ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
                oiseau = choix_oiseau()
                main_Flying_Birdies(oiseau)
        elif choix == 2:
            for i in range(10):
                print("\n")
                print("""

Flying Birdies est un jeu d'arcade simple, Le but du jeu est de guider un petit oiseau volant à travers une série d'obstacles verticaux, représentés sous la forme de tuyaux verts.
Le joueur doit appuyer sur espace pour faire battre les ailes de l'oiseau, ce qui le fait monter légèrement. En relâchant l'écran, l'oiseau descend naturellement.
dans cette variante de Flappy Bird, vous pouvez également choisir votre oiseau !



                     Bonne chance et bon jeu !


                """)
                print("\n\n\n")
                return description_Flying_birdies()
        else:
            return description_Flying_birdies()
    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################

def launch_game_Snuke():
    pygame.init()
    pygame.mixer.music.load("Athletic_Theme.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.01)

    screen_width = 1000
    screen_height = 800
    black = (50, 50, 50)
    white = (255, 255, 255)
    blue = (0, 0, 255)
    rainbow_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130),
                      (238, 130, 238), (255, 20, 147), (0, 255, 255), (255, 215, 0), (255, 99, 71)]

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snuke")
    font = pygame.font.Font(None, 36)

    class Snake:
        def __init__(self, block_size):
            self.block_size = block_size
            self.length = 1
            self.positions = [((screen_width // 2), (screen_height // 2))]
            self.direction = random.choice(['up', 'down', 'left', 'right'])
            self.color = white
            self.color_change_time = 0

        def get_head_position(self):
            return self.positions[0]

        def move(self):
            current = self.get_head_position()
            x, y = 0, 0
            if self.direction == 'up':
                y = -self.block_size
            elif self.direction == 'down':
                y = self.block_size
            elif self.direction == 'left':
                x = -self.block_size
            elif self.direction == 'right':
                x = self.block_size

            new = (current[0] + x, current[1] + y)
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

        def draw(self):
            for p in self.positions:
                pygame.draw.rect(screen, self.color, (p[0], p[1], self.block_size, self.block_size))

        def change_color(self):
            self.color = random.choice(rainbow_colors)
            self.color_change_time = time.time()
            return self.color

    def game_Snuke():
        block_size = 20
        score = 0

        snake = Snake(block_size)

        apple_pos = (random.randint(20, (screen_width - block_size) // block_size) * block_size,
                     random.randint(20, (screen_height - block_size) // block_size) * block_size)
        apple_color = random.choice(rainbow_colors)

        last_color_change_time = pygame.time.get_ticks()

        game_over = False
        game_quit = False

        snake_speed = 15

        clock = pygame.time.Clock()

        while not game_quit:
            color = random.choice(rainbow_colors)
            while game_over:
                screen.fill(black)
                font2 = pygame.font.Font(None, 72)
                score_text = font.render("Score: " + str(score), True, white)
                game_over_text = font2.render("Game Over!", True, color)
                retry_text = font.render("Cliquez pour rejouer", True, white)
                quit_text = font.render("Appuyez sur Echap pour quitter", True, white)

                screen.blit(score_text, (10, 10))
                screen.blit(game_over_text, ((screen_width // 2) - 120, (screen_height // 2) - 100))
                screen.blit(retry_text, ((screen_width // 2) - 120, (screen_height // 2) + 20))
                screen.blit(quit_text, ((screen_width // 2) - 190, (screen_height // 2) + 50))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        game_Snuke()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_UP and snake.direction != 'down':
                        snake.direction = 'up'
                    if event.key == pygame.K_DOWN and snake.direction != 'up':
                        snake.direction = 'down'
                    if event.key == pygame.K_LEFT and snake.direction != 'right':
                        snake.direction = 'left'
                    if event.key == pygame.K_RIGHT and snake.direction != 'left':
                        snake.direction = 'right'

            snake.move()

            current_time = pygame.time.get_ticks()
            if current_time - last_color_change_time >= 50:
                apple_color = random.choice(rainbow_colors)
                last_color_change_time = current_time

            if snake.get_head_position() == apple_pos:
                taille_increase = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1,
                                   1, 1, 1, 1, 1, 1, 1]
                snake.length += random.choice(taille_increase)
                score += 1
                apple_pos = (random.randint(0, (screen_width - block_size) // block_size) * block_size,
                             random.randint(0, (screen_height - block_size) // block_size) * block_size)
                a = snake.change_color()
                snake_speed = rainbow_colors.index(a) * 3
                if snake_speed < 15:
                    snake_speed = 15
            screen.fill(black)
            pygame.draw.rect(screen, apple_color, (apple_pos[0], apple_pos[1], block_size, block_size))
            snake.draw()

            if (snake.get_head_position()[0] < 0 or snake.get_head_position()[0] >= screen_width or
                    snake.get_head_position()[1] < 0 or snake.get_head_position()[1] >= screen_height or
                    snake.get_head_position() in snake.positions[1:]):
                game_over = True

            score_text = font.render("Score: " + str(score), True, snake.color)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(snake_speed)

    def show_menu_Snuke():
        menu = True
        color = random.choice(rainbow_colors)
        while menu:
            font2 = pygame.font.Font(None, 100)
            screen.fill(black)
            title_text = font2.render("Snuke", True, color)
            start_text = font.render("Jouer", True, white)
            quit_text = font.render("Quitter", True, white)

            screen.blit(title_text, ((screen_width // 2) - 120, (screen_height // 2) - 100))
            screen.blit(start_text, ((screen_width // 2) - 50, (screen_height // 2) + 10))
            screen.blit(quit_text, ((screen_width // 2) - 60, (screen_height // 2) + 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if (screen_width // 2) - 60 <= x <= (screen_width // 2) + 60 and \
                            (screen_height // 2) + 10 <= y <= (screen_height // 2) + 40:
                        menu = False
                        game_Snuke()
                    elif (screen_width // 2) - 70 <= x <= (screen_width // 2) + 70 and \
                            (screen_height // 2) + 50 <= y <= (screen_height // 2) + 80:
                        pygame.quit()
                        return

    show_menu_Snuke()


def description_jeu_Snuke():
    try:
        print("=== Bienvenue sur le jeu Snuke ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
            launch_game_Snuke()
        elif choix == 2:
            for i in range(100):
                print("\n")
            print("""
Snuke est un jeu captivant qui offre une nouvelle perspective sur le classique Snake.

Contrôle un serpent blanc et mange des pommes magiques pour des transformations surprenantes.

Les pommes modifient la couleur, la taille et la vitesse du serpent, ajoutant une touche d'imprévisibilité.

Parcours des niveaux stimulants, évite les obstacles et teste tes réflexes.

Plonge dans cet univers captivant et défie tes compétences de serpent dans Snuke.


"""
                  )
            print("Amusez-vous bien !\n\n\n")
            return description_jeu_Snuke()
        else:
            return description_jeu_Snuke()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################


SCREEN_WIDTH_Tetris = 350
SCREEN_HEIGHT_Tetris = 600
GRID_SIZE_Tetris = 25
GRID_WIDTH_Tetris = SCREEN_WIDTH_Tetris // GRID_SIZE_Tetris
GRID_HEIGHT_Tetris = SCREEN_HEIGHT_Tetris // GRID_SIZE_Tetris

INITIAL_SPEED_Tetris = 0.0007

BLACK_Tetris = (0, 0, 0)
WHITE_Tetris = (255, 255, 255)
RED_Tetris = (255, 0, 0)
GREEN_Tetris = (0, 255, 0)
BLUE_Tetris = (0, 0, 255)
YELLOW_Tetris = (255, 255, 0)
CYAN_Tetris = (0, 255, 255)
MAGENTA_Tetris = (255, 0, 255)
ORANGE_Tetris = (255, 165, 0)

SHAPES_Tetris = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]


class TetrisGame:
    def __init__(self):
        self.grid = [[BLACK_Tetris] * GRID_WIDTH_Tetris for _ in range(GRID_HEIGHT_Tetris)]
        self.current_shape = None
        self.current_shape_color = None
        self.current_shape_x = 0
        self.current_shape_y = 0
        self.score = 0
        self.game_over = False
        self.speed = INITIAL_SPEED_Tetris
        self.generate_new_shape()

    def generate_new_shape(self):
        shape_index = random.randint(0, len(SHAPES_Tetris) - 1)
        self.current_shape = SHAPES_Tetris[shape_index]
        self.current_shape_color = random.choice(
            [RED_Tetris, GREEN_Tetris, BLUE_Tetris, YELLOW_Tetris, CYAN_Tetris, MAGENTA_Tetris, ORANGE_Tetris])
        self.current_shape_x = (GRID_WIDTH_Tetris - len(self.current_shape[0])) // 2
        self.current_shape_y = 0

    def check_collision(self):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[0])):
                if (
                        self.current_shape[y][x]
                        and (
                        self.current_shape_x + x < 0
                        or self.current_shape_x + x >= GRID_WIDTH_Tetris
                        or self.current_shape_y + y >= GRID_HEIGHT_Tetris
                        or self.grid[self.current_shape_y + y][self.current_shape_x + x] != BLACK_Tetris
                )
                ):
                    return True
        return False

    def merge_shape_with_grid(self):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[0])):
                if self.current_shape[y][x]:
                    self.grid[self.current_shape_y + y][self.current_shape_x + x] = self.current_shape_color

    def remove_completed_lines(self):
        lines_removed = 0
        for y in range(GRID_HEIGHT_Tetris - 1, -1, -1):
            if BLACK_Tetris not in self.grid[y]:
                del self.grid[y]
                lines_removed += 1
        self.grid = [[BLACK_Tetris] * GRID_WIDTH_Tetris] * lines_removed + self.grid
        self.score += lines_removed
        self.speed = 0.07 + (lines_removed * 0.001)

    def update(self):
        if not self.game_over:
            self.current_shape_y += 1
            if self.check_collision():
                self.current_shape_y -= 1
                self.merge_shape_with_grid()
                self.remove_completed_lines()
                if self.current_shape_y <= 0:
                    self.game_over = True
                else:
                    self.generate_new_shape()

    def move_shape(self, dx):
        self.current_shape_x += dx
        if self.check_collision():
            self.current_shape_x -= dx

    def rotate_shape(self):
        old_shape = self.current_shape
        self.current_shape = list(zip(*self.current_shape[::-1]))
        if self.check_collision():
            self.current_shape = old_shape

    def draw(self, screen):
        for y in range(GRID_HEIGHT_Tetris):
            for x in range(GRID_WIDTH_Tetris):
                pygame.draw.rect(
                    screen,
                    self.grid[y][x],
                    (x * GRID_SIZE_Tetris, y * GRID_SIZE_Tetris, GRID_SIZE_Tetris, GRID_SIZE_Tetris),
                )

        if not self.game_over:
            for y in range(len(self.current_shape)):
                for x in range(len(self.current_shape[0])):
                    if self.current_shape[y][x]:
                        pygame.draw.rect(
                            screen,
                            self.current_shape_color,
                            (
                                (self.current_shape_x + x) * GRID_SIZE_Tetris,
                                (self.current_shape_y + y) * GRID_SIZE_Tetris,
                                GRID_SIZE_Tetris,
                                GRID_SIZE_Tetris,
                            ),
                        )

        pygame.draw.rect(screen, WHITE_Tetris, (0, 0, SCREEN_WIDTH_Tetris, SCREEN_HEIGHT_Tetris), 2)

        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, WHITE_Tetris)
        screen.blit(score_text, (20, 20))

        if self.game_over:
            game_over_text = font.render("Game Over", True, WHITE_Tetris)
            screen.blit(game_over_text,
                        (SCREEN_WIDTH_Tetris // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT_Tetris // 2))


def initialize_pygame_Tetris():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH_Tetris, SCREEN_HEIGHT_Tetris))
    pygame.display.set_caption("Tetris")

    return screen


def main_Tetris():
    screen = initialize_pygame_Tetris()

    menu_running = True
    game_running = False
    selected_option = None

    clock = pygame.time.Clock()

    while menu_running:
        screen.fill(BLACK_Tetris)

        font = pygame.font.Font(None, 36)
        title_text = font.render("Tetris", True, WHITE_Tetris)
        screen.blit(title_text, (SCREEN_WIDTH_Tetris // 2 - title_text.get_width() // 2, 100))

        play_text = font.render("Jouer", True, BLUE_Tetris)
        quit_text = font.render("Quitter", True, RED_Tetris)

        play_rect = play_text.get_rect(center=(SCREEN_WIDTH_Tetris // 2, 300))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH_Tetris // 2, 400))

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse_pos):
                    selected_option = "play"
                    menu_running = False
                    game_running = True
                elif quit_rect.collidepoint(mouse_pos):
                    selected_option = "quit"
                    menu_running = False

        if play_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, WHITE_Tetris, play_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, BLACK_Tetris, play_rect, border_radius=10)

        if quit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, WHITE_Tetris, quit_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, BLACK_Tetris, quit_rect, border_radius=10)

        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

    if selected_option == "play":
        tetris_game = TetrisGame()

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetris_game.move_shape(-1)
                    elif event.key == pygame.K_RIGHT:
                        tetris_game.move_shape(1)
                    elif event.key == pygame.K_DOWN:
                        tetris_game.speed = INITIAL_SPEED_Tetris * 10
                    elif event.key == pygame.K_UP:
                        tetris_game.rotate_shape()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        tetris_game.speed = INITIAL_SPEED_Tetris

            screen.fill(BLACK_Tetris)
            tetris_game.update()
            tetris_game.draw(screen)
            pygame.display.flip()
            clock.tick(4)

    pygame.quit()


def description_jeu_Tetris():
    try:
        print("=== Bienvenue sur le jeu Tetris ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
            main_Tetris()
        elif choix == 2:
            for i in range(100):
                print("\n")
            print("""
Tetris est un jeu de puzzle classique où le joueur doit empiler des formes géométriques pour créer des lignes complètes.

Les pièces tombent du haut de l'écran et le joueur doit les déplacer et les faire pivoter pour les placer stratégiquement.

L'objectif est de marquer le plus de points possible en effaçant des lignes complètes.

Si les pièces atteignent le sommet de l'écran, la partie est terminée.

Le jeu devient de plus en plus difficile car la vitesse de chute des pièces augmente.

 C'est un jeu intemporel apprécié par les joueurs de tous les âges. Préparez-vous à être captivé par ce jeu de puzzle emblématique !

"""
                  )
            print("Amusez-vous bien !\n\n\n")
            return description_jeu_Tetris()
        else:
            return description_jeu_Tetris()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


###################################################################################################################################################################################################################################################

def afficher_piece(niveau, cases_visitees):
    if niveau == "simple":
        print("-------")
        print("| {} {} |".format("D" if 1 in cases_visitees else 1, "D" if 2 in cases_visitees else 2))
        print("| {} {} |".format("D" if 3 in cases_visitees else 3, "D" if 4 in cases_visitees else 4))
        print("-------")
    elif niveau == "intermédiaire":
        print("-------------")
        print("| {} {} {} |".format("D" if 1 in cases_visitees else 1, "D" if 2 in cases_visitees else 2,
                                    "D" if 3 in cases_visitees else 3))
        print("| {}   {} |".format("D" if 4 in cases_visitees else 4, "D" if 5 in cases_visitees else 5))
        print("| {} {} {} |".format("D" if 6 in cases_visitees else 6, "D" if 7 in cases_visitees else 7,
                                    "D" if 8 in cases_visitees else 8))
        print("-------------")
    elif niveau == "dur":
        print("----------------")
        print("| {} {} {} |".format("D" if 1 in cases_visitees else 1, "D" if 2 in cases_visitees else 2,
                                    "D" if 3 in cases_visitees else 3))
        print("| {} {} {} |".format("D" if 4 in cases_visitees else 4, "D" if 5 in cases_visitees else 5,
                                    "D" if 6 in cases_visitees else 6))
        print("| {} {} {} |".format("D" if 7 in cases_visitees else 7, "D" if 8 in cases_visitees else 8,
                                    "D" if 9 in cases_visitees else 9))
        print("----------------")


def generer_enigmes(niveau):
    liste_choix = []
    choix = []
    liste_questions = []
    if niveau == "simple":
        for i in range(40):
            liste_choix.append(1)
        for i in range(20):
            liste_choix.append(2)
        for i in range(7):
            liste_choix.append(3)
        choix = random.sample(liste_choix, 4)

    if niveau == "intermédiaire":
        for i in range(20):
            liste_choix.append(1)
        for i in range(40):
            liste_choix.append(2)
        for i in range(10):
            liste_choix.append(3)
        choix = random.sample(liste_choix, 8)
    if niveau == "dur":
        for i in range(10):
            liste_choix.append(1)
        for i in range(10):
            liste_choix.append(2)
        for i in range(20):
            liste_choix.append(7)
        choix = random.sample(liste_choix, 9)

    for lvl in choix:
        if lvl == 1:
            enigmes = [
                {
                    "type": "mathematique",
                    "enonce": "Résolvez l'énigme suivante : 2 + 3 = ?",
                    "reponse": 5,
                    "indice": "ff"
                },
                {
                    "type": "mots",
                    "enonce": "Trouvez la traduction anglaise du mot 'chat'.",
                    "reponse": "cat",
                    "indice": "idk"
                },
                {
                    "type": "mots",
                    "enonce": "Trouvez la traduction espagnole du mot 'maison'.",
                    "reponse": "casa",
                    "indice": "jfd"
                },
                {
                    "type": "logique",
                    "enonce": "Quel est le meilleur langage de programmation ?",
                    "reponse": "Python",
                    "indice": "ldodjd"
                },
                {
                    "type": "logique",
                    "enonce": "Quel est le meilleur système d'exploitation pour les serveurs ?",
                    "reponse": "Linux",
                    "indice": "C'est pas windaube bien sûr"
                }
            ]
            question = random.choice(enigmes)
            liste_questions.append(question)
        elif lvl == 2:
            enigmes = [
                {
                    "type": "mathematique",
                    "enonce": "Résolvez l'énigme suivante : x^2 - 7x + 12 = 0",
                    "reponse": "3 et 4",
                    "indice": "dd"
                },
                {
                    "type": "mathematique",
                    "enonce": "Résolvez l'équation suivante : 2x + 5 = 124+143-34",
                    "reponse": 114,
                    "indice": "fjf"
                },
                {
                    "type": "mathematique",
                    "enonce": "Résolvez l'énigme suivante : 3x - 2 * 26 = 8",
                    "reponse": 20,
                    "indice": "fk"
                },
                {
                    "type": "mathematique",
                    "enonce": "Résolvez l'équation suivante : x^2 - 5x + 6 = 0",
                    "reponse": "2 et 3",
                    "indice": " dk"
                }

            ]
            question = random.choice(enigmes)
            liste_questions.append(question)
        elif lvl == 3:
            enigmes = [
                {
                    "type": "logique",
                    "enonce": "Quel est le langage de programmation utilisé pour les applications iOS ?",
                    "reponse": "Swift",
                    "indice": "kk "
                }
            ]
            question = random.choice(enigmes)
            liste_questions.append(question)

    return liste_questions


def resoudre_enigme(enigme, nombre_indices):
    print("type:" + enigme["type"])
    print(enigme["enonce"])
    print(f" Il vous reste {nombre_indices} indices.")
    print("Entrez votre réponse ou 'indice' pour avoir un indice.")
    print("=======================================================")
    reponse = input("> ")
    if reponse == "indice":
        if nombre_indices == 0:
            print("Vous n'avez plus d'indices...")
            print("Entrez votre réponse: ")
            print("=======================================================")
            reponse = input("> ")
        else:
            nombre_indices = nombre_indices - 1
            print("indice:" + enigme["indice"])
            print("Entrez votre réponse: ")
            print("=======================================================")
            reponse = input("> ")
    elif enigme["type"] == "mathematique":
        return reponse == str(enigme["reponse"])
    elif enigme["type"] == "mots" or enigme["type"] == "logique":
        return reponse.lower() == enigme["reponse"].lower(), f"\nIl vous reste {nombre_indices} indices."


def description(taille, ambiance, objet):
    if taille == 4:
        if ambiance == 1 and objet == 0:
            print("Vous vous trouvez dans une petite pièce aux allures mystérieuses.")
            print("L'obscurité ambiante est à la fois inquiétante et intrigante, laissant deviner des secrets enfouis.")
            print(
                "Les murs délabrés portent des traces du temps passé, mais il y a quelque chose de captivant dans ce lieu.")
            print(
                "Dans les coins sombres, vous apercevez des énigmes soigneusement dissimulées, attendant d'être résolues.")
            print("Chaque recoin de cette pièce renferme un indice, une clé vers votre évasion.")
            print("Soyez vigilant et explorez avec précaution. Chaque énigme résolue vous rapproche de la sortie.")
        if objet == 1 and ambiance == 1:
            print(
                "Sur une étagère, vous apercevez un vieux livre poussiéreux;\nDont la première page semble contenir un code. ")
        elif objet == 2 and ambiance == 1:
            print(
                "Au coin de la pièce, un coffre en bois massif attire votre attention.\nIl est fermé avec un cadenas à code.")
        elif objet == 3 and ambiance == 1:
            print(
                "Vous utilisez le code pour ouvrir le coffre en bois et vous trouvez une clé qui vous permet de sortir !")
        elif ambiance == 2 and objet == 0:
            print("Bienvenue dans cette petite pièce énigmatique.")
            print("Une faible lueur illumine l'espace, révélant des indices dispersés dans toute la pièce.")
            print(
                "Les murs usés témoignent d'une longue histoire, tandis que l'atmosphère mystérieuse vous pousse à explorer davantage.")
            print("Les énigmes, dissimulées avec soin, attendent patiemment votre esprit perspicace.")
            print(
                "Utilisez votre logique et votre intuition pour résoudre chaque énigme et ouvrir la voie vers la liberté.")
        if objet == 1 and ambiance == 2:
            print("Sur une table, vous voyez un mystérieux artefact.\nIl a une forme spéciale.")
        elif objet == 2 and ambiance == 2:
            print(
                "Dans un coin, une étrange boîte en métal attire votre attention.\nCependant il semble que la clé soit spéciale.\nVous n'avez jamais vu une serrure de la sorte.")
        elif objet == 3 and ambiance == 2:
            print(
                "Il semblerait que l'artefact permet d'ouvrir la boîte en métal.\nVous trouvez un code pour ouvrir la porte et sortir.")
        elif ambiance == 3:
            print("Vous êtes enfermé dans cette petite pièce aux allures intrigantes.")
            print("L'atmosphère est électrique, teintée de mystère et d'excitation.")
            print("Les murs, ornés de symboles énigmatiques, semblent raconter une histoire ancienne.")
            print("Des énigmes, à première vue impossibles à résoudre, parsèment la pièce.")
            print("Chaque défi relevé vous rapproche de votre liberté.")
            print(
                "Soyez attentif aux détails et faites preuve d'ingéniosité pour percer les mystères de cette pièce.")
        if objet == 1 and ambiance == 3:
            print(
                "Sur une étagère, vous découvrez un vieux grimoire couvert de poussière;\nIl semble contenir des formules magiques.")
        elif objet == 2 and ambiance == 3:
            print(
                "Dans un coin sombre, un coffre ancien attire votre regard.\nIl est protégé par un mécanisme complexe.")
        elif objet == 3 and ambiance == 3:
            print(
                "En utilisant les formules magiques du grimoire, vous activez le mécanisme du coffre.\nÀ l'intérieur se trouve une clé qui vous mènera vers la sortie.")
    elif taille == 8:
        if ambiance == 1 and objet == 0:
            print("Vous vous trouvez dans une pièce de taille moyenne, enveloppée d'un mystère palpable.")
            print(
                "L'obscurité ambiante est troublante, mais les énigmes qui vous entourent sont une invitation à la réflexion.")
            print("Les murs, ornés de symboles anciens, semblent détenir les clés de votre liberté.")
            print("Chaque énigme résolue vous rapproche de la vérité.")
            print(
                "Explorez chaque recoin de la pièce avec attention, car la clé de votre évasion réside dans ces énigmes.")
        if objet == 1 and ambiance == 1:
            print("Un objet mystérieux brille faiblement au centre de la pièce.")
        elif objet == 2 and ambiance == 1:
            print("Un coffre ancien, couvert de symboles ésotériques, trône au milieu de la pièce.")
        elif objet == 3 and ambiance == 1:
            print("En résolvant une série d'énigmes, vous activez un mécanisme secret qui révèle une porte cachée.")
        elif ambiance == 2 and objet == 0:
            print("Bienvenue dans cette pièce de taille moyenne, remplie de mystères à découvrir.")
            print("La faible lueur qui baigne la pièce met en valeur les énigmes qui vous entourent.")
            print("Les murs décrépits portent des inscriptions énigmatiques, témoignant d'un savoir ancien.")
            print("Chaque énigme est un défi à relever, une clé vers votre évasion.")
            print("Faites preuve d'ingéniosité et de perspicacité pour progresser dans cette quête.")
        if objet == 1 and ambiance == 2:
            print("Un objet mystérieux attire votre regard au centre de la pièce.")
        elif objet == 2 and ambiance == 2:
            print("Un coffre énigmatique repose au milieu de la pièce, défiant toute logique.")
        elif objet == 3 and ambiance == 2:
            print("En combinant les indices des énigmes, vous découvrez un passage secret dissimulé dans les murs.")
        elif ambiance == 3 and objet == 0:
            print("Vous pénétrez dans une pièce de taille moyenne, plongée dans un mystère envoûtant.")
            print("La lueur faible mais captivante révèle les énigmes qui vous entourent.")
            print("Les murs, ornés de symboles anciens et de motifs ésotériques, semblent renfermer un savoir caché.")
            print("Chaque énigme résolue est un pas de plus vers votre évasion.")
            print("Restez concentré et persévérez dans votre quête.")
        if objet == 1 and ambiance == 3:
            print("Un objet brillant trône majestueusement au centre de la pièce.")
        elif objet == 2 and ambiance == 3:
            print("Un coffre mystérieux, scellé par une énigme complexe, capte votre attention.")
        elif objet == 3 and ambiance == 3:
            print(
                "En résolvant les énigmes disséminées dans la pièce, vous découvrez un mécanisme secret qui dévoile une porte cachée.")
        elif taille == 9:
            if ambiance == 1 and objet == 0:
                print("Vous pénétrez dans une pièce spacieuse, remplie de mystères et d'énigmes.")
                print("L'atmosphère est électrique, créant une tension palpable dans l'air.")
                print("Les murs en pierre brute racontent une histoire ancienne, empreinte de secrets bien gardés.")
                print(
                    "Devant vous s'étendent neuf emplacements, chacun renfermant une énigme qui demande à être résolue.")
                print(
                    "Des artefacts énigmatiques ornent la pièce, vous rappelant la complexité des défis qui vous attendent.")
                print(
                    "Un éclairage tamisé projette des ombres dansantes sur les murs, ajoutant une dimension supplémentaire à cette épreuve.")
                print(
                    "Explorez méticuleusement chaque coin de cette pièce et laissez votre perspicacité guider votre chemin vers la liberté.")
                print("La résolution de chaque énigme est une victoire vers votre évasion imminente.")
            if objet == 1 and ambiance == 1:
                print("Un étrange artefact repose près de l'une des énigmes, attirant votre attention.")
            elif objet == 2 and ambiance == 1:
                print("Un coffre ancien, couvert de symboles énigmatiques, se trouve à l'un des emplacements.")
            elif objet == 3 and ambiance == 1:
                print(
                    "Vous trouvez une clé cachée derrière l'un des artefacts, qui vous permettra de sortir de la pièce.")
            elif ambiance == 2 and objet == 0:
                print("Bienvenue dans cette immense pièce remplie d'énigmes intrigantes.")
                print("Une lumière douce illumine neuf énigmes, chacune promettant de révéler des indices cruciaux.")
                print("Les murs robustes portent des marques anciennes, laissant entrevoir un passé mystérieux.")
                print(
                    "Chaque énigme représente un défi unique, nécessitant une réflexion approfondie et une approche méthodique.")
                print(
                    "Prenez votre temps pour explorer chaque recoin de cette pièce, car chaque énigme résolue vous rapproche de votre liberté.")
            if objet == 1 and ambiance == 2:
                print("Un objet énigmatique est soigneusement placé près de l'une des énigmes.")
            elif objet == 2 and ambiance == 2:
                print(
                    "Un coffre verrouillé, recouvert de symboles complexes, attire votre regard à l'un des emplacements.")
            elif objet == 3 and ambiance == 2:
                print(
                    "En résolvant toutes les énigmes, vous activez un mécanisme secret qui révèle une clé, votre ticket pour la sortie.")
            elif ambiance == 3 and objet == 0:
                print("Vous entrez dans une pièce gigantesque, imprégnée de mystère et d'intrigue.")
                print("Une lueur faible mais captivante met en valeur les neuf énigmes qui vous attendent.")
                print("Les murs sont ornés de symboles ésotériques, offrant un aperçu d'un monde caché.")
                print("Chaque énigme est un test de votre intelligence et de votre capacité à résoudre des problèmes.")
                print(
                    "Explorez chaque recoin de cette pièce avec détermination, car chaque énigme résolue vous rapproche de votre liberté tant désirée.")
            if objet == 1 and ambiance == 3:
                print("Un objet mystérieux attire votre attention près d'une des énigmes.")
            elif objet == 2 and ambiance == 3:
                print("Un coffre ancien, orné de symboles mystiques, se trouve à l'un des emplacements.")
            elif objet == 3 and ambiance == 3:
                print(
                    "En étudiant attentivement les symboles sur les murs, vous déchiffrez un message qui indique l'emplacement d'une clé.")
                print("Cette clé déverrouillera la porte vous permettant de quitter la pièce.")
    print("\n\n")


def jouer_escape_room():
    print("Vous vous retrouvez enfermé dans une mystérieuse pièce.")
    print("Pour sortir, vous devez résoudre les énigmes de chaque zone de la pièce.")
    print("Choisissez votre niveau de difficulté :")
    print("- 'simple'")
    print("- 'intermédiaire'")
    print("- 'dur'")
    niveau = input("> ")
    print("\n\n\n")
    if niveau not in ["simple", "intermédiaire", "dur"]:
        print("Niveau de difficulté invalide.")
        return

    print("Explorez la pièce, trouvez les indices et utilisez votre logique pour les résoudre.")
    cases_visitees = []
    liste_objets = []
    nombre_indice = 0
    ambiance = randint(1, 3)
    diff = False
    taille = 0
    if niveau == "simple":
        liste = [i for i in range(1, 5)]
        while not diff:
            liste_objets = random.sample(liste, 2)
            if liste_objets[0] != liste_objets[1]:
                diff = True
        nombre_indice = 2
        taille = 4
        description(taille, ambiance, 0)

    elif niveau == "intermédiaire":
        liste = [i for i in range(1, 9)]
        while not diff:
            liste_objets = random.sample(liste, 2)
            if liste_objets[0] != liste_objets[1]:
                diff = True
        nombre_indice = 3
        taille = 8
        description(taille, ambiance, 0)
    elif niveau == "dur":
        liste = [i for i in range(1, 10)]
        while not diff:
            liste_objets = random.sample(liste, 2)
            if liste_objets[0] != liste_objets[1]:
                diff = True
        nombre_indice = 3
        taille = 9
        description(taille, ambiance, 0)
    afficher_piece(niveau, cases_visitees)

    enigmes = generer_enigmes(niveau)
    cases_visitees = set()
    while True:
        print("\nQue voulez-vous faire ?")
        print("- 'q' pour quitter")
        print("- 'e' pour examiner une case")
        action = input("> ")
        if action == "q":
            print("Vous quittez le jeu.")
            break
        elif action == "e":
            print("Entrez le numéro de la case à examiner :")
            case = input("> ")
            if niveau == "simple":
                if case.isdigit() and 1 <= int(case) <= 4:
                    case = int(case)
                else:
                    print("Numéro de case invalide.")
                    continue
            elif niveau == "intermédiaire":
                if case.isdigit() and 1 <= int(case) <= 8:
                    case = int(case)
                else:
                    print("Numéro de case invalide.")
                    continue
            elif niveau == "dur":
                if case.isdigit() and 1 <= int(case) <= 9:
                    case = int(case)
                else:
                    print("Numéro de case invalide.")
                    continue

            if case in cases_visitees:
                print("Vous avez déjà résolu l'énigme de cette case.")
            else:

                enigme = random.choice(enigmes)
                if resoudre_enigme(enigme, nombre_indice):
                    for i in range(100):
                        print("\n")
                    if case not in liste_objets:
                        if len(liste_objets) == 2:
                            description(taille, ambiance, 0)

                    if case in liste_objets:
                        liste_objets.remove(case)
                        if not liste_objets:
                            description(taille, ambiance, 3)
                            print("Félicitations ! Vous avez trouvé tous les objets !")
                            break
                        elif len(liste_objets) == 1:
                            description(taille, ambiance, 1)
                    cases_visitees.add(case)
                    enigmes.remove(enigme)
                    if len(enigmes) == 0:
                        print(
                            "Félicitations ! Vous avez résolu toutes les énigmes et vous vous échappez de la pièce.")
                        break
                    else:
                        print("Félicitations ! Vous avez résolu l'énigme de la case. Continuez à explorer.")
                        afficher_piece(niveau, cases_visitees)
                else:
                    print("Mauvaise réponse. Continuez à chercher.")
        else:
            print("Commande invalide.")


def description_jeu_EscapeTheRoom():
    try:
        print("=== Bienvenue dans l'Escape Room ! ===")
        print("1. Jouer")
        print("2. Description du jeu")
        choix = int(input("Choisissez une option (1-2) : "))
        if choix == 1:
            for i in range(100):
                print("\n")
                jouer_escape_room()
        elif choix == 2:
            for i in range(100):
                print("\n")
                print("Bienvenue dans le jeu EscapeTheRoom !\n\n")
                print(
                    "Le but du jeu est de résoudre une série d'énigmes pour vous échapper de la pièce dans laquelle vous êtes enfermé.\n")
                print("Vous serez confronté à différentes énigmes de difficultés variées.\n")
                print(
                    "Au début du jeu, vous pouvez choisir parmi trois niveaux de difficulté : simple, intermédiaire ou dur.\n")
                print("Chaque niveau de difficulté a ses propres énigmes et défis.\n")
                print(
                    "Vous commencerez dans une pièce spécifique, représentée visuellement par des cases numérotées.\n")
                print("Votre objectif est de visiter toutes les cases en résolvant les énigmes correspondantes.\n")
                print("Lorsque vous résolvez une énigme, vous marquez la case correspondante comme visitée.\n")
                print(
                    "Pour résoudre une énigme, vous devez entrer la bonne réponse ou utiliser un indice si vous en avez.\n")
                print(
                    "Vous pouvez demander un indice pour chaque énigme, mais gardez à l'esprit que le nombre d'indices est limité.\n")
                print(
                    "Utilisez les indices avec précaution pour vous aider à résoudre les énigmes les plus difficiles.\n")
                print(
                    "Une fois que vous avez visité toutes les cases, vous avez terminé le jeu et vous pouvez vous échapper de la pièce.\n")
                print("Préparez-vous à faire travailler votre cerveau et à relever des défis pour sortir de la pièce !")
                print("\n\n\n")
                description_jeu_EscapeTheRoom()
        else:
            description_jeu_EscapeTheRoom()
    except ValueError:
        print("Veuillez entrer un nombre valide.")


enigmes = [
    {
        "type": "mots",
        "enonce": "Trouvez la traduction anglaise du mot 'livraison'.",
        "reponse": "delivery"
    },
    {
        "type": "traduction",
        "langue_depart": "anglais",
        "langue_arrivee": "français",
        "niveau": "intermédiaire",
        "enonce": "Traduisez le mot 'fan' en français.",
        "reponse": "ventilateur"
    },
    {
        "type": "traduction",
        "langue_depart": "anglais",
        "langue_arrivee": "espagnol",
        "niveau": "intermédiaire",
        "enonce": "Traduisez le mot 'book' en espagnol.",
        "reponse": "libro"
    },
    {
        "type": "logique",
        "enonce": "Quel est le meilleur système d'exploitation ?",
        "reponse": "Linux"
    },
    {
        "type": "logique",
        "enonce": "Un magicien charge un voyageur d’une mission étrange.\n « 500 perles se trouvent dans cette grotte. Je vous demande d’y pénétrer et de me ramener un certain nombre de perles.\n Ce nombre doit me permettre de diviser les perles en lots de 2, 3, 4, 5, 6 ou 7 perles, tout en laissant toujours la dernière perle de côté. »\n Le voyageur fait son possible pour remplir cette mission, mais commet une erreur.\n En effet, le nombre de perles qu’il ramène ne permet pas de diviser les perles en lots de quatre tout en laissant une perle de côté.\n Combien de perles a-t-il ramenées ?",
        "reponse": 211
    },
]


############################################################################################################################################################################################################################################################
# MENU DE LANCEMENT DE TOUS LES JEUX
def lancer_jeu():
    ok = False
    try:
        print("\n\n========== Bienvenue dans Python Games ! ===========")
        print("\n\nA quel type de jeu voulez vous jouez ?")
        print("Jeux à un joueur : 1, jeux multijoueurs : 2 ")
        choix_type = int(input("Choisissez une option (1-2) : "))
        if choix_type == 1:
            while not ok:
                print("\n\n\n\n\n=== Jeux à un joueur ! ===\n\n")
                print("A quel jeu voulez vous jouez ?")
                print(
                    "\n  \n=============================================================================================\n  |  Voltorbataille : 1  |  EscapeTheRoom : 2  |  Pendu : 3  |  RememberTheColors : 4  |  \n=============================================================================================\n |  Jeu des allumettes(vs IA) : 5  |  2048 : 6  |  Taquin : 7  |  Puissance4(vs IA) : 8  |  \n=============================================================================================\n  |  Morpion(vs IA) : 9  |  Dodger's Rush : 10  |  Space Lost Bird : 11  |  Snuke : 12  |  \n=============================================================================================\n  |  Flying Birdies : 13  |  Tetris : 14  |  choix du type de jeu : 15  | \n=============================================================================================\n  ")
                choix_jeu_solo = int(input("Choisissez une option (1-15) : "))
                if choix_jeu_solo == 1:
                    ok = True
                    description_jeu_Voltorbe()
                elif choix_jeu_solo == 2:
                    ok = True
                    description_jeu_EscapeTheRoom()
                elif choix_jeu_solo == 3:
                    ok = True
                    description_jeu_pendu()
                elif choix_jeu_solo == 4:
                    ok = True
                    rejouer_jeu_couleur(0)
                    description_jeu_pendu()
                elif choix_jeu_solo == 5:
                    ok = True
                    lancer_jeu_des_allumettesIA()
                elif choix_jeu_solo == 6:
                    ok = True
                    jouer_2048_final()
                elif choix_jeu_solo == 7:
                    ok = True
                    jeu_taquin()
                elif choix_jeu_solo == 8:
                    ok = True
                    description_puissance_4()
                elif choix_jeu_solo == 9:
                    ok = True
                    description_jeu_morpion_IA()
                elif choix_jeu_solo == 10:
                    ok = True
                    description_jeu_Dodgers_Rush()
                elif choix_jeu_solo == 11:
                    ok = True
                    description_Space_Lost_Bird()
                elif choix_jeu_solo == 12:
                    ok = True
                    description_jeu_Snuke()
                elif choix_jeu_solo == 13:
                    ok = True
                    description_Flying_birdies()
                elif choix_jeu_solo == 14:
                    ok = True
                    description_jeu_Tetris()

                elif choix_jeu_solo == 15:
                    lancer_jeu()
        elif choix_type == 2:
            while not ok:
                print("\n\n\n\n\n=== Jeux multijoueurs ! ===\n\n")
                print("A quel jeu voulez vous jouez ?")
                print(
                    "\n|  Bataille Navale (2 joueurs) : 1  |  Jeu des allumettes (2 joueurs) : 2  |  Pendu(mode Duo) : 3  |  Morpion(2 joueurs) : 4  |  Puissance4(2 joueurs) : 5 |  Pong(2 joueurs) : 6 |  retourner au choix du type de jeu : 7 | ")
                choix_jeu_multi = int(input("Choisissez une option (1-7) : "))
                if choix_jeu_multi == 1:
                    ok = True
                    bataille_navale()
                elif choix_jeu_multi == 2:
                    ok = True
                    lancer_jeu_des_allumettes()
                elif choix_jeu_multi == 3:
                    ok = True
                    description_jeu_pendu()
                elif choix_jeu_multi == 4:
                    ok = True
                    description_jeu_morpion()
                elif choix_jeu_multi == 5:
                    ok = True
                    description_puissance_4()
                elif choix_jeu_multi == 6:
                    ok = True
                    description_Pong_JEU()
                elif choix_jeu_multi == 7:
                    lancer_jeu()
        else:
            print("Vous devez choisir un nombre entre 1 et 2.")
            lancer_jeu()

    except ValueError:
        print("Veuillez entrer un nombre valide.")


lancer_jeu()
