<script>
	import { page } from '$app/state';
	import RuleChaptersSidebar from '$lib/components/RuleChaptersSidebar.svelte';
	import ChapterContentView from '$lib/components/ChapterContentView.svelte';
	import LibraryChatPanel from '$lib/components/LibraryChatPanel.svelte';
	import kmbrData from '$lib/data/kmbr.json';

	// Map of rule IDs to data (in a real app this would be more dynamic)
	const rulesData = {
		kmbr: kmbrData
	};

	let ruleId = $derived(page.params.ruleId);
	let chapterId = $derived(page.params.chapterId);

	let currentRule = $derived(rulesData[ruleId]);
	let currentChapter = $derived(currentRule?.chapters.find((c) => c.id === chapterId));
	let currentContent = $derived(currentRule?.content[chapterId]);
</script>

<div class="flex flex-1 overflow-hidden h-full">
	{#if currentRule}
		<RuleChaptersSidebar ruleData={currentRule} activeChapterId={chapterId} />

		<ChapterContentView
			chapterContent={currentContent}
			ruleName={currentRule.name}
			chapterTitle={currentChapter?.title || ''}
			chapterNumber={currentChapter?.number || ''}
			{ruleId}
			chapters={currentRule.chapters}
		/>

		<LibraryChatPanel />
	{:else}
		<div class="flex-1 flex items-center justify-center bg-white dark:bg-slate-900">
			<div class="text-center">
				<h2 class="text-xl font-bold text-slate-900 dark:text-white mb-2">Rule Not Found</h2>
				<p class="text-slate-600 dark:text-slate-400 mb-4">
					The regulation you are looking for does not exist or has not been digitized yet.
				</p>
				<a href="/" class="text-primary font-bold hover:underline">Return to Library</a>
			</div>
		</div>
	{/if}
</div>
