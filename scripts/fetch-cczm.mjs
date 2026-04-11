#!/usr/bin/env node
/**
 * Fetch CCZM grid data for all 4 Kerala airports and save as GeoJSON.
 * Run: node scripts/fetch-cczm.mjs
 */

const AIRPORTS = [
	{ id: 'cial',              layerId: 196, name: 'CIAL (Kochi)' },
	{ id: 'kannur',            layerId: 174, name: 'Kannur International' },
	{ id: 'calicut',           layerId: 147, name: 'Calicut (Kozhikode)' },
	{ id: 'thiruvananthapuram',layerId: 129, name: 'Thiruvananthapuram' }
];

const BASE = 'https://nocas.aai.aero/server/rest/services/NOCAS/CCZM_Zone43/MapServer';
const OUT_DIR = new URL('../web-app/static/data/', import.meta.url).pathname;

import { writeFileSync, mkdirSync } from 'fs';

async function fetchAll(layerId) {
	let allFeatures = [];
	let offset = 0;
	const limit = 500;

	while (true) {
		const params = new URLSearchParams({
			f: 'json',
			where: '1=1',
			outFields: 'GRIDNAME,PERMISSIBLE_HEIGHT,AIRPORTNAME',
			returnGeometry: 'true',
			outSR: '4326',
			resultOffset: offset,
			resultRecordCount: limit
		});

		console.log(`  Fetching offset ${offset}...`);
		const res = await fetch(`${BASE}/${layerId}/query?${params}`);
		const data = await res.json();

		if (!data.features || data.features.length === 0) break;
		allFeatures = allFeatures.concat(data.features);

		if (!data.exceededTransferLimit) break;
		offset += limit;
	}

	return allFeatures;
}

function toGeojson(features) {
	return {
		type: 'FeatureCollection',
		features: features.map((f) => {
			const coords = f.geometry.rings.map((ring) =>
				ring.map(([lon, lat]) => [lon, lat])
			);
			return {
				type: 'Feature',
				properties: {
					grid: f.attributes.GRIDNAME,
					height: f.attributes.PERMISSIBLE_HEIGHT,
					airport: f.attributes.AIRPORTNAME
				},
				geometry: {
					type: 'Polygon',
					coordinates: coords
				}
			};
		})
	};
}

mkdirSync(OUT_DIR, { recursive: true });

for (const airport of AIRPORTS) {
	console.log(`\nFetching ${airport.name} (layer ${airport.layerId})...`);
	try {
		const features = await fetchAll(airport.layerId);
		const geojson = toGeojson(features);
		const path = `${OUT_DIR}cczm_${airport.id}.geojson`;
		writeFileSync(path, JSON.stringify(geojson));
		console.log(`  ✓ Saved ${features.length} features → ${path}`);
	} catch (e) {
		console.error(`  ✗ Failed: ${e.message}`);
	}
}

console.log('\nDone.');
