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

export const CATEGORY_CONFIG: Record<
  Category,
  { label: string; color: string; glow: string; icon: string }
> = {
  toxic: { label: '恶意攻击', color: 'var(--color-toxic)', glow: 'var(--color-toxic-glow)', icon: '⛔' },
  negative: { label: '负面评论', color: 'var(--color-negative)', glow: 'var(--color-negative-glow)', icon: '▼' },
  neutral: { label: '中性评论', color: 'var(--color-neutral)', glow: 'var(--color-neutral-glow)', icon: '◆' },
  positive: { label: '正面评论', color: 'var(--color-positive)', glow: 'var(--color-positive-glow)', icon: '▲' },
  constructive: { label: '建设性反馈', color: 'var(--color-constructive)', glow: 'var(--color-constructive-glow)', icon: '★' },
}
