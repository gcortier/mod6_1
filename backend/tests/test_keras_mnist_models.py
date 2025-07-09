import numpy as np
import pytest
from models.keras_mnist_models import (
    create_nn_model,
    train_model,
    model_predict,
    model_evaluate,
    model_preprocess
)

def test_create_nn_model():
    model = create_nn_model(input_dim=(28, 28, 1))
    assert model is not None
    assert hasattr(model, 'fit')

def test_model_preprocess():
    X = np.random.randint(0, 256, (10, 28, 28, 1), dtype=np.uint8)
    X_processed = model_preprocess(X)
    assert np.all(X_processed >= 0) and np.all(X_processed <= 1)
    assert X_processed.shape == (10, 28, 28, 1)

def test_train_and_evaluate():
    # Jeu de données jouet
    X = np.random.rand(100, 28, 28, 1).astype('float32')
    y = np.eye(10)[np.random.randint(0, 10, 100)]  # one-hot
    model = create_nn_model(input_dim=(28, 28, 1))
    model, hist = train_model(model, X, y, epochs=1, batch_size=16, validation_split=0.1, verbose=0)
    loss, acc = model_evaluate(model, X, y)
    assert 0 <= acc <= 1
    assert loss >= 0

def test_model_predict():
    X = np.random.rand(5, 28, 28, 1).astype('float32')
    model = create_nn_model(input_dim=(28, 28, 1))
    y = np.eye(10)[np.random.randint(0, 10, 5)]
    model, _ = train_model(model, X, y, epochs=1, batch_size=2, validation_split=0.1, verbose=0)
    y_pred = model_predict(model, X)
    assert y_pred.shape[0] == 50  # 5*10 flatten
