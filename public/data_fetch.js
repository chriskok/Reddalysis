function fetchJson(url, kwds) {
	return fetch(url, {
		headers: {
			Accept: "application/json",
			"Content-Type": "application/json",
		},
		credentials: "include",
		...kwds,
	}).then(res => res.json())
	.then((responseData) => {
		return responseData;
	});
}

function getTest() {
	return fetchJson(`http://localhost:8000/`);
}

function getBow(subreddit_name) {
	return fetchJson(
		`http://localhost:8000/api/v1/get_bow?subreddit_name=${subreddit_name}`
	);
}

function getYearlyBow(subreddit_name) {
	return fetchJson(
		`http://localhost:8000/api/v1/get_yearly_bow?subreddit_name=${subreddit_name}`
	);
}

