<script>
	import { onMount } from 'svelte';
	import { selectedDistrict, theme } from '$lib/store.js';
	import { Map as MapIcon, ChevronRight } from 'lucide-svelte';

	const districts = [
		'Alappuzha',
		'Ernakulam',
		'Idukki',
		'Kannur',
		'Kasaragod',
		'Kollam',
		'Kottayam',
		'Kozhikode',
		'Malappuram',
		'Palakkad',
		'Pathanamthitta',
		'Thiruvananthapuram',
		'Thrissur',
		'Wayanad'
	];

	function selectDistrict(district) {
		selectedDistrict.set(district);
	}
</script>

<div
	class="fixed bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-2 px-4 py-2 backdrop-blur-xl border border-white/10 rounded-full z-40 max-w-[90vw] overflow-x-auto no-scrollbar shadow-2xl {$theme ===
	'light'
		? 'bg-white/90'
		: 'bg-slate-900/90'}"
>
	<div class="flex items-center gap-2 pr-3 border-r border-white/10 shrink-0">
		<MapIcon class="w-4 h-4 text-brand-secondary" />
		<span class="text-[10px] font-black uppercase text-slate-500 tracking-widest leading-none"
			>Districts</span
		>
	</div>

	<div class="flex items-center gap-1">
		{#each districts as district (district)}
			<button
				on:click={() => selectDistrict(district)}
				class="px-3 py-1.5 rounded-full text-[10px] font-bold transition-all whitespace-nowrap border {selectedDistrict ===
				district
					? 'bg-brand-primary border-brand-primary text-white scale-105 shadow-lg shadow-brand-primary/20'
					: 'bg-white/5 border-white/5 text-slate-400 hover:bg-white/10 hover:text-white'}"
			>
				{district}
			</button>
		{/each}
	</div>
</div>

<style>
	.no-scrollbar::-webkit-scrollbar {
		display: none;
	}
	.no-scrollbar {
		-ms-overflow-style: none;
		scrollbar-width: none;
	}
</style>
