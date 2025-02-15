import numpy as np
import torch
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score
import json
import sys
import torch.nn.functional as F
from tqdm import tqdm
from collections import defaultdict, Counter

sys.path.append("/home/hust-ls/worksapce/RetrievalBackdoor/common/defender")
from fp.detecter import BERTDetecter


class FPDefender:
    def __init__(self, **kwargs):
        assert kwargs.get("output_dir", None)
        assert kwargs.get("device", None)

        self.output_dir = kwargs.get("output_dir", None)
        self.device = kwargs.get("device", None)

        self.bert_detector = BERTDetecter(
            device=self.device, output_dir=self.output_dir
        )
        self.bert_detector.load()

    def detect(self, texts, poisoned_labels, batch_size=64):
        assert self.bert_detector.get_valid()
        logits = []
        features = []
        for i in tqdm(range(0, len(texts), batch_size), ncols=100, desc="logits"):
            texts_batch = texts[i : i + batch_size]
            texts_batch = [str(text) for text in texts_batch]
            feature = self.bert_detector.feature(texts_batch)
            features.append(feature)
            logits.append(self.bert_detector.logits(texts_batch))

        logits = torch.cat(logits, dim=0)
        features = torch.cat(features, dim=0)
        self.bert_detector.t_SNE(features, poisoned_labels)
        exit(0)
        mixed_scores = torch.softmax(logits, dim=1)[:, 1]
        # for i in range(len(mixed_scores)):
        #     if mixed_scores[i] < 1e-2 and poisoned_labels[i]:
        #         print(f"poisoned: {texts[i]}, {mixed_scores[i]}")
        preds = torch.argmax(logits, dim=1).tolist()
        preds = [score > 1e-2 for score in mixed_scores.tolist()]
        print(f"poisoned_labels: {Counter(poisoned_labels)}")
        output_json = {
            "detects": preds,
            "auc": roc_auc_score(poisoned_labels, mixed_scores.tolist()),
            "f1": f1_score(poisoned_labels, preds),
            "precision": precision_score(poisoned_labels, preds),
            "recall": recall_score(poisoned_labels, preds),
        }
        return output_json
