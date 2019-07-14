# Programme de la boursière

## Avant de lancer le serveur

### Requirements  pour pip

```python
Django==2.2.3                                         
django-crispy-forms==1.7.2
django-csp==3.5
jsonify==0.5
Pillow==6.0.0
python-crontab==2.3.8
python-dateutil==2.8.0
pytz==2018.4
schedule==0.6.0
six==1.11.0
sqlparse==0.3.0
```

Pour installer les dépendances ci-dessus, enregistrer le texte ci-dessus dans un fichier et exécuter la commande suivante.

```bash
pip install -r <nom_du_fichier>.txt
```

## Lancer le serveur et le timer de mise à jour des prix

Avant de lancer le serveur, il est nécessaire d'initialiser la base de donner si cela n'as pas été fait. 

Pour se faire, il faut supprimer le fichier `db.sql3` et effectuer les commandes suivantes dans l'ordre.

1. ```bash
   python.exe .\manage.py migrate
   ```

2. ```bash
   python.exe .\manage.py makemigrations
   ```

3. ```
   python.exe .\manage.py createsuperuser
   ```

4. Suivre les instructions de la console.

5. ```bash
   python.exe .\manage.py init_db	
   ```

## Lancer le serveur

Pour lancer le serveur il faut effectuer la commande suivante.

```bash
python.exe .\manage.py runserver
```

Pour lancer le timer afin que les prix soit mis à jours il faut lancer le script externe `cron_job.py`.

```bash
python.exe .\cron_job.py
```

Pour stopper ce script (et donc le timer) il faut faire `ctrl + c` dans la console de `cron_job.py`

Pour stopper le serveur (et donc le site web) il faut faire `ctrl + c`  dans la console du serveur.

## URL disponnible

|      `/url/`      | Objectif de la page                                          |
| :---------------: | ------------------------------------------------------------ |
|     `/admin/`     | Panel d'amistration dajngo                                   |
| `/beer_ordering/` | Page principal pour l'ajout de commande lors de la boursière |
|   `/add_beer/`    | Utilisé pour ajouter des bières à la base de données         |
|     `/login/`     | Login                                                        |
|    `/logout/`     | Logout                                                       |
|  `/stock_page/`   | Page des stock affiché par les projecteurs (informe de l'état du marché) |
|   `/dashboard/`   | Page tréso pour la gestion des prix (cas de soucis avec l'algo + informations sur les bénefs et consommation) |