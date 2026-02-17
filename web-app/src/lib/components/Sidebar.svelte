<script>
	import { onMount } from 'svelte';
	import { selectedLSG, searchQuery } from '$lib/store.js';
	import {
		Search,
		MapPin,
		Phone,
		Mail,
		Globe,
		User,
		Landmark,
		ChevronLeft,
		X,
		Link,
		Sun,
		Moon
	} from 'lucide-svelte';
	import { fade, slide } from 'svelte/transition';
	import { markedLocation, markerLink, theme } from '$lib/store.js';
	import { parseGoogleMapsLink } from '$lib/utils/googleMaps.js';

	let searchIndex = [];
	let filteredResults = [];
	let isSearching = false;

	onMount(async () => {
		const res = await fetch('/data/search_index.json');
		searchIndex = await res.json();
	});

	async function handleLinkInput(e) {
		const url = e.target.value;
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

	function clearLink() {
		markerLink.set('');
		markedLocation.set(null);
	}

	$: {
		if ($searchQuery.length > 1) {
			const q = $searchQuery.toLowerCase();
			filteredResults = searchIndex
				.filter(
					(item) =>
						item.name.toLowerCase().includes(q) || (item.name_ml && item.name_ml.includes(q))
				)
				.slice(0, 10);
			isSearching = true;
		} else {
			filteredResults = [];
			isSearching = false;
		}
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
		searchQuery.set('');
	}

	function toggleTheme() {
		theme.update((t) => (t === 'dark' ? 'light' : 'dark'));
	}
</script>

<aside
	class="sidebar fixed top-4 left-4 w-96 h-[calc(100vh-32px)] backdrop-blur-xl border border-white/10 rounded-2xl z-50 flex flex-col overflow-hidden shadow-2xl {$theme ===
	'light'
		? 'bg-white/90'
		: 'bg-slate-900/90'}"
>
	<div class="p-6 border-b border-white/10 flex items-center justify-between">
		<div class="flex items-center gap-3">
			<div class="bg-brand-primary p-2.5 rounded-xl shadow-lg shadow-brand-primary/20">
				<Landmark class="text-white w-5 h-5" />
			</div>
			<h1
				class="text-xl font-black tracking-tight {$theme === 'dark'
					? 'bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent'
					: 'text-slate-900'}"
			>
				Jurisdiction
			</h1>
		</div>

		<button
			on:click={toggleTheme}
			class="p-2 rounded-xl hover:bg-white/10 transition-all group"
			title="Toggle {$theme === 'dark' ? 'Light' : 'Dark'} Mode"
		>
			{#if $theme === 'dark'}
				<Sun class="w-5 h-5 text-yellow-400 group-hover:scale-110 transition-transform" />
			{:else}
				<Moon class="w-5 h-5 text-slate-600 group-hover:scale-110 transition-transform" />
			{/if}
		</button>
	</div>

	<div class="p-6 space-y-4">
		<!-- Search Input -->
		<div class="relative group">
			<Search
				class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted group-focus-within:text-brand-primary transition-colors"
			/>
			<input
				type="text"
				bind:value={$searchQuery}
				placeholder="Search for LSG (e.g. Kochi, Vorkady)..."
				class="w-full border border-white/10 rounded-xl py-3 pl-10 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all {$theme ===
				'light'
					? 'bg-white placeholder:text-slate-400'
					: 'bg-slate-800/40 placeholder:text-slate-600'}"
			/>
			{#if $searchQuery}
				<button
					on:click={clearSearch}
					class="absolute right-3 top-1/2 -translate-y-1/2 p-1 hover:bg-white/10 rounded-full transition-colors"
				>
					<X class="w-3.5 h-3.5 text-muted" />
				</button>
			{/if}

			<!-- Search Results Dropdown -->
			{#if isSearching && filteredResults.length > 0}
				<div
					in:fade={{ duration: 150 }}
					class="absolute top-full left-0 w-full mt-2 border rounded-xl shadow-2xl overflow-hidden z-[60] {$theme ===
					'light'
						? 'bg-white border-slate-200'
						: 'bg-slate-900 border-white/10'}"
				>
					<ul class="divide-y {$theme === 'light' ? 'divide-slate-100' : 'divide-white/5'}">
						{#each filteredResults as item (item.name)}
							<li>
								<button
									on:click={() => selectResult(item)}
									class="w-full text-left p-4 hover:bg-brand-primary/10 transition-colors flex flex-col gap-0.5"
								>
									<span
										class="text-sm font-bold leading-none {$theme === 'light'
											? 'text-slate-900'
											: 'text-white'}">{item.name}</span
									>
									{#if item.name_ml && false}
										<span
											class="text-xs font-medium {$theme === 'light'
												? 'text-slate-500'
												: 'text-slate-400'}">{item.name_ml}</span
										>
									{/if}
									<div class="flex items-center gap-2 mt-1">
										<span class="text-[10px] text-brand-secondary font-bold uppercase"
											>{item.lsg_type || 'LSG'}</span
										>
										<span class="text-[10px] text-slate-500">•</span>
										<span class="text-[10px] text-slate-500">{item.district}</span>
									</div>
								</button>
							</li>
						{/each}
					</ul>
				</div>
			{/if}
		</div>

		<div class="flex items-center gap-4 px-2">
			<div class="h-[1px] flex-1 bg-white/10"></div>
			<span class="text-[10px] font-black text-slate-500 tracking-widest">OR</span>
			<div class="h-[1px] flex-1 bg-white/10"></div>
		</div>

		<!-- Link Input -->
		<div class="relative group">
			<Link
				class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted group-focus-within:text-brand-primary transition-colors"
			/>
			<input
				type="text"
				value={$markerLink}
				on:input={handleLinkInput}
				placeholder="Paste Google Maps Link..."
				class="w-full border border-white/10 rounded-xl py-3 pl-10 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all {$theme ===
				'light'
					? 'bg-white placeholder:text-slate-400'
					: 'bg-slate-800/40 placeholder:text-slate-600'}"
			/>
			{#if $markerLink}
				<button
					on:click={clearLink}
					class="absolute right-3 top-1/2 -translate-y-1/2 p-1 hover:bg-white/10 rounded-full transition-colors"
				>
					<X class="w-3.5 h-3.5 text-muted" />
				</button>
			{/if}
		</div>
	</div>

	<div class="flex-1 overflow-y-auto custom-scrollbar">
		{#if $selectedLSG}
			<div in:fade={{ duration: 200 }} class="p-6">
				<button
					on:click={clearSelection}
					class="flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-brand-secondary mb-6 transition-colors uppercase tracking-wider"
				>
					<ChevronLeft class="w-4 h-4" /> Back to Explore
				</button>

				<div class="mb-10 relative">
					<div
						class="absolute -left-6 top-1/2 -translate-y-1/2 w-1.5 h-16 rounded-r-full shadow-[0_0_15px_rgba(16,185,129,0.5)]"
						style="background-color: {$selectedLSG.lsg_type === 'municipal corporation'
							? '#ec4899'
							: $selectedLSG.lsg_type === 'municipality'
								? '#f59e0b'
								: '#10b981'}"
					></div>
					<span
						class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black uppercase tracking-widest mb-3 border"
						style="
              background-color: {$selectedLSG.lsg_type === 'municipal corporation'
							? 'rgba(236, 72, 153, 0.1)'
							: $selectedLSG.lsg_type === 'municipality'
								? 'rgba(245, 158, 11, 0.1)'
								: 'rgba(16, 185, 129, 0.1)'};
              color: {$selectedLSG.lsg_type === 'municipal corporation'
							? '#ec4899'
							: $selectedLSG.lsg_type === 'municipality'
								? '#f59e0b'
								: '#10b981'};
              border-color: {$selectedLSG.lsg_type === 'corporation'
							? 'rgba(236, 72, 153, 0.2)'
							: $selectedLSG.lsg_type === 'municipality'
								? 'rgba(245, 158, 11, 0.2)'
								: 'rgba(16, 185, 129, 0.2)'};
            "
					>
						{$selectedLSG.lsg_type || 'Local Self Government'}
					</span>
					<h2 class="text-3xl font-black leading-none mb-2 tracking-tight">
						{$selectedLSG.name || $selectedLSG.lsg_name}
					</h2>
					<p class="text-xl text-slate-400 font-medium mb-4">
						{$selectedLSG.name_ml || $selectedLSG.lsg_name_ml || ''}
					</p>

					<div class="flex items-center gap-2 text-sm text-slate-500 font-medium italic">
						<MapPin class="w-4 h-4 text-brand-secondary" />
						<span>{$selectedLSG.district || 'Kerala'} District</span>
					</div>
				</div>
			</div>
		{:else}
			<div
				in:fade={{ duration: 200 }}
				class="p-8 flex flex-col items-center justify-center h-full text-center"
			>
				<p
					class="text-sm font-medium px-4 {$theme === 'dark' ? 'text-slate-500' : 'text-slate-600'}"
				>
					Search by name or select a Local Self Government (LSG) on the map.
				</p>
			</div>
		{/if}
	</div>
</aside>

<style>
	.sidebar {
		height: calc(100vh - 32px);
	}
</style>
