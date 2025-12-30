#  Collection de Jeux Python

Bienvenue dans cette collection complète de jeux en Python ! Voici tous les jeux disponibles :

---

##  Table des matières

1. [Jeux de Stratégie](#jeux-de-stratégie)
2. [Jeux Arcade](#jeux-arcade)
3. [Jeux de Réflexe](#jeux-de-réflexe)
4. [Jeux de Puzzle](#jeux-de-puzzle)
5. [Jeux de Réflexion](#jeux-de-réflexion)

---

##  Jeux de Stratégie

### 1. **Bataille Navale**
- **Description** : Jeu classique pour deux joueurs où l'objectif est de couler tous les navires adversaires.
- **Règles** : Placez vos navires sur une grille 10x10, puis attaquez les positions adverses. Un "touché" vous permet de rejouer.
- **Compositions** : Deux compositions de navires disponibles
- **Fonction** : `bataille_navale()`

### 2. **Puissance 4**
- **Description** : Jeu de stratégie où il faut aligner 4 jetons horizontalement, verticalement ou en diagonale.
- **Modes** :
  - Mode Duo : Affrontement entre deux joueurs
  - Mode Solo vs IA : Jouez contre une intelligence artificielle avec algorithme Minimax
- **Grille** : 6x7
- **Fonction** : `description_puissance_4()` ou `jouer_puissance4_ia()`

### 3. **Morpion (Tic-Tac-Toe)**
- **Description** : Jeu classique sur une grille 3x3.
- **Modes** :
  - Mode Duo : Deux joueurs
  - Mode Solo vs IA : Contre une IA utilisant l'algorithme Minimax
- **Symboles** : X et O (choix personnalisable)
- **Fonction** : `description_jeu_morpion()` ou `description_jeu_morpion_IA()`

---

##  Jeux Arcade

### 4. **Flying Birdies (Flappy Bird)**
- **Description** : Jeu de réflexe où vous devez éviter les tuyaux.
- **Fonction** : Sauter avec la barre d'espace pour naviguer entre les obstacles
- **Choix d'oiseaux** : 6 variantes disponibles (Flappy, Doge, Nyan, Cool, Weird, Angry)
- **Musique** : "How_about_a_song_Jubilife_city.mp3"
- **Fonction** : `description_Flying_birdies()`
- **Note** : Gestion automatique des images manquantes avec fallback coloré

### 5. **Space Lost Bird**
- **Description** : Aidez un oiseau alien à rejoindre l'espace en évitant les obstacles.
- **Niveaux** : 11 niveaux progressifs avec augmentation de difficulté
- **Obstacles** : Nuages (niveaux 1-5) et astéroïdes (niveaux 6-10)
- **Score** : Suivi du temps en millisecondes
- **Classement** : Sauvegarde des meilleures performances
- **Musique** : "Eterna_Forest.mp3"
- **Fonction** : `description_Space_Lost_Bird()`

### 6. **Dodger's Rush**
- **Description** : Jeu d'esquive où il faut éviter les blocs qui tombent.
- **Contrôles** : Flèches gauche/droite pour se déplacer
- **Système** : Score augmente avec le temps, invincibilité temporaire après collision
- **Fonction** : `description_jeu_Dodgers_Rush()`

### 7. **Pong**
- **Description** : Classique jeu de ping-pong pour deux joueurs.
- **Contrôles** : 
  - Joueur 1 : Z (haut) et S (bas)
  - Joueur 2 : Flèches haut/bas
- **Objectif** : Atteindre 5 points pour gagner
- **Niveaux** : Augmentation progressive de la difficulté
- **Fonction** : `description_Pong_JEU()`

---

##  Jeux de Réflexe

### 8. **Jeu de Mémoire**
- **Description** : Reproduisez des séquences de couleurs de plus en plus longues.
- **Niveaux** : 15 niveaux progressifs
- **Système de vie** : 3 vies disponibles
- **Couleurs** :
  - Niveaux 1-3 : 4 couleurs
  - Niveaux 4-5 : 5 couleurs
  - Niveaux 6-8 : 6 couleurs
  - Niveaux 9+ : 7 couleurs
- **Délai** : Le temps d'affichage diminue avec les niveaux
- **Fonction** : `jouer_jeu_memoire()`

### 9. **Voltorbataille**
- **Description** : Minijeu inspiré de Pokémon, basé sur le Démineur.
- **Grille** : 5x5 tuiles retournées
- **Objectif** : Éviter les Voltorbes et accumuler des points
- **Niveaux** : 5 niveaux avec augmentation du nombre de Voltorbes
- **Système** : Redescendre d'un niveau en cas d'échec
- **Fonction** : `description_jeu_Voltorbe()`

---

##  Jeux de Puzzle

### 10. **2048**
- **Description** : Combinez des nombres pour atteindre 2048.
- **Grille** : 4x4
- **Contrôles** : Z (haut), S (bas), Q (gauche), D (droite)
- **Objectif** : Fusionner les nombres identiques pour créer 2048
- **Nouvelles cases** : Apparaissent aléatoirement (2 ou 4)
- **Fonction** : `jouer_2048_final()`

### 11. **Taquin**
- **Description** : Réorganisez les nombres pour les remettre en ordre numérique.
- **Grille** : Taille variable (3x3 à 9x9)
- **Système** : Une case vide permet les déplacements
- **Objectif** : Placer les nombres dans l'ordre croissant
- **Fonction** : `jeu_taquin()`

### 12. **Tetris**
- **Description** : Le classique jeu de chute de blocs.
- **Grille** : 14x24 cases (25px par case)
- **Blocs** : 7 formes différentes (Tétriminos)
- **Couleurs** : Rouge, Vert, Bleu, Jaune, Cyan, Magenta, Orange
- **Vitesse** : Augmente progressivement
- **Fonction** : `description_jeu_Tetris()`

---

##  Jeux de Réflexion

### 13. **Pendu**
- **Description** : Devinez un mot avant de vous tromper 7 fois.
- **Mots** : Liste de plus de 900 mots en anglais
- **Modes** : 
  - Mode classique : Jeu standard
  - Mode thématique : Catégories spécifiques
  - Mode personnalisé : Créez vos propres mots
  - Mode mixte : Mélange de tous les modes
- **Système** : Affichage du pendu progressif
- **Fonction** : `description_jeu_pendu()`

### 14. **Jeu des Allumettes**
- **Description** : Jeu de stratégie pour deux joueurs.
- **Règles** : Chaque joueur retire 1, 2 ou 3 allumettes. Celui qui prend la dernière perd.
- **Modes** :
  - Mode local : Deux joueurs
  - Mode IA : Contre une intelligence artificielle
- **Fonction** : `lancer_jeu_des_allumettes()` ou `lancer_jeu_des_allumettesIA()`

### 15. **Snake (Snuke)**
- **Description** : Classique jeu du serpent qui grandit en mangeant des pommes.
- **Grille** : 1000x800 pixels avec blocs de 20px
- **Système de score** : Augmente avec les pommes mangées
- **Couleurs** : Arc-en-ciel pour les segments
- **Vitesse** : 15 FPS
- **Musique** : "Athletic_Theme.mp3"
- **Fonction** : `launch_game_Snuke()`


### Installation des dépendances

```bash
pip install pygame
```

### Lancer les jeux

Chaque jeu possède une fonction de description accessible via le menu principal.

Exemple pour lancer les jeux directement:
```python
python Python\ Games.py
```
