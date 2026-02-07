import os
import numpy as np

class CarbonTracker:
    """
    Sustainability Carbon Tracker using XGBoost-like logic.
    Estimates produce weight from image dimensions and calculates CO2 footprint.
    """
    def __init__(self):
        # Emission factors (kg CO2 per kg produce)
        self.emission_factors = {
            "Tomato": {"local": 0.3, "imported": 1.5, "avg_density": 0.95},
            "Banana": {"local": 0.2, "imported": 0.8, "avg_density": 0.92},
            "Apple": {"local": 0.4, "imported": 1.2, "avg_density": 0.85}
        }
        print("Sustainability Carbon Tracker Initialized.")

    def estimate_weight(self, area_pixels, distance_cm=30, produce_type="Tomato"):
        """
        Estimates weight using bounding box area and distance (simulating XGBoost).
        Formula: Volume proxy * Density
        """
        # Simplified geometric proxy: Area to Volume
        # In production, XGBoost would use [area, perimeter, eccentricity, distance, type]
        density = self.emission_factors.get(produce_type, {"avg_density": 0.9})["avg_density"]
        
        # Scaling factor based on camera distance (simulated)
        pixel_to_cm2 = (distance_cm / 500) ** 2 
        area_cm2 = area_pixels * pixel_to_cm2
        
        # Volume estimate (assuming spherical proxy)
        radius = np.sqrt(area_cm2 / np.pi)
        volume = (4/3) * np.pi * (radius ** 3)
        
        weight_kg = (volume * density) / 1000 # Convert to kg
        return round(weight_kg, 2)

    def calculate_co2(self, weight_kg, produce_type, is_local=True):
        """
        Calculates CO2 based on provenance.
        """
        factors = self.emission_factors.get(produce_type, {"local": 0.5, "imported": 1.5})
        factor = factors["local"] if is_local else factors["imported"]
        
        co2_kg = weight_kg * factor
        return round(co2_kg, 2)

    def get_sustainability_report(self, area_pixels, produce_type, origin_geo):
        """
        Generates a summary report.
        """
        weight = self.estimate_weight(area_pixels, produce_type=produce_type)
        is_local = "Local" in origin_geo # Simple proxy
        
        co2 = self.calculate_co2(weight, produce_type, is_local)
        
        report = (
            f"Sustainability Report for {produce_type}:\n"
            f"- Estimated Weight: {weight}kg\n"
            f"- Origin: {origin_geo}\n"
            f"- Carbon Footprint: {co2}kg CO2\n"
        )
        
        if not is_local:
            local_co2 = self.calculate_co2(weight, produce_type, True)
            report += f"💡 Switch to local {produce_type} to save {round(co2 - local_co2, 2)}kg CO2!"
            
        return report

if __name__ == "__main__":
    tracker = CarbonTracker()
    print(tracker.get_sustainability_report(area_pixels=50000, produce_type="Tomato", origin_geo="Imported"))
