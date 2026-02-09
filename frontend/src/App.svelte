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

<div class="app-shell">
  <!-- Decorative corner accent -->
  <div class="corner-accent top-left"></div>
  <div class="corner-accent top-right"></div>

  <header class="hero">
    <div class="hero-badge">BERT-Powered Sentiment Analysis</div>
    <h1 class="hero-title">
      <span class="title-main">评论区情感过滤器</span>
    </h1>
    <p class="hero-subtitle">
      <span class="subtitle-divider"></span>
      恶意评论检测 · 建设性反馈高亮 · 中英文双语支持
      <span class="subtitle-divider"></span>
    </p>
  </header>

  <main class="main-content">
    <section class="input-section">
      <CommentInput onAnalyze={analyzeComment} />
      <div class="action-row">
        <button class="btn-samples" onclick={loadSamples} disabled={loadingSamples}>
          <span class="btn-icon">◈</span>
          {loadingSamples ? '加载中...' : '加载样本评论'}
        </button>
        {#if allResults.length > 0}
          <button class="btn-clear" onclick={clearResults}>
            <span class="btn-icon">✕</span>
            清空结果
          </button>
          <span class="result-count">{allResults.length} 条已分析</span>
        {/if}
      </div>
    </section>

    <div class="content-grid">
      <section class="results-column">
        <FilterBar
          {activeFilter}
          {counts}
          {showToxic}
          onFilterChange={(f) => (activeFilter = f)}
          onToggleToxic={() => (showToxic = !showToxic)}
        />
        <CommentList results={filteredResults} />
      </section>

      <aside class="stats-column">
        <StatsPanel {counts} />
      </aside>
    </div>
  </main>

  <footer class="app-footer">
    <span class="footer-text">Comment Sentiment Filter v0.1.0</span>
  </footer>
</div>

<style>
  .app-shell {
    max-width: 1180px;
    margin: 0 auto;
    padding: 2.5rem 2rem 3rem;
    min-height: 100vh;
    position: relative;
    animation: fadeIn 0.6s ease-out;
  }

  /* Corner accents */
  .corner-accent {
    position: fixed;
    width: 120px;
    height: 120px;
    pointer-events: none;
    z-index: 0;
  }
  .corner-accent.top-left {
    top: 0;
    left: 0;
    border-top: 1px solid var(--border-subtle);
    border-left: 1px solid var(--border-subtle);
  }
  .corner-accent.top-right {
    top: 0;
    right: 0;
    border-top: 1px solid var(--border-subtle);
    border-right: 1px solid var(--border-subtle);
  }

  /* Hero header */
  .hero {
    text-align: center;
    margin-bottom: 3rem;
    padding: 1rem 0 2rem;
    animation: fadeInUp 0.8s var(--ease-out-expo);
  }

  .hero-badge {
    display: inline-block;
    padding: 0.3rem 1rem;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent-solid);
    border: 1px solid var(--border-subtle);
    border-radius: 2px;
    margin-bottom: 1.5rem;
    background: var(--glass-bg);
  }

  .hero-title {
    margin: 0;
  }

  .title-main {
    font-family: var(--font-display);
    font-size: 2.8rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    background: var(--accent-gradient);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientFlow 6s ease infinite;
    line-height: 1.2;
  }

  .hero-subtitle {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    color: var(--text-secondary);
    font-size: 0.88rem;
    font-weight: 300;
    margin-top: 1rem;
    letter-spacing: 0.04em;
  }

  .subtitle-divider {
    display: inline-block;
    width: 32px;
    height: 1px;
    background: var(--border-medium);
  }

  /* Input section */
  .input-section {
    margin-bottom: 2rem;
    animation: fadeInUp 0.8s var(--ease-out-expo) 0.1s both;
  }

  .action-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 1rem;
  }

  .btn-samples,
  .btn-clear {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1.2rem;
    border-radius: 4px;
    font-family: var(--font-body);
    font-size: 0.82rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s var(--ease-out-expo);
    letter-spacing: 0.02em;
  }

  .btn-samples {
    background: var(--glass-bg);
    border: 1px solid var(--border-medium);
    color: var(--text-primary);
    backdrop-filter: blur(8px);
  }

  .btn-samples:hover:not(:disabled) {
    border-color: var(--accent-solid);
    color: var(--accent-solid);
    box-shadow: 0 0 20px rgba(129, 140, 248, 0.1);
  }

  .btn-samples:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .btn-clear {
    background: transparent;
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
  }

  .btn-clear:hover {
    border-color: var(--color-toxic);
    color: var(--color-toxic);
  }

  .btn-icon {
    font-size: 0.75rem;
  }

  .result-count {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-tertiary);
    margin-left: auto;
    letter-spacing: 0.05em;
  }

  /* Content grid */
  .content-grid {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 2rem;
    align-items: start;
    animation: fadeInUp 0.8s var(--ease-out-expo) 0.2s both;
  }

  .results-column {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  /* Footer */
  .app-footer {
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-subtle);
    text-align: center;
  }

  .footer-text {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    color: var(--text-tertiary);
    text-transform: uppercase;
  }

  @media (max-width: 820px) {
    .app-shell {
      padding: 1.5rem 1rem 2rem;
    }
    .title-main {
      font-size: 2rem;
    }
    .content-grid {
      grid-template-columns: 1fr;
    }
    .stats-column {
      order: -1;
    }
    .corner-accent {
      display: none;
    }
  }
</style>
