<script lang="ts">
  import { CATEGORY_CONFIG, type Category } from './types'

  let { counts }: { counts: Record<Category | 'all', number> } = $props()

  let total = $derived(counts.all)

  const categories: Category[] = ['constructive', 'positive', 'neutral', 'negative', 'toxic']
</script>

<div class="panel">
  <div class="panel-header">
    <h3 class="panel-title">分析统计</h3>
    <span class="panel-badge">STATS</span>
  </div>

  {#if total === 0}
    <div class="no-data">
      <span class="no-data-icon">—</span>
      <span>暂无数据</span>
    </div>
  {:else}
    <div class="stats-list">
      {#each categories as cat, i}
        {@const cfg = CATEGORY_CONFIG[cat]}
        {@const count = counts[cat] ?? 0}
        {@const pct = total > 0 ? (count / total) * 100 : 0}
        <div class="stat-item" style="animation-delay: {i * 80}ms">
          <div class="stat-header">
            <span class="stat-icon" style="color: {cfg.color}">{cfg.icon}</span>
            <span class="stat-name">{cfg.label}</span>
            <span class="stat-value">{count}</span>
          </div>
          <div class="stat-track">
            <div
              class="stat-fill"
              style="width: {pct}%; background: {cfg.color}; animation-delay: {i * 80 + 200}ms"
            ></div>
          </div>
          <span class="stat-pct">{pct.toFixed(0)}%</span>
        </div>
      {/each}
    </div>

    <div class="panel-footer">
      <span class="total-label">共计</span>
      <span class="total-value">{total}</span>
      <span class="total-unit">条评论</span>
    </div>
  {/if}
</div>

<style>
  .panel {
    background: var(--card-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    overflow: hidden;
    backdrop-filter: blur(8px);
    position: sticky;
    top: 1.5rem;
  }

  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .panel-title {
    font-family: var(--font-display);
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
  }

  .panel-badge {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: var(--text-tertiary);
    padding: 0.15rem 0.5rem;
    border: 1px solid var(--border-subtle);
    border-radius: 2px;
  }

  .no-data {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 2.5rem 1rem;
    color: var(--text-tertiary);
    font-size: 0.82rem;
  }

  .no-data-icon {
    font-size: 1.5rem;
    opacity: 0.3;
  }

  .stats-list {
    padding: 1rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .stat-item {
    animation: fadeInUp 0.5s var(--ease-out-expo) both;
  }

  .stat-header {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.35rem;
  }

  .stat-icon {
    font-size: 0.7rem;
    width: 1rem;
    text-align: center;
  }

  .stat-name {
    font-size: 0.78rem;
    font-weight: 400;
    color: var(--text-secondary);
    flex: 1;
  }

  .stat-value {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-primary);
    min-width: 1.5rem;
    text-align: right;
  }

  .stat-track {
    height: 3px;
    background: var(--border-subtle);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 0.15rem;
  }

  .stat-fill {
    height: 100%;
    border-radius: 2px;
    transform-origin: left;
    animation: barGrow 0.8s var(--ease-out-expo) both;
    opacity: 0.85;
  }

  .stat-pct {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-tertiary);
    letter-spacing: 0.05em;
  }

  .panel-footer {
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
    padding: 0.85rem 1.25rem;
    border-top: 1px solid var(--border-subtle);
  }

  .total-label {
    font-size: 0.78rem;
    color: var(--text-tertiary);
  }

  .total-value {
    font-family: var(--font-mono);
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-primary);
  }

  .total-unit {
    font-size: 0.78rem;
    color: var(--text-tertiary);
  }
</style>
