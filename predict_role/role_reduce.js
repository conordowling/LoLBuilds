function role_reduce(key, values) {
	roleCount = Object();

	for(i=0; i < values.length; ++i) {
		role = values[i];
		if(roleCount[role] == null) {
			roleCount[role] = 0;
		}
		roleCount[role] += 1;
	}
	return roleCount;

	roleFrequency = Object()
	for( key in roleCount) {
		roleFrequency[key] = roleCount[key] * 1.0 / values.length;

	}
	//roleFrequency.patch = key[1];
	//roleFrequency.champion = key[0];
	return roleFrequency

}