# Listes de tâches collaboratives — cahier des charges du projet

## 1. Objectif et périmètre

Construire une petite application web où les utilisateurs créent des listes de tâches, invitent des collaborateurs, attribuent des tâches et discutent du travail au même endroit. Chaque membre doit toujours savoir ce qu’il reste à faire, qui en est responsable et ce qui a changé.

Cette base ne fournit que la structure des pages et leur mise en forme. Les étudiants réalisent le comportement de l’application. La première version comporte un seul espace de travail avec plusieurs listes de tâches. La messagerie d’équipe, les pièces jointes, les notifications, le suivi du temps, les tâches récurrentes et les tableaux avec glisser-déposer sont hors périmètre.

## 2. Utilisateurs et rôles

| Rôle | Définition | Principales possibilités |
| --- | --- | --- |
| Visiteur | Utilisateur non connecté | Accéder uniquement aux pages de connexion et d’inscription. |
| Membre | Utilisateur connecté et ajouté à une liste | Consulter cette liste ; créer et modifier des tâches ; commenter ; voir les tâches qui lui sont attribuées. |
| Propriétaire de la liste | Membre ayant créé une liste | Disposer de toutes les possibilités d’un membre ; modifier les informations de la liste ; inviter ou retirer des membres ; supprimer la liste. |

Un utilisateur peut être propriétaire d’une liste et simple membre d’une autre. Seuls les membres d’une liste peuvent voir ses tâches et ses commentaires. Un membre ne peut attribuer une tâche qu’à un autre membre de cette même liste. Lorsqu’un membre est retiré, ses commentaires existants sont conservés et les tâches qui lui étaient attribuées deviennent non attribuées. L’application doit signaler cette conséquence au propriétaire avant le retrait.

## 3. Principaux parcours utilisateur

1. **Créer une liste :** se connecter, saisir un nom obligatoire et une description facultative, enregistrer la liste et en devenir propriétaire.
2. **Collaborer :** le propriétaire ajoute un utilisateur existant à l’aide de son adresse e-mail ou de son nom d’utilisateur. Le nouveau membre voit la liste dans sa vue d’ensemble. Le propriétaire peut ensuite retirer un membre.
3. **Planifier le travail :** un membre crée une tâche dans une liste avec un titre, une description facultative, une échéance facultative, un statut et un responsable facultatif.
4. **Travailler sur une tâche :** un membre ouvre la tâche, modifie les champs autorisés et publie un commentaire. La page de détail présente l’état actuel et les échanges dans l’ordre chronologique.
5. **Suivre le travail :** la vue d’ensemble présente les listes auxquelles appartient le membre et les tâches qui lui sont attribuées. La page d’une liste affiche toutes ses tâches et son avancement.
6. **Terminer le travail :** un membre marque une tâche comme terminée. Le nombre de tâches terminées de la liste est mis à jour. Le propriétaire ne peut supprimer une liste qu’après confirmation ; la suppression efface ses tâches et ses commentaires.

## 4. Modèle de données

| Entité | Champs obligatoires | Champs facultatifs et règles |
| --- | --- | --- |
| User | Identifiant utilisateur Django, nom d’utilisateur, adresse e-mail, empreinte du mot de passe | Utiliser l’authentification Django plutôt que stocker les mots de passe dans un nouveau modèle. L’adresse e-mail doit être unique si les invitations reposent sur elle. |
| TaskList | ID, name, owner, created_at | Description, updated_at. Le propriétaire est également membre. |
| Membership | ID, task_list, user, joined_at | Le couple `(task_list, user)` doit être unique. |
| Task | ID, task_list, title, status, created_by, created_at, updated_at | Description, assignee, due_at, completed_at. Le responsable doit appartenir à la même liste. |
| Comment | ID, task, author, body, created_at | Le contenu ne peut pas être vide. L’auteur doit être membre de la liste au moment de la publication. |

Statuts des tâches : **À faire**, **En cours**, **Terminée**. Une nouvelle tâche commence avec le statut À faire. Lors du passage au statut Terminée, renseigner `completed_at` ; effacer cette valeur si la tâche est rouverte. Définir un fuseau horaire pour les horodatages stockés et les convertir dans le fuseau utilisé pour l’affichage à l’utilisateur. L’avancement d’une liste correspond à `tâches terminées / toutes les tâches` ; afficher `0 sur 0` pour une liste vide.

Relations suggérées : `TaskList.owner → User`, `Membership → TaskList + User`, `Task → TaskList`, `Task.assignee → User`, `Comment → Task + User`. Définir et tester le comportement à la suppression pour chaque clé étrangère, en particulier celles des propriétaires et des auteurs de commentaires.

## 5. Pages et données attendues par les gabarits

| Page | Gabarit | Données ou commandes à fournir |
| --- | --- | --- |
| Vue d’ensemble | `tasks/dashboard.html` | `task_lists` visibles par l’utilisateur connecté ; tâches qui lui sont attribuées ; action de création d’une liste ; affichage adapté aux listes vides. |
| Détail d’une liste | `tasks/list_detail.html` | `task_list`, membres, tâches, avancement, action d’ajout d’une tâche et commandes de gestion des membres réservées au propriétaire. |
| Détail d’une tâche | `tasks/task_detail.html` | `task`, liste parente, commentaires, commandes de modification et formulaire de commentaire. |
| Connexion / inscription | À créer | Formulaires d’authentification et messages d’erreur de validation clairs. |
| Formulaires de création / modification | À créer | Formulaires pour les listes, les tâches, les membres et les commentaires ; confirmation des actions destructrices. |

`templates/base.html` définit la structure commune des pages ainsi que les points d’insertion `{% block title %}` et `{% block content %}`. Les trois gabarits de page contiennent des blocs provisoires lisibles et des commentaires `TODO` ; remplacez-les par des variables, boucles, liens et formulaires Django. Réutilisez les classes existantes de `static/css/style.css` pour conserver la disposition des cartes et des lignes de tâches. Ajoutez les styles des formulaires et des erreurs lors de leur réalisation.

Routes suggérées : `/` pour la vue d’ensemble, `/lists/<id>/` pour une liste, `/lists/<id>/tasks/<id>/` pour une tâche, ainsi que des routes pour la création, la modification, la gestion des membres, les commentaires et l’authentification. Utilisez des URL Django nommées dans les gabarits. Une liste ou une tâche inexistante, ou à laquelle l’utilisateur n’a pas accès, ne doit pas révéler son contenu.

## 6. Règles fonctionnelles et critères d’acceptation

| Fonctionnalité | Critère d’acceptation |
| --- | --- |
| Accès | Un visiteur non connecté est redirigé vers la connexion. Un utilisateur qui n’est pas membre ne peut accéder à aucune liste, tâche ou commentaire de cette liste, même en devinant les identifiants. |
| Listes | Un utilisateur connecté peut créer une liste avec un nom non vide, puis la voit dans sa vue d’ensemble. Seul son propriétaire peut la renommer ou la supprimer. |
| Membres | Seul le propriétaire peut ajouter ou retirer des membres. Un même utilisateur ne peut pas être ajouté deux fois. Un membre retiré perd immédiatement l’accès. |
| Tâches | Un membre peut ajouter, modifier et terminer une tâche. Le titre est obligatoire. Le statut est limité aux trois valeurs définies. |
| Attribution | Une tâche peut rester sans responsable ou être attribuée à un membre actuel de la liste. Elle apparaît dans la vue d’ensemble de ce membre. Le serveur refuse son attribution à une personne extérieure à la liste. |
| Échéances | Une échéance vide est autorisée. Si une date est fournie, elle est stockée et affichée de manière cohérente ; un style pour les tâches en retard pourra être ajouté plus tard. |
| Commentaires | Un membre peut publier un texte non vide. Les commentaires affichent leur auteur et leur date de publication dans l’ordre chronologique. Le HTML saisi par les utilisateurs est échappé. |
| États vides | Les listes vides et les vues sans tâche attribuée affichent un texte utile plutôt qu’une section vide ou défectueuse. |
| Suppression | La suppression d’une liste exige une confirmation et n’efface que les tâches et commentaires de cette liste. |

## 7. Exigences de sécurité et de qualité

- Vérifier l’appartenance à la liste et les droits du propriétaire dans les vues ou dans une fonction d’accès commune pour **chaque** lecture et écriture, et pas seulement en masquant les boutons.
- Utiliser les formulaires Django ou une validation équivalente côté serveur, une protection CSRF pour les écritures et des requêtes POST pour les changements d’état. Ne jamais placer une action destructrice derrière un lien GET.
- Conserver les secrets dans des variables d’environnement ; ne pas enregistrer `.env`, les fichiers de base de données ou les mots de passe dans le dépôt. Pour un déploiement au-delà d’un usage pédagogique local, utiliser un serveur et une configuration adaptés à la production.
- Préserver l’utilisation au clavier et sur les écrans étroits. Lors du remplacement des blocs provisoires, utiliser de vrais liens, boutons et libellés, ainsi que des indications de focus visibles.
- Paginer les listes de tâches et de commentaires si elles deviennent longues. Charger les objets liés efficacement pour éviter une requête par carte ou par ligne.
- Ajouter des tests pour les limites d’accès, la validation des attributions, les changements de statut et la suppression d’une liste avant de considérer la réalisation comme terminée.

## 8. Ordre de réalisation suggéré

1. Créer le projet et l’application Django ; configurer les fichiers statiques, les gabarits, les URL nommées et l’authentification.
2. Ajouter les cinq entités de données et les migrations ; inscrire automatiquement le propriétaire parmi les membres.
3. Remplacer les blocs provisoires de la vue d’ensemble et des pages de liste par des données filtrées selon les droits d’accès et par des affichages adaptés aux listes vides.
4. Ajouter les formulaires des listes et des tâches, la validation des attributions et les changements de statut.
5. Ajouter la gestion des membres, les commentaires et la confirmation avant suppression.
6. Tester les règles d’accès et les cas limites ; vérifier l’utilisation au clavier et sur mobile.

La réalisation est terminée lorsque tous les critères d’acceptation de la section 6 sont satisfaits et qu’aucune action provisoire ne subsiste sur une page censée être fonctionnelle.
