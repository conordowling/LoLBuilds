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

		itemBuild.sort(function(a,b){ return a.timestamp - b.timestamp});

		function newBlock() {
			block = Object();
			
			block.recMath = false;
			block.minSummonerLevel = -1;
			block.maxSummonerLevel = -1;
			block.showIfSummonerSpell = "";
			block.hideIfSummonerSpell = "";
			block.items = [];
			return block;
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
		first_block = newBlock();
		first_block.type = "First Buy";
		
		for(i in itemBuild) {
			item = itemBuild[i];
			if(item.timestamp < 120000 && (item.itemId < 2000 || item.itemId >= 3000)) {
				itemEntry = Object();
				itemEntry["id"] = item.itemId;
				itemEntry.count = 1;
				first_block.items.push(itemEntry);
			}
		}

		for(i in itemBuild) {
			item = itemBuild[i];
			if(item.timestamp < 120000 && item.itemId >= 2000 && item.itemId < 3000) {
				itemEntry = Object();
				itemEntry["id"] = item.itemId;
				itemEntry.count = 1;
				first_block.items.push(itemEntry);
			}
		}

		blocks.push(first_block);

		complete_items = [3714, 3717, 3716, 3924, 1305, 3434, 3719, 1307, 2138, 3170, 3041, 1300, 3043, 3345, 1309, 3285, 1301, 1076, 1074, 1303, 3124, 3174, 1340, 3190, 2010, 1317, 1316, 1315, 1314, 1313, 1312, 1311, 1310, 1308, 3931, 3930, 1319, 1318, 3135, 3137, 3139, 1336, 3430, 3243, 3242, 1063, 1062, 3031, 3244, 3840, 2140, 1337, 1333, 3241, 1322, 1323, 1320, 1321, 1326, 1327, 1324, 1325, 1328, 1329, 3829, 3141, 3142, 3143, 1304, 3040, 3029, 3027, 3025, 3023, 3022, 3652, 1334, 3046, 3068, 1339, 1338, 1335, 1331, 3744, 3745, 3742, 1330, 1332, 3153, 3152, 1306, 3150, 3157, 3156, 3154, 3159, 2054, 3508, 2047, 2044, 2045, 2043, 3460, 3504, 3151, 3092, 3090, 3091, 3611, 3612, 1075, 3614, 3615, 3616, 3617, 3613, 1341, 3599, 3800, 3001, 3165, 3290, 3901, 2051, 2050, 2052, 3078, 3364, 3512, 3431, 3361, 3362, 3363, 3104, 3089, 3085, 3084, 3087, 3083, 3035, 1302, 3071, 3072, 3074, 3075, 3724, 3725, 3172, 3720, 3721, 3723, 2041, 3146, 3902, 3903, 3060, 3065, 3069, 3222, 2137, 3348, 1055, 1056, 3100, 3102, 2139, 3184, 3185, 3187, 3180, 3181, 3911, 3621, 3623, 3622, 3625, 3624, 3626, 3708, 3709, 3933, 3056, 1054, 3932, 3707, 3050, 3401, 3240, 3116, 3115, 3112, 3110, 2003, 2004, 3026, 2009, 3198, 3003, 3004, 3008,];

		first_item = newBlock();

		// Find first item finished
		first = null;
		for(i=0; first = null && i < itemBuild.length; ++i) {
			if(complete_items.indexOf(itemBuild[i].itemId) > -1) {
				first = itemBuild[i].itemId;
			}
		}

		if(first) {
			first_item.type = "First Item";
			first_item.items.push(first);
		}

		blocks.push(first_item);

		build.blocks = blocks;

		value.json = build;
		emit(key, value);
	}
}