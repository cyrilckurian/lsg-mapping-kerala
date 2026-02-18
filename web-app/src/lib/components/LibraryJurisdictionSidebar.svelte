<script>
	let activeTab = 'states';
</script>

<aside
	class="w-72 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 overflow-y-auto flex flex-col"
>
	<div class="px-6 pt-6 pb-2">
		<!-- Header Branding -->
		<div class="flex items-center gap-3 text-primary mb-6">
			<div class="size-8 flex items-center justify-center bg-primary/10 rounded-lg shrink-0">
				<span class="material-symbols-outlined text-primary text-xl">account_balance</span>
			</div>
			<h2 class="text-slate-900 dark:text-white text-base font-bold leading-tight tracking-tight">
				Architecture Law
			</h2>
		</div>
		<h1 class="text-slate-900 dark:text-white text-2xl font-bold mb-6">Library</h1>
	</div>

	<!-- Toggle Tabs -->
	<div class="flex w-full border-b border-slate-200 dark:border-slate-800">
		<button
			class="flex-1 pb-3 pt-2 text-sm transition-colors text-center relative border-b-2 {activeTab ===
			'states'
				? 'font-semibold text-primary border-primary'
				: 'font-medium text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 border-transparent'}"
			on:click={() => (activeTab = 'states')}
		>
			States
		</button>
		<button
			class="flex-1 pb-3 pt-2 text-sm transition-colors text-center border-b-2 {activeTab ===
			'other'
				? 'font-semibold text-primary border-primary'
				: 'font-medium text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 border-transparent'}"
			on:click={() => (activeTab = 'other')}
		>
			General
		</button>
	</div>

	<div class="flex-1 overflow-y-auto px-6 py-6">
		{#if activeTab === 'states'}
			<p
				class="text-slate-500 dark:text-slate-400 text-xs font-semibold uppercase tracking-wider mb-4"
			>
				Available Regions
			</p>
			<!-- States Section -->
			<div class="space-y-1">
				<!-- Kerala Dropdown -->
				<details class="group" open>
					<summary
						class="flex cursor-pointer items-center justify-between gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors list-none select-none"
					>
						<div class="flex items-center gap-3">
							<span class="material-symbols-outlined text-primary">location_on</span>
							<span class="text-sm font-medium">Kerala</span>
						</div>
						<span
							class="material-symbols-outlined text-slate-400 group-open:rotate-180 transition-transform text-lg"
							>expand_more</span
						>
					</summary>
					<div
						class="mt-1 ml-9 flex flex-col gap-1 border-l border-slate-100 dark:border-slate-800 pl-2"
					>
						<a
							class="px-3 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded-md block transition-colors"
							href="javascript:void(0)">Municipality Building Rules</a
						>
						<a
							class="px-3 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded-md block transition-colors"
							href="javascript:void(0)">Panchayat Building Rules</a
						>
						<a
							class="px-3 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded-md block transition-colors"
							href="javascript:void(0)">Coastal Regulation Zone</a
						>
					</div>
				</details>

				<!-- Karnataka Dropdown -->
				<details class="group">
					<summary
						class="flex cursor-pointer items-center justify-between gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors list-none select-none"
					>
						<div class="flex items-center gap-3">
							<span
								class="material-symbols-outlined text-slate-400 group-hover:text-slate-500 dark:group-hover:text-slate-300 transition-colors"
								>location_on</span
							>
							<span class="text-sm font-medium">Karnataka</span>
						</div>
						<span
							class="material-symbols-outlined text-slate-400 group-open:rotate-180 transition-transform text-lg"
							>expand_more</span
						>
					</summary>
					<div
						class="mt-1 ml-9 flex flex-col gap-1 border-l border-slate-100 dark:border-slate-800 pl-2"
					>
						<a
							class="px-3 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded-md block transition-colors"
							href="javascript:void(0)">BBMP Building Bye-laws</a
						>
						<a
							class="px-3 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded-md block transition-colors"
							href="javascript:void(0)">Town & Country Planning</a
						>
					</div>
				</details>
			</div>
		{:else}
			<!-- Other Jurisdictions Section -->
			<div class="space-y-1">
				<a
					class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors"
					href="javascript:void(0)"
				>
					<span class="material-symbols-outlined text-slate-400">menu_book</span>
					<span class="text-sm font-medium">National Building Code</span>
				</a>
				<a
					class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors"
					href="javascript:void(0)"
				>
					<span class="material-symbols-outlined text-slate-400">local_fire_department</span>
					<span class="text-sm font-medium">Fire Safety Norms</span>
				</a>
				<a
					class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors"
					href="javascript:void(0)"
				>
					<span class="material-symbols-outlined text-slate-400">history</span>
					<span class="text-sm font-medium">Recent Updates</span>
				</a>
			</div>
		{/if}
	</div>
</aside>
