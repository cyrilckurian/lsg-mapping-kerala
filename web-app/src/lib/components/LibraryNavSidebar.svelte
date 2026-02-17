<script>
	import { page } from '$app/state';
	import { base } from '$app/paths';
	import { theme } from '$lib/store.js';
</script>

<nav
	class="w-16 h-full bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col items-center py-6 gap-6 z-20 shrink-0"
>
	<!-- Logo / Brand Placeholder -->
	<div
		class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-primary mb-2"
	>
		<span class="material-symbols-outlined text-2xl">gavel</span>
	</div>

	<!-- Navigation Icons -->
	<div class="flex flex-col gap-4 w-full px-2">
		<!-- Library Link -->
		{#if page.url.pathname === '/'}
			<div
				class="w-full aspect-square rounded-lg flex flex-col items-center justify-center bg-primary/10 text-primary transition-colors relative"
			>
				<span class="material-symbols-outlined text-2xl fill-1">menu_book</span>
				<span class="text-[10px] font-medium mt-1">Library</span>
				<!-- Active Indicator -->
				<div
					class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary rounded-r-full"
				></div>
			</div>
		{:else}
			<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
			<a
				href="{base}/"
				data-sveltekit-preload-data="hover"
				class="w-full aspect-square rounded-lg flex flex-col items-center justify-center text-slate-500 hover:bg-slate-50 hover:text-primary dark:text-slate-400 dark:hover:bg-slate-800 transition-colors group"
			>
				<span class="material-symbols-outlined text-2xl group-hover:scale-110 transition-transform"
					>menu_book</span
				>
				<span class="text-[10px] font-medium mt-1">Library</span>
			</a>
		{/if}

		<!-- Map Link -->
		{#if page.url.pathname.startsWith('/map')}
			<div
				class="w-full aspect-square rounded-lg flex flex-col items-center justify-center bg-primary/10 text-primary transition-colors relative"
			>
				<span class="material-symbols-outlined text-2xl fill-1">map</span>
				<span class="text-[10px] font-medium mt-1">Map</span>
				<!-- Active Indicator -->
				<div
					class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary rounded-r-full"
				></div>
			</div>
		{:else}
			<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
			<a
				href="{base}/map"
				data-sveltekit-preload-data="hover"
				class="w-full aspect-square rounded-lg flex flex-col items-center justify-center text-slate-500 hover:bg-slate-50 hover:text-primary dark:text-slate-400 dark:hover:bg-slate-800 transition-colors group"
			>
				<span class="material-symbols-outlined text-2xl group-hover:scale-110 transition-transform"
					>map</span
				>
				<span class="text-[10px] font-medium mt-1">Map</span>
			</a>
		{/if}

		<!-- Settings / Theme Toggle -->
		<button
			on:click={() => theme.update((t) => (t === 'dark' ? 'light' : 'dark'))}
			class="w-full aspect-square rounded-lg flex flex-col items-center justify-center text-slate-500 hover:bg-slate-50 hover:text-primary dark:text-slate-400 dark:hover:bg-slate-800 transition-colors group"
			title="Toggle Theme"
		>
			<span class="material-symbols-outlined text-2xl group-hover:scale-110 transition-transform">
				{$theme === 'dark' ? 'light_mode' : 'dark_mode'}
			</span>
			<span class="text-[10px] font-medium mt-1">{$theme === 'dark' ? 'Light' : 'Dark'}</span>
		</button>
	</div>

	<div class="mt-auto flex flex-col gap-4 w-full px-2">
		<button
			class="w-full aspect-square rounded-lg flex flex-col items-center justify-center text-slate-500 hover:bg-slate-50 hover:text-primary dark:text-slate-400 dark:hover:bg-slate-800 transition-colors"
		>
			<span class="material-symbols-outlined text-2xl">account_circle</span>
		</button>
	</div>
</nav>
