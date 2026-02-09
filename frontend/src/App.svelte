<script lang="ts">
  import CommentInput from './lib/CommentInput.svelte'
  import CommentList from './lib/CommentList.svelte'
  import FilterBar from './lib/FilterBar.svelte'
  import StatsPanel from './lib/StatsPanel.svelte'
  import type { Category, CommentResult, SampleComment } from './lib/types'

  let allResults: CommentResult[] = $state([])
  let activeFilter: Category | 'all' = $state('all')
  let showToxic: boolean = $state(false)
  let loadingSamples: boolean = $state(false)

  let filteredResults = $derived.by(() => {
    let results = allResults
    if (!showToxic) {
      results = results.filter((r) => r.category !== 'toxic')
    }
    if (activeFilter !== 'all') {
      results = results.filter((r) => r.category === activeFilter)
    }
    return results
  })

  let counts = $derived.by(() => {
    const c: Record<string, number> = { all: allResults.length }
    for (const r of allResults) {
      c[r.category] = (c[r.category] ?? 0) + 1
    }
    return c as Record<Category | 'all', number>
  })

  async function analyzeComment(text: string) {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    if (!res.ok) throw new Error('分析请求失败')
    const result: CommentResult = await res.json()
    allResults = [result, ...allResults]
  }

  async function loadSamples() {
    if (loadingSamples) return
    loadingSamples = true
    try {
      const samplesRes = await fetch('/api/samples')
      if (!samplesRes.ok) throw new Error('加载样本失败')
      const samples: SampleComment[] = await samplesRes.json()

      const batchRes = await fetch('/api/analyze/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comments: samples.map((s) => ({ text: s.text })) }),
      })
      if (!batchRes.ok) throw new Error('批量分析失败')
      const { results }: { results: CommentResult[] } = await batchRes.json()
      allResults = [...results, ...allResults]
    } finally {
      loadingSamples = false
    }
  }

  function clearResults() {
    allResults = []
    activeFilter = 'all'
  }
</script>

<div class="app">
  <header>
    <h1>评论区情感过滤器</h1>
    <p class="subtitle">基于 BERT 的恶意评论检测与建设性反馈高亮 · 支持中英文</p>
  </header>

  <main>
    <section class="input-section">
      <CommentInput onAnalyze={analyzeComment} />
      <div class="sample-actions">
        <button class="sample-btn" onclick={loadSamples} disabled={loadingSamples}>
          {loadingSamples ? '加载中...' : '加载样本评论'}
        </button>
        {#if allResults.length > 0}
          <button class="clear-btn" onclick={clearResults}>清空结果</button>
        {/if}
      </div>
    </section>

    <div class="content-grid">
      <section class="results-section">
        <FilterBar
          {activeFilter}
          {counts}
          {showToxic}
          onFilterChange={(f) => (activeFilter = f)}
          onToggleToxic={() => (showToxic = !showToxic)}
        />
        <CommentList results={filteredResults} />
      </section>

      <aside class="sidebar">
        <StatsPanel {counts} />
      </aside>
    </div>
  </main>
</div>

<style>
  .app {
    max-width: 1100px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
  header {
    text-align: center;
    margin-bottom: 2rem;
  }
  h1 {
    font-size: 1.8rem;
    margin: 0;
    color: var(--text-color);
  }
  .subtitle {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin: 0.4rem 0 0;
  }
  .input-section {
    margin-bottom: 1.5rem;
  }
  .sample-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.75rem;
  }
  .sample-btn {
    padding: 0.4rem 1rem;
    background: var(--card-bg);
    border: 1px solid var(--accent-color);
    color: var(--accent-color);
    border-radius: 6px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  .sample-btn:hover:not(:disabled) {
    background: var(--accent-color);
    color: white;
  }
  .sample-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .clear-btn {
    padding: 0.4rem 1rem;
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    border-radius: 6px;
    font-size: 0.85rem;
    cursor: pointer;
  }
  .clear-btn:hover {
    border-color: #ef4444;
    color: #ef4444;
  }
  .content-grid {
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 1.5rem;
    align-items: start;
  }
  .results-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  @media (max-width: 768px) {
    .content-grid {
      grid-template-columns: 1fr;
    }
    .sidebar {
      order: -1;
    }
  }
</style>
