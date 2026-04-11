<script>
	import { onMount } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import { selectedLSG, selectedDistrict, mapReady, markedLocation, theme, cczmInfo } from '$lib/store.js';
	import { queryCCZM } from '$lib/utils/cczm.js';

	let mapContainer;
	let map;
	let userMarker;
	let flyToLock = false;

	// CCZM overlay toggle (hidden by default)
	let showCCZM = false;

	const styles = {
		dark: 'https://tiles.basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
		light: 'https://tiles.basemaps.cartocdn.com/gl/positron-gl-style/style.json'
	};

	// Airport reference points for markers
	const AIRPORTS = [
		{ id: 'cial',              name: 'CIAL (Kochi)',          lat: 10.1520, lon: 76.4019 },
		{ id: 'kannur',            name: 'Kannur International',  lat: 11.9186, lon: 75.5477 },
		{ id: 'calicut',           name: 'Calicut (Kozhikode)',   lat: 11.1368, lon: 75.9553 },
		{ id: 'thiruvananthapuram',name: 'Thiruvananthapuram',    lat:  8.4821, lon: 76.9201 }
	];

	// React to theme change
	$: if (map && $mapReady) {
		map.setStyle(styles[$theme]);
	}

	// React to markedLocation — place marker, fly, query CCZM
	$: if (map && $markedLocation) {
		const { lat, lon } = $markedLocation;
		if (!userMarker) {
			userMarker = new maplibregl.Marker({ color: '#ef4444' }).setLngLat([lon, lat]).addTo(map);
		} else {
			userMarker.setLngLat([lon, lat]);
		}

		map.flyTo({ center: [lon, lat], zoom: 14, essential: true });

		map.once('moveend', () => {
			const features = map.queryRenderedFeatures(map.project([lon, lat]), {
				layers: ['lsgs-fill']
			});
			if (features.length > 0) {
				selectedLSG.set(features[0].properties);
			}
		});

		// Query CCZM data for the marked location
		cczmInfo.set({ loading: true });
		queryCCZM(lat, lon)
			.then((result) => cczmInfo.set(result ? { ...result, loading: false } : { loading: false, noZone: true }))
			.catch(() => cczmInfo.set({ loading: false, error: true }));
	}

	$: if (map && !$markedLocation && userMarker) {
		userMarker.remove();
		userMarker = null;
		cczmInfo.set(null);
	}

	// React to LSG selection
	$: if (map && $selectedLSG) {
		let lat, lon;
		if ($selectedLSG.centroid && Array.isArray($selectedLSG.centroid)) {
			[lon, lat] = $selectedLSG.centroid;
		} else {
			lat = parseFloat($selectedLSG.lat || $selectedLSG.centroid_lat);
			lon = parseFloat($selectedLSG.lon || $selectedLSG.centroid_lon);
		}

		if (lat && lon && !flyToLock) {
			map.flyTo({ center: [lon, lat], zoom: 12, essential: true });
		}
		flyToLock = false;

		if ($mapReady && map.getLayer('lsgs-selection')) {
			map.setFilter('lsgs-selection', ['==', ['get', 'name'], $selectedLSG.name]);
		}
	}

	$: if (map && $mapReady && !$selectedLSG) {
		if (map.getLayer('lsgs-selection')) {
			map.setFilter('lsgs-selection', ['==', ['get', 'name'], '']);
		}
	}

	// React to District selection
	$: if (map && $selectedDistrict) {
		const districtCenters = {
			Alappuzha: [76.33, 9.49],
			Ernakulam: [76.27, 9.98],
			Idukki: [76.99, 9.85],
			Kannur: [75.37, 11.87],
			Kasaragod: [75.0, 12.5],
			Kollam: [76.59, 8.89],
			Kottayam: [76.52, 9.59],
			Kozhikode: [75.78, 11.25],
			Malappuram: [76.07, 11.07],
			Palakkad: [76.65, 10.78],
			Pathanamthitta: [76.79, 9.26],
			Thiruvananthapuram: [76.94, 8.52],
			Thrissur: [76.21, 10.52],
			Wayanad: [76.08, 11.69]
		};
		const center = districtCenters[$selectedDistrict];
		if (center) {
			map.flyTo({ center: [center[0], center[1]], zoom: 9.5, essential: true });
		}
	}

	// Toggle CCZM layers
	$: if (map && $mapReady) {
		const layers = ['cczm-fill', 'cczm-line', 'cczm-labels'];
		layers.forEach((id) => {
			if (map.getLayer(id)) {
				map.setLayoutProperty(id, 'visibility', showCCZM ? 'visible' : 'none');
			}
		});
	}

	onMount(() => {
		map = new maplibregl.Map({
			container: mapContainer,
			style: styles[$theme],
			center: [76.5, 10.5],
			zoom: 7,
			antialias: true
		});

		map.on('style.load', setupLayers);

		function setupLayers() {
			// ── Base Sources ──────────────────────────────────────────────────────
			if (!map.getSource('districts')) {
				map.addSource('districts', { type: 'geojson', data: '/data/kerala_districts.geojson' });
			}
			if (!map.getSource('lsgs')) {
				map.addSource('lsgs', { type: 'geojson', data: '/data/kerala_lsg_final.geojson', generateId: true });
			}
			if (!map.getSource('mahe')) {
				map.addSource('mahe', { type: 'geojson', data: '/data/mahe_boundary.geojson' });
			}

			// ── CCZM Sources (merged virtual source using expression) ─────────────
			// Load all 4 airport CCZM GeoJSON files as separate sources
			const cczmAirports = ['cial', 'kannur', 'calicut', 'thiruvananthapuram'];
			cczmAirports.forEach((id) => {
				if (!map.getSource(`cczm-${id}`)) {
					map.addSource(`cczm-${id}`, {
						type: 'geojson',
						data: `/data/cczm_${id}.geojson`
					});
				}
			});

			// ── Base Layers ───────────────────────────────────────────────────────
			map.addLayer({ id: 'districts-line', type: 'line', source: 'districts',
				paint: { 'line-color': '#0d9488', 'line-width': 2.5, 'line-opacity': 0.5 }
			});

			map.addLayer({ id: 'lsgs-fill', type: 'fill', source: 'lsgs',
				paint: {
					'fill-color': ['match', ['get', 'lsg_type'],
						'municipal corporation', '#ec4899',
						'municipality', '#f59e0b',
						'gram panchayat', '#10b981',
						'#94a3b8'],
					'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], 0.6, 0.2]
				}
			});

			map.addLayer({ id: 'lsgs-line', type: 'line', source: 'lsgs',
				paint: {
					'line-color': $theme === 'dark'
						? ['match', ['get', 'lsg_type'],
							'municipal corporation', '#fbcfe8',
							'municipality', '#fde68a',
							'gram panchayat', '#a7f3d0',
							'#f1f5f9']
						: '#475569',
					'line-width': 1.5,
					'line-opacity': 0.6
				}
			});

			map.addLayer({ id: 'lsgs-selection', type: 'line', source: 'lsgs',
				paint: {
					'line-color': $theme === 'dark' ? '#ffffff' : '#000000',
					'line-width': 2.5,
					'line-opacity': 0.9
				},
				filter: ['==', ['get', 'name'], $selectedLSG?.name || '']
			});

			map.addLayer({ id: 'mahe-fill', type: 'fill', source: 'mahe',
				paint: { 'fill-color': '#475569', 'fill-opacity': 0.4 }
			});
			map.addLayer({ id: 'mahe-line', type: 'line', source: 'mahe',
				paint: { 'line-color': '#0ea5e9', 'line-width': 2, 'line-dasharray': [2, 1] }
			});

			// ── CCZM Overlay Layers (one set per airport, grouped by visibility) ──
			cczmAirports.forEach((airportId) => {
				const src = `cczm-${airportId}`;

				// Height-based colour: green (safe) → yellow → orange → red (restrictive)
				const heightColor = [
					'step', ['get', 'height'],
					'#22c55e',   // < 50m → green
					50,  '#84cc16',
					100, '#eab308',
					150, '#f97316',
					200, '#ef4444'  // ≥ 200m → red
				];

				map.addLayer({
					id: `cczm-fill-${airportId}`, type: 'fill', source: src,
					layout: { visibility: 'none' },
					paint: { 'fill-color': heightColor, 'fill-opacity': 0.22 }
				});

				map.addLayer({
					id: `cczm-line-${airportId}`, type: 'line', source: src,
					layout: { visibility: 'none' },
					paint: { 'line-color': heightColor, 'line-width': 0.8, 'line-opacity': 0.7 }
				});

				map.addLayer({
					id: `cczm-labels-${airportId}`, type: 'symbol', source: src,
					layout: {
						visibility: 'none',
						'text-field': ['concat', ['get', 'grid'], '\n', ['to-string', ['get', 'height']], 'm'],
						'text-size': ['interpolate', ['linear'], ['zoom'], 10, 8, 14, 11],
						'text-font': ['Noto Sans Regular'],
						'text-anchor': 'center',
						'text-justify': 'center',
						'text-allow-overlap': false
					},
					paint: {
						'text-color': $theme === 'dark' ? '#f8fafc' : '#0f172a',
						'text-halo-color': $theme === 'dark' ? '#0f172a' : '#ffffff',
						'text-halo-width': 1.5
					}
				});
			});

			setupInteractions();
			mapReady.set(true);
		}

		function setupInteractions() {
			const tooltip = document.getElementById('map-tooltip');
			let hoveredId = null;

			map.on('mousemove', 'lsgs-fill', (e) => {
				if (e.features.length > 0) {
					if (hoveredId !== null) {
						map.setFeatureState({ source: 'lsgs', id: hoveredId }, { hover: false });
					}
					const feature = e.features[0];
					hoveredId = feature.id;
					map.setFeatureState({ source: 'lsgs', id: hoveredId }, { hover: true });
					map.getCanvas().style.cursor = 'pointer';

					const { name, lsg_type, district } = feature.properties;
					const typeColor =
						lsg_type === 'municipal corporation' ? '#ec4899'
						: lsg_type === 'municipality' ? '#f59e0b'
						: '#10b981';

					tooltip.innerHTML = `
            <div class="px-3 py-2">
              <div class="flex items-center gap-2 mb-1">
                <span class="w-2 h-2 rounded-full" style="background-color: ${typeColor}"></span>
                <span class="text-[10px] font-black uppercase tracking-widest ${$theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}">${lsg_type}</span>
              </div>
              <div class="text-sm font-bold ${$theme === 'dark' ? 'text-white' : 'text-slate-900'}">${name}</div>
              <div class="text-[10px] ${$theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} font-medium">${district} District</div>
            </div>
          `;
					tooltip.style.display = 'block';
					tooltip.style.left = e.point.x + 15 + 'px';
					tooltip.style.top = e.point.y + 15 + 'px';
				}
			});

			map.on('mouseleave', 'lsgs-fill', () => {
				if (hoveredId !== null) {
					map.setFeatureState({ source: 'lsgs', id: hoveredId }, { hover: false });
				}
				hoveredId = null;
				map.getCanvas().style.cursor = '';
				tooltip.style.display = 'none';
			});

			map.on('click', 'lsgs-fill', (e) => {
				const feature = e.features[0];
				if (feature) {
					flyToLock = true;
					selectedLSG.set(feature.properties);
				}
			});
		}

		return () => {
			if (map) map.remove();
		};
	});

	function toggleCCZM() {
		showCCZM = !showCCZM;
		const airports = ['cial', 'kannur', 'calicut', 'thiruvananthapuram'];
		airports.forEach((id) => {
			['cczm-fill', 'cczm-line', 'cczm-labels'].forEach((prefix) => {
				const layerId = `${prefix}-${id}`;
				if (map && map.getLayer(layerId)) {
					map.setLayoutProperty(layerId, 'visibility', showCCZM ? 'visible' : 'none');
				}
			});
		});

		// Zoom out to see all airports if enabling
		if (showCCZM) {
			map.flyTo({ center: [76.5, 10.5], zoom: 7, essential: true });
		}
	}
</script>

<div bind:this={mapContainer} class="map-container relative">
	<div
		id="map-tooltip"
		class="fixed hidden backdrop-blur-md rounded-xl shadow-2xl z-[100] pointer-events-none min-w-[150px] border border-white/10 overflow-hidden {$theme ===
		'light'
			? 'bg-white/90'
			: 'bg-slate-900/90'}"
	></div>
</div>

<!-- CCZM Toggle Button -->
<button
	on:click={toggleCCZM}
	title={showCCZM ? 'Hide Airport Zones' : 'Show Airport Zones (CCZM)'}
	class="absolute bottom-[10.5rem] right-8 z-30 w-10 h-10 rounded-lg shadow-md border flex items-center justify-center transition-all
		{showCCZM
		? 'bg-amber-500 border-amber-400 text-white shadow-amber-200 dark:shadow-amber-900/40'
		: 'bg-white dark:bg-slate-900 border-gray-100 dark:border-slate-800 text-gray-700 dark:text-slate-200 hover:bg-gray-50 dark:hover:bg-slate-800'}"
>
	<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
		<path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.82a19.79 19.79 0 01-3.07-8.63A2 2 0 012 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 9a16 16 0 006.86 6.86l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
		<path d="M16 2a6 6 0 010 9"/>
		<path d="M19.5 2A10.5 10.5 0 0119.5 19.5"/>
	</svg>
</button>

<!-- CCZM Legend (shown when overlay is active) -->
{#if showCCZM}
	<div class="absolute bottom-36 right-20 z-30 pointer-events-none">
		<div class="bg-white/90 dark:bg-slate-900/90 backdrop-blur-sm rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 p-3 text-xs w-44">
			<p class="font-bold text-slate-700 dark:text-slate-200 mb-2 text-[10px] uppercase tracking-wider">Airport Zone Height</p>
			<div class="flex flex-col gap-1">
				{#each [
					{ color: '#22c55e', label: '< 50 m' },
					{ color: '#84cc16', label: '50 – 99 m' },
					{ color: '#eab308', label: '100 – 149 m' },
					{ color: '#f97316', label: '150 – 199 m' },
					{ color: '#ef4444', label: '≥ 200 m' }
				] as item}
					<div class="flex items-center gap-2">
						<span class="w-4 h-3 rounded-sm shrink-0" style="background:{item.color}; opacity:0.8"></span>
						<span class="text-slate-600 dark:text-slate-300">{item.label}</span>
					</div>
				{/each}
			</div>
			<p class="text-[9px] text-slate-400 dark:text-slate-500 mt-2 leading-tight">Max permissible building height per AAI NOCAS CCZM</p>
		</div>
	</div>
{/if}

<style>
	.map-container {
		width: 100%;
		height: 100%;
	}
</style>
