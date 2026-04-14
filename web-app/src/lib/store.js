import { writable } from 'svelte/store';

export const selectedLSG = writable(null);
export const hoveredLSG = writable(null);
export const selectedDistrict = writable(null);
export const mapReady = writable(false);
export const searchQuery = writable('');
export const markedLocation = writable(null); // {lat, lon}
export const markerLink = writable('');
export const cczmInfo = writable(null); // {airport, grid, permissibleHeight, distanceKm, loading, error}
export const crzInfo = writable(null);  // {inZone, sheet, district, pdfUrl} | {inZone: false} | null
const initialTheme = (typeof window !== 'undefined' && localStorage.getItem('theme')) || 'light';
export const theme = writable(initialTheme);

if (typeof window !== 'undefined') {
	theme.subscribe((value) => {
		localStorage.setItem('theme', value);
	});
}
