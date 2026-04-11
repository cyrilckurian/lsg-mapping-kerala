/**
 * Civil Communication Zone Mapping (CCZM) Utility
 * Queries the AAI NOCAS API (via our proxy) for permissible building heights
 * near Kerala airports.
 */

// Aerodrome Reference Points (ARP) for Kerala airports
export const KERALA_AIRPORTS = [
	{
		id: 'cial',
		name: 'CIAL (Kochi)',
		iata: 'COK',
		layerId: 196,
		arp: { lat: 10.1520, lon: 76.4019 }
	},
	{
		id: 'kannur',
		name: 'Kannur International',
		iata: 'CNN',
		layerId: 174,
		arp: { lat: 11.9186, lon: 75.5477 }
	},
	{
		id: 'calicut',
		name: 'Calicut (Kozhikode)',
		iata: 'CCJ',
		layerId: 147,
		arp: { lat: 11.1368, lon: 75.9553 }
	},
	{
		id: 'thiruvananthapuram',
		name: 'Thiruvananthapuram',
		iata: 'TRV',
		layerId: 129,
		arp: { lat: 8.4821, lon: 76.9201 }
	}
];

/**
 * Haversine distance between two lat/lon points in kilometres.
 */
export function haversineKm(lat1, lon1, lat2, lon2) {
	const R = 6371;
	const dLat = toRad(lat2 - lat1);
	const dLon = toRad(lon2 - lon1);
	const a =
		Math.sin(dLat / 2) ** 2 +
		Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
	return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function toRad(deg) {
	return (deg * Math.PI) / 180;
}

/**
 * Returns airports sorted by distance to the given point, with distanceKm attached.
 */
export function nearestAirports(lat, lon) {
	return KERALA_AIRPORTS.map((a) => ({
		...a,
		distanceKm: haversineKm(lat, lon, a.arp.lat, a.arp.lon)
	})).sort((a, b) => a.distanceKm - b.distanceKm);
}

/**
 * Query CCZM data for a point via the server-side proxy.
 * Returns the first matching feature's attributes plus distanceKm, or null.
 */
export async function queryCCZM(lat, lon) {
	const nearby = nearestAirports(lat, lon);

	// Only query airports within 25 km (CCZM outer radius is 20 km)
	const candidates = nearby.filter((a) => a.distanceKm <= 25);
	if (candidates.length === 0) return null;

	// Query the closest airport first; if no hit, try the next
	for (const airport of candidates) {
		try {
			const params = new URLSearchParams({
				layerId: airport.layerId,
				lat,
				lon
			});
			const res = await fetch(`/api/cczm?${params}`);
			if (!res.ok) continue;
			const data = await res.json();

			if (data.feature) {
				return {
					airport: airport.name,
					iata: airport.iata,
					distanceKm: airport.distanceKm,
					grid: data.feature.GRIDNAME,
					permissibleHeight: data.feature.PERMISSIBLE_HEIGHT
				};
			}
		} catch (e) {
			console.warn(`CCZM query failed for ${airport.name}:`, e);
		}
	}

	return null;
}
