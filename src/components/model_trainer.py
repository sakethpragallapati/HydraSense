import numpy as np
import pandas as pd
from dataclasses import dataclass
import os
import sys

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


class BalancedEnsembleLinearSVC(BaseEstimator, ClassifierMixin):
    """
    Balanced Partition-based Ensemble using LinearSVC for Imbalanced Datasets.
    Partitions the majority class into N subsets and pairs each subset with all minority
    samples to train N perfectly balanced (1:1) LinearSVC sub-models.
    Predictions are aggregated via continuous decision margin averaging (soft) or majority voting (hard).
    """
    def __init__(self, n_splits=4, voting="soft", random_state=42):
        self.n_splits = n_splits
        self.voting = voting  # 'soft' (average decision margin) or 'hard' (majority voting)
        self.random_state = random_state
        self.models = []
        self.classes_ = None

    def fit(self, X, y):
        try:
            self.models = []
            self.classes_, counts = np.unique(y, return_counts=True)
            if len(self.classes_) != 2:
                raise ValueError("BalancedEnsembleLinearSVC supports binary classification.")

            majority_class = self.classes_[np.argmax(counts)]
            minority_class = self.classes_[np.argmin(counts)]

            maj_indices = np.where(y == majority_class)[0]
            min_indices = np.where(y == minority_class)[0]

            rng = np.random.RandomState(self.random_state)
            shuffled_maj = maj_indices.copy()
            rng.shuffle(shuffled_maj)

            maj_chunks = np.array_split(shuffled_maj, self.n_splits)

            logging.info(
                f"Training BalancedEnsembleLinearSVC with {self.n_splits} sub-models. "
                f"Majority samples: {len(maj_indices)}, Minority samples: {len(min_indices)}"
            )

            for i, chunk in enumerate(maj_chunks):
                subset_indices = np.concatenate([chunk, min_indices])
                rng.shuffle(subset_indices)

                clf = LinearSVC(dual="auto", random_state=self.random_state + i)
                clf.fit(X[subset_indices], y[subset_indices])
                self.models.append(clf)

                logging.info(
                    f"Sub-Model {i+1} trained on {len(chunk)} majority + {len(min_indices)} minority = {len(subset_indices)} samples (1:1 balanced)"
                )

            return self
        except Exception as e:
            custom_exception = CustomException(e, sys)
            logging.error(custom_exception)
            raise custom_exception

    def decision_function(self, X):
        decision_scores = np.array([m.decision_function(X) for m in self.models])
        return decision_scores.mean(axis=0)

    def predict(self, X):
        if self.voting == "soft":
            return (self.decision_function(X) > 0).astype(int)
        else:
            predictions = np.array([m.predict(X) for m in self.models])
            return (predictions.mean(axis=0) >= 0.5).astype(int)


@dataclass
class ModelTrainerConfig:
    model_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, preprocessed_train_array, preprocessed_test_array):
        try:
            logging.info("Model Training is initiated with BalancedEnsembleLinearSVC")
            x_train = preprocessed_train_array[:, :-1]
            y_train = preprocessed_train_array[:, -1]

            x_test = preprocessed_test_array[:, :-1]
            y_test = preprocessed_test_array[:, -1]

            # Train Balanced Ensemble LinearSVC
            ensemble_model = BalancedEnsembleLinearSVC(n_splits=4, voting="soft", random_state=42)
            ensemble_model.fit(x_train, y_train)

            # Evaluate on test set
            y_pred = ensemble_model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average="weighted")
            recall = recall_score(y_test, y_pred, average="weighted")
            f1 = f1_score(y_test, y_pred, average="weighted")
            roc_auc = roc_auc_score(y_test, y_pred)
            cm = confusion_matrix(y_test, y_pred)

            logging.info(
                f"BalancedEnsembleLinearSVC Performance -> Accuracy: {accuracy:.4f}, "
                f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}, ROC-AUC: {roc_auc:.4f}"
            )
            logging.info(f"Confusion Matrix:\n{cm}")

            print("=" * 80)
            print("         BALANCED ENSEMBLE LINEAR SVC - TRAINING RESULTS")
            print("=" * 80)
            print(f"Accuracy:  {accuracy:.4f}")
            print(f"Precision: {precision:.4f}")
            print(f"Recall:    {recall:.4f}")
            print(f"F1 Score:  {f1:.4f}")
            print(f"ROC-AUC:   {roc_auc:.4f}")
            print(f"Confusion Matrix:\n{cm}")
            print("=" * 80)

            if accuracy < 0.6:
                custom_exception = CustomException("Model accuracy too low for the dataset", sys)
                logging.error(custom_exception)
                raise custom_exception

            save_object(
                self.model_trainer_config.model_path,
                ensemble_model
            )

            logging.info("BalancedEnsembleLinearSVC model saved successfully to artifacts/model.pkl")

            return (
                "BalancedEnsembleLinearSVC",
                accuracy,
                self.model_trainer_config.model_path
            )
        except Exception as e:
            custom_exception = CustomException(e, sys)
            logging.error(custom_exception)
            raise custom_exception