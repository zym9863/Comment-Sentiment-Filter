<script lang="ts">
  import { CATEGORY_CONFIG, type CommentResult } from './types'

  let { result }: { result: CommentResult } = $props()

  let expanded: boolean = $state(false)

  let config = $derived(CATEGORY_CONFIG[result.category])
  let isToxic = $derived(result.category === 'toxic')
  let isConstructive = $derived(result.category === 'constructive')
</script>

<div
  class="comment-card"
  class:toxic={isToxic}
  class:constructive={isConstructive}
  style="--category-color: {config.color}"
>
  {#if isToxic && !expanded}
    <div class="toxic-overlay">
      <span class="toxic-label">{config.icon} 此评论已被隐藏（检测到恶意内容）</span>
      <button class="reveal-btn" onclick={() => (expanded = true)}>点击查看</button>
    </div>
  {:else}
    <div class="card-header">
      <span class="category-badge" style="background: {config.color}">
        {config.icon} {config.label}
      </span>
      <span class="confidence">置信度 {(result.confidence * 100).toFixed(1)}%</span>
      {#if isToxic}
        <button class="hide-btn" onclick={() => (expanded = false)}>隐藏</button>
      {/if}
    </div>
    <p class="comment-text">{result.text}</p>
    <div class="card-footer">
      <div class="confidence-bar">
        <div class="confidence-fill" style="width: {result.confidence * 100}%; background: {config.color}"></div>
      </div>
      <span class="sentiment-stars">
        {'★'.repeat(result.sentiment_score)}{'☆'.repeat(5 - result.sentiment_score)}
      </span>
    </div>
  {/if}
</div>

<style>
  .comment-card {
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--category-color);
    border-radius: 8px;
    padding: 1rem;
    background: var(--card-bg);
    transition: box-shadow 0.2s;
  }
  .comment-card:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  .comment-card.constructive {
    background: color-mix(in srgb, var(--category-color) 5%, var(--card-bg));
  }
  .comment-card.toxic {
    border-left-width: 4px;
  }
  .toxic-overlay {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.25rem 0;
    color: var(--text-muted);
  }
  .toxic-label {
    font-size: 0.85rem;
  }
  .reveal-btn,
  .hide-btn {
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    color: var(--text-muted);
    cursor: pointer;
  }
  .reveal-btn:hover,
  .hide-btn:hover {
    background: var(--border-color);
  }
  .card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
  }
  .category-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.15rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
    color: white;
    font-weight: 500;
  }
  .confidence {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-left: auto;
  }
  .comment-text {
    margin: 0.5rem 0;
    line-height: 1.6;
    color: var(--text-color);
  }
  .card-footer {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.5rem;
  }
  .confidence-bar {
    flex: 1;
    height: 4px;
    background: var(--border-color);
    border-radius: 2px;
    overflow: hidden;
  }
  .confidence-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.3s ease;
  }
  .sentiment-stars {
    font-size: 0.85rem;
    color: #eab308;
    white-space: nowrap;
  }
</style>
