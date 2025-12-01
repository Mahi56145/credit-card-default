from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

def split_and_scale(df, target_col, test_size=0.2, random_state=42, save_scaler=None):
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
    if save_scaler:
        import joblib
        joblib.dump(scaler, save_scaler)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler
