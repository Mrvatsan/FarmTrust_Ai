import os
import cv2
import numpy as np
import tensorflow as tf
from ultralytics import YOLO

class FarmTrustClassifier:
    """
    Core Classification Model for FarmTrust AI.
    Handles Organic vs Inorganic classification using YOLOv8,
    with CLAHE preprocessing and synthetic NIR augmentation.
    """
    def __init__(self, model_path=None):
        # Using yolov8n-cls (classification nano) for speed and cross-platform compatibility
        if model_path and os.path.exists(model_path):
            self.model = YOLO(model_path)
        else:
            print("Initializing with base YOLOv8n-cls model...")
            self.model = YOLO('yolov8n-cls.pt')

    def apply_clahe(self, image_path):
        """
        Applies Contrast Limited Adaptive Histogram Equalization (CLAHE).
        Useful for enhancing wax/residue textures on fruit surfaces.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
            
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L-channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        
        # Merge channels back
        limg = cv2.merge((cl,a,b))
        final_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return final_img

    def synthetic_nir_augmentation(self, image):
        """
        Simulates Near-Infrared (NIR) spectral cues.
        NIR reflectance often differs significantly between organic (thin wax) 
        and inorganic (thick wax/pesticide residue) produce.
        """
        # Convert to float for manipulation
        nir_sim = image.copy().astype(np.float32)
        
        # In NIR, organic matter tends to reflect more in Red/IR wavelengths
        # We simulate this by enhancing red and suppressing blue/green noise
        nir_sim[:,:,2] *= 1.4 # Red channel enhancement
        nir_sim[:,:,0] *= 0.6 # Blue channel suppression
        nir_sim[:,:,1] *= 0.8 # Green channel suppression
        
        # Apply a slight blur to simulate the 'glow' often seen in NIR captures
        nir_sim = cv2.GaussianBlur(nir_sim, (5,5), 0)
        
        return np.clip(nir_sim, 0, 255).astype(np.uint8)

    def preprocess_multi_angle(self, top_path, side_path, cut_path):
        """
        Prepares images from three standard angles for unified feature extraction.
        """
        angles = {'top': top_path, 'side': side_path, 'cut': cut_path}
        processed_data = {}
        
        for angle, path in angles.items():
            img = self.apply_clahe(path)
            nir = self.synthetic_nir_augmentation(img)
            processed_data[angle] = {
                'clahe': img,
                'nir_sim': nir
            }
        return processed_data

    def train_on_kaggle(self, data_yaml_path, epochs=50):
        """
        Fine-tunes the YOLOv8 model on the specified dataset.
        """
        print(f"Starting fine-tuning on {data_yaml_path} for {epochs} epochs...")
        results = self.model.train(data=data_yaml_path, epochs=epochs, imgsz=224)
        return results

    def export_for_mobile(self, format='tflite'):
        """
        Exports the model to mobile-friendly formats (TFLite or TFJS).
        """
        print(f"Exporting model to {format} format...")
        export_path = self.model.export(format=format)
        return export_path

if __name__ == "__main__":
    # Example usage / Sanity check
    try:
        classifier = FarmTrustClassifier()
        print("FarmTrust Classifier Initialized Successfully.")
    except Exception as e:
        print(f"Initialization Failed: {e}")
