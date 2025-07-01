WidgetHora
WidgetHora est un widget d’horloge personnalisable pour Windows, développé en Python avec PyQt5. Il s’affiche sur le bureau, propose de nombreux réglages d’apparence et de format, et peut démarrer automatiquement avec Windows.
Ce projet vise à offrir une horloge élégante, légère et pratique pour votre environnement de travail.

Fonctionnalités
Affichage de l’heure et de la date dans différents formats (24h, 12h, formats personnalisés…)

Personnalisation complète : police, taille, couleur, espacement, affichage/masquage de l’heure ou de la date

Mode sombre automatique selon le thème Windows

Déplacement du widget sur le bureau (drag & drop)

Démarrage automatique avec Windows (ajout/suppression dans le dossier de démarrage)

Sauvegarde des paramètres via QSettings

Panneau de paramètres convivial

Fenêtre "À propos" avec lien vers le dépôt GitHub

Aperçu en images
1. Widget principal (horloge sur le bureau)
![Capture widget principal](https://raw.githubusercontent.com/Nkounga42/WidgetHora/main/screenshots/widget_mainanneau de paramètres (Options)
![Capture panneau paramètres](https://raw.githubusercontent.com/Nkounga42/WidgetHora/main/screenshots/settings 3. Fenêtre « À propos »
![Capture fenêtre À propos](https://raw.githubusercontent.com/Nkounga42/WidgetHora/main/screenshots/about_window**

Si tu n’as pas encore de captures d’écran, crée un dossier screenshots à la racine du dépôt, ajoute tes images, puis mets à jour les liens ci-dessus.

Installation
Prérequis
Python 3.7+

Windows (testé sur Windows 10/11)

Les modules suivants :

PyQt5

pywin32 (pour la gestion du démarrage automatique)

Installation des dépendances
bash
pip install pyqt5 pywin32
Téléchargement
Clonez ou téléchargez ce dépôt GitHub :

bash
git clone https://github.com/Nkounga42/WidgetHora.git
cd WidgetHora
Utilisation
Lancez simplement le script principal :

bash
python widgethora.py
Le widget s’affiche sur votre bureau.
Faites un clic-droit sur le widget pour accéder au menu contextuel (Options, À propos, Quitter).

Personnalisation
Cliquez sur Options (clic droit sur le widget) pour ouvrir le panneau de configuration.

Modifiez le format de l’heure, la police, la couleur, l’espacement, activez/désactivez l’affichage de la date ou de l’heure, etc.

Activez l’option « Lancer au démarrage » pour que WidgetHora se lance automatiquement à chaque démarrage de Windows.

Les paramètres sont sauvegardés automatiquement.

Structure du code
ClockWidget : Fenêtre principale affichant l’heure et la date, gère le déplacement, le menu contextuel et la personnalisation.

SettingsPanel/SettingsWindow : Panneau de configuration pour tous les réglages (apparence, format, options…).

AboutWindow : Fenêtre « À propos » avec informations sur l’auteur et lien GitHub.

Fonctions utilitaires : gestion du thème sombre, ajout/suppression au démarrage, gestion des paramètres utilisateur.

Ressources
Les icônes et images doivent être placés dans le dossier assets/images/ et assets/svg/.

Le projet utilise les paramètres Windows pour détecter le thème sombre.

Auteur
Développé par Nkounga Exauce
GitHub : Nkounga42/WidgetHora

Licence
Ce projet est open source, sous licence MIT (voir le fichier LICENSE).
