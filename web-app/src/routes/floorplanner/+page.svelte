<script>
	import FloorPlannerSidebar from '$lib/components/FloorPlannerSidebar.svelte';
	import FloorPlannerCanvas from '$lib/components/FloorPlannerCanvas.svelte';
	import LibraryChatPanel from '$lib/components/LibraryChatPanel.svelte';
</script>

<div class="flex h-screen flex-col bg-slate-50 dark:bg-slate-950 overflow-hidden font-display">
	<main class="flex flex-1 overflow-hidden">
		<!-- Left: Plan History Sidebar -->
		<FloorPlannerSidebar />

		<!-- Center: Canvas Workspace -->
		<FloorPlannerCanvas />

		<!-- Right: AI Chat Panel (shared component) -->
		<LibraryChatPanel />
	</main>
</div>
