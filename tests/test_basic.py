from src.preprocessing import split_and_scale
import pandas as pd
import numpy as np

def test_split_and_scale():
    df = pd.DataFrame({
        "Income": np.random.rand(100),
        "Age": np.random.randint(18, 70, 100),
        "Loan": np.random.rand(100),
        "Loan to Income": np.random.rand(100),
        "Default": np.random.randint(0, 2, 100)
    })
    X_train, X_test, y_train, y_test, scaler = split_and_scale(df, "Default", test_size=0.2, random_state=1)
    assert X_train.shape[0] == 80
    assert X_test.shape[0] == 20
