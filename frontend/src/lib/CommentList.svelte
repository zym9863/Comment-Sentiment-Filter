<script lang="ts">
  import type { CommentResult } from './types'
  import CommentCard from './CommentCard.svelte'

  let { results }: { results: CommentResult[] } = $props()
</script>

{#if results.length === 0}
  <div class="empty-state">
    <p>暂无评论分析结果</p>
    <p class="empty-hint">输入评论或加载样本数据开始体验</p>
  </div>
{:else}
  <div class="comment-list">
    {#each results as result, i (i)}
      <CommentCard {result} />
    {/each}
  </div>
{/if}

<style>
  .comment-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--text-muted);
  }
  .empty-state p {
    margin: 0.25rem 0;
  }
  .empty-hint {
    font-size: 0.85rem;
  }
</style>
