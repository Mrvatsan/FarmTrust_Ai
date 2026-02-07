import os
import numpy as np

class AllergyRiskScanner:
    """
    Allergy-Risk Scanner using Graph-based logic.
    Maps detected residues to chemical sensitivity risks and common allergens.
    """
    def __init__(self):
        # Simplified Pesticide to Allergen/Sensitivity Map
        # In a real scenario, this would be a GNN (e.g., using DGL or PyG)
        self.pesticide_db = {
            "Thiabendazole": {
                "risk": "HIGH",
                "sensitivity": "Chemical sensitivity",
                "symptoms": "Nausea, skin irritation",
                "related_allergens": ["Latex", "Mold"] # Cross-reactivity proxy
            },
            "Chlorpyrifos": {
                "risk": "SEVERE",
                "sensitivity": "Neurological sensitivity",
                "symptoms": "Headache, dizziness",
                "related_allergens": []
            },
            "Glyphosate": {
                "risk": "MEDIUM",
                "sensitivity": "General irritant",
                "symptoms": "Digestive discomfort",
                "related_allergens": ["Gluten"] # Simulated link for prototype
            }
        }
        print("Allergy-Risk Scanner Initialized.")

    def scan_for_risks(self, detected_chemicals):
        """
        Cross-references detected chemicals with the database.
        """
        risks = []
        for chemical in detected_chemicals:
            if chemical in self.pesticide_db:
                risks.append({
                    "chemical": chemical,
                    "info": self.pesticide_db[chemical]
                })
        return risks

    def get_allergy_warning(self, detected_chemicals):
        """
        Generates a user-friendly warning message.
        """
        risks = self.scan_for_risks(detected_chemicals)
        if not risks:
            return "✅ No high-risk pesticide residues detected matching your profile."
            
        warnings = []
        for r in risks:
            warning = f"⚠️ {r['chemical']} detected - {r['info']['risk']} risk for {r['info']['sensitivity']}."
            if r['info']['related_allergens']:
                warning += f" (Cross-reactivity path: {', '.join(r['info']['related_allergens'])})"
            warnings.append(warning)
            
        return "\n".join(warnings)

if __name__ == "__main__":
    scanner = AllergyRiskScanner()
    test_chemicals = ["Thiabendazole", "Glyphosate"]
    print(scanner.get_allergy_warning(test_chemicals))
