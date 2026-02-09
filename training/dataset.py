import json

import torch
from torch.utils.data import Dataset


class CommentDataset(Dataset):
    """评论分类数据集，支持 JSON 格式输入。

    JSON 格式：[{"text": "...", "label": "toxic|negative|neutral|positive|constructive"}, ...]
    """

    LABEL_MAP = {
        "toxic": 0,
        "negative": 1,
        "neutral": 2,
        "positive": 3,
        "constructive": 4,
    }
    ID_TO_LABEL = {v: k for k, v in LABEL_MAP.items()}

    def __init__(self, file_path: str, tokenizer, max_length: int = 128):
        with open(file_path, encoding="utf-8") as f:
            raw_data = json.load(f)

        self.texts = []
        self.labels = []
        for item in raw_data:
            text = item.get("text", "")
            label = item.get("label") or item.get("expected", "neutral")
            if label in self.LABEL_MAP:
                self.texts.append(text)
                self.labels.append(self.LABEL_MAP[label])

        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": torch.tensor(self.labels[idx], dtype=torch.long),
        }

    @classmethod
    def num_labels(cls) -> int:
        return len(cls.LABEL_MAP)
