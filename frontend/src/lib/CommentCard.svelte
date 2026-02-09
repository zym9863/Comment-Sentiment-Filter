<script lang="ts">
  import { CATEGORY_CONFIG, type CommentResult } from './types'

  let { result }: { result: CommentResult } = $props()

  let expanded: boolean = $state(false)

  let config = $derived(CATEGORY_CONFIG[result.category])
  let isToxic = $derived(result.category === 'toxic')
  let isConstructive = $derived(result.category === 'constructive')
</script>

<article
  class="card"
  class:toxic={isToxic}
  class:constructive={isConstructive}
  style="--cat-color: {config.color}; --cat-glow: {config.glow}"
>
  <!-- Accent line -->
  <div class="card-accent"></div>

  {#if isToxic && !expanded}
    <div class="toxic-mask">
      <div class="toxic-icon">⛔</div>
      <div class="toxic-info">
        <span class="toxic-label">此评论已被屏蔽</span>
        <span class="toxic-reason">检测到恶意内容 · 置信度 {(result.confidence * 100).toFixed(0)}%</span>
      </div>
      <button class="reveal-btn" onclick={() => (expanded = true)}>
        查看内容
      </button>
    </div>
  {:else}
    <div class="card-body">
      <div class="card-meta">
        <span class="category-tag">
          <span class="tag-icon">{config.icon}</span>
          {config.label}
        </span>
        <div class="meta-right">
          {#if isToxic}
            <button class="hide-btn" onclick={() => (expanded = false)}>隐藏</button>
          {/if}
          <span class="confidence-label">
            {(result.confidence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      <p class="card-text">{result.text}</p>

      <div class="card-data">
        <div class="confidence-track">
          <div
            class="confidence-fill"
            style="width: {result.confidence * 100}%"
          ></div>
        </div>
        <div class="sentiment-meter">
          {#each Array(5) as _, i}
            <span class="meter-dot" class:active={i < result.sentiment_score}></span>
          {/each}
        </div>
      </div>
    </div>
  {/if}
</article>

<style>
  .card {
    position: relative;
    background: var(--card-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    overflow: hidden;
    transition: all 0.35s var(--ease-out-expo);
    backdrop-filter: blur(8px);
  }

  .card:hover {
    background: var(--card-bg-hover);
    border-color: var(--border-medium);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
  }

  .card.constructive {
    box-shadow: inset 0 0 30px var(--cat-glow);
  }

  .card.constructive:hover {
    box-shadow: inset 0 0 30px var(--cat-glow), var(--shadow-md);
  }

  /* Left accent stripe */
  .card-accent {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: var(--cat-color);
    opacity: 0.8;
    transition: opacity 0.3s, width 0.3s;
  }

  .card:hover .card-accent {
    opacity: 1;
    width: 4px;
  }

  /* Toxic overlay */
  .toxic-mask {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1rem 1rem 1.5rem;
  }

  .toxic-icon {
    font-size: 1.2rem;
    opacity: 0.6;
  }

  .toxic-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  .toxic-label {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-secondary);
  }

  .toxic-reason {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-tertiary);
    letter-spacing: 0.03em;
  }

  .reveal-btn,
  .hide-btn {
    padding: 0.3rem 0.8rem;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.05em;
    background: transparent;
    border: 1px solid var(--border-subtle);
    border-radius: 3px;
    color: var(--text-tertiary);
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .reveal-btn:hover,
  .hide-btn:hover {
    border-color: var(--text-secondary);
    color: var(--text-secondary);
  }

  /* Card body */
  .card-body {
    padding: 1rem 1.25rem 1rem 1.5rem;
  }

  .card-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }

  .category-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.2rem 0.75rem;
    background: var(--cat-glow);
    border-radius: 3px;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--cat-color);
    letter-spacing: 0.02em;
  }

  .tag-icon {
    font-size: 0.7rem;
  }

  .meta-right {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .confidence-label {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-tertiary);
    letter-spacing: 0.04em;
  }

  .card-text {
    font-size: 0.92rem;
    font-weight: 300;
    line-height: 1.75;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
  }

  .card-data {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .confidence-track {
    flex: 1;
    height: 2px;
    background: var(--border-subtle);
    border-radius: 1px;
    overflow: hidden;
  }

  .confidence-fill {
    height: 100%;
    background: var(--cat-color);
    border-radius: 1px;
    transition: width 0.5s var(--ease-out-expo);
    opacity: 0.7;
  }

  .sentiment-meter {
    display: flex;
    gap: 4px;
  }

  .meter-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--border-subtle);
    transition: all 0.3s;
  }

  .meter-dot.active {
    background: var(--cat-color);
    box-shadow: 0 0 6px var(--cat-glow);
  }
</style>
