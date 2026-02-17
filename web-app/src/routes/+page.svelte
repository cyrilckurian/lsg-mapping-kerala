<script>
	import Map from '$lib/components/Map.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { mapReady } from '$lib/store.js';
	import { fade } from 'svelte/transition';
</script>

<main class="relative w-full h-screen overflow-hidden bg-slate-950">
	<Map />

	<Sidebar />

	{#if !$mapReady}
		<div
			out:fade
			class="fixed inset-0 z-[100] bg-slate-950 flex flex-col items-center justify-center"
		>
			<div
				class="w-12 h-12 border-4 border-brand-primary border-t-transparent rounded-full animate-spin mb-4"
			></div>
			<p class="text-slate-400 font-medium animate-pulse">Initializing Kerala Officials Map...</p>
		</div>
	{/if}
</main>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
	}
</style>
