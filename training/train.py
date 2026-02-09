"""BERT 微调训练脚本。

使用方法：
    uv run python -m training.train --data data/train.json --epochs 5

数据格式（JSON）：
    [{"text": "评论内容", "label": "toxic|negative|neutral|positive|constructive"}, ...]
"""

import argparse
from pathlib import Path

import torch
from torch.utils.data import DataLoader, random_split
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    get_linear_schedule_with_warmup,
)

from .dataset import CommentDataset


def train(
    data_path: str,
    model_name: str = "bert-base-multilingual-uncased",
    output_dir: str = "model_cache/finetuned",
    epochs: int = 5,
    batch_size: int = 16,
    lr: float = 2e-5,
    max_length: int = 128,
    val_split: float = 0.2,
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=CommentDataset.num_labels()
    ).to(device)

    dataset = CommentDataset(data_path, tokenizer, max_length)
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=total_steps // 10, num_training_steps=total_steps
    )

    print(f"训练集: {train_size} 条, 验证集: {val_size} 条")
    print(f"开始训练 {epochs} 个 epoch...")

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

        avg_loss = total_loss / len(train_loader)

        # 验证
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)

                outputs = model(input_ids, attention_mask=attention_mask)
                preds = outputs.logits.argmax(dim=-1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

        val_acc = correct / total if total > 0 else 0
        print(f"Epoch {epoch + 1}/{epochs} - Loss: {avg_loss:.4f} - Val Acc: {val_acc:.4f}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print(f"模型已保存到 {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BERT 评论分类微调训练")
    parser.add_argument("--data", required=True, help="训练数据路径 (JSON)")
    parser.add_argument("--model", default="bert-base-multilingual-uncased", help="基础模型")
    parser.add_argument("--output", default="model_cache/finetuned", help="输出目录")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=2e-5)
    args = parser.parse_args()

    train(
        data_path=args.data,
        model_name=args.model,
        output_dir=args.output,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
    )
