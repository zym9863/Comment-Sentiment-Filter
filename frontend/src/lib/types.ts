export type Category = 'toxic' | 'negative' | 'neutral' | 'positive' | 'constructive'

export interface CommentResult {
  text: string
  category: Category
  confidence: number
  sentiment_score: number
  is_toxic: boolean
  is_constructive: boolean
}

export interface SampleComment {
  text: string
  expected: Category
}

export const CATEGORY_CONFIG: Record<Category, { label: string; color: string; icon: string }> = {
  toxic: { label: '恶意攻击', color: '#ef4444', icon: '🚫' },
  negative: { label: '负面评论', color: '#f97316', icon: '👎' },
  neutral: { label: '中性评论', color: '#6b7280', icon: '💬' },
  positive: { label: '正面评论', color: '#3b82f6', icon: '👍' },
  constructive: { label: '建设性反馈', color: '#22c55e', icon: '⭐' },
}
