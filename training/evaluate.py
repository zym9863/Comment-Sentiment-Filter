"""模型评估脚本。

使用方法：
    uv run python -m training.evaluate --model model_cache/finetuned --data data/test.json
"""

import argparse
import json

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from .dataset import CommentDataset


def evaluate(model_path: str, data_path: str, max_length: int = 128):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
    model.eval()

    dataset = CommentDataset(data_path, tokenizer, max_length)
    loader = torch.utils.data.DataLoader(dataset, batch_size=32)

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"]

            outputs = model(input_ids, attention_mask=attention_mask)
            preds = outputs.logits.argmax(dim=-1).cpu()

            all_preds.extend(preds.tolist())
            all_labels.extend(labels.tolist())

    # 计算准确率
    correct = sum(p == l for p, l in zip(all_preds, all_labels))
    accuracy = correct / len(all_labels) if all_labels else 0

    # 按类别统计
    num_labels = CommentDataset.num_labels()
    tp = [0] * num_labels
    fp = [0] * num_labels
    fn = [0] * num_labels

    for pred, label in zip(all_preds, all_labels):
        if pred == label:
            tp[label] += 1
        else:
            fp[pred] += 1
            fn[label] += 1

    print(f"\n总准确率: {accuracy:.4f} ({correct}/{len(all_labels)})")
    print(f"\n{'类别':<15} {'Precision':>10} {'Recall':>10} {'F1':>10}")
    print("-" * 47)

    for i in range(num_labels):
        label_name = CommentDataset.ID_TO_LABEL[i]
        precision = tp[i] / (tp[i] + fp[i]) if (tp[i] + fp[i]) > 0 else 0
        recall = tp[i] / (tp[i] + fn[i]) if (tp[i] + fn[i]) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        print(f"{label_name:<15} {precision:>10.4f} {recall:>10.4f} {f1:>10.4f}")

    # 混淆矩阵
    print("\n混淆矩阵:")
    header = "".join(f"{CommentDataset.ID_TO_LABEL[i]:>12}" for i in range(num_labels))
    print(f"{'预测→':>15}{header}")
    for i in range(num_labels):
        row = [0] * num_labels
        for pred, label in zip(all_preds, all_labels):
            if label == i:
                row[pred] += 1
        row_str = "".join(f"{v:>12}" for v in row)
        print(f"{CommentDataset.ID_TO_LABEL[i]:>15}{row_str}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="评估微调后的 BERT 模型")
    parser.add_argument("--model", required=True, help="模型路径")
    parser.add_argument("--data", required=True, help="测试数据路径 (JSON)")
    args = parser.parse_args()

    evaluate(model_path=args.model, data_path=args.data)
