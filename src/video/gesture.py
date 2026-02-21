import numpy as np
from joblib import load
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

class Gesture:
    def __init__(self, model=r"models\runs\knn\knn.joblib", scaler=r"models\runs\knn\scaler.joblib"):
        self.model = load(model) if model else KNeighborsClassifier(n_neighbors=3)
        self.scaler = load(scaler) if scaler else StandardScaler()

    def flatten_keypoints(self, keypoints):
        base_x, base_y = keypoints[0]
        relative_coords = keypoints - [base_x, base_y]
        
        flattened = relative_coords.flatten()
        
        max_val = np.max(np.abs(flattened))
        if max_val > 0:
            flattened = flattened / max_val
            
        return flattened
    
    def detect_gesture(self, keypoints):
        if len(keypoints) == 0:
            return (0.0, None)
        
        keypoints = self.flatten_keypoints(keypoints)
        vector = self.scaler.transform([keypoints])
        label = self.model.predict(vector)[0]
        confidence = max(self.model.predict_proba(vector)[0])
        return confidence, label