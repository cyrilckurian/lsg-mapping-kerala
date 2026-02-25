<script>
	let activeTab = $state('chats');

	const recentProjects = [
		{
			id: 1,
			name: 'Modern 2BHK Layout',
			updated: '12 mins ago',
			rooms: 3,
			area: '200m²',
			active: true
		},
		{
			id: 2,
			name: 'Studio Apartment A',
			updated: '2 hours ago',
			rooms: 1,
			area: '45m²',
			active: false
		},
		{
			id: 3,
			name: 'Villa Concept v2',
			updated: 'Yesterday',
			rooms: 5,
			area: '380m²',
			active: false
		},
		{
			id: 4,
			name: 'Corner Plot – 3BHK',
			updated: '2 days ago',
			rooms: 4,
			area: '230m²',
			active: false
		},
		{
			id: 5,
			name: 'Commercial Unit - A3',
			updated: 'Last week',
			rooms: 2,
			area: '120m²',
			active: false
		}
	];

	const galleryItems = [
		{ id: 1, label: 'Living Room Concepts', count: 4 },
		{ id: 2, label: 'Kitchen Layouts', count: 7 },
		{ id: 3, label: 'Master Bedroom', count: 3 },
		{ id: 4, label: 'Exterior Views', count: 5 }
	];

	let selectedProject = $state(1);
</script>

<aside
	class="w-72 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col shrink-0"
>
	<!-- Header -->
	<div class="px-6 pt-6 pb-2 flex items-center justify-between">
		<h1 class="text-slate-900 dark:text-white text-2xl font-bold">Floor Planner</h1>
	</div>

	<!-- New Plan Button -->
	<div class="px-4 pb-3">
		<button
			class="w-full py-2 px-4 bg-slate-900 dark:bg-white text-white dark:text-slate-900 rounded-lg text-xs font-bold hover:bg-slate-800 dark:hover:bg-slate-100 transition-colors flex items-center justify-center gap-2"
		>
			<span class="material-symbols-outlined text-sm">add</span>
			New Plan
		</button>
	</div>

	<!-- Toggle Tabs — same design as LibraryJurisdictionSidebar -->
	<div class="flex w-full border-b border-slate-200 dark:border-slate-800">
		<button
			class="flex-1 pb-3 pt-2 text-sm transition-colors text-center relative border-b-2 {activeTab ===
			'chats'
				? 'font-semibold text-primary border-primary'
				: 'font-medium text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 border-transparent'}"
			onclick={() => (activeTab = 'chats')}
		>
			Chats
		</button>
		<button
			class="flex-1 pb-3 pt-2 text-sm transition-colors text-center border-b-2 {activeTab ===
			'gallery'
				? 'font-semibold text-primary border-primary'
				: 'font-medium text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 border-transparent'}"
			onclick={() => (activeTab = 'gallery')}
		>
			Gallery
		</button>
	</div>

	<!-- Content -->
	<div class="flex-1 overflow-y-auto px-4 py-4">
		{#if activeTab === 'chats'}
			<!-- Plan History -->
			<p
				class="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-3"
			>
				Recent Projects
			</p>
			<div class="space-y-2">
				{#each recentProjects as project (project.id)}
					<button
						class="w-full text-left p-3 rounded-lg border transition-all {selectedProject ===
						project.id
							? 'border-primary bg-primary/5 dark:bg-primary/10'
							: 'border-slate-100 dark:border-slate-800 hover:border-slate-200 dark:hover:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50'}"
						onclick={() => (selectedProject = project.id)}
					>
						<div class="flex items-start justify-between gap-2">
							<div class="min-w-0">
								<p class="text-xs font-bold text-slate-900 dark:text-slate-100 truncate">
									{project.name}
								</p>
								<p class="text-[10px] text-slate-400 dark:text-slate-500 mt-0.5">
									Updated {project.updated}
								</p>
							</div>
							{#if selectedProject === project.id}
								<span class="material-symbols-outlined text-primary text-base shrink-0"
									>edit_note</span
								>
							{/if}
						</div>
						<div class="flex items-center gap-3 mt-2">
							<span class="text-[10px] text-slate-500 dark:text-slate-400 flex items-center gap-1">
								<span class="material-symbols-outlined text-xs">bed</span>
								{project.rooms} rooms
							</span>
							<span class="text-[10px] text-slate-500 dark:text-slate-400 flex items-center gap-1">
								<span class="material-symbols-outlined text-xs">straighten</span>
								{project.area}
							</span>
						</div>
					</button>
				{/each}
			</div>
		{:else}
			<!-- Gallery Tab -->
			<p
				class="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-3"
			>
				Generated Images
			</p>
			<div class="space-y-2">
				{#each galleryItems as item (item.id)}
					<button
						class="w-full text-left flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors border border-transparent hover:border-slate-100 dark:hover:border-slate-700"
					>
						<span class="material-symbols-outlined text-slate-400 text-base">image</span>
						<div class="flex-1 min-w-0">
							<p class="text-xs font-medium truncate">{item.label}</p>
						</div>
						<span
							class="text-[10px] bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 rounded-full px-2 py-0.5 font-bold"
						>
							{item.count}
						</span>
					</button>
				{/each}
			</div>
		{/if}
	</div>
</aside>
