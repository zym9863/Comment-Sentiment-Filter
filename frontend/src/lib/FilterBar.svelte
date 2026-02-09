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

  const filters: { key: Category | 'all'; label: string; color: string; glow: string }[] = [
    { key: 'all', label: '全部', color: 'var(--accent-solid)', glow: 'rgba(129, 140, 248, 0.15)' },
    ...Object.entries(CATEGORY_CONFIG).map(([key, cfg]) => ({
      key: key as Category,
      label: cfg.label,
      color: cfg.color,
      glow: cfg.glow,
    })),
  ]
</script>

<div class="filter-bar">
  <div class="filter-row">
    {#each filters as f, i}
      <button
        class="filter-pill"
        class:active={activeFilter === f.key}
        style="--pill-color: {f.color}; --pill-glow: {f.glow}; animation-delay: {i * 40}ms"
        onclick={() => onFilterChange(f.key)}
      >
        <span class="pill-label">{f.label}</span>
        <span class="pill-count">{counts[f.key] ?? 0}</span>
      </button>
    {/each}
  </div>

  <label class="toxic-toggle">
    <div class="toggle-track" class:on={showToxic}>
      <div class="toggle-thumb"></div>
    </div>
    <input
      type="checkbox"
      checked={showToxic}
      onchange={onToggleToxic}
      class="toggle-input"
    />
    <span class="toggle-label">显示恶意评论</span>
  </label>
</div>

<style>
  .filter-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }

  .filter-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .filter-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.85rem;
    border: 1px solid var(--border-subtle);
    border-radius: 3px;
    background: transparent;
    color: var(--text-secondary);
    font-family: var(--font-body);
    font-size: 0.78rem;
    font-weight: 400;
    cursor: pointer;
    transition: all 0.3s var(--ease-out-expo);
    animation: slideInLeft 0.4s var(--ease-out-expo) both;
    letter-spacing: 0.02em;
  }

  .filter-pill:hover {
    border-color: var(--pill-color);
    color: var(--pill-color);
    background: var(--pill-glow);
  }

  .filter-pill.active {
    background: var(--pill-glow);
    border-color: var(--pill-color);
    color: var(--pill-color);
    font-weight: 500;
    box-shadow: 0 0 16px var(--pill-glow);
  }

  .pill-count {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    opacity: 0.6;
  }

  .filter-pill.active .pill-count {
    opacity: 1;
  }

  /* Custom toggle switch */
  .toxic-toggle {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    cursor: pointer;
    position: relative;
  }

  .toggle-input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
  }

  .toggle-track {
    width: 32px;
    height: 18px;
    border-radius: 9px;
    background: var(--border-subtle);
    position: relative;
    transition: background 0.3s;
    flex-shrink: 0;
  }

  .toggle-track.on {
    background: var(--color-toxic);
  }

  .toggle-thumb {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: white;
    transition: transform 0.3s var(--ease-spring);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }

  .toggle-track.on .toggle-thumb {
    transform: translateX(14px);
  }

  .toggle-label {
    font-size: 0.78rem;
    color: var(--text-tertiary);
    white-space: nowrap;
    letter-spacing: 0.02em;
  }

  @media (max-width: 600px) {
    .filter-bar {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>
