<script lang="ts">
  import { CATEGORY_CONFIG, type Category } from './types'

  let { counts }: { counts: Record<Category | 'all', number> } = $props()

  let total = $derived(counts.all)

  const categories: Category[] = ['constructive', 'positive', 'neutral', 'negative', 'toxic']
</script>

<div class="stats-panel">
  <h3>分析统计</h3>
  {#if total === 0}
    <p class="no-data">暂无数据</p>
  {:else}
    <div class="stats-grid">
      {#each categories as cat}
        {@const cfg = CATEGORY_CONFIG[cat]}
        {@const count = counts[cat] ?? 0}
        {@const pct = total > 0 ? (count / total) * 100 : 0}
        <div class="stat-row">
          <span class="stat-label" style="color: {cfg.color}">{cfg.icon} {cfg.label}</span>
          <div class="stat-bar-wrapper">
            <div class="stat-bar" style="width: {pct}%; background: {cfg.color}"></div>
          </div>
          <span class="stat-value">{count} ({pct.toFixed(0)}%)</span>
        </div>
      {/each}
    </div>
    <div class="total">共 {total} 条评论</div>
  {/if}
</div>

<style>
  .stats-panel {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    background: var(--card-bg);
  }
  h3 {
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
    color: var(--text-color);
  }
  .no-data {
    color: var(--text-muted);
    font-size: 0.85rem;
    text-align: center;
    padding: 1rem 0;
  }
  .stats-grid {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .stat-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .stat-label {
    font-size: 0.82rem;
    font-weight: 500;
    min-width: 6rem;
    white-space: nowrap;
  }
  .stat-bar-wrapper {
    flex: 1;
    height: 8px;
    background: var(--border-color);
    border-radius: 4px;
    overflow: hidden;
  }
  .stat-bar {
    height: 100%;
    border-radius: 4px;
    transition: width 0.4s ease;
  }
  .stat-value {
    font-size: 0.78rem;
    color: var(--text-muted);
    min-width: 4.5rem;
    text-align: right;
    white-space: nowrap;
  }
  .total {
    margin-top: 0.75rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    text-align: right;
  }
</style>
