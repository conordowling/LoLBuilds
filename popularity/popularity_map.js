function popularity_map() {
	var game = this;

	if(game.timeline == null) {
		return;
	}

	patch = game.matchVersion.substring(0,game.matchVersion.indexOf(".",2));

	for(var i in game.timeline.frames) {
		frame = game.timeline.frames[i];
		for(var j in frame.events) {
			lol_event = frame.events[j];
			if(lol_event.eventType == "ITEM_PURCHASED") {
				item = lol_event.itemId;
				champion = game.participants[lol_event.participantId-1].championId;
				lane = game.participants[lol_event.participantId - 1].timeline.lane;
				if(lane == "JUNGLE") {
					role = "JUNGLE";
				} else if(lane == "MIDDLE") {
					role = "MID";
				} else if(lane == "TOP") {
					role = "TOP";
				} else if(lane == "BOTTOM") {
					if(game.participants[lol_event.participantId - 1].timeline.role == "DUO_SUPPORT") {
						role = "SUPPORT";
					} else {
						role = "ADC";
					}
				} else{
					role = lane;
				}
				key = Object()
				key.champion = champion;
				key.patch = patch;
				key.role = role;
				emit(key, item);
				//emit(champion.toString() + "-" + role + "-" + patch, item);
			}
		}

	}
}