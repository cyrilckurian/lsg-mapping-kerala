<script>
	import { onMount } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import { selectedLSG, selectedDistrict, mapReady, markedLocation, theme } from '$lib/store.js';

	let mapContainer;
	let map;
	let userMarker;
	let flyToLock = false;

	const styles = {
		dark: 'https://tiles.basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
		light: 'https://tiles.basemaps.cartocdn.com/gl/positron-gl-style/style.json'
	};

	// React to theme change
	$: if (map && $mapReady) {
		map.setStyle(styles[$theme]);
	}

	// React to markedLocation from paste
	$: if (map && $markedLocation) {
		const { lat, lon } = $markedLocation;
		if (!userMarker) {
			userMarker = new maplibregl.Marker({ color: '#ef4444' }).setLngLat([lon, lat]).addTo(map);
		} else {
			userMarker.setLngLat([lon, lat]);
		}

		map.flyTo({
			center: [lon, lat],
			zoom: 14,
			essential: true
		});

		map.once('moveend', () => {
			const features = map.queryRenderedFeatures(map.project([lon, lat]), {
				layers: ['lsgs-fill']
			});
			if (features.length > 0) {
				selectedLSG.set(features[0].properties);
			}
		});
	}

	$: if (map && !$markedLocation && userMarker) {
		userMarker.remove();
		userMarker = null;
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
			map.flyTo({
				center: [lon, lat],
				zoom: 12,
				essential: true
			});
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
			map.flyTo({
				center: [center[0], center[1]],
				zoom: 9.5,
				essential: true
			});
		}
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
			// Add Sources
			if (!map.getSource('districts')) {
				map.addSource('districts', {
					type: 'geojson',
					data: '/data/kerala_districts.geojson'
				});
			}
			if (!map.getSource('lsgs')) {
				map.addSource('lsgs', {
					type: 'geojson',
					data: '/data/kerala_lsg_final.geojson',
					generateId: true
				});
			}
			if (!map.getSource('mahe')) {
				map.addSource('mahe', {
					type: 'geojson',
					data: '/data/mahe_boundary.geojson'
				});
			}

			// Add Layers
			map.addLayer({
				id: 'districts-line',
				type: 'line',
				source: 'districts',
				paint: {
					'line-color': '#0d9488',
					'line-width': 2.5,
					'line-opacity': 0.5
				}
			});

			map.addLayer({
				id: 'lsgs-fill',
				type: 'fill',
				source: 'lsgs',
				paint: {
					'fill-color': [
						'match',
						['get', 'lsg_type'],
						'municipal corporation',
						'#ec4899',
						'municipality',
						'#f59e0b',
						'gram panchayat',
						'#10b981',
						'#94a3b8'
					],
					'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], 0.6, 0.2]
				}
			});

			map.addLayer({
				id: 'lsgs-line',
				type: 'line',
				source: 'lsgs',
				paint: {
					'line-color':
						$theme === 'dark'
							? [
									'match',
									['get', 'lsg_type'],
									'municipal corporation',
									'#fbcfe8',
									'municipality',
									'#fde68a',
									'gram panchayat',
									'#a7f3d0',
									'#f1f5f9'
								]
							: '#475569', // Dark grey for light mode
					'line-width': 1.5,
					'line-opacity': 0.6
				}
			});

			map.addLayer({
				id: 'lsgs-selection',
				type: 'line',
				source: 'lsgs',
				paint: {
					'line-color': $theme === 'dark' ? '#ffffff' : '#000000',
					'line-width': 2.5,
					'line-opacity': 0.9
				},
				filter: ['==', ['get', 'name'], $selectedLSG?.name || '']
			});

			map.addLayer({
				id: 'mahe-fill',
				type: 'fill',
				source: 'mahe',
				paint: { 'fill-color': '#475569', 'fill-opacity': 0.4 }
			});

			map.addLayer({
				id: 'mahe-line',
				type: 'line',
				source: 'mahe',
				paint: {
					'line-color': '#0ea5e9',
					'line-width': 2,
					'line-dasharray': [2, 1]
				}
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
						lsg_type === 'municipal corporation'
							? '#ec4899'
							: lsg_type === 'municipality'
								? '#f59e0b'
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
</script>

<div bind:this={mapContainer} class="map-container relative">
	<div
		id="map-tooltip"
		class="fixed hidden glass rounded-xl shadow-2xl z-[100] pointer-events-none min-w-[150px] border border-white/10 overflow-hidden backdrop-blur-md"
	></div>
</div>

<style>
	.map-container {
		width: 100%;
		height: 100%;
	}
</style>
