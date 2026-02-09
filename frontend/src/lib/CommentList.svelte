<script lang="ts">
  import type { CommentResult } from './types'
  import CommentCard from './CommentCard.svelte'

  let { results }: { results: CommentResult[] } = $props()
</script>

{#if results.length === 0}
  <div class="empty">
    <div class="empty-icon">◇</div>
    <p class="empty-title">等待分析</p>
    <p class="empty-hint">输入评论或加载样本数据开始体验</p>
  </div>
{:else}
  <div class="list">
    {#each results as result, i (i)}
      <div class="list-item" style="animation-delay: {Math.min(i * 60, 600)}ms">
        <CommentCard {result} />
      </div>
    {/each}
  </div>
{/if}

<style>
  .list {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }

  .list-item {
    animation: fadeInUp 0.5s var(--ease-out-expo) both;
  }

  .empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 1rem;
    text-align: center;
    animation: fadeIn 0.6s ease;
  }

  .empty-icon {
    font-size: 2rem;
    color: var(--text-tertiary);
    margin-bottom: 1rem;
    animation: pulseGlow 3s ease infinite;
  }

  .empty-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    color: var(--text-secondary);
    margin-bottom: 0.4rem;
  }

  .empty-hint {
    font-size: 0.82rem;
    color: var(--text-tertiary);
    font-weight: 300;
  }
</style>
