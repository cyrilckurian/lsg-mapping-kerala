/**
 * Coastal Regulation Zone (CRZ) utility.
 * Uses Kerala CZMP 2019 grid sheets (7'30" = 0.125° cells) to determine
 * whether a point falls within a CRZ sheet and which district PDF applies.
 */

const BASE =
	'https://keralaczma.gov.in/images/pdf/coastal-zone-management-plan-2019-final/';

const SZ = 0.125; // 7'30" grid step in decimal degrees

// 87 sheets — n = north edge lat, w = west edge lon
// South = n - 0.125, East = w + 0.125
// d = [[district, pdfPath], ...] (multiple for shared-boundary sheets)
const SHEETS = [
	{ no: 'KL-01', n: 8.375,  w: 76.875, d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-01.pdf']] },
	{ no: 'KL-02', n: 8.375,  w: 77.0,   d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-02.pdf']] },
	{ no: 'KL-03', n: 8.5,    w: 76.875, d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-03.pdf']] },
	{ no: 'KL-04', n: 8.5,    w: 77.0,   d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-04.pdf']] },
	{ no: 'KL-05', n: 8.625,  w: 76.75,  d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-05.pdf']] },
	{ no: 'KL-06', n: 8.625,  w: 76.875, d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-06.pdf']] },
	{ no: 'KL-07', n: 8.75,   w: 76.625, d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-07.pdf']] },
	{ no: 'KL-08', n: 8.75,   w: 76.75,  d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-08.pdf']] },
	{ no: 'KL-09', n: 8.875,  w: 76.5,   d: [['Kollam', 'kollam/KL-09.pdf']] },
	{ no: 'KL-10', n: 8.875,  w: 76.625, d: [['Thiruvananthapuram', 'thiruvananthapuram/KL-10.pdf'], ['Kollam', 'kollam/KL-10.pdf']] },
	{ no: 'KL-11', n: 9.0,    w: 76.5,   d: [['Kollam', 'kollam/KL-11.pdf']] },
	{ no: 'KL-12', n: 9.0,    w: 76.625, d: [['Kollam', 'kollam/KL-12.pdf']] },
	{ no: 'KL-13', n: 9.125,  w: 76.375, d: [['Kollam', 'kollam/KL-13.pdf']] },
	{ no: 'KL-14', n: 9.125,  w: 76.5,   d: [['Kollam', 'kollam/KL-14.pdf'], ['Alappuzha', 'alappuzha/KL-14.pdf']] },
	{ no: 'KL-15', n: 9.125,  w: 76.625, d: [['Kollam', 'kollam/KL-15.pdf']] },
	{ no: 'KL-16', n: 9.25,   w: 76.375, d: [['Kollam', 'kollam/KL-16.pdf'], ['Alappuzha', 'alappuzha/KL-16.pdf']] },
	{ no: 'KL-17', n: 9.25,   w: 76.5,   d: [['Kollam', 'kollam/KL-17.pdf'], ['Alappuzha', 'alappuzha/KL-17.pdf']] },
	{ no: 'KL-18', n: 9.375,  w: 76.25,  d: [['Alappuzha', 'alappuzha/KL-18.pdf']] },
	{ no: 'KL-19', n: 9.375,  w: 76.375, d: [['Alappuzha', 'alappuzha/KL-19.pdf']] },
	{ no: 'KL-20', n: 9.375,  w: 76.5,   d: [['Alappuzha', 'alappuzha/KL-20.pdf']] },
	{ no: 'KL-21', n: 9.5,    w: 76.25,  d: [['Alappuzha', 'alappuzha/KL-21.pdf']] },
	{ no: 'KL-22', n: 9.5,    w: 76.5,   d: [['Kottayam', 'kottayam/KL-22.pdf'], ['Alappuzha', 'alappuzha/KL-22.pdf']] },
	{ no: 'KL-23', n: 9.625,  w: 76.25,  d: [['Alappuzha', 'alappuzha/KL-23.pdf']] },
	{ no: 'KL-24', n: 9.625,  w: 76.375, d: [['Kottayam', 'kottayam/KL-24.pdf'], ['Alappuzha', 'alappuzha/KL-24.pdf']] },
	{ no: 'KL-25', n: 9.625,  w: 76.5,   d: [['Kottayam', 'kottayam/KL-25.pdf']] },
	{ no: 'KL-26', n: 9.75,   w: 76.25,  d: [['Alappuzha', 'alappuzha/KL-26.pdf']] },
	{ no: 'KL-27', n: 9.75,   w: 76.375, d: [['Kottayam', 'kottayam/KL-27.pdf']] },
	{ no: 'KL-28', n: 9.75,   w: 76.5,   d: [['Kottayam', 'kottayam/KL-28.pdf']] },
	{ no: 'KL-29', n: 9.875,  w: 76.25,  d: [['Kottayam', 'kottayam/KL-29.pdf'], ['Alappuzha', 'alappuzha/KL-29.pdf'], ['Ernakulam', 'ernakulam/KL-29.pdf']] },
	{ no: 'KL-30', n: 9.875,  w: 76.375, d: [['Kottayam', 'kottayam/KL-30.pdf'], ['Alappuzha', 'alappuzha/KL-30.pdf'], ['Ernakulam', 'ernakulam/KL-30.pdf']] },
	{ no: 'KL-31', n: 10.0,   w: 76.125, d: [['Ernakulam', 'ernakulam/KL-31.pdf']] },
	{ no: 'KL-32', n: 10.0,   w: 76.25,  d: [['Alappuzha', 'alappuzha/KL-32.pdf'], ['Ernakulam', 'ernakulam/KL-32.pdf']] },
	{ no: 'KL-33', n: 10.0,   w: 76.375, d: [['Ernakulam', 'ernakulam/KL-33.pdf']] },
	{ no: 'KL-34', n: 10.125, w: 76.125, d: [['Ernakulam', 'ernakulam/KL-34.pdf']] },
	{ no: 'KL-35', n: 10.125, w: 76.25,  d: [['Ernakulam', 'ernakulam/KL-35.pdf']] },
	{ no: 'KL-36', n: 10.125, w: 76.375, d: [['Ernakulam', 'ernakulam/KL-36.pdf']] },
	{ no: 'KL-37', n: 10.25,  w: 76.125, d: [['Ernakulam', 'ernakulam/KL-37.pdf'], ['Thrissur', 'thrissur/KL-37.pdf']] },
	{ no: 'KL-38', n: 10.25,  w: 76.25,  d: [['Ernakulam', 'ernakulam/KL-38.pdf'], ['Thrissur', 'thrissur/KL-38.pdf']] },
	{ no: 'KL-39', n: 10.375, w: 76.0,   d: [['Thrissur', 'thrissur/KL-39.pdf']] },
	{ no: 'KL-40', n: 10.375, w: 76.125, d: [['Thrissur', 'thrissur/KL-40.pdf']] },
	{ no: 'KL-41', n: 10.375, w: 76.25,  d: [['Thrissur', 'thrissur/KL-41.pdf']] },
	{ no: 'KL-42', n: 10.5,   w: 76.0,   d: [['Thrissur', 'thrissur/KL-42.pdf']] },
	{ no: 'KL-43', n: 10.5,   w: 76.125, d: [['Thrissur', 'thrissur/KL-43.pdf']] },
	{ no: 'KL-44', n: 10.625, w: 75.875, d: [['Thrissur', 'thrissur/KL-44.pdf']] },
	{ no: 'KL-45', n: 10.625, w: 76.0,   d: [['Thrissur', 'thrissur/KL-45.pdf']] },
	{ no: 'KL-46', n: 10.625, w: 76.125, d: [['Thrissur', 'thrissur/KL-46.pdf']] },
	{ no: 'KL-47', n: 10.75,  w: 75.875, d: [['Thrissur', 'thrissur/KL-47.pdf'], ['Malappuram', 'malappuram/KL-47.pdf']] },
	{ no: 'KL-48', n: 10.75,  w: 76.0,   d: [['Thrissur', 'thrissur/KL-48.pdf'], ['Malappuram', 'malappuram/KL-48.pdf']] },
	{ no: 'KL-49', n: 10.875, w: 75.875, d: [['Malappuram', 'malappuram/KL-49.pdf']] },
	{ no: 'KL-50', n: 10.875, w: 76.0,   d: [['Malappuram', 'malappuram/KL-50.pdf']] },
	{ no: 'KL-51', n: 11.0,   w: 75.75,  d: [['Malappuram', 'malappuram/KL-51.pdf']] },
	{ no: 'KL-52', n: 11.0,   w: 75.875, d: [['Malappuram', 'malappuram/KL-52.pdf']] },
	{ no: 'KL-53', n: 11.125, w: 75.75,  d: [['Malappuram', 'malappuram/KL-53.pdf']] },
	{ no: 'KL-54', n: 11.125, w: 75.875, d: [['Malappuram', 'malappuram/KL-54.pdf']] },
	{ no: 'KL-55', n: 11.25,  w: 75.75,  d: [['Malappuram', 'malappuram/KL-55.pdf'], ['Kozhikode', 'kozhikode/KL-55.pdf']] },
	{ no: 'KL-56', n: 11.25,  w: 75.875, d: [['Malappuram', 'malappuram/KL-56.pdf'], ['Kozhikode', 'kozhikode/KL-56.pdf']] },
	{ no: 'KL-57', n: 11.375, w: 75.625, d: [['Kozhikode', 'kozhikode/KL-57.pdf']] },
	{ no: 'KL-58', n: 11.375, w: 75.75,  d: [['Kozhikode', 'kozhikode/KL-58.pdf']] },
	{ no: 'KL-59', n: 11.5,   w: 75.5,   d: [['Kozhikode', 'kozhikode/KL-59.pdf']] },
	{ no: 'KL-60', n: 11.5,   w: 75.625, d: [['Kozhikode', 'kozhikode/KL-60.pdf']] },
	{ no: 'KL-61', n: 11.5,   w: 75.75,  d: [['Kozhikode', 'kozhikode/KL-61.pdf']] },
	{ no: 'KL-62', n: 11.625, w: 75.5,   d: [['Kozhikode', 'kozhikode/KL-62.pdf']] },
	{ no: 'KL-63', n: 11.625, w: 75.625, d: [['Kozhikode', 'kozhikode/KL-63.pdf']] },
	{ no: 'KL-64', n: 11.75,  w: 75.375, d: [['Kannur', 'kannur/KL-64.pdf']] },
	{ no: 'KL-65', n: 11.75,  w: 75.5,   d: [['Kozhikode', 'kozhikode/KL-65.pdf'], ['Kannur', 'kannur/KL-65.pdf']] },
	{ no: 'KL-66', n: 11.75,  w: 75.625, d: [['Kozhikode', 'kozhikode/KL-66.pdf'], ['Kannur', 'kannur/KL-66.pdf']] },
	{ no: 'KL-67', n: 11.875, w: 75.25,  d: [['Kannur', 'kannur/KL-67.pdf']] },
	{ no: 'KL-68', n: 11.875, w: 75.375, d: [['Kannur', 'kannur/KL-68.pdf']] },
	{ no: 'KL-69', n: 11.875, w: 75.5,   d: [['Kannur', 'kannur/KL-69.pdf']] },
	{ no: 'KL-70', n: 12.0,   w: 75.25,  d: [['Kannur', 'kannur/KL-70.pdf']] },
	{ no: 'KL-71', n: 12.0,   w: 75.375, d: [['Kannur', 'kannur/KL-71.pdf']] },
	{ no: 'KL-72', n: 12.0,   w: 75.5,   d: [['Kannur', 'kannur/KL-72.pdf']] },
	{ no: 'KL-73', n: 12.125, w: 75.125, d: [['Kannur', 'kannur/KL-73.pdf'], ['Kasaragod', 'kasaragod/KL-73.pdf']] },
	{ no: 'KL-74', n: 12.125, w: 75.25,  d: [['Kannur', 'kannur/KL-74.pdf']] },
	{ no: 'KL-75', n: 12.125, w: 75.375, d: [['Kannur', 'kannur/KL-75.pdf']] },
	{ no: 'KL-76', n: 12.25,  w: 75.0,   d: [['Kasaragod', 'kasaragod/KL-76.pdf']] },
	{ no: 'KL-77', n: 12.25,  w: 75.125, d: [['Kannur', 'kannur/KL-77.pdf'], ['Kasaragod', 'kasaragod/KL-77.pdf']] },
	{ no: 'KL-78', n: 12.375, w: 75.0,   d: [['Kasaragod', 'kasaragod/KL-78.pdf']] },
	{ no: 'KL-79', n: 12.375, w: 75.125, d: [['Kasaragod', 'kasaragod/KL-79.pdf']] },
	{ no: 'KL-80', n: 12.375, w: 75.25,  d: [['Kannur', 'kannur/KL-80.pdf'], ['Kasaragod', 'kasaragod/KL-80.pdf']] },
	{ no: 'KL-81', n: 12.5,   w: 74.875, d: [['Kasaragod', 'kasaragod/KL-81.pdf']] },
	{ no: 'KL-82', n: 12.5,   w: 75.0,   d: [['Kasaragod', 'kasaragod/KL-82.pdf']] },
	{ no: 'KL-83', n: 12.625, w: 74.875, d: [['Kasaragod', 'kasaragod/KL-83.pdf']] },
	{ no: 'KL-84', n: 12.625, w: 75.0,   d: [['Kasaragod', 'kasaragod/KL-84.pdf']] },
	{ no: 'KL-85', n: 12.75,  w: 74.75,  d: [['Kasaragod', 'kasaragod/KL-85.pdf']] },
	{ no: 'KL-86', n: 12.75,  w: 74.875, d: [['Kasaragod', 'kasaragod/KL-86.pdf']] },
	{ no: 'KL-87', n: 12.875, w: 74.75,  d: [['Kasaragod', 'kasaragod/KL-87.pdf']] }
];

/**
 * Check whether a lat/lon point falls within any CZMP 2019 sheet.
 *
 * @param {number} lat
 * @param {number} lon
 * @param {string|null} district - LSG district of the point (used to pick the
 *   correct PDF when the sheet straddles a district boundary). Pass null if unknown.
 * @returns {{ inZone: false } | { inZone: true, sheet: string, district: string, pdfUrl: string }}
 */
export function queryCRZ(lat, lon, district = null) {
	// Find all sheets whose bounding box contains the point
	const matches = SHEETS.filter(
		(s) => lat >= s.n - SZ && lat < s.n && lon >= s.w && lon < s.w + SZ
	);

	if (matches.length === 0) return { inZone: false };

	// Flatten all [district, pdf] pairs from every matching sheet
	const options = [];
	for (const sheet of matches) {
		for (const [dist, pdf] of sheet.d) {
			options.push({ sheet: sheet.no, district: dist, pdfUrl: BASE + pdf });
		}
	}

	// If a district is known, prefer its entry
	if (district) {
		const norm = (s) => s.toLowerCase().trim();
		const hit = options.find((o) => norm(o.district) === norm(district));
		if (hit) return { inZone: true, ...hit };
	}

	// Fall back to the first available option
	return { inZone: true, ...options[0] };
}
