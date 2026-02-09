<script lang="ts">
  let { onAnalyze }: { onAnalyze: (text: string) => Promise<void> } = $props()

  let text: string = $state('')
  let loading: boolean = $state(false)
  let focused: boolean = $state(false)

  async function handleSubmit() {
    if (!text.trim() || loading) return
    loading = true
    try {
      await onAnalyze(text.trim())
      text = ''
    } finally {
      loading = false
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSubmit()
    }
  }
</script>

<div class="input-wrapper" class:focused class:loading>
  <div class="input-chrome">
    <div class="input-header">
      <span class="input-label">评论分析</span>
      <span class="char-count">{text.length}</span>
    </div>
    <textarea
      bind:value={text}
      placeholder="在此输入评论内容进行情感分析..."
      rows="3"
      onkeydown={handleKeydown}
      onfocus={() => (focused = true)}
      onblur={() => (focused = false)}
      disabled={loading}
    ></textarea>
    <div class="input-footer">
      <kbd class="shortcut">Ctrl <span class="kbd-plus">+</span> Enter</kbd>
      <button class="submit-btn" onclick={handleSubmit} disabled={!text.trim() || loading}>
        {#if loading}
          <span class="loading-dot"></span>
          分析中
        {:else}
          <span class="submit-arrow">→</span>
          分析评论
        {/if}
      </button>
    </div>
  </div>
</div>

<style>
  .input-wrapper {
    position: relative;
    border-radius: 8px;
    transition: all 0.4s var(--ease-out-expo);
  }

  .input-chrome {
    background: var(--card-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.4s var(--ease-out-expo);
    backdrop-filter: blur(12px);
  }

  .input-wrapper.focused .input-chrome {
    border-color: var(--border-medium);
    box-shadow: var(--shadow-glow), 0 0 0 1px var(--border-subtle);
  }

  .input-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 1rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .input-label {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-tertiary);
  }

  .char-count {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-tertiary);
    tabular-nums: true;
  }

  textarea {
    width: 100%;
    padding: 1rem;
    border: none;
    background: transparent;
    color: var(--text-primary);
    font-family: var(--font-body);
    font-size: 0.92rem;
    font-weight: 300;
    line-height: 1.7;
    resize: vertical;
    min-height: 80px;
    outline: none;
  }

  textarea::placeholder {
    color: var(--text-tertiary);
    font-style: italic;
  }

  textarea:disabled {
    opacity: 0.5;
  }

  .input-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 1rem;
    border-top: 1px solid var(--border-subtle);
  }

  .shortcut {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-tertiary);
    padding: 0.2rem 0.5rem;
    border: 1px solid var(--border-subtle);
    border-radius: 3px;
    background: var(--glass-bg);
  }

  .kbd-plus {
    opacity: 0.5;
  }

  .submit-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 1.3rem;
    background: var(--accent-gradient);
    background-size: 200% 200%;
    border: none;
    border-radius: 4px;
    color: white;
    font-family: var(--font-body);
    font-size: 0.82rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s var(--ease-out-expo);
    letter-spacing: 0.02em;
  }

  .submit-btn:hover:not(:disabled) {
    animation: gradientFlow 3s ease infinite;
    box-shadow: 0 4px 20px rgba(129, 140, 248, 0.25);
    transform: translateY(-1px);
  }

  .submit-btn:active:not(:disabled) {
    transform: translateY(0);
  }

  .submit-btn:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }

  .submit-arrow {
    font-size: 1rem;
    transition: transform 0.2s;
  }

  .submit-btn:hover:not(:disabled) .submit-arrow {
    transform: translateX(2px);
  }

  .loading-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: white;
    animation: pulseGlow 1s ease infinite;
  }

  .input-wrapper.loading .input-chrome {
    border-color: var(--accent-solid);
  }
</style>
