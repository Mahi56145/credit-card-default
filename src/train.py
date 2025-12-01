import argparse
import os
import joblib
from src.data_loader import load_csv
from src.preprocessing import split_and_scale
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

def main(data_path, out_dir, random_state):
    os.makedirs(os.path.join(out_dir, "models"), exist_ok=True)
    df = load_csv(data_path)
    X_train, X_test, y_train, y_test, scaler = split_and_scale(
        df, target_col="Default", test_size=0.2, random_state=random_state,
        save_scaler=os.path.join(out_dir, "models", "scaler_standard.joblib")
    )
    train_arr = X_train.values
    test_arr = X_test.values
    y_train_arr = y_train.values
    lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state)
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=random_state)
    lr.fit(train_arr, y_train_arr)
    rf.fit(train_arr, y_train_arr)
    joblib.dump(lr, os.path.join(out_dir, "models", "logisticregression.joblib"))
    joblib.dump(rf, os.path.join(out_dir, "models", "randomforest.joblib"))
    from sklearn.metrics import roc_auc_score
    auc_lr = roc_auc_score(y_test, lr.predict_proba(test_arr)[:,1])
    auc_rf = roc_auc_score(y_test, rf.predict_proba(test_arr)[:,1])
    best = ("randomforest" if auc_rf >= auc_lr else "logisticregression")
    joblib.dump(rf if best == "randomforest" else lr, os.path.join(out_dir, "models", "best_model.joblib"))
    os.makedirs(os.path.join(out_dir, "data", "processed"), exist_ok=True)
    X_train.to_csv(os.path.join(out_dir, "data", "processed", "train_processed.csv"), index=False)
    X_test.to_csv(os.path.join(out_dir, "data", "processed", "test_processed.csv"), index=False)
    print("Saved models. Best model:", best, "AUCs:", {"lr": auc_lr, "rf": auc_rf})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--out-dir", type=str, default=".")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()
    main(args.data_path, args.out_dir, args.random_state)
