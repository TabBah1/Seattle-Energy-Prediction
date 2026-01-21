# Ce script utilise la bibliothèque Pydantic pour définir le schéma de données attendu par l'API. 
# Son rôle est de garantir que seules des données valides et cohérentes sont traitées par le modèle SVR.

from pydantic import BaseModel, Field

class BuildingData(BaseModel):
    # Caractéristiques physiques (Numériques)
    PropertyGFATotal: float = Field(..., gt=0, description="Surface totale du bâtiment")
    NumberofFloors: int = Field(..., ge=1, description="Nombre d'étages")
    BuildingAge: int = Field(..., ge=0, description="Âge du bâtiment")
    
    # Variable binaire (Gaz : 0 ou 1)
    HasGas: int = Field(..., ge=0, le=1, description="Présence de gaz (1/0)")

    # AJOUT : La variable manquante identifiée par l'erreur
    ENERGYSTARScore: float = Field(default=50.0, ge=0, le=100, description="Score Energy Star")

    class Config:
        json_schema_extra = {
            "example": {
                "PropertyGFATotal": 50000.0,
                "NumberofFloors": 5,
                "BuildingAge": 25,
                "HasGas": 1,
                "ENERGYSTARScore": 65.0
            }
        }