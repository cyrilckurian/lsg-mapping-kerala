import { writable } from 'svelte/store';

export const selectedLSG = writable(null);
export const hoveredLSG = writable(null);
export const selectedDistrict = writable(null);
export const mapReady = writable(false);
export const searchQuery = writable('');
