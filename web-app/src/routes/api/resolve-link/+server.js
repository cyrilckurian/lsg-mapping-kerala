export async function GET({ url }) {
	const shortUrl = url.searchParams.get('url');

	if (!shortUrl) {
		return new Response(JSON.stringify({ error: 'No URL provided' }), { status: 400 });
	}

	try {
		// We only want to follow the redirect, not download the whole page
		const response = await fetch(shortUrl, {
			method: 'HEAD',
			redirect: 'follow'
		});

		return new Response(
			JSON.stringify({
				finalUrl: response.url
			}),
			{
				headers: {
					'Content-Type': 'application/json'
				}
			}
		);
	} catch (e) {
		console.error('Error resolving short URL:', e);
		return new Response(JSON.stringify({ error: 'Failed to resolve URL' }), { status: 500 });
	}
}
