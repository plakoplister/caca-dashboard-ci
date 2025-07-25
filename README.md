# 🌍 Dashboard Cacao Côte d'Ivoire

Dashboard professionnel d'analyse des exportations de cacao de Côte d'Ivoire (2013-2023).

## 📊 Fonctionnalités

- **Volumes par saison** : Analyse des 10 saisons cacaoyères
- **Top exportateurs** : Classement et parts de marché
- **Répartition produits** : Fèves, liqueur, beurre, poudre, chocolat
- **Destinations** : Top pays et destinataires
- **Évolution temporelle** : Tendances mensuelles et annuelles

## 🚀 Déploiement Streamlit Cloud

### Étape 1 : Créer un repository GitHub

1. Créez un nouveau repository sur GitHub
2. Uploadez ces fichiers :
   - `webapp_volumes_reels.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `DB - Cocoa CIV - Shipping 20212022.xlsb`
   - `README.md`

### Étape 2 : Déployer sur Streamlit Cloud

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez votre compte GitHub
3. Cliquez "New app"
4. Sélectionnez votre repository
5. Main file path : `webapp_volumes_reels.py`
6. Cliquez "Deploy!"

### Étape 3 : Configuration

L'application sera disponible sur une URL comme :
`https://your-app-name.streamlit.app`

## 📁 Structure du projet

```
cacao-dashboard/
├── webapp_volumes_reels.py      # Application principale
├── requirements.txt             # Dépendances Python
├── .streamlit/
│   └── config.toml             # Configuration Streamlit
├── DB - Cocoa CIV - Shipping 20212022.xlsb  # Données
└── README.md                   # Documentation
```

## 🔧 Développement local

```bash
pip install -r requirements.txt
streamlit run webapp_volumes_reels.py
```

## 📊 Données

Le dashboard analyse **18,86 millions de tonnes** de cacao exportées entre 2013-2023 :
- **131,293 opérations** d'exportation
- **2 ports** : Abidjan et San Pedro
- **99+ exportateurs**
- **76+ pays** de destination

## 🎨 Design

Interface moderne avec :
- Palette de couleurs professionnelle
- Police système élégante
- Responsive design
- Animations fluides

---

Développé avec ❤️ pour l'analyse du secteur cacaoyer ivoirien