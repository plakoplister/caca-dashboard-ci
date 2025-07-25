#!/usr/bin/env python3
"""
CACAO CÔTE D'IVOIRE - DASHBOARD PROFESSIONNEL
Analyse des exportations de cacao (2013-2023)
Optimisé pour Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(
    page_title="Cacao Côte d'Ivoire - Dashboard", 
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io/community',
        'Report a bug': None,
        'About': "Dashboard d'analyse des exportations de cacao - Côte d'Ivoire 2013-2023"
    }
)

@st.cache_data(ttl=3600)
def load_real_volumes():
    """Chargement avec volumes RÉELS garantis - Optimisé pour cloud"""
    
    try:
        # Vérifier l'existence des fichiers
        file_path = "DB - Cocoa CIV - Shipping 20212022.xlsb"
        if not os.path.exists(file_path):
            st.error(f"❌ Fichier non trouvé: {file_path}")
            st.info("Assurez-vous que le fichier de données est présent dans le repository")
            return None
        
        # Charger ABJ et SP avec TOUTES les données
        with st.spinner("Chargement des données..."):
            abj = pd.read_excel(file_path, sheet_name="DB ABJ", engine='pyxlsb')
            sp = pd.read_excel(file_path, sheet_name="DB SP", engine='pyxlsb')
        
        # Ajouter source
        abj['PORT'] = 'ABIDJAN'
        sp['PORT'] = 'SAN PEDRO'
        
        # Combiner
        df = pd.concat([abj, sp], ignore_index=True)
        
        # Nettoyer volume
        df = df.dropna(subset=['PDSNET'])
        df = df[df['PDSNET'] > 0]
        df['VOLUME_TONNES'] = df['PDSNET'] / 1000
        
        # DATES CORRECTES - Méthode directe
        df['DATENR'] = pd.to_numeric(df['DATENR'], errors='coerce')
        df = df.dropna(subset=['DATENR'])
        
        # Conversion Excel date correcte
        df['DATE'] = pd.to_datetime('1900-01-01') + pd.to_timedelta(df['DATENR'] - 2, unit='D')
        
        # SAISONS DIRECTES - Méthode simple
        df['ANNEE'] = df['DATE'].dt.year
        df['MOIS'] = df['DATE'].dt.month
        
        # Saison cacaoyère SIMPLE
        conditions = [
            (df['MOIS'] >= 10),  # Oct-Déc = année courante-suivante
            (df['MOIS'] <= 9)    # Jan-Sep = année précédente-courante
        ]
        choices = [
            df['ANNEE'].astype(str) + '-' + (df['ANNEE'] + 1).astype(str),
            (df['ANNEE'] - 1).astype(str) + '-' + df['ANNEE'].astype(str)
        ]
        df['SAISON'] = pd.Series(np.select(conditions, choices, default='INCONNU'))
        
        # Produits simples
        def get_produit_simple(postar):
            if pd.isna(postar):
                return 'AUTRE'
            try:
                code = str(int(postar))[:4]
                return {'1801': 'FÈVES', '1803': 'LIQUEUR', '1804': 'BEURRE', 
                       '1805': 'POUDRE', '1806': 'CHOCOLAT'}.get(code, 'AUTRE')
            except:
                return 'AUTRE'
        
        df['PRODUIT'] = df['POSTAR'].apply(get_produit_simple)
        
        # Colonnes finales
        df['EXPORTATEUR'] = df['EXPORTATEUR SIMPLE'].fillna('INCONNU')
        df['DESTINATION'] = df['DESTINATION'].fillna('INCONNU')
        
        # Sauvegarder les stats pour affichage ultérieur
        df.attrs['saisons_volumes'] = df.groupby('SAISON')['VOLUME_TONNES'].sum().sort_index()
        
        return df
        
    except Exception as e:
        st.error(f"Erreur: {e}")
        return None

def check_authentication():
    """Système d'authentification simple"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown('<h1 class="main-title">CACAO CÔTE D\'IVOIRE</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Accès sécurisé au dashboard</p>', unsafe_allow_html=True)
        
        # Interface de connexion élégante
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Authentification")
            password = st.text_input("Code d'accès", type="password", placeholder="Entrez votre code")
            
            if st.button("Se connecter", use_container_width=True):
                if password == "jo06v2":
                    st.session_state.authenticated = True
                    st.success("✅ Accès autorisé")
                    st.rerun()
                else:
                    st.error("❌ Code d'accès incorrect")
            
            # Info de contact (optionnel)
            st.markdown("---")
            st.markdown("*Pour obtenir l'accès, contactez l'administrateur*")
        
        st.stop()

def main():
    # Vérification de l'authentification en premier
    check_authentication()
    
    # CSS élégant avec police professionnelle
    st.markdown("""
    <style>
        /* Police professionnelle pour tout */
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        }
        
        .main-title {
            font-size: 2.5rem;
            font-weight: 300;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 0.5rem;
            letter-spacing: 1px;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 300;
        }
        .metric-container {
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .season-info {
            background: #fafafa;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 2rem;
            border-left: 3px solid #7f8c8d;
        }
        
        /* Harmonisation des métriques Streamlit */
        [data-testid="metric-container"] {
            font-weight: 300;
        }
        [data-testid="metric-container"] > div:first-child {
            font-weight: 400;
            font-size: 0.9rem;
            color: #7f8c8d;
        }
        [data-testid="metric-container"] > div:nth-child(2) {
            font-weight: 300;
            font-size: 2rem;
        }
        
        /* Style des headers */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 300;
            letter-spacing: 0.5px;
            color: #2c3e50;
        }
        
        /* Style général du texte */
        p, span, div {
            font-weight: 300;
            color: #2c3e50;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">CACAO CÔTE D\'IVOIRE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Dashboard d\'analyse des exportations</p>', unsafe_allow_html=True)
    
    # Chargement
    df = load_real_volumes()
    
    if df is None:
        return
    
    # Métriques globales
    total_volume = df['VOLUME_TONNES'].sum()
    st.metric("Volume Total Toutes Saisons", f"{total_volume:,.0f} tonnes")
    
    # Filtres
    st.sidebar.header("Filtres")
    
    # Bouton de déconnexion
    if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    
    saisons = sorted([str(x) for x in df['SAISON'].unique() if pd.notna(x)])
    saison_selected = st.sidebar.selectbox("Saison", options=saisons, index=len(saisons)-1)
    
    # Filtrer sur saison
    df_saison = df[df['SAISON'] == saison_selected].copy()
    
    if len(df_saison) == 0:
        st.warning(f"Aucune donnée pour {saison_selected}")
        return
    
    # Métriques saison
    st.subheader(f"Saison {saison_selected}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Volume Total", f"{df_saison['VOLUME_TONNES'].sum():,.0f} tonnes")
    with col2:
        st.metric("Expéditions", f"{len(df_saison):,}")
    with col3:
        st.metric("Exportateurs", f"{df_saison['EXPORTATEUR'].nunique()}")
    with col4:
        feves = df_saison[df_saison['PRODUIT'] == 'FÈVES']['VOLUME_TONNES'].sum()
        st.metric("Fèves", f"{feves:,.0f} tonnes")
    
    # Graphiques - Ligne 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Top exportateurs
        top_exp = df_saison.groupby('EXPORTATEUR')['VOLUME_TONNES'].sum().sort_values(ascending=False).head(10)
        fig1 = px.bar(x=top_exp.values, y=top_exp.index, orientation='h',
                     title="Top 10 Exportateurs", labels={'x': 'Tonnes', 'y': 'Exportateur'},
                     color_discrete_sequence=['#34495e'])
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Répartition produits
        prod_vol = df_saison.groupby('PRODUIT')['VOLUME_TONNES'].sum()
        fig2 = px.pie(values=prod_vol.values, names=prod_vol.index, title="Répartition par Produit",
                     color_discrete_sequence=['#2c3e50', '#34495e', '#5a6c7d', '#7f8c8d', '#95a5a6', '#bdc3c7'])
        st.plotly_chart(fig2, use_container_width=True)
    
    # Graphiques - Ligne 2
    col3, col4 = st.columns(2)
    
    with col3:
        # Top destinataires
        if 'DESTINATAIRE SIMPLE' in df_saison.columns:
            top_dest = df_saison.groupby('DESTINATAIRE SIMPLE')['VOLUME_TONNES'].sum().sort_values(ascending=False).head(10)
            fig3 = px.bar(x=top_dest.values, y=top_dest.index, orientation='h',
                         title="Top 10 Destinataires", labels={'x': 'Tonnes', 'y': 'Destinataire'},
                         color_discrete_sequence=['#5a6c7d'])
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Données destinataires non disponibles")
    
    with col4:
        # Histogramme pays de destination
        pays_vol = df_saison.groupby('DESTINATION')['VOLUME_TONNES'].sum().sort_values(ascending=False).head(15)
        fig4 = px.bar(x=pays_vol.index, y=pays_vol.values,
                     title="Top 15 Pays de Destination", labels={'x': 'Pays', 'y': 'Tonnes'},
                     color_discrete_sequence=['#7f8c8d'])
        fig4.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Évolution mensuelle
    st.subheader("Évolution Mensuelle")
    df_saison['MOIS_NOM'] = df_saison['DATE'].dt.strftime('%Y-%m')
    vol_mensuel = df_saison.groupby('MOIS_NOM')['VOLUME_TONNES'].sum().reset_index()
    fig3 = px.bar(vol_mensuel, x='MOIS_NOM', y='VOLUME_TONNES', title="Volume par Mois",
                 color_discrete_sequence=['#34495e'])
    st.plotly_chart(fig3, use_container_width=True)
    
    # Validation finale
    st.subheader("Validation")
    st.write(f"**Données chargées pour {saison_selected}:**")
    st.write(f"- Volume total: {df_saison['VOLUME_TONNES'].sum():,.0f} tonnes")
    st.write(f"- Fèves: {df_saison[df_saison['PRODUIT'] == 'FÈVES']['VOLUME_TONNES'].sum():,.0f} tonnes")
    st.write(f"- Liqueur: {df_saison[df_saison['PRODUIT'] == 'LIQUEUR']['VOLUME_TONNES'].sum():,.0f} tonnes")
    st.write(f"- Nombre d'expéditions: {len(df_saison):,}")
    
    # Table détaillée
    if st.checkbox("Voir données détaillées"):
        cols = ['DATE', 'EXPORTATEUR', 'PRODUIT', 'DESTINATION', 'PORT', 'VOLUME_TONNES']
        st.dataframe(df_saison[cols].head(100))
    
    # Afficher volumes historiques en bas
    st.markdown("---")
    st.subheader("Historique des Volumes par Saison")
    
    if hasattr(df, 'attrs') and 'saisons_volumes' in df.attrs:
        saisons_volumes = df.attrs['saisons_volumes']
        
        # Créer un graphique élégant
        fig_historique = px.bar(
            x=saisons_volumes.index, 
            y=saisons_volumes.values,
            title="Évolution des Volumes d'Exportation (2013-2023)",
            labels={'x': 'Saison Cacaoyère', 'y': 'Volume (tonnes)'},
            color=saisons_volumes.values,
            color_continuous_scale='Greys'
        )
        fig_historique.update_layout(
            showlegend=False,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12)
        )
        st.plotly_chart(fig_historique, use_container_width=True)
        
        # Tableau récapitulatif élégant
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown('<div class="season-info">', unsafe_allow_html=True)
            st.markdown("**Récapitulatif des Volumes**")
            for saison, volume in saisons_volumes.items():
                st.write(f"• Saison {saison} : **{volume:,.0f}** tonnes")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
