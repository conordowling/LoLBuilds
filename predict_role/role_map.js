function role_map() {
	game = this;

	patch = game.matchVersion.substring(0,game.matchVersion.indexOf(".",2));

	for( i in game.participants) {
		key = Object()
		key.champion = game.participants[i].championId;
		//key.patch = game.matchVersion.substring(0,game.matchVersion.indexOf(".",2));

		lane = game.participants[i].timeline.lane;
		if(lane == "JUNGLE") {
			role = "JUNGLE";
		} else if(lane == "MIDDLE") {
			role = "MIDDLE";
		} else if(lane == "TOP") {
			role = "TOP";
		} else if(game.participants[i].timeline.role == "DUO_SUPPORT") {
			role = "SUPPORT";
		} else if(game.participants[i].timeline.role == "DUO_CARRY") {
			role = "ADC";
		} else {
			return;
		}
		role = game.participants[i].timeline.role + " " + lane;

		emit(key, role);
	}

}