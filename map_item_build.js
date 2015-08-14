function itemMap() {
	var game = this;

	if(game.timeline == null) {
		return;
	}

	var info = Object();

	info.patch = game.matchVersion;
	info.matchId = game.matchId;


	for(int i=1; i<=10; ++i) {
		itemBuild = Object();
		for(var i in game.timeline.frames) {
			frame = game.timeline.frames[i];
			for(var j in frame.events) {
				lol_event = frame.events[j];
				if(lol_event.eventType == "ITEM_PURCHASED") {
					if
				}
			}

		}
		emit(info.matchId, itemBuild)

	}	



}