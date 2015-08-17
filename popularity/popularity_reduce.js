function popularity_reduce(key, values) {
	itemCount = Object();

	for(i=0; i < values.length; ++i) {
		item = values[i];
		if(itemCount[item] == null) {
			itemCount[item] = 0;
		}
		itemCount[item] += 1;
	}

	itemFrequency = Object()
	for( key in itemCount) {
		itemFrequency[key] = itemCount[key] * 1.0 / values.length;

	}
	//itemFrequency.patch = key[1];
	//itemFrequency.champion = key[0];
	return itemFrequency
}