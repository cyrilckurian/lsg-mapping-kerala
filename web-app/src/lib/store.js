import { writable } from 'svelte/store';

export const selectedLSG = writable(null);
export const hoveredLSG = writable(null);
export const selectedDistrict = writable(null);
export const mapReady = writable(false);
export const searchQuery = writable('');
export const markedLocation = writable(null); // {lat, lon}
export const markerLink = writable('');
const initialTheme = (typeof window !== 'undefined' && localStorage.getItem('theme')) || 'dark';
export const theme = writable(initialTheme);

if (typeof window !== 'undefined') {
	theme.subscribe((value) => {
		localStorage.setItem('theme', value);
	});
}
