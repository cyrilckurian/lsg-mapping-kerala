<script>
	// No props needed for now
</script>

<header
	class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 py-3 shrink-0"
>
	<div class="flex items-center gap-4 text-primary">
		<div class="size-8 flex items-center justify-center bg-primary/10 rounded-lg">
			<span class="material-symbols-outlined text-primary text-2xl">account_balance</span>
		</div>
		<h2 class="text-slate-900 dark:text-white text-lg font-bold leading-tight tracking-tight">
			Architecture Law Library
		</h2>
	</div>
	<div class="flex flex-1 justify-end gap-6 items-center">
		<div class="relative w-full max-w-md hidden md:block">
			<span
				class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xl"
				>search</span
			>
			<input
				class="w-full h-10 pl-10 pr-4 rounded-lg border-none bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary text-sm"
				placeholder="Search laws, sections, or codes..."
			/>
		</div>
		<div class="flex gap-3">
			<button
				class="flex items-center justify-center rounded-lg size-10 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 transition-colors"
			>
				<span class="material-symbols-outlined">notifications</span>
			</button>
		</div>
	</div>
</header>
