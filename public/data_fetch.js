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

function parse_input() {
    console.log(document.getElementById('chosen_sub').value);
}


// Joel's Example

// componentDidMount = async () => {
//     const animeId = this.props.match.params.searchId;
//     const referenceAnime = await getAnime(animeId);
//     const recommendations = await getRecommendations(animeId, 15);
//     this.setState({ referenceAnime, recommendations });
// };

// const animeToDisplay = this.state.recommendations[
//     recCategoryMapping[this.state.recCategory]
// ];