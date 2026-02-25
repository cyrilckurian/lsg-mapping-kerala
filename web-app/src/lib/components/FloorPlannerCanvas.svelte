<script>
	let zoom = $state(100);

	function zoomIn() {
		zoom = Math.min(zoom + 10, 200);
	}

	function zoomOut() {
		zoom = Math.max(zoom - 10, 30);
	}

	function fitView() {
		zoom = 100;
	}
</script>

<section
	class="flex-[2] flex flex-col bg-slate-50 dark:bg-slate-950 relative min-w-0 overflow-hidden"
>
	<!-- Canvas Area -->
	<div class="flex-1 overflow-auto p-8 flex items-center justify-center relative">
		<!-- Drafting board -->
		<div
			class="relative bg-white dark:bg-slate-900 shadow-2xl rounded-sm border border-slate-200 dark:border-slate-700 overflow-hidden transition-all duration-300"
			style="width: {8 * zoom}px; height: {6 *
				zoom}px; max-width: 100%; max-height: 100%; background-image: radial-gradient(#e5e7eb 1px, transparent 1px); background-size: 20px 20px;"
		>
			<!-- Site boundary -->
			<div class="absolute inset-0 opacity-40">
				<div
					class="w-full h-full bg-slate-50 dark:bg-slate-900/50 flex items-center justify-center"
				>
					<span
						class="text-slate-300 dark:text-slate-700 font-mono text-sm uppercase tracking-widest"
						>Site Boundary Reference</span
					>
				</div>
			</div>

			<!-- Usable area overlay -->
			<div
				class="absolute border-2 border-dashed border-primary/40 bg-primary/5 rounded-sm flex items-start justify-end p-2"
				style="top: 10%; left: 8%; width: 62%; height: 66%"
			>
				<span class="text-[10px] font-bold text-primary/60 uppercase"
					>Derived Usable Area: 200m²</span
				>
			</div>

			<!-- Room: Master Bed -->
			<div
				class="absolute border border-primary bg-primary/10 cursor-move rounded flex flex-col p-2 shadow-sm hover:shadow-md transition-shadow"
				style="top: 18%; left: 14%; width: 20%; height: 22%"
			>
				<div class="flex justify-between items-start">
					<span class="text-[10px] font-bold text-primary uppercase">Master Bed</span>
					<span class="material-symbols-outlined text-xs text-primary/60">open_with</span>
				</div>
				<span class="mt-auto text-[9px] text-primary/80">4.2m × 3.8m</span>
			</div>

			<!-- Room: Kitchen -->
			<div
				class="absolute border border-primary bg-primary/10 cursor-move rounded flex flex-col p-2 shadow-sm hover:shadow-md transition-shadow"
				style="top: 18%; left: 36%; width: 14%; height: 22%"
			>
				<div class="flex justify-between items-start">
					<span class="text-[10px] font-bold text-primary uppercase">Kitchen</span>
					<span class="material-symbols-outlined text-xs text-primary/60">open_with</span>
				</div>
				<span class="mt-auto text-[9px] text-primary/80">2.8m × 3.8m</span>
			</div>

			<!-- Room: Living Room -->
			<div
				class="absolute border border-primary bg-primary/10 cursor-move rounded flex flex-col p-2 shadow-sm hover:shadow-md transition-shadow"
				style="top: 44%; left: 14%; width: 34%; height: 24%"
			>
				<div class="flex justify-between items-start">
					<span class="text-[10px] font-bold text-primary uppercase">Living Room</span>
					<span class="material-symbols-outlined text-xs text-primary/60">open_with</span>
				</div>
				<span class="mt-auto text-[9px] text-primary/80">7.2m × 4.2m</span>
			</div>

			<!-- Scale & North indicator -->
			<div class="absolute bottom-4 right-6 flex flex-col items-end gap-2 text-slate-400">
				<div class="flex items-center gap-1">
					<span class="text-[10px] font-mono">SCALE 1:100</span>
					<div class="w-12 h-[1px] bg-slate-300"></div>
				</div>
				<div class="flex flex-col items-center">
					<span class="text-[10px] font-bold">N</span>
					<span class="material-symbols-outlined text-xl">navigation</span>
				</div>
			</div>
		</div>

		<!-- Zoom Controls -->
		<div
			class="absolute bottom-6 left-6 flex bg-white dark:bg-slate-800 rounded-lg shadow-lg border border-slate-200 dark:border-slate-700 p-1 gap-1 items-center"
		>
			<button
				onclick={zoomIn}
				class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded text-slate-600 dark:text-slate-300 transition-colors"
				title="Zoom In"
			>
				<span class="material-symbols-outlined text-lg">add</span>
			</button>
			<div class="w-[1px] h-4 bg-slate-200 dark:bg-slate-700"></div>
			<span
				class="text-[11px] font-mono font-bold text-slate-500 dark:text-slate-400 px-1 min-w-[36px] text-center"
				>{zoom}%</span
			>
			<div class="w-[1px] h-4 bg-slate-200 dark:bg-slate-700"></div>
			<button
				onclick={zoomOut}
				class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded text-slate-600 dark:text-slate-300 transition-colors"
				title="Zoom Out"
			>
				<span class="material-symbols-outlined text-lg">remove</span>
			</button>
			<div class="w-[1px] h-4 bg-slate-200 dark:bg-slate-700"></div>
			<button
				onclick={fitView}
				class="px-2 text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase hover:text-primary dark:hover:text-primary transition-colors"
				title="Fit to view"
			>
				Fit
			</button>
		</div>
	</div>

	<!-- Status Bar -->
	<footer
		class="h-8 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 px-4 flex items-center justify-between text-[10px] text-slate-500 dark:text-slate-400 font-mono shrink-0"
	>
		<div class="flex gap-4">
			<span>X: 142.04</span>
			<span>Y: 328.11</span>
			<span>Z: 0.00</span>
		</div>
		<div class="flex gap-4 items-center">
			<span class="flex items-center gap-1">
				<span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
				AI Assistant Online
			</span>
			<span>v2.4.0-Stable</span>
		</div>
	</footer>
</section>
