# **TP Multithreading**

Ce projet a pour but de comparer différentes approches pour l'exécution parallèle de tâches. La tâche à réaliser consiste en l'inversion de matrices.

## **Description**

Le projet repose sur une architecture composée des éléments suivants :
- **Queue Manager (QueueManager.py)** : Gère les files de tâches et de résultats.
- **Boss** : Crée les tâches, les ajoute dans la file des tâches, et récupère les résultats.
- **Minions** : Récupèrent les tâches, les exécutent, et ajoutent les résultats dans la file des résultats.

### **Types de Minions**
1. **Minion Python (Minion.py)** : Écrit en Python.
2. **Minion C++ (low_level.cpp)** : Communique avec le gestionnaire de queue à l’aide d’un proxy Python (proxy.py) pour échanger des données sérialisées.

---

## **Installation et Compilation**

### **Cloner le repository**
Assurez-vous d'avoir installé `uv`. Ensuite, synchronisez les dépendances :
```bash
uv sync --dev
```

### **Minion C++**
Pour compiler le Minion C++, utilisez CMake :
```bash
# Configure
cmake -B build -S .

# Compile
cmake --build build
```

---

## **Tests et Résultats**

### **1. Comparaison entre Minion Python et Minion C++**
Les tests suivants ont été réalisés avec des matrices de taille fixe (500x500). Le temps mesuré correspond uniquement à la résolution des matrices.

#### **Scénario 1 : 1 Minion Python**
- Nombre de tâches : 20
- Nombre de minions : 1
- Temps total (s) : **0.0684**

#### **Scénario 2 : 1 Minion C++**
- Nombre de tâches : 20
- Nombre de minions : 1
- Temps total (s) : **0.1894**

**Conclusion :** Python est environ 2,8 fois plus rapide que C++ dans ce cas particulier. Cela est probablement dû à l’optimisation poussée de **NumPy** pour ce type de résolution linéaire.

---

### **2. Parallélisation des Tâches**
Les tests suivants montrent l’impact de la parallélisation sur le temps total d’exécution.
- Taille des matrices : 1500x1500
- Nombre de tâches : 100
- Minions lancés dans des processus distincts (script : `execute_n_minion.sh`).
- Le temps mesuré débute à la création des tâches et se termine à l’exécution de la dernière tâche.

#### **Scénario 1 : 1 Minion Python**
- Nombre de minions : 1
- Temps total (s) : **20.63**

#### **Scénario 2 : 2 Minions Python**
- Nombre de minions : 2
- Temps total (s) : **12.46**

#### **Scénario 3 : 4 Minions Python**
- Nombre de minions : 4
- Temps total (s) : **11.81**

#### **Scénario 4 : 6 Minions Python**
- Nombre de minions : 6
- Temps total (s) : **12.61**

#### **Scénario 5 : 12 Minions Python**
- Nombre de minions : 12
- Temps total (s) : **13.80**

---

### **Conclusion**
Les résultats montrent clairement l’impact de la parallélisation :
- Avec un seul minion, le temps total est de **20,63 secondes**.
- L’ajout de minions réduit significativement le temps d’exécution, atteignant un minimum de **11,81 secondes avec 4 minions**.
- Au-delà de 4 minions, les gains diminuent et le temps d’exécution augmente légèrement.

Cela s’explique par la configuration matérielle : le processeur dispose de **6 cœurs physiques**, mais l'exécution d'autres processus en arrière-plan limite l'efficacité au-delà de 4 à 6 minions. De plus, l’overhead lié à la gestion des processus devient plus important que les gains obtenus par la parallélisation.

---

### **Ordre d'Exécution Recommandé**
1. **QueueManager**
2. **Boss**
3. **Minions Python ou Proxy + Minion C++**

---
