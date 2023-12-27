# Python_ENSAE_2A

Projet Python de deuxième année 2023-2024 pour le cours Python pour la Data Science réalisé par Yassine Boukhateb & Zakarya Elmimouni. 

## Le but de ce projet est de créer un sytème de recommendation de film. 
Pour cela nous avons travaillé les thématiques suivantes : 

* I. Récupération des données par l'API TMDB
* II. Nettoyage des données
* III. Visualisation des données
* IV. Modélisation par la cosine similarity
* V. Evaluation du modèle et conclusion
* VI. Annexe : Application

## Modules et packages nécessaires :

1. Récupération et export des données

  `import requests`

  `import json`

  `import pandas as pd`

  `import pickle`
  
2. Visualisation et analyse des données

  `import numpy as np`

  `import matplotlib.pyplot as plt`

  `import geopandas as` 

  `import contextily as ctx`

  `import seaborn as sns`

4. Modélisation

  `from nltk.stem.porter import PorterStemmer`

  `from sklearn.feature_extraction.text import CountVectorizer`

  `from sklearn.metrics.pairwise import cosine_similarity`


5. Application

  `import dash`

  `from dash import html, dcc`

  `from dash.dependencies import Input, Output`

  `import pickle`

  `import pandas as pd` 