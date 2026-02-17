<script>
	import { onMount, createEventDispatcher } from 'svelte';
	import { selectedLSG, searchQuery, markedLocation, markerLink } from '$lib/store.js';
	import { parseGoogleMapsLink } from '$lib/utils/googleMaps.js';
	import { fade, fly, crossfade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	const dispatch = createEventDispatcher();
	const [send, receive] = crossfade({
		duration: 400,
		easing: cubicInOut
	});

	let searchIndex = [];
	let filteredResults = [];
	let isSearching = false;
	let isLinkMode = false;
	let inputElement;

	onMount(async () => {
		const res = await fetch('/data/search_index.json');
		searchIndex = await res.json();
	});

	async function handleLinkInput(e) {
		const url = e.target.value || $markerLink;
		markerLink.set(url);
		if (!url) {
			markedLocation.set(null);
			return;
		}

		// Try direct parsing first
		let coords = parseGoogleMapsLink(url);

		// If it's a short link and not parsed, resolve it
		if (!coords && (url.includes('maps.app.goo.gl') || url.includes('goo.gl/maps'))) {
			try {
				const res = await fetch(`/api/resolve-link?url=${encodeURIComponent(url)}`);
				const data = await res.json();
				if (data.finalUrl) {
					coords = parseGoogleMapsLink(data.finalUrl);
				}
			} catch (err) {
				console.error('Failed to resolve short link:', err);
			}
		}

		if (coords) {
			markedLocation.set(coords);
		}
	}

	function toggleLinkMode() {
		isLinkMode = !isLinkMode;
		if (isLinkMode) {
			searchQuery.set('');
			setTimeout(() => inputElement?.focus(), 100);
		} else {
			markerLink.set('');
			// markedLocation.set(null); // Optional: clear marker when exiting mode? Keeping it might be better.
			setTimeout(() => inputElement?.focus(), 100);
		}
	}

	function handleInput(e) {
		const val = e.target.value;
		if (isLinkMode) {
			markerLink.set(val);
		} else {
			searchQuery.set(val);
		}
	}

	// Sync local input with stores when modes change or external updates happen
	$: if (isLinkMode) {
		if (inputElement && document.activeElement !== inputElement) inputElement.value = $markerLink;
	} else {
		if (inputElement && document.activeElement !== inputElement) inputElement.value = $searchQuery;
	}

	function checkEnter(e) {
		if (e.key === 'Enter' && isLinkMode) {
			handleLinkInput({ target: { value: $markerLink } });
		}
	}

	function clearLink() {
		markerLink.set('');
		markedLocation.set(null);
	}

	$: if ($searchQuery.length > 1 && !isLinkMode) {
		const q = $searchQuery.toLowerCase();
		filteredResults = searchIndex
			.filter(
				(item) => item.name.toLowerCase().includes(q) || (item.name_ml && item.name_ml.includes(q))
			)
			.slice(0, 10);
		isSearching = true;
	} else {
		filteredResults = [];
		isSearching = false;
	}

	function selectResult(item) {
		selectedLSG.set(item);
		searchQuery.set('');
		isSearching = false;
	}

	function clearSelection() {
		selectedLSG.set(null);
	}

	function clearSearch() {
		if (isLinkMode) {
			markerLink.set('');
		} else {
			searchQuery.set('');
		}
	}
</script>

<!-- Floating Search Bar -->
<div class="absolute top-6 left-1/2 transform -translate-x-1/2 z-30 w-full max-w-xl px-4">
	<div
		class="bg-white dark:bg-slate-900 rounded-lg shadow-lg flex items-center p-1 border border-slate-100 dark:border-slate-800 h-14 relative overflow-hidden"
	>
		<!-- Permanent Search Icon / Reset Button -->
		{#if isLinkMode}
			<button
				on:click={() => {
					isLinkMode = false;
					setTimeout(() => inputElement?.focus(), 100);
				}}
				class="pl-3 pr-2 text-slate-400 hover:text-primary transition-colors shrink-0 flex items-center justify-center cursor-pointer"
				title="Back to Default Search"
			>
				<span class="material-symbols-outlined">search</span>
			</button>
		{:else}
			<div class="pl-3 pr-2 text-slate-400 shrink-0 flex items-center justify-center">
				<span class="material-symbols-outlined">search</span>
			</div>
		{/if}

		{#if isLinkMode}
			<div class="w-px h-6 bg-slate-200 dark:bg-slate-700 mx-1 shrink-0" transition:fade></div>
			<button
				in:fly={{ x: -30, duration: 400, easing: cubicInOut }}
				out:fly={{ x: -30, duration: 400, easing: cubicInOut }}
				on:click={toggleLinkMode}
				class="p-1.5 mx-1 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shrink-0"
				title="Back to Search"
			>
				<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path
						d="M12 2C8.13 2 5 5.13 5 9C5 14.25 12 22 12 22C12 22 19 14.25 19 9C19 5.13 15.87 2 12 2Z"
						fill="#EA4335"
					/>
					<path
						d="M12 11.5C13.3807 11.5 14.5 10.3807 14.5 9C14.5 7.61929 13.3807 6.5 12 6.5C10.6193 6.5 9.5 7.61929 9.5 9C9.5 10.3807 10.6193 11.5 12 11.5Z"
						fill="#1967D2"
					/>
				</svg>
			</button>
		{/if}

		{#key isLinkMode}
			<input
				bind:this={inputElement}
				in:fly={{ x: 100, duration: 400, easing: cubicInOut, delay: 100 }}
				out:fly={{ x: -100, duration: 400, easing: cubicInOut }}
				class="flex-1 border-none focus:ring-0 text-slate-700 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 text-sm h-full bg-transparent min-w-0 pl-2"
				placeholder={isLinkMode
					? 'Paste Google Map Link and Press Enter'
					: 'Search jurisdiction, district, or statute...'}
				type="text"
				on:input={handleInput}
				on:keydown={checkEnter}
			/>
		{/key}

		{#if isLinkMode ? $markerLink : $searchQuery}
			<button
				on:click={clearSearch}
				class="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 shrink-0"
			>
				<span class="material-symbols-outlined text-sm">close</span>
			</button>
		{/if}

		{#if !isLinkMode}
			<div class="w-px h-6 bg-slate-200 dark:bg-slate-700 mx-2 shrink-0" transition:fade></div>
			<button
				in:fly={{ x: 30, duration: 400, easing: cubicInOut }}
				out:fly={{ x: 30, duration: 400, easing: cubicInOut }}
				on:click={toggleLinkMode}
				class="p-1.5 mr-1 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shrink-0"
				title="Search by Map Link"
			>
				<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path
						d="M12 2C8.13 2 5 5.13 5 9C5 14.25 12 22 12 22C12 22 19 14.25 19 9C19 5.13 15.87 2 12 2Z"
						fill="#EA4335"
					/>
					<circle cx="12" cy="9" r="2.5" fill="#1967D2" />
					<path
						d="M7 9C7 9.8 7.2 10.5 7.5 11.2L12 22L16.5 11.2C16.8 10.5 17 9.8 17 9C17 6.2 14.8 4 12 4C9.2 4 7 6.2 7 9Z"
						stroke="url(#paint0_linear)"
						stroke-opacity="0.2"
					/>
					<defs>
						<linearGradient
							id="paint0_linear"
							x1="12"
							y1="4"
							x2="12"
							y2="22"
							gradientUnits="userSpaceOnUse"
						>
							<stop stop-color="white" stop-opacity="0.5" />
							<stop offset="1" stop-color="white" stop-opacity="0" />
						</linearGradient>
					</defs>
				</svg>
			</button>
		{/if}
	</div>

	<!-- Search Results Dropdown -->
	{#if isSearching && filteredResults.length > 0}
		<div
			class="absolute top-full left-4 right-4 mt-2 bg-white dark:bg-slate-900 rounded-xl shadow-xl border border-slate-100 dark:border-slate-800 overflow-hidden z-50 max-h-96 overflow-y-auto custom-scrollbar"
		>
			{#each filteredResults as item (item.id)}
				<button
					on:click={() => selectResult(item)}
					class="w-full text-left px-4 py-3 hover:bg-emerald-50 dark:hover:bg-emerald-900/10 border-b border-slate-100 dark:border-slate-800 last:border-0 transition-colors flex flex-col gap-0.5"
				>
					<p class="text-sm font-bold text-slate-900 dark:text-slate-100">
						{item.name}
					</p>
					<div class="flex items-center gap-1.5">
						<span
							class="text-[10px] font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-500"
						>
							{item.lsg_type}
						</span>
						<span class="text-slate-300 dark:text-slate-600">•</span>
						<p class="text-xs text-slate-500 dark:text-slate-400">
							{item.district}
						</p>
					</div>
				</button>
			{/each}
		</div>
	{/if}
</div>

<!-- Floating Slide-out Details Panel -->
{#if $selectedLSG}
	<aside
		transition:fly={{ y: 20, duration: 300 }}
		class="absolute top-24 left-6 z-30 w-96 bg-white/95 dark:bg-slate-900/95 backdrop-blur-sm rounded-xl shadow-xl border border-slate-200/60 dark:border-slate-700/60 overflow-hidden flex flex-col max-h-[calc(100vh-8rem)]"
	>
		<!-- Panel Header -->
		<div
			class="p-5 border-b border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 relative"
		>
			<div class="flex justify-between items-start">
				<div>
					<div
						class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold uppercase tracking-wide mb-2 border"
						style="
                            background-color: {$selectedLSG.lsg_type === 'municipal corporation'
							? 'rgba(239, 68, 68, 0.1)'
							: $selectedLSG.lsg_type === 'municipality'
								? 'rgba(245, 158, 11, 0.1)'
								: 'rgba(59, 130, 246, 0.1)'};
                            color: {$selectedLSG.lsg_type === 'municipal corporation'
							? '#ef4444'
							: $selectedLSG.lsg_type === 'municipality'
								? '#f59e0b'
								: '#3b82f6'};
                            border-color: {$selectedLSG.lsg_type === 'municipal corporation'
							? 'rgba(239, 68, 68, 0.2)'
							: $selectedLSG.lsg_type === 'municipality'
								? 'rgba(245, 158, 11, 0.2)'
								: 'rgba(59, 130, 246, 0.2)'};
                        "
					>
						<span class="material-symbols-outlined" style="font-size: 14px;">domain</span>
						{$selectedLSG.lsg_type}
					</div>
					<h2 class="text-xl font-bold text-slate-900 dark:text-white leading-tight">
						{$selectedLSG.name}
					</h2>
					<p class="text-slate-500 dark:text-slate-400 text-sm mt-1">
						{$selectedLSG.district} District, Kerala
					</p>
					<button
						class="mt-4 w-full bg-primary hover:bg-primary/90 text-white py-2.5 px-4 rounded-lg text-sm font-semibold transition-all flex items-center justify-center gap-2 shadow-md shadow-primary/20"
					>
						<span class="material-symbols-outlined" style="font-size: 18px;">add</span>
						Add New Project
					</button>
				</div>
				<button
					on:click={clearSelection}
					class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1 rounded-md hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
				>
					<span class="material-symbols-outlined">close</span>
				</button>
			</div>
		</div>

		<!-- Scrollable Content -->
		<div class="overflow-y-auto custom-scrollbar flex-1 p-0 bg-white/50 dark:bg-slate-900/50">
			<!-- Stats / Laws -->
			<div class="p-5 pb-2">
				<div class="flex items-center justify-between mb-4">
					<h3 class="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wide">
						Applicable Statutes
					</h3>
					<span
						class="bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 text-xs px-2 py-0.5 rounded-full font-medium"
						>12 Active</span
					>
				</div>
				<div class="flex flex-col gap-3">
					<a
						class="group flex items-start gap-3 p-3 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-primary/30 hover:bg-primary/5 transition-all bg-white dark:bg-slate-800 shadow-sm"
						href="javascript:void(0)"
					>
						<div
							class="bg-blue-100 dark:bg-blue-900/30 text-primary p-2 rounded-md shrink-0 mt-0.5 group-hover:bg-primary group-hover:text-white transition-colors"
						>
							<span class="material-symbols-outlined" style="font-size: 20px;">gavel</span>
						</div>
						<div>
							<h4
								class="text-sm font-semibold text-slate-800 dark:text-slate-200 group-hover:text-primary transition-colors leading-snug"
							>
								The Kerala Municipality Act, 1994
							</h4>
							<p class="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-1">
								The primary legislation governing...
							</p>
						</div>
					</a>
					<a
						class="group flex items-start gap-3 p-3 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-primary/30 hover:bg-primary/5 transition-all bg-white dark:bg-slate-800 shadow-sm"
						href="javascript:void(0)"
					>
						<div
							class="bg-blue-100 dark:bg-blue-900/30 text-primary p-2 rounded-md shrink-0 mt-0.5 group-hover:bg-primary group-hover:text-white transition-colors"
						>
							<span class="material-symbols-outlined" style="font-size: 20px;">apartment</span>
						</div>
						<div>
							<h4
								class="text-sm font-semibold text-slate-800 dark:text-slate-200 group-hover:text-primary transition-colors leading-snug"
							>
								Building Rules 2019
							</h4>
							<p class="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-1">
								Chapter 4: General Building Requirements
							</p>
						</div>
					</a>
				</div>
			</div>

			<!-- Resources -->
			<div class="p-5 pt-2">
				<div
					class="flex items-center justify-between mb-4 mt-2 pt-4 border-t border-slate-100 dark:border-slate-800"
				>
					<h3 class="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wide">
						Resources
					</h3>
				</div>
				<div class="flex flex-col gap-3">
					<a
						class="flex items-center gap-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-primary/30 hover:bg-primary/5 transition-all group"
						href="javascript:void(0)"
					>
						<div
							class="size-10 rounded-lg bg-red-100 dark:bg-red-900/30 flex items-center justify-center text-red-600 dark:text-red-400 shrink-0"
						>
							<span class="material-symbols-outlined">picture_as_pdf</span>
						</div>
						<div class="flex-1">
							<h4
								class="text-sm font-semibold text-slate-800 dark:text-slate-200 group-hover:text-primary transition-colors"
							>
								Master Plan 2040
							</h4>
							<p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">PDF • 12.5 MB</p>
						</div>
						<span class="material-symbols-outlined text-slate-400 group-hover:text-primary"
							>download</span
						>
					</a>
				</div>
			</div>
		</div>
	</aside>
{/if}

<!-- Map Controls (Zoom / Layers) -->
<div class="absolute bottom-8 right-8 z-30 flex flex-col gap-2 pointer-events-none">
	<div
		class="bg-white dark:bg-slate-900 rounded-lg shadow-md border border-gray-100 dark:border-slate-800 overflow-hidden flex flex-col pointer-events-auto"
	>
		<button
			class="p-2 hover:bg-gray-50 dark:hover:bg-slate-800 text-gray-700 dark:text-slate-200 border-b border-gray-100 dark:border-slate-800 flex items-center justify-center w-10 h-10 transition-colors"
			title="Zoom In"
		>
			<span class="material-symbols-outlined">add</span>
		</button>
		<button
			class="p-2 hover:bg-gray-50 dark:hover:bg-slate-800 text-gray-700 dark:text-slate-200 flex items-center justify-center w-10 h-10 transition-colors"
			title="Zoom Out"
		>
			<span class="material-symbols-outlined">remove</span>
		</button>
	</div>
	<button
		class="bg-white dark:bg-slate-900 p-2 rounded-lg shadow-md border border-gray-100 dark:border-slate-800 hover:bg-gray-50 dark:hover:bg-slate-800 text-gray-700 dark:text-slate-200 flex items-center justify-center w-10 h-10 group relative pointer-events-auto transition-colors"
		title="Layers"
	>
		<span class="material-symbols-outlined">layers</span>
		<!-- Tooltip -->
		<span
			class="absolute right-full mr-2 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrappointer-events-none"
			>Map Layers</span
		>
	</button>
	<button
		class="bg-white dark:bg-slate-900 p-2 rounded-lg shadow-md border border-gray-100 dark:border-slate-800 hover:bg-gray-50 dark:hover:bg-slate-800 text-gray-700 dark:text-slate-200 flex items-center justify-center w-10 h-10 group relative pointer-events-auto transition-colors"
		title="My Location"
	>
		<span class="material-symbols-outlined">my_location</span>
	</button>
</div>

<!-- Legend Overlay -->
<div class="absolute bottom-4 left-4 z-20 pointer-events-none">
	<div
		class="text-[10px] text-slate-500 dark:text-slate-400 bg-white/80 dark:bg-slate-900/80 px-2 py-1 rounded backdrop-blur-sm pointer-events-auto border border-slate-200 dark:border-slate-800"
	>
		© OpenStreetMap contributors | GIS Data 2024
	</div>
</div>
