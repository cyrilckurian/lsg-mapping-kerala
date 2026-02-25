<script>
	import { base } from '$app/paths';
	let { chapterContent, ruleName, chapterTitle, chapterNumber, ruleId, chapters = [] } = $props();

	let currentIndex = $derived(chapters.findIndex((c) => c.number === chapterNumber));
	let prevChapter = $derived(currentIndex > 0 ? chapters[currentIndex - 1] : null);
	let nextChapter = $derived(
		currentIndex < chapters.length - 1 ? chapters[currentIndex + 1] : null
	);
</script>

<main class="flex-[2] flex flex-col bg-white dark:bg-slate-900 overflow-hidden h-full">
	<div class="flex-1 overflow-y-auto custom-scrollbar px-8 py-12 lg:px-16">
		<div class="mx-auto max-w-3xl">
			<!-- Breadcrumbs -->
			<nav
				class="mb-8 flex items-center gap-2 text-xs font-medium text-slate-400 dark:text-slate-500"
			>
				<a class="hover:text-primary transition-colors" href="{base}/">Home</a>
				<span class="material-symbols-outlined text-xs">chevron_right</span>
				<a class="hover:text-primary transition-colors" href="{base}/">{ruleName}</a>
				<span class="material-symbols-outlined text-xs">chevron_right</span>
				<span class="text-slate-900 dark:text-slate-200"
					>Chapter {chapterNumber} - {chapterTitle}</span
				>
			</nav>

			<article class="prose prose-slate dark:prose-invert max-w-none">
				<header class="mb-10 border-b border-slate-100 dark:border-slate-800 pb-10">
					<h1 class="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
						Chapter {chapterNumber}: {chapterTitle}
					</h1>
					{#if chapterContent?.description}
						<p class="mt-4 text-lg text-slate-600 dark:text-slate-400 leading-relaxed">
							{chapterContent.description}
						</p>
					{/if}
					<div class="mt-6 flex gap-3">
						<button
							class="flex items-center gap-2 rounded-lg bg-slate-100 dark:bg-slate-800 px-4 py-2 text-sm font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
						>
							<span class="material-symbols-outlined text-lg">download</span>
							Download PDF
						</button>
						<button
							class="flex items-center gap-2 rounded-lg bg-slate-100 dark:bg-slate-800 px-4 py-2 text-sm font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
						>
							<span class="material-symbols-outlined text-lg">print</span>
							Print
						</button>
					</div>
				</header>

				<section class="space-y-10">
					{#each chapterContent?.sections || [] as section (section.number)}
						<div class="section-group">
							<h2
								class="text-2xl font-bold text-slate-900 dark:text-white flex items-start gap-3 mb-6"
							>
								<span class="text-primary/40 dark:text-primary/30 shrink-0">{section.number}.</span>
								<span>{section.title}</span>
							</h2>

							<div class="space-y-4">
								{#each section.paragraphs || [] as para, i (i)}
									<p class="text-slate-700 dark:text-slate-300 leading-relaxed">
										{para}
									</p>
								{/each}

								{#each section.subPoints || [] as point (point.label)}
									<div class="flex items-start gap-3 pl-4">
										<span class="font-bold text-slate-900 dark:text-slate-200 min-w-[1.5rem]"
											>{point.label}</span
										>
										<p class="text-slate-700 dark:text-slate-300 leading-relaxed">
											{point.text}
										</p>
									</div>
								{/each}

								{#if section.tables}
									{#each section.tables as table, i (i)}
										<div class="mt-8">
											<h4
												class="text-sm font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2"
											>
												<span class="material-symbols-outlined text-primary text-lg"
													>table_chart</span
												>
												{table.title}
											</h4>
											<div
												class="overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800"
											>
												<table class="w-full text-left text-sm border-collapse">
													<thead class="bg-slate-50 dark:bg-slate-800/50">
														<tr>
															{#each table.headers as header, i (i)}
																<th
																	class="px-4 py-3 font-bold text-slate-900 dark:text-white border-b border-slate-200 dark:border-slate-800"
																	>{header}</th
																>
															{/each}
														</tr>
													</thead>
													<tbody
														class="divide-y divide-slate-100 dark:divide-slate-800 bg-white dark:bg-slate-900"
													>
														{#each table.rows as row, i (i)}
															<tr
																class="hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors"
															>
																{#each row as cell, j (j)}
																	<td class="px-4 py-3 text-slate-700 dark:text-slate-300"
																		>{cell}</td
																	>
																{/each}
															</tr>
														{/each}
													</tbody>
												</table>
											</div>
										</div>
									{/each}
								{/if}
							</div>
						</div>
					{/each}
				</section>
			</article>
		</div>
	</div>

	<!-- Fixed Pagination Footer -->
	<footer
		class="sticky bottom-0 border-t border-slate-100 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md px-8 py-4 lg:px-16 flex-shrink-0 z-10"
	>
		<div class="mx-auto max-w-3xl flex items-center justify-between">
			{#if prevChapter}
				<a
					href="{base}/rules/{ruleId}/{prevChapter.id}"
					class="flex flex-col items-start gap-1 text-slate-400 hover:text-primary transition-colors group"
				>
					<span class="text-[10px] font-bold uppercase tracking-wider">Previous</span>
					<span
						class="font-bold text-slate-600 dark:text-slate-400 group-hover:text-primary whitespace-nowrap overflow-hidden text-ellipsis max-w-[200px]"
						>Chapter {prevChapter.number} - {prevChapter.title}</span
					>
				</a>
			{:else}
				<div></div>
			{/if}

			{#if nextChapter}
				<a
					href="{base}/rules/{ruleId}/{nextChapter.id}"
					class="flex flex-col items-end gap-1 text-slate-400 hover:text-primary transition-colors group"
				>
					<span class="text-[10px] font-bold uppercase tracking-wider">Next</span>
					<span
						class="font-bold text-slate-600 dark:text-slate-400 group-hover:text-primary whitespace-nowrap overflow-hidden text-ellipsis max-w-[200px]"
						>Chapter {nextChapter.number} - {nextChapter.title}</span
					>
				</a>
			{:else}
				<div></div>
			{/if}
		</div>
	</footer>
</main>
