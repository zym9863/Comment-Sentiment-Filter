<script lang="ts">
  import { CATEGORY_CONFIG, type Category } from './types'

  let {
    activeFilter,
    counts,
    showToxic,
    onFilterChange,
    onToggleToxic,
  }: {
    activeFilter: Category | 'all'
    counts: Record<Category | 'all', number>
    showToxic: boolean
    onFilterChange: (filter: Category | 'all') => void
    onToggleToxic: () => void
  } = $props()

  const filters: { key: Category | 'all'; label: string; color: string }[] = [
    { key: 'all', label: '全部', color: '#8b5cf6' },
    ...Object.entries(CATEGORY_CONFIG).map(([key, cfg]) => ({
      key: key as Category,
      label: cfg.label,
      color: cfg.color,
    })),
  ]
</script>

<div class="filter-bar">
  <div class="filter-buttons">
    {#each filters as f}
      <button
        class="filter-btn"
        class:active={activeFilter === f.key}
        style="--btn-color: {f.color}"
        onclick={() => onFilterChange(f.key)}
      >
        {f.label}
        <span class="count">{counts[f.key] ?? 0}</span>
      </button>
    {/each}
  </div>
  <label class="toggle-toxic">
    <input type="checkbox" checked={showToxic} onchange={onToggleToxic} />
    <span>显示恶意评论</span>
  </label>
</div>

<style>
  .filter-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
  }
  .filter-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }
  .filter-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 16px;
    background: transparent;
    color: var(--text-color);
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  .filter-btn:hover {
    border-color: var(--btn-color);
  }
  .filter-btn.active {
    background: var(--btn-color);
    border-color: var(--btn-color);
    color: white;
  }
  .count {
    font-size: 0.75rem;
    opacity: 0.7;
  }
  .toggle-toxic {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.85rem;
    color: var(--text-muted);
    cursor: pointer;
  }
  .toggle-toxic input {
    cursor: pointer;
  }
</style>
