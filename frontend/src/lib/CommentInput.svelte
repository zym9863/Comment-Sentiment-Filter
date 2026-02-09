<script lang="ts">
  import type { CommentResult } from './types'

  let { onAnalyze }: { onAnalyze: (text: string) => Promise<void> } = $props()

  let text: string = $state('')
  let loading: boolean = $state(false)

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

<div class="comment-input">
  <textarea
    bind:value={text}
    placeholder="输入评论内容进行分析（支持中英文）..."
    rows="3"
    onkeydown={handleKeydown}
    disabled={loading}
  ></textarea>
  <div class="input-actions">
    <span class="hint">Ctrl + Enter 提交</span>
    <button onclick={handleSubmit} disabled={!text.trim() || loading}>
      {loading ? '分析中...' : '分析评论'}
    </button>
  </div>
</div>

<style>
  .comment-input {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--card-bg);
    color: var(--text-color);
    font-size: 0.95rem;
    resize: vertical;
    font-family: inherit;
    line-height: 1.5;
    box-sizing: border-box;
  }
  textarea:focus {
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }
  textarea:disabled {
    opacity: 0.6;
  }
  .input-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .hint {
    font-size: 0.8rem;
    color: var(--text-muted);
  }
  button {
    padding: 0.5rem 1.5rem;
    background: var(--accent-color);
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: opacity 0.2s;
  }
  button:hover:not(:disabled) {
    opacity: 0.9;
  }
  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
