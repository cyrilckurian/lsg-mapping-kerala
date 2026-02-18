<script>
	let activeTab = 'states';
</script>

<aside
	class="w-72 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 overflow-y-auto flex flex-col"
>
	<div class="p-6">
		<h1 class="text-slate-900 dark:text-white text-xl font-bold mb-4">Library</h1>

		<!-- Toggle Tabs -->
		<div class="bg-slate-100 dark:bg-slate-800 p-1 rounded-lg flex mb-6">
			<button
				class="flex-1 py-1.5 text-xs font-semibold rounded-md transition-all duration-200 {activeTab ===
				'states'
					? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm'
					: 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}"
				on:click={() => (activeTab = 'states')}
			>
				States
			</button>
			<button
				class="flex-1 py-1.5 text-xs font-semibold rounded-md transition-all duration-200 {activeTab ===
				'other'
					? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm'
					: 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}"
				on:click={() => (activeTab = 'other')}
			>
				Other
			</button>
		</div>

		{#if activeTab === 'states'}
			<!-- States Section -->
			<div class="space-y-1">
				<!-- Kerala Dropdown -->
				<details class="group" open>
					<summary
						class="flex cursor-pointer items-center justify-between gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors list-none"
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
						class="mt-1 ml-9 flex flex-col gap-1 border-l border-slate-100 dark:border-slate-800"
					>
						<a
							class="px-4 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary border-l-2 border-transparent hover:border-primary"
							href="javascript:void(0)">Municipality Building Rules</a
						>
						<a
							class="px-4 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary border-l-2 border-transparent hover:border-primary"
							href="javascript:void(0)">Panchayat Building Rules</a
						>
						<a
							class="px-4 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary border-l-2 border-transparent hover:border-primary"
							href="javascript:void(0)">Coastal Regulation Zone</a
						>
					</div>
				</details>

				<!-- Karnataka Dropdown -->
				<details class="group">
					<summary
						class="flex cursor-pointer items-center justify-between gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors list-none"
					>
						<div class="flex items-center gap-3">
							<span class="material-symbols-outlined text-slate-400">location_on</span>
							<span class="text-sm font-medium">Karnataka</span>
						</div>
						<span
							class="material-symbols-outlined text-slate-400 group-open:rotate-180 transition-transform text-lg"
							>expand_more</span
						>
					</summary>
					<div
						class="mt-1 ml-9 flex flex-col gap-1 border-l border-slate-100 dark:border-slate-800"
					>
						<a
							class="px-4 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary border-l-2 border-transparent"
							href="javascript:void(0)">BBMP Building Bye-laws</a
						>
						<a
							class="px-4 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary border-l-2 border-transparent"
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
