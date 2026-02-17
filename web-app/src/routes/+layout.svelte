<script>
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { theme } from '$lib/store.js';
	import LibraryNavSidebar from '$lib/components/LibraryNavSidebar.svelte';

	let { children } = $props();

	$effect(() => {
		if ($theme === 'dark') {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link
		href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div
	class="flex h-screen w-full overflow-hidden bg-slate-50 dark:bg-slate-900 font-display text-[#111318] dark:text-slate-100"
>
	<LibraryNavSidebar />
	<div class="flex flex-1 flex-col h-full overflow-hidden relative">
		{@render children()}
	</div>
</div>
