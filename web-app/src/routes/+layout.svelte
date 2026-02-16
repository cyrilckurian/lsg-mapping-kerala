<script>
	import "./layout.css";
	import favicon from "$lib/assets/favicon.svg";
	import { theme } from "$lib/store.js";

	let { children } = $props();

	$effect(() => {
		if ($theme === "light") {
			document.documentElement.classList.add("light");
		} else {
			document.documentElement.classList.remove("light");
		}
	});
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}
