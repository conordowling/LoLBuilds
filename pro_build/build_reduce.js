function build_reduce(key, values) {

	max_build = values[0]
	for( i in values) {
		if(values[i].kda > max_build.kda) {
			max_build = values[i];
		}
	}

	return max_build;
}