function firstBuyMap() {
	var game = this;

	if(game.timeline == null) {
		return;
	}

	for(p=1; p<=game.participants.length; ++p) {
		firstBuy = Array();
		for(var i in [0,1]) {
			frame = game.timeline.frames[i];
			for(var j in frame.events) {
				lol_event = frame.events[j];
				if(lol_event.eventType == "ITEM_PURCHASED") {
					if(lol_event.participantId == p) {
						firstBuy.push(lol_event.itemId);
					}
				}
			}

		}
		//emit(game.participants[i-1].championId, firstBuy);
		//key = Object();
		//key.champion = game.participants[p-1]
		record = Object();
		record.items = firstBuy;
		record.matchId = game.matchId;
		record.player = game.participantIdentities[p-1].player.summonerName;
		emit(game.participants[p-1].championId, record);
	}	
}