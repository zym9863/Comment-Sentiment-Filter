import torch

MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"

# transformers pipeline expects an int: 0 for first CUDA device, -1 for CPU
DEVICE = 0 if torch.cuda.is_available() else -1

# 毒性检测阈值：情感评分 <= 此值且命中关键词 → toxic
TOXIC_SENTIMENT_THRESHOLD = 1  # 1星
TOXIC_CONFIDENCE_THRESHOLD = 0.5

# 建设性检测：情感评分 >= 此值且命中特征词 → constructive
CONSTRUCTIVE_SENTIMENT_THRESHOLD = 4  # 4星

# 中英文毒性关键词（用于辅助判定，配合低情感分）
TOXIC_KEYWORDS_ZH = [
    "垃圾", "废物", "白痴", "蠢货", "滚", "去死", "脑残", "智障",
    "傻逼", "狗东西", "贱人", "畜生", "混蛋", "王八蛋", "神经病",
    "恶心", "变态", "人渣", "败类", "无耻",
]

TOXIC_KEYWORDS_EN = [
    "idiot", "stupid", "moron", "trash", "garbage", "loser", "die",
    "hate", "kill", "ugly", "dumb", "pathetic", "worthless", "disgusting",
    "shut up", "get lost", "scum", "freak", "creep",
]

# 中英文建设性特征词
CONSTRUCTIVE_KEYWORDS_ZH = [
    "建议", "可以改进", "希望", "如果能", "就更好了", "优化",
    "改善", "提升", "完善", "推荐", "不妨", "试试", "考虑",
    "或许可以", "期待", "加油",
]

CONSTRUCTIVE_KEYWORDS_EN = [
    "suggest", "recommend", "could improve", "would be better",
    "consider", "try", "perhaps", "might want to", "tip",
    "advice", "improvement", "enhance", "keep up", "great job but",
    "one thing", "feedback",
]
