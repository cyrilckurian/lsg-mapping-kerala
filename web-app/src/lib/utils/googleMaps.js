/**
 * Utility to parse Google Maps URLs for coordinates.
 * Handles:
 * 1. Coordinates: https://www.google.com/maps/place/9.9312,76.2673/...
 * 2. Search: https://www.google.com/maps/search/9.9312,76.2673/...
 * 3. @ format: https://www.google.com/maps/@9.9312,76.2673,15z/...
 */
export function parseGoogleMapsLink(url) {
	try {
		const decodedUrl = decodeURIComponent(url);

		// Pattern 1: /place/lat,lng or /search/lat,lng
		const placeMatch = decodedUrl.match(/\/(?:place|search)\/([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)/);
		if (placeMatch) {
			return {
				lat: parseFloat(placeMatch[1]),
				lon: parseFloat(placeMatch[2])
			};
		}

		// Pattern 2: @lat,lng
		const atMatch = decodedUrl.match(/@([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)/);
		if (atMatch) {
			return {
				lat: parseFloat(atMatch[1]),
				lon: parseFloat(atMatch[2])
			};
		}

		// Pattern 3: query parameter q=lat,lng
		const urlObj = new URL(url);
		const q = urlObj.searchParams.get('q');
		if (q) {
			const qMatch = q.match(/([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)/);
			if (qMatch) {
				return {
					lat: parseFloat(qMatch[1]),
					lon: parseFloat(qMatch[2])
				};
			}
		}

		return null;
	} catch (e) {
		console.error('Error parsing Google Maps link:', e);
		return null;
	}
}
