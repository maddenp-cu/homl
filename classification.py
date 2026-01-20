import logging
from pathlib import Path

from sklearn.datasets import fetch_openml
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# from matplotlib import pyplot as plt
# from sklearn.metrics import ConfusionMatrixDisplay

logging.basicConfig(
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)8s %(message)s",
)


def sgd() -> None:
    n = 60000
    X_train, _X_test, y_train, _y_test = X[:n], X[n:], y[:n], y[n:]
    classifier = SGDClassifier(random_state=42)
    logging.info("Cross-validating")
    y_pred = cross_val_predict(classifier, X_train, y_train, cv=3)
    logging.info("f1 score: %s", f1_score(y_train, y_pred, average="weighted"))
    logging.info("Scaling data")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train.astype("float64"))
    logging.info("Cross-validating")
    y_pred_scaled = cross_val_predict(classifier, X_train_scaled, y_train, cv=3)
    logging.info("f1 score: %s", f1_score(y_train, y_pred_scaled, average="weighted"))


def svc() -> None:
    n = 2000
    X_train, _X_test, y_train, _y_test = X[:n], X[n:], y[:n], y[n:]
    classifier = SVC(C=10, random_state=42)
    logging.info("Cross-validating")
    y_pred = cross_val_predict(classifier, X_train, y_train, cv=3)
    logging.info("f1 score: %s", f1_score(y_train, y_pred, average="weighted"))
    # ConfusionMatrixDisplay.from_predictions(y_train, y_pred)
    # plt.show()
    logging.info("Scaling data")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train.astype("float64"))
    logging.info("Looking for best estimator")
    gscv = GridSearchCV(
        classifier,
        {"C": [0.1, 1, 10], "kernel": ["rbf", "poly", "sigmoid", "linear"]},
        scoring="accuracy",
        cv=3,
        n_jobs=-1,
        verbose=4,
    )
    gscv.fit(X_train_scaled, y_train)
    classifier = gscv.best_estimator_
    logging.info("Cross-validating")
    y_pred_scaled = cross_val_predict(classifier, X_train_scaled, y_train, cv=3)
    logging.info("f1 score: %s", f1_score(y_train, y_pred_scaled, average="weighted"))
    # ConfusionMatrixDisplay.from_predictions(y_train, y_pred_scaled)
    # plt.show()


dataset = "mnist_784"
logging.info("Loading %s", dataset)
cachedir = Path(__file__).parent / ".cache"
mnist = fetch_openml(dataset, as_frame=False, data_home=str(cachedir))
X, y = mnist.data, mnist.target

svc()
