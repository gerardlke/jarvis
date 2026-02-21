import pandas as pd
from joblib import dump
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


if __name__ == '__main__':
    # Create model
    knn = KNeighborsClassifier(
        n_neighbors=3,
        metric="cosine"
    )

    # Load data and create dataset
    dfs = []
    dataset = Path.cwd() / "datasets" / "gestures"
    for file in dataset.glob("*.csv"):
        df = pd.read_csv(file, header=None)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    y = df.iloc[:, 0].values
    X = df.iloc[:, 1:].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )

    # Train model and scaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    knn.fit(X_train, y_train)

    print("Done.")

    # Save model and scaler
    dump(knn, r"models/runs/knn/knn.joblib")
    dump(scaler, r"models/runs/knn/scaler.joblib")