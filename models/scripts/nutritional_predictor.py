import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np

class NutritionalDeficiencyPredictor:
    """
    Nutritional Deficiency Predictor using ResNet-50.
    Detects N/P/K/Ca deficiencies based on visual discoloration and necrosis patterns.
    """
    def __init__(self, model_path=None):
        # Using pre-trained ResNet-50 as a base
        self.model = models.resnet50(pretrained=True)
        # Assuming 5 classes for now: Healthy, N-Deficiency, P-Deficiency, K-Deficiency, Ca-Deficiency
        num_ftrs = self.model.fc.in_features
        self.model.fc = torch.nn.Linear(num_ftrs, 5)
        
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.classes = ['Healthy', 'Nitrogen (N) deficiency', 'Phosphorus (P) deficiency', 'Potassium (K) deficiency', 'Calcium (Ca) deficiency']

    def predict(self, image_path):
        """
        Predicts the nutritional deficiency from an image.
        """
        image = Image.open(image_path).convert('RGB')
        image_tensor = self.transform(image).unsqueeze(0)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted_idx = torch.max(probabilities, 0)
            
        result = {
            'deficiency': self.classes[predicted_idx],
            'confidence': confidence.item(),
            'severity': self.estimate_severity(image_path, predicted_idx)
        }
        return result

    def estimate_severity(self, image_path, deficiency_idx):
        """
        Estimates severity based on the area of discoloration.
        1. Healthy: 0%
        2. Others: Calculated via pixel intensity/color thresholding.
        """
        if deficiency_idx == 0:
            return "0%"
            
        img = cv2.imread(image_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Define ranges for "unhealthy" colors (yellowing, browning, etc.)
        # This is a simplified proxy - real models would use semantic segmentation
        lower_unhealthy = np.array([5, 50, 50])
        upper_unhealthy = np.array([30, 255, 255])
        
        mask = cv2.inRange(hsv, lower_unhealthy, upper_unhealthy)
        total_pixels = mask.size
        unhealthy_pixels = cv2.countNonZero(mask)
        
        severity_val = (unhealthy_pixels / total_pixels) * 100
        return f"{min(99, int(severity_val * 2))}%" # Scale for demonstration

if __name__ == "__main__":
    predictor = NutritionalDeficiencyPredictor()
    print("Nutritional Deficiency Predictor Initialized.")
