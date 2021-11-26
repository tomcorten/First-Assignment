import _ne_based_Tom


PERS = _ne_based_Tom.get_random_entities('P31' ,'Q5') # get 20 random instances of Q5: human
LOC = _ne_based_Tom.get_random_entities('P31','Q486972') # get 20 random instances of Q486972: human settlement
ORG = _ne_based_Tom.get_random_entities('P31','Q6881511') # get 20 random instances of Q6881511: enterprise

pers_overlap = _ne_based_Tom.get_p_overlap(PERS)
org_overlap = _ne_based_Tom.get_p_overlap(ORG)
loc_overlap = _ne_based_Tom.get_p_overlap(LOC)

print('pers', pers_overlap)
print('org', org_overlap)
print('loc', loc_overlap)

_ne_based_Tom.ne_based_model("<http://www.wikidata.org/entity/Q918>", random_overlap = loc_overlap)