"""
Exercise 1: Python Basics for AI
Complete the functions below
"""

def normalize_data(data):
    """Normalize a list of numbers to range [0, 1]"""
    # TODO: Implement min-max normalization
    pass

def filter_outliers(data, threshold=2):
    """Remove outliers using standard deviation method"""
    # TODO: Remove values beyond threshold standard deviations
    pass

def create_feature_matrix(height, weight, age):
    """Create a feature matrix from individual features"""
    # TODO: Return a 2D list where each row is [height, weight, age]
    pass

# Test your functions
if __name__ == "__main__":
    # Test data
    sample_data = [1, 2, 3, 100, 4, 5, 6]
    heights = [170, 180, 165, 175]
    weights = [70, 80, 60, 75]
    ages = [25, 30, 22, 28]
    
    print("Original data:", sample_data)
    print("Normalized:", normalize_data(sample_data))
    print("Without outliers:", filter_outliers(sample_data))
    print("Feature matrix:", create_feature_matrix(heights, weights, ages))