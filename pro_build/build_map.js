function build_map() {
	game = this;
	for( p in game.participants ) {
		playerId = game.participants[p].participantId;
		itemBuild = Array()

		for(var i in game.timeline.frames) {
			frame = game.timeline.frames[i];
			for(var j in frame.events) {
				lol_event = frame.events[j];
				if(lol_event.eventType == "ITEM_PURCHASED" && lol_event.participantId == playerId) {
					itemBuild.push(lol_event);					
				}
			}

		}
		player = game.participants[p];
		key = player.championId;
		value = Object();
		value.kda = (player.stats.kills + player.stats.assists) * 1.0 / Math.max(1, player.stats.deaths);
		value.items = itemBuild;
		for( x in game.participantIdentities) {
			if( game.participantIdentities[x].participantId == playerId) {
				value.summoner = game.participantIdentities[x].player.summonerName;
			}
		}

		// construct item build json
		build = Object();
		build.title = value.summoner + " " + player.stats.kills + "/" + player.stats.deaths + "/" + player.stats.assists;
		build.type = "global";
		build.map = "SR";
		build.map = "CLASSIC";
		build.priority = true;
		build.sortrank = 0;
		blocks = Array();

		//first buy
		first_block = Object();
		first_block.type = "First Buy";
		first_block.recMath = false;
		first_block.minSummonerLevel = -1;
		first_block.maxSummonerLevel = -1;
		first_block.showIfSummonerSpell = "";
		first_block.hideIfSummonerSpell = "";
		
		first_block.items = Array();
		
		first_count = Object();
		for(i in itemBuild) {
			item = itemBuild[i];
			if(item.timestamp < 1200000) {
				if(first_count[item.itemId] == null ) {
					first_count[item.itemId] = 0;
				}
				first_count[item.itemId] += 1;
			}
		}
		// Non-consumables first

		for( key in first_count) {
			itemEntry = Object();
			itemEntry.id = key;
			itemEntry.count = first_count.key;
			first_block.items.push(itemEntry);
		}
		/*
		for( key in first_count) {
			if(parseInt(key) < 2000 || parseInt(key) >= 3000) {
				itemEntry = Object();
				itemEntry.id = key;
				itemEntry.count = first_count.key;
				first_block.items.push(itemEntry);
			}
		}

		//Now consumables
		for( key in first_count) {
			if(parseInt(key) >= 2000 && parseInt(key) < 3000) {
				itemEntry = Object();
				itemEntry.id = key;
				itemEntry.count = first_count.key;
				first_block.items.push(itemEntry);
			}
		}*/
		blocks.push(first_count);


		build.blocks = blocks;

		value.json = build;
		emit(key, value);
	}
}