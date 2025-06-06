import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray
import pandas as pd
import uuid

class AnimalSculptureClassifier:
    def __init__(self, model_path=None):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.model_path = model_path
        self.classes = ['lion', 'elephant', 'bird', 'horse', 'other']  # Example animal classes
        if model_path and os.path.exists(model_path):
            self.load_model()

    def preprocess_image(self, image_path):
        """Preprocess image for classification."""
        try:
            image = imread(image_path)
            image = rgb2gray(image)
            image = resize(image, (100, 100))
            image = image.flatten()
            return image
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None

    def train(self, image_paths, labels):
        """Train the classifier with images and labels."""
        features = []
        for path in image_paths:
            feat = self.preprocess_image(path)
            if feat is not None:
                features.append(feat)
        features = np.array(features)
        features = self.scaler.fit_transform(features)
        self.model.fit(features, labels)

    def predict(self, image_path):
        """Predict the animal sculpture type."""
        features = self.preprocess_image(image_path)
        if features is not None:
            features = self.scaler.transform([features])
            prediction = self.model.predict(features)[0]
            return prediction
        return None

    def save_model(self, path):
        """Save the trained model."""
        import joblib
        joblib.dump({'model': self.model, 'scaler': self.scaler}, path)

    def load_model(self):
        """Load a trained model."""
        import joblib
        data = joblib.load(self.model_path)
        self.model = data['model']
        self.scaler = data['scaler']

    def store_sculpture_data(self, image_path, prediction, price, dataframe_path='sculptures.csv'):
        """Store sculpture data in a DataFrame."""
        unique_code = str(uuid.uuid4())
        data = {
            'unique_code': unique_code,
            'image_path': image_path,
            'animal_type': prediction,
            'price': price
        }
        df = pd.DataFrame([data])
        if os.path.exists(dataframe_path):
            existing_df = pd.read_csv(dataframe_path)
            df = pd.concat([existing_df, df], ignore_index=True)
        df.to_csv(dataframe_path, index=False)
        return unique_code
