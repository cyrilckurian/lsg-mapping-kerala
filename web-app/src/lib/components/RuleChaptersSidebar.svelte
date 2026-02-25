<script>
	import { base } from '$app/paths';

	let { ruleData, activeChapterId } = $props();

	let chapters = $derived(ruleData?.chapters || []);
</script>

<aside
	class="w-72 flex-shrink-0 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 overflow-y-auto hidden lg:block"
>
	<a
		class="mb-8 flex items-center gap-2 text-sm font-semibold text-primary hover:underline"
		href="{base}/"
	>
		<span class="material-symbols-outlined text-sm">arrow_back</span>
		Back to Library
	</a>

	<div class="mb-8">
		<span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500"
			>Current Regulation</span
		>
		<h1 class="mt-1 text-base font-bold leading-tight text-slate-900 dark:text-white">
			{ruleData?.name || 'Regulation'}
		</h1>
		<p class="mt-1 text-xs text-slate-500 dark:text-slate-400">
			Last updated: {ruleData?.lastUpdated || 'Unknown'}
		</p>
	</div>

	<nav class="space-y-1">
		{#each chapters as chapter (chapter.id)}
			<a
				href="{base}/rules/{ruleData.id}/{chapter.id}"
				class="group flex items-center gap-3 rounded-lg px-3 py-2 text-xs transition-colors {activeChapterId ===
				chapter.id
					? 'bg-primary/10 text-primary font-bold'
					: 'font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-primary dark:hover:text-primary'}"
			>
				<span
					class="material-symbols-outlined {activeChapterId === chapter.id
						? 'text-primary'
						: 'text-slate-400 dark:text-slate-500 group-hover:text-primary'}"
				>
					{chapter.icon || 'menu_book'}
				</span>
				Chapter {chapter.number} - {chapter.title}
			</a>
		{/each}
	</nav>
</aside>
