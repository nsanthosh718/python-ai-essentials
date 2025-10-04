# Python Essentials for AI Engineering

## 1. Core Python Fundamentals

### Data Types & Variables
```python
# Essential data types
numbers = 42
text = "AI Engineer"
is_learning = True
data_list = [1, 2, 3, 4, 5]
data_dict = {"name": "model", "accuracy": 0.95}
```

### Control Flow
```python
# Conditional logic
if accuracy > 0.9:
    print("Good model")
elif accuracy > 0.8:
    print("Decent model")
else:
    print("Needs improvement")

# Loops for data processing
for epoch in range(100):
    # Training loop
    pass

# List comprehensions (crucial for data manipulation)
squared = [x**2 for x in range(10)]
filtered_data = [x for x in data if x > threshold]
```

## 2. Functions & Classes

### Functions
```python
def preprocess_data(data, normalize=True):
    """Essential for data preprocessing pipelines"""
    if normalize:
        return (data - data.mean()) / data.std()
    return data

# Lambda functions for quick operations
transform = lambda x: x * 2 + 1
```

### Classes (for custom models/components)
```python
class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.weights = []
    
    def forward(self, x):
        # Forward pass implementation
        return x
    
    def train(self, data, labels):
        # Training logic
        pass
```

## 3. Essential Libraries

### NumPy - Numerical Computing
```python
import numpy as np

# Arrays and matrices
data = np.array([[1, 2], [3, 4]])
weights = np.random.randn(784, 128)

# Mathematical operations
result = np.dot(data, weights)
normalized = data / np.linalg.norm(data)
```

### Pandas - Data Manipulation
```python
import pandas as pd

# Data loading and exploration
df = pd.read_csv('dataset.csv')
print(df.head(), df.info(), df.describe())

# Data cleaning
df.dropna(inplace=True)
df['new_feature'] = df['feature1'] * df['feature2']
```

### Matplotlib/Seaborn - Visualization
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Essential plots for AI
plt.plot(epochs, loss)
plt.xlabel('Epochs')
plt.ylabel('Loss')

# Data distribution
sns.histplot(data['target'])
sns.heatmap(correlation_matrix)
```

## 4. File I/O & Data Handling

```python
# Reading different file formats
import json
import pickle

# JSON for configurations
with open('config.json', 'r') as f:
    config = json.load(f)

# Pickle for model saving
with open('model.pkl', 'wb') as f:
    pickle.dump(trained_model, f)

# CSV handling
data = pd.read_csv('training_data.csv')
```

## 5. Error Handling

```python
try:
    model = load_model('model.pkl')
except FileNotFoundError:
    print("Model not found, training new model...")
    model = train_new_model()
except Exception as e:
    print(f"Error loading model: {e}")
```

## 6. Advanced Python for AI

### Decorators (for timing, logging)
```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def train_model(data):
    # Training code
    pass
```

### Generators (for large datasets)
```python
def data_generator(batch_size=32):
    """Memory-efficient data loading"""
    while True:
        batch = load_batch(batch_size)
        yield batch
```

### Context Managers
```python
class ModelTrainer:
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Training completed in {time.time() - self.start_time:.2f}s")

# Usage
with ModelTrainer() as trainer:
    trainer.train()
```

## 7. Essential Patterns for AI

### Data Pipeline
```python
class DataPipeline:
    def __init__(self):
        self.steps = []
    
    def add_step(self, func):
        self.steps.append(func)
        return self
    
    def process(self, data):
        for step in self.steps:
            data = step(data)
        return data

# Usage
pipeline = (DataPipeline()
           .add_step(normalize)
           .add_step(remove_outliers)
           .add_step(feature_engineering))
```

### Configuration Management
```python
from dataclasses import dataclass

@dataclass
class ModelConfig:
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 100
    hidden_layers: list = None
    
    def __post_init__(self):
        if self.hidden_layers is None:
            self.hidden_layers = [128, 64]
```

## Next Steps

1. **Practice with real datasets** - Kaggle, UCI ML Repository
2. **Learn specific AI libraries**:
   - **Scikit-learn** - Traditional ML
   - **TensorFlow/PyTorch** - Deep Learning
   - **Transformers** - NLP
   - **OpenCV** - Computer Vision

3. **Build projects**:
   - Image classifier
   - Text sentiment analyzer
   - Recommendation system
   - Time series predictor

4. **Advanced topics**:
   - Async programming for API serving
   - Docker for model deployment
   - Git for version control
   - Testing for ML code