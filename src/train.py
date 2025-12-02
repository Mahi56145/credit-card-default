import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import joblib
import pandas as pd                     # <--- needed for concatenating before saving
from src.data_loader import load_csv
from src.preprocessing import split_and_scale
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

def main(data_path, out_dir, random_state):
    # ensure output dirs exist
    os.makedirs(os.path.join(out_dir, "models"), exist_ok=True)
    processed_dir = os.path.join(out_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    # load data
    df = load_csv(data_path)

    # split + scale. save_scaler path provided so split_and_scale can save it (if implemented)
    X_train, X_test, y_train, y_test, scaler = split_and_scale(
        df,
        target_col="Default",
        test_size=0.2,
        random_state=random_state,
        save_scaler=os.path.join(out_dir, "models", "scaler_standard.joblib")
    )

    # training arrays
    train_arr = X_train.values
    test_arr = X_test.values
    y_train_arr = y_train.values
    y_test_arr = y_test.values

    # initialize & fit
    lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state)
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=random_state)
    lr.fit(train_arr, y_train_arr)
    rf.fit(train_arr, y_train_arr)

    # save individual models
    joblib.dump(lr, os.path.join(out_dir, "models", "logisticregression.joblib"))
    joblib.dump(rf, os.path.join(out_dir, "models", "randomforest.joblib"))

    # choose best by ROC AUC and save
    from sklearn.metrics import roc_auc_score
    auc_lr = roc_auc_score(y_test_arr, lr.predict_proba(test_arr)[:, 1])
    auc_rf = roc_auc_score(y_test_arr, rf.predict_proba(test_arr)[:, 1])
    best_name = "randomforest" if auc_rf >= auc_lr else "logisticregression"
    best_model = rf if best_name == "randomforest" else lr
    joblib.dump(best_model, os.path.join(out_dir, "models", "best_model.joblib"))

    # save processed train/test WITH target column (useful for reproducibility/submission)
    train_df = pd.concat([X_train.reset_index(drop=True), y_train.reset_index(drop=True)], axis=1)
    test_df  = pd.concat([X_test.reset_index(drop=True),  y_test.reset_index(drop=True)], axis=1)
    train_df.to_csv(os.path.join(processed_dir, "train_processed.csv"), index=False)
    test_df.to_csv(os.path.join(processed_dir, "test_processed.csv"), index=False)

    print("Saved models. Best model:", best_name, "AUCs:", {"lr": auc_lr, "rf": auc_rf})
    print("Saved processed files to:", processed_dir)
    print("Saved models to:", os.path.join(out_dir, "models"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # default to the raw data shipped in the repo so script runs without extra args
    parser.add_argument("--data-path", type=str, default="data/raw/credit_card.csv", help="path to raw csv")
    parser.add_argument("--out-dir", type=str, default=".", help="base output directory")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()
    main(args.data_path, args.out_dir, args.random_state)
