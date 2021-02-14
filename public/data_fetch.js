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
	return fetchJson(`https://reddalysis.herokuapp.com/`);
}

function getBow(subreddit_name) {
	return fetchJson(
		`https://reddalysis-api.herokuapp.com/api/v1/get_bow?subreddit_name=${subreddit_name}`
	);
}

function getYearlyBow(subreddit_name) {
	return fetchJson(
		`https://reddalysis-api.herokuapp.com/api/v1/get_yearly_bow?subreddit_name=${subreddit_name}`
	);
}

