# Ce script définit le service BentoML qui expose notre modèle SVR optimisé.
#Il assure le lien entre les données envoyées par l'utilisateur et les exigences mathématiques du modèle entraîné.

#Import des librairies et configuration
import bentoml
import numpy as np
import pandas as pd
from .validation import BuildingData

# Chargement des ressources
model_info = bentoml.sklearn.get("seattle_energy_svr:latest")
model_instance = bentoml.sklearn.load_model("seattle_energy_svr:latest")
scaler_instance = model_info.custom_objects["scaler"]
features_list = model_info.custom_objects["features"]

@bentoml.service(name="energy_prediction_service")
class EnergyService:
    @bentoml.api
    def predict(self, data: BuildingData) -> dict:
        input_dict = data.model_dump() if hasattr(data, 'model_dump') else data.dict()

        # 1. Création du DataFrame initial (avec tes 24 noms connus)
        full_input = pd.DataFrame(0.0, index=[0], columns=features_list)
        
        # 2. Remplissage des valeurs de base
        if 'PropertyGFATotal' in input_dict:
            full_input.at[0, 'PropertyGFATotal_log'] = np.log1p(float(input_dict['PropertyGFATotal']))
        
        for col in ['BuildingAge', 'NumberofFloors', 'HasGas']:
            if col in input_dict:
                full_input.at[0, col] = float(input_dict[col])
        
        # 3. Gestion du décalage (Scaler=25, SVR=24)
        try:
            v = full_input.values
            n_scaler = scaler_instance.n_features_in_ # Doit être 25
            
            # On ajuste à 25 pour le Scaler
            if v.shape[1] < n_scaler:
                v = np.pad(v, ((0, 0), (0, n_scaler - v.shape[1])), mode='constant')
            
            # Étape A: On scale avec les 25 colonnes
            input_scaled = scaler_instance.transform(v)
            
            # Étape B: On ne garde que les 24 premières pour le SVR
            # C'est ici que l'erreur se corrige !
            input_for_model = input_scaled[:, :24] 
            
            # Étape C: Prédiction
            log_pred = model_instance.predict(input_for_model)
            
            # 5. Résultat
            prediction = np.expm1(log_pred)[0]
            
            return {
                "prediction_kbtu": round(float(prediction), 2),
                "status": "success"
            }
        except Exception as e:
            return {"status": "error", "message": f"Erreur de calcul: {str(e)}"}

svc = EnergyService