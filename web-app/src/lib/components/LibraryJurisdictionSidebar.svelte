<script>
	let activeTab = 'states';

	const statesData = [
		{
			name: 'Andhra Pradesh',
			open: true,
			rules: [
				'State Building Rules / Model Bye-laws',
				'Municipal Corporation / Development Authority DCRs',
				'Town & Country Planning Acts',
				'State Fire Service Rules',
				'Pollution Control Board Consents',
				'Electricity Board Clearances',
				'Coastal / CRZ Overlays',
				'Airport NOC (AAI/DGCA)'
			]
		},
		{
			name: 'Arunachal Pradesh',
			rules: [
				'State Building Bye-laws',
				'Hill / Forest Protections',
				'Town Planning Rules',
				'Fire, Environment, Electricity',
				'Defence & Special Land-use'
			]
		},
		{
			name: 'Assam',
			rules: [
				'SBR / Municipal DCRs',
				'State Town & Country Planning',
				'River-floodplain / Erosion Overlays',
				'State Pollution & Environment',
				'Airport / Defence Overlays'
			]
		},
		{
			name: 'Bihar',
			rules: [
				'SBR / Municipal DCRs',
				'Master Plan & Land-use Zoning',
				'Floodplain / River Safety',
				'Fire & Environment Regs',
				'Electricity & Telecom ROW'
			]
		},
		{
			name: 'Chhattisgarh',
			rules: [
				'SBR / Municipal DCRs',
				'Industrial Zone & Mining Overlays',
				'Forest / Environmental Restrictions',
				'Fire & Pollution Controls'
			]
		},
		{
			name: 'Goa',
			rules: [
				'SBR / Corporation / Municipal DCRs',
				'CRZ Regulations',
				'Coastal Zone Management Authority',
				'Tourism / Speciality Use Rules',
				'Fire, Environment, Electricity'
			]
		},
		{
			name: 'Gujarat',
			rules: [
				'SBR / DCRs (Ahmedabad etc.)',
				'Industrial & Port Zone Overlays',
				'CRZ (Coastal Districts)',
				'Fire & NBC-based Safety',
				'Special Economic Zone Rules'
			]
		},
		{
			name: 'Haryana',
			rules: [
				'SBR / Development Authority DCRs',
				'Master Plan / Development Plans',
				'Airport & Defence Overlays',
				'Fire, Environment, Electricity'
			]
		},
		{
			name: 'Himachal Pradesh',
			rules: [
				'Hill-area Construction Controls',
				'SBR / Municipal Rules',
				'Forest & Environment Fragile Zones',
				'Disaster-resilience / Seismic Overlays'
			]
		},
		{
			name: 'Jharkhand',
			rules: [
				'SBR / Municipal DCRs',
				'Mining / Industrial Overlays',
				'Forest & Environment Permissions'
			]
		},
		{
			name: 'Karnataka',
			rules: [
				'State Building Rules / BDA DCRs',
				'Urban Local Body DCRs',
				'CRZ (Karwar, Mangaluru)',
				'Fire & KSPCB Rules',
				'Airport NOC'
			]
		},
		{
			name: 'Kerala',
			rules: [
				'Panchayat Building Rules (KPBR)',
				'Municipality Building Rules (KMBR)',
				'District / Local Development Plans',
				'CRZ (Coastal/Backwaters)',
				'State Fire, Environment, KSEB',
				'Airport / DGCA Overlays'
			]
		},
		{
			name: 'Madhya Pradesh',
			rules: [
				'SBR / Municipal DCRs',
				'Forest / Protected Area Overlays',
				'Fire & Environment Clearances'
			]
		},
		{
			name: 'Maharashtra',
			rules: [
				'SBR / Mumbai / Pune / ULB DCRs',
				'Coastal (Konkan) CRZ Overlays',
				'Fire, Environment, Electricity',
				'Special Heritage & Planning Controls'
			]
		},
		{
			name: 'Manipur',
			rules: ['SBR / Local Planning Rules', 'Hill & Tribal Area Controls', 'Environment / Forest']
		},
		{
			name: 'Meghalaya',
			rules: ['SBR / Town Planning', 'Hill Slope Controls', 'Forest / Tribal Protections']
		},
		{
			name: 'Mizoram',
			rules: ['SBR / Local Authority Rules', 'Hill Protections', 'Environment']
		},
		{
			name: 'Nagaland',
			rules: ['SBR / Town Planning', 'Tribal Governance Overlays']
		},
		{
			name: 'Odisha',
			rules: [
				'SBR / Municipal DCRs',
				'Coastal & Cyclone-resilience',
				'Pollution Control Board & Fire Rules'
			]
		},
		{
			name: 'Punjab',
			rules: [
				'SBR / Municipal DCRs',
				'Master Plan',
				'Defence / Airport Overlays',
				'Fire & Environment'
			]
		},
		{
			name: 'Rajasthan',
			rules: [
				'SBR / Municipal DCRs',
				'Heritage / Archaeological Overlays',
				'Fire & Environment Rules'
			]
		},
		{
			name: 'Sikkim',
			rules: ['Hill & Seismic Protections', 'SBR / Local Rules', 'Environment Clearances']
		},
		{
			name: 'Tamil Nadu',
			rules: [
				'SBR / Chennai & Municipal DCRs',
				'Extensive CRZ Zones',
				'Fire, Pollution, Electricity'
			]
		},
		{
			name: 'Telangana',
			rules: ['SBR / GHMC DCRs', 'Fire & Environment Rules', 'Airport / Defence Overlays']
		},
		{
			name: 'Tripura',
			rules: ['SBR / Local Authority Rules', 'Hill / Forest Overlays', 'Environment']
		},
		{
			name: 'Uttar Pradesh',
			rules: ['SBR / Luckow, Noida DCRs', 'River & Floodplain Overlays', 'Fire & Environment']
		},
		{
			name: 'Uttarakhand',
			rules: [
				'Hill & Seismic / Landslide Resilience',
				'SBR / Municipal Rules',
				'Forest & Environment'
			]
		},
		{
			name: 'West Bengal',
			rules: ['SBR / Kolkata & ULB DCRs', 'River / Coastal Overlays', 'Fire & Pollution Controls']
		}
	];
</script>

<aside
	class="w-72 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 overflow-y-auto flex flex-col"
>
	<div class="px-6 pt-6 pb-2">
		<h1 class="text-slate-900 dark:text-white text-2xl font-bold mb-6">Library</h1>
	</div>

	<!-- Toggle Tabs -->
	<div class="flex w-full border-b border-slate-200 dark:border-slate-800">
		<button
			class="flex-1 pb-3 pt-2 text-sm transition-colors text-center relative border-b-2 {activeTab ===
			'states'
				? 'font-semibold text-primary border-primary'
				: 'font-medium text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 border-transparent'}"
			on:click={() => (activeTab = 'states')}
		>
			States
		</button>
		<button
			class="flex-1 pb-3 pt-2 text-sm transition-colors text-center border-b-2 {activeTab ===
			'other'
				? 'font-semibold text-primary border-primary'
				: 'font-medium text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 border-transparent'}"
			on:click={() => (activeTab = 'other')}
		>
			General
		</button>
	</div>

	<div class="flex-1 overflow-y-auto px-6 py-6">
		{#if activeTab === 'states'}
			<!-- States Section -->
			<div class="space-y-1">
				{#each statesData as state}
					<details class="group" open={state.open}>
						<summary
							class="flex cursor-pointer items-center justify-between gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors list-none select-none"
						>
							<div class="flex items-center gap-3">
								<span
									class="material-symbols-outlined {state.open
										? 'text-primary'
										: 'text-slate-400 group-hover:text-slate-500 dark:group-hover:text-slate-300'}"
									>location_on</span
								>
								<span class="text-sm font-medium">{state.name}</span>
							</div>
							<span
								class="material-symbols-outlined text-slate-400 group-open:rotate-180 transition-transform text-lg"
								>expand_more</span
							>
						</summary>
						<div
							class="mt-1 ml-9 flex flex-col gap-1 border-l border-slate-100 dark:border-slate-800 pl-2"
						>
							{#each state.rules as rule}
								<a
									class="px-3 py-2 text-xs text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded-md block transition-colors"
									href="javascript:void(0)">{rule}</a
								>
							{/each}
						</div>
					</details>
				{/each}
			</div>
		{:else}
			<!-- Other Jurisdictions Section -->
			<div class="space-y-1">
				<a
					class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors"
					href="javascript:void(0)"
				>
					<span class="material-symbols-outlined text-slate-400">menu_book</span>
					<span class="text-sm font-medium">National Building Code</span>
				</a>
				<a
					class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors"
					href="javascript:void(0)"
				>
					<span class="material-symbols-outlined text-slate-400">local_fire_department</span>
					<span class="text-sm font-medium">Fire Safety Norms</span>
				</a>
				<a
					class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-colors"
					href="javascript:void(0)"
				>
					<span class="material-symbols-outlined text-slate-400">history</span>
					<span class="text-sm font-medium">Recent Updates</span>
				</a>
			</div>
		{/if}
	</div>
</aside>
