import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

import matplotlib.pyplot as plt

def create_nn_model(arg_lenth=None):
    """
    Fonction pour créer et compiler un modèle avec keras.
    """
    # Définition du modèle CNN avec Keras
    model = keras.Sequential([
        layers.Conv2D(16, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)),
        # Cette couche réduit la taille de l’image de moitié (de 28x28 à 14x14) en ne gardant que la valeur maximale dans chaque bloc 2x2.
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

def train_model(model, X, y, X_val=None, y_val=None, epochs=5, batch_size=32, validation_split=0.2, verbose=0 ):
    """
    Entraine le modèle de réseau de neurones sur les données fournies.
    Args:
        model: Modèle de réseau de neurones à entraîner.
        X: Données d'entrée pour l'entraînement (X_train)
        y: Cibles pour l'entraînement (y_train)
        X_val: Données d'entrée pour la validation (optionnel).
        y_val: Cibles pour la validation (optionnel).
        epochs: Nombre d'époques pour l'entraînement (par défaut 5).
        batch_size: Taille du lot pour l'entraînement (par défaut 32).
        validation_split: Proportion des données à utiliser pour la validation (par défaut 0.2).
        verbose: Niveau de verbosité de l'entraînement (par défaut 0, aucune sortie).
    """
    # Entraînement du modèle
    hist = model.fit(X, y, 
                validation_data=(X_val, y_val) if X_val is not None and y_val is not None else None,
                validation_split=validation_split,
                epochs=epochs, 
                batch_size=batch_size, 
                verbose=verbose)

    
    return model , hist


def model_predict(model, X):
    """
    Fonction pour prédire les valeurs cibles à partir des données d'entrée en utilisant le modèle de réseau de neurones.
    Args:
        model: Modèle de réseau de neurones entraîné : model_2024_08.pkl
        X: Données d'entrée pour la prédiction.
        Returns:
        y_pred: Prédictions du modèle sur les données d'entrée.
    """
        
    y_pred = model.predict(X).flatten()
    return y_pred

def model_evaluate(model, X_test, y_test):
    """
    Fonction pour évaluer le modèle de réseau de neurones sur les données de test.
    Args:
        model: Modèle de réseau de neurones entraîné.
        X_test: Données d'entrée pour les tests.
        y_test: Cibles pour les tests.
    Returns:
        accuracy: Précision du modèle sur les données de test.
        cm_display: Affichage de la matrice de confusion.
    """
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    
    # y_pred = model_predict(model, X_test)
    # accuracy = accuracy_score(y_test, y_pred.argmax(axis=1))
    
    # cm = confusion_matrix(y_test, y_pred.argmax(axis=1))
    # cm_display = ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    
    return loss, accuracy

def model_preprocess(df, settings=None):
    """
    Prétraitement pour MNIST :
    - Normalisation des pixels (0-255 -> 0-1)
    - Reshape éventuel pour CNN
    - One-hot encoding des labels pour categorical_crossentropy
    """
    X = df.drop(columns=["target"]).values.astype("float32") / 255.0
    X = X.reshape(-1, 28, 28, 1)  # Pour un CNN Keras
    y = to_categorical(df["target"].values.astype("int64"), num_classes=10)
    preprocessor = None  # Pas de pipeline complexe nécessaire
    return X, y, preprocessor

def model_print_draw(model):
    """
    Fonction pour afficher la structure du modèle de réseau de neurones.
    Args:
        model: Modèle de réseau de neurones à afficher.
    """
    model.summary()
    
    # Affichage des couches du modèle
    for layer in model.layers:
        print(f"Layer: {layer.name}, Output Shape: {layer.output_shape}, Parameters: {layer.count_params()}")
        
def draw_loss(history, cm, save_path=None):
    """
    Affiche ou enregistre les courbes de loss et val_loss de l'historique d'entraînement d'un modèle.
    loss  = perte sur l'ensemble d'entraînement
    val_loss = perte sur l'ensemble de validation
    
    Args:
        history: Objet d'historique retourné par l'entraînement du modèle (contenant 'loss' et 'val_loss').
        save_path: Chemin du fichier pour enregistrer la figure. Si None, affiche la figure.
    """
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=range(10))
    disp.plot(cmap='Blues')
    plt.title("Matrice de confusion - CNN (Keras)")
    
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Loss (Entraînement)')
    plt.plot(history.history['val_loss'], label='Val Loss (Validation)', linestyle='--')
    plt.title('Courbes de Loss et Val Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()      

def print_data(loss, accuracy):
    """
    Affiche les métriques de performance du modèle (loss, accuracy) dans la console.
    
    Args:
        loss (float): Perte du modèle sur les données de test.
        accuracy (float): Précision du modèle sur les données de test.
    """
    print(f"{'='*60}")
    print(f"Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")
    print(f"{'='*60}")

