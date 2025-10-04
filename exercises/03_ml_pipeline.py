"""
Exercise 3: ML Pipeline Implementation
Build a complete machine learning pipeline
"""

class SimpleMLPipeline:
    def __init__(self):
        self.is_fitted = False
        self.mean = None
        self.std = None
    
    def preprocess(self, X):
        """Normalize features"""
        # TODO: Implement standardization (mean=0, std=1)
        pass
    
    def fit(self, X, y):
        """Train the pipeline"""
        # TODO: Calculate mean and std for normalization
        # TODO: Set is_fitted to True
        pass
    
    def predict(self, X):
        """Make predictions"""
        # TODO: Check if fitted, preprocess X, return dummy predictions
        pass
    
    def evaluate(self, X, y):
        """Calculate accuracy"""
        # TODO: Get predictions and calculate accuracy
        pass

# Usage example
if __name__ == "__main__":
    # Sample data
    X_train = [[1, 2], [2, 3], [3, 4], [4, 5]]
    y_train = [0, 0, 1, 1]
    X_test = [[1.5, 2.5], [3.5, 4.5]]
    y_test = [0, 1]
    
    # Create and use pipeline
    pipeline = SimpleMLPipeline()
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    accuracy = pipeline.evaluate(X_test, y_test)
    
    print(f"Predictions: {predictions}")
    print(f"Accuracy: {accuracy}")