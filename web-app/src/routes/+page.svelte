<script>
	import LibraryHeader from '$lib/components/LibraryHeader.svelte';
	import LibraryJurisdictionSidebar from '$lib/components/LibraryJurisdictionSidebar.svelte';
	import LibraryChatPanel from '$lib/components/LibraryChatPanel.svelte';
</script>

<div class="flex h-screen flex-col bg-slate-50 dark:bg-slate-900 overflow-hidden font-display">
	<!-- <LibraryHeader /> -->

	<main class="flex flex-1 overflow-hidden">
		<LibraryJurisdictionSidebar />

		<!-- Column 2: Main Content (Documentation View) -->
		<section
			class="flex-[2] overflow-y-auto bg-white dark:bg-slate-900 p-8 md:p-12 lg:p-16 custom-scrollbar"
		>
			<div class="max-w-3xl mx-auto">
				<div class="mb-10">
					<div
						class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-wider mb-4"
					>
						<span class="material-symbols-outlined text-sm">verified</span>
						Official Repository
					</div>
					<h1 class="text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-4">
						Welcome to the Architecture Law Library
					</h1>
					<p class="text-xl text-slate-600 dark:text-slate-400 leading-relaxed">
						Your centralized, searchable repository for Indian building regulations, municipality
						codes, and regional architectural compliance standards.
					</p>
				</div>

				<div class="grid grid-cols-1 gap-6 mb-12">
					<div
						class="p-6 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50"
					>
						<h3
							class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-3"
						>
							<span class="material-symbols-outlined text-primary">auto_stories</span>
							Getting Started
						</h3>
						<p class="text-slate-600 dark:text-slate-400 text-sm leading-normal mb-4">
							Select a state or jurisdiction from the left sidebar to begin browsing official
							documentation. All documents are sourced from authorized legislative portals and
							updated regularly.
						</p>
						<div class="flex flex-wrap gap-3">
							<button
								class="px-4 py-2 bg-primary text-white text-sm font-bold rounded-lg hover:bg-primary/90 transition-colors"
								>Browse Kerala Rules</button
							>
							<button
								class="px-4 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 text-sm font-bold rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
								>View NBC 2024</button
							>
						</div>
					</div>
				</div>

				<div class="prose prose-slate dark:prose-invert max-w-none">
					<h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">
						Current Library Coverage
					</h2>
					<ul class="space-y-4 list-none p-0">
						<li class="flex items-start gap-4">
							<div class="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg text-primary">
								<span class="material-symbols-outlined">description</span>
							</div>
							<div>
								<h4 class="font-bold text-slate-800 dark:text-slate-200">Building Codes (NBC)</h4>
								<p class="text-sm text-slate-500 dark:text-slate-400">
									Complete digitized version of the National Building Code of India with
									cross-references.
								</p>
							</div>
						</li>
						<li class="flex items-start gap-4">
							<div class="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg text-primary">
								<span class="material-symbols-outlined">gavel</span>
							</div>
							<div>
								<h4 class="font-bold text-slate-800 dark:text-slate-200">State Amendments</h4>
								<p class="text-sm text-slate-500 dark:text-slate-400">
									Specific variations for Kerala and Karnataka municipalities including FAR,
									setbacks, and density.
								</p>
							</div>
						</li>
						<li class="flex items-start gap-4">
							<div class="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg text-primary">
								<span class="material-symbols-outlined">eco</span>
							</div>
							<div>
								<h4 class="font-bold text-slate-800 dark:text-slate-200">
									Environmental Regulations
								</h4>
								<p class="text-sm text-slate-500 dark:text-slate-400">
									CRZ norms, rain water harvesting mandates, and solar energy requirements for
									residential plots.
								</p>
							</div>
						</li>
					</ul>
				</div>

				<!-- Hero/Context Image -->
				<div
					class="mt-12 rounded-xl overflow-hidden border border-slate-200 dark:border-slate-800 h-64 relative bg-slate-200"
				>
					<img
						alt="Architectural Building"
						class="w-full h-full object-cover opacity-60 dark:opacity-40"
						src="https://lh3.googleusercontent.com/aida-public/AB6AXuBV9fIPy6DqCGpuEc8XAnHVrHfePZBhPdRc5FJhPb0aUe-kOi7K7v5KdzcIH2VzVw59yLZ--CellDjuUF2ZltIpGD3gcqUjPlRkUTkTTDQC1UWJSrw-8upow3G0myDUwSZH-abBfyOVrDKf_NcINb8zl7B_0eX4cPrTZWZg4zmPaRVlX3ZqaSs1C15n2RFcNQovd0dG9Gjp0IYdR_e7LssSME7H6JH-_IOULjDmzkAcfGjag4jss9THm2ql_FMQLIl1M2Cc-DVuPyc"
					/>
					<div
						class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-8"
					>
						<p class="text-white font-medium italic">
							"Architecture should speak of its time and place, but yearn for timelessness."
						</p>
					</div>
				</div>
			</div>
		</section>

		<LibraryChatPanel />
	</main>
</div>
