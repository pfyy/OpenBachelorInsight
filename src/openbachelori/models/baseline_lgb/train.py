import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
import lightgbm as lgb


def main():
    df = pd.read_csv("csv/multiOperationMatch_act3enemyduel_01b.csv")

    df["label"] = df["label"].replace(-1, 0)

    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    clf = lgb.LGBMClassifier(random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_pred_proba = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    pre = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    auc = roc_auc_score(y_test, y_pred_proba)

    cm = confusion_matrix(y_test, y_pred)

    print("accuracy_score:", acc)
    print("precision_score:", pre)
    print("recall_score:", rec)
    print("f1_score:", f1)
    print("roc_auc_score:", auc)
    print(
        f"confusion_matrix:\n{cm}",
    )
    print(f"classification_report:\n{classification_report(y_test, y_pred)}")


if __name__ == "__main__":
    main()
