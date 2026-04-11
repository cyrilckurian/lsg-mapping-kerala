/**
 * Server-side proxy for AAI NOCAS CCZM API.
 * Avoids CORS issues and keeps the API request server-side.
 *
 * GET /api/cczm?layerId=196&lat=10.15&lon=76.40
 * Returns: { feature: { GRIDNAME, PERMISSIBLE_HEIGHT, AIRPORTNAME } | null }
 */

const NOCAS_BASE = 'https://nocas.aai.aero/server/rest/services/NOCAS/CCZM_Zone43/MapServer';

export async function GET({ url }) {
	const layerId = url.searchParams.get('layerId');
	const lat = url.searchParams.get('lat');
	const lon = url.searchParams.get('lon');

	if (!layerId || !lat || !lon) {
		return new Response(JSON.stringify({ error: 'Missing parameters' }), { status: 400 });
	}

	// Build a small bounding-box geometry around the point (roughly 10m radius)
	const delta = 0.0001;
	const geometry = JSON.stringify({
		xmin: parseFloat(lon) - delta,
		ymin: parseFloat(lat) - delta,
		xmax: parseFloat(lon) + delta,
		ymax: parseFloat(lat) + delta,
		spatialReference: { wkid: 4326 }
	});

	const params = new URLSearchParams({
		f: 'json',
		geometry,
		geometryType: 'esriGeometryEnvelope',
		spatialRel: 'esriSpatialRelIntersects',
		outFields: 'GRIDNAME,PERMISSIBLE_HEIGHT,AIRPORTNAME',
		returnGeometry: 'false',
		inSR: '4326',
		outSR: '4326'
	});

	const nocasUrl = `${NOCAS_BASE}/${layerId}/query?${params}`;

	try {
		const res = await fetch(nocasUrl, {
			headers: { 'User-Agent': 'Kerala-Map/1.0' },
			signal: AbortSignal.timeout(8000)
		});

		if (!res.ok) {
			return new Response(JSON.stringify({ feature: null, error: 'NOCAS API error' }), {
				status: 200
			});
		}

		const data = await res.json();

		if (data.features && data.features.length > 0) {
			// Return the feature with the lowest (most restrictive) height if there are multiple
			const sorted = data.features.sort(
				(a, b) => a.attributes.PERMISSIBLE_HEIGHT - b.attributes.PERMISSIBLE_HEIGHT
			);
			return new Response(
				JSON.stringify({ feature: sorted[0].attributes }),
				{
					status: 200,
					headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=3600' }
				}
			);
		}

		return new Response(JSON.stringify({ feature: null }), { status: 200 });
	} catch (e) {
		console.error('NOCAS proxy error:', e);
		return new Response(JSON.stringify({ feature: null, error: e.message }), { status: 200 });
	}
}
