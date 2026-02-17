<script>
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { theme } from '$lib/store.js';

	let { children } = $props();

	$effect(() => {
		if ($theme === 'dark') {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
	});
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}
