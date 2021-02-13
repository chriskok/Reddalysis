function fetchJson(url, kwds) {
	return fetch(url, {
		headers: {
			Accept: "application/json",
			"Content-Type": "application/json",
		},
		credentials: "include",
		...kwds,
	}).then(res => res.json());
}

function getNames() {
	return fetchJson(`http://localhost:8000/`);
}

function getRecommendations(animeId, quantity = 5) {
	return fetchJson(
		`localhost:8000/api/v1/recommendations?anime_code=${animeId}&n_recommendations=${quantity}`
	);
}