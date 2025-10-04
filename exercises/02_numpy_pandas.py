"""
Exercise 2: NumPy and Pandas for AI
Essential data manipulation skills
"""

import numpy as np
import pandas as pd

# NumPy exercises
def matrix_operations():
    """Practice essential NumPy operations"""
    # Create a 3x3 matrix with random values
    matrix = np.random.randn(3, 3)
    
    # TODO: Calculate mean, std, and normalize the matrix
    # TODO: Perform matrix multiplication with its transpose
    # TODO: Find eigenvalues and eigenvectors
    
    return matrix

def data_preprocessing():
    """Practice pandas data preprocessing"""
    # Create sample dataset
    data = {
        'feature1': [1, 2, np.nan, 4, 5],
        'feature2': [10, 20, 30, 40, 50],
        'target': [0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    
    # TODO: Handle missing values
    # TODO: Create new features (feature1 * feature2)
    # TODO: Split into features and target
    
    return df

if __name__ == "__main__":
    print("Matrix operations:")
    matrix_operations()
    
    print("\nData preprocessing:")
    result = data_preprocessing()
    print(result)