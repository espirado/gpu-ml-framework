from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, brier_score_loss


@dataclass
class EvalResult:
    report: Dict
    confusion: np.ndarray
    ece: float
    brier: float


def multiclass_brier(y_true: np.ndarray, probas: np.ndarray, classes: List[str]) -> float:
    scores = []
    for i, c in enumerate(classes):
        y_bin = (y_true == c).astype(int)
        scores.append(brier_score_loss(y_bin, probas[:, i]))
    return float(np.mean(scores))


def expected_calibration_error(y_true: np.ndarray, probas: np.ndarray, classes: List[str], bins: int = 15) -> float:
    confidences = probas.max(axis=1)
    predictions = probas.argmax(axis=1)
    classes_np = np.array(classes)
    correct = (classes_np[predictions] == y_true)
    bin_bounds = np.linspace(0.0, 1.0, bins + 1)
    ece = 0.0
    for i in range(bins):
        lo, hi = bin_bounds[i], bin_bounds[i + 1]
        mask = (confidences > lo) & (confidences <= hi)
        if not np.any(mask):
            continue
        acc = correct[mask].mean()
        conf = confidences[mask].mean()
        ece += (mask.mean()) * abs(acc - conf)
    return float(ece)


def evaluate(y_true: np.ndarray, probas: np.ndarray, classes: List[str]) -> EvalResult:
    preds = np.array(classes)[probas.argmax(axis=1)]
    rpt = classification_report(y_true, preds, output_dict=True)
    cm = confusion_matrix(y_true, preds, labels=classes)
    brier = multiclass_brier(y_true, probas, classes)
    ece = expected_calibration_error(y_true, probas, classes)
    return EvalResult(report=rpt, confusion=cm, ece=ece, brier=brier)


