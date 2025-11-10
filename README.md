# 🚀 Projet d'API de Commande de Menus (LittleLemon-like API)

Une API RESTful construite avec **Django** et **Django REST Framework (DRF)** pour la gestion des menus, des catégories, des paniers et des commandes. Elle intègre un système d'autorisation robuste basé sur les rôles d'utilisateurs.

---

## 💻 Installation et Démarrage

Suivez ces étapes pour configurer et lancer l'API en local.

### Création de l'Environnement Virtuel

Il est **fortement recommandé** d'utiliser un environnement virtuel pour isoler les dépendances du projet.

**Via `venv` (standard Python) :**

```bash
#### Crée l'environnement virtuel (nommé 'venv')
python3 -m venv venv

#### Active l'environnement virtuel
#### Sur Linux/macOS :
source venv/bin/activate
#### Sur Windows (PowerShell) :
.\venv\Scripts\Activate.ps1
#### Sur Windows (Cmd) :
.\venv\Scripts\activate.bat
```

---

## ✨ Fonctionnalités Clés

* **Gestion des Menus et Catégories** : Opérations CRUD complètes sur les éléments de menu et leurs catégories.
* **Système de Panier** : Les utilisateurs peuvent ajouter, visualiser et vider leur panier (`Cart`).
* **Gestion des Commandes** :
    * Création de commandes à partir du panier existant.
    * Filtrage des commandes par utilisateur (Clients et Livreurs) ou visualisation de toutes les commandes (Gestionnaires).
* **Rôles Utilisateur (Groupes)** :
    * **Gestionnaire (Manager)** : Gère les menus et les autres utilisateurs/groupes.
    * **Livreur (Delivery Crew)** : Peut uniquement mettre à jour le statut de la livraison d'une commande assignée.
    * **Client (Standard User)** : Peut consulter les menus, gérer son panier et passer/consulter ses propres commandes.
* **Recherche et Pagination** : Filtrage (`title`, `featured`, `category`), tri (`ordering`) et pagination disponibles sur l'endpoint des éléments de menu.

---

## 🛠️ Modèles de Données

| Modèle | Description | Attributs Clés |
| :--- | :--- | :--- |
| `Category` | Catégories des éléments de menu. | `slug`, `title` |
| `MenuItem` | Éléments disponibles sur le menu. | `title`, `price`, `featured`, `category` |
| `Cart` | Représente le panier d'un utilisateur. | `user`, `menuitem`, `quantity`, `unit_price`, `price` |
| `Order` | La commande passée. | `user`, `delivery_crew`, `status` (livré/non livré), `total`, `date` |
| `OrderItem` | Les articles spécifiques dans une commande. | `order`, `menuitem`, `quantity`, `unit_price`, `price` |

---

## 🗺️ Endpoints de l'API

L'API est structurée autour des rôles pour garantir une sécurité appropriée.

### 🍽️ Gestion des Menus et Catégories

| Méthode | Endpoint | Rôle(s) Requis | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/menu-items/` | Tous | Liste, filtre (`title`, `featured`, `category`), trie et pagine les éléments de menu. |
| **POST** | `/api/menu-items/` | Gestionnaire | Crée un nouvel élément de menu. |
| **GET** | `/api/menu-items/<int:pk>` | Tous | Détail d'un élément de menu. |
| **PUT/PATCH/DELETE** | `/api/menu-items/<int:pk>` | Gestionnaire | Modification ou suppression d'un élément. |

### 🛒 Gestion du Panier (Client)

| Méthode | Endpoint | Rôle(s) Requis | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/cart/menu-items/` | Authentifié | Affiche tous les articles dans le panier de l'utilisateur. |
| **POST** | `/api/cart/menu-items/` | Authentifié | Ajoute un article au panier (gère l'ajout ou la mise à jour de la quantité). |
| **DELETE** | `/api/cart/menu-items/` | Authentifié | Vide complètement le panier de l'utilisateur. |

### 📦 Gestion des Commandes

| Méthode | Endpoint | Rôle(s) Requis | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/orders/` | Authentifié | Affiche les commandes (toutes pour Gestionnaire, les siennes pour les autres). |
| **POST** | `/api/orders/` | Authentifié | Crée une nouvelle commande à partir du contenu du panier. |
| **GET** | `/api/orders/<int:pk>` | Authentifié | Affiche les `OrderItem`s d'une commande spécifique. |
| **PATCH** | `/api/orders/<int:pk>` | Livreur | Met à jour le statut de livraison d'une commande (champ `status`). |
| **PUT/DELETE** | `/api/orders/<int:pk>` | Gestionnaire | Modification complète ou suppression d'une commande. |

### 👥 Gestion des Utilisateurs (Gestionnaire)

| Méthode | Endpoint | Rôle(s) Requis | Description |
| :--- | :--- | :--- | :--- |
| **GET/POST** | `/api/groups/manager/users/` | Gestionnaire | Liste ou ajoute un utilisateur au groupe **Gestionnaire**. |
| **DELETE** | `/api/groups/manager/users/<int:pk>` | Gestionnaire | Retire un utilisateur du groupe **Gestionnaire**. |
| **GET/POST** | `/api/groups/delivery-crew/users/` | Gestionnaire | Liste ou ajoute un utilisateur au groupe **Livreur**. |
| **DELETE** | `/api/groups/delivery-crew/users/<int:pk>` | Gestionnaire | Retire un utilisateur du groupe **Livreur**. |

---

## 🔒 Sécurité et Autorisation

L'autorisation est gérée par la vérification de l'appartenance de l'utilisateur aux groupes Django :

```python
if request.user.groups.filter(name='Gestionnaire').exists():
    # L'utilisateur est autorisé à effectuer cette action d'administration
    pass
