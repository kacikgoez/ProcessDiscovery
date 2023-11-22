from backend.src.flask.services.process_mining_service import ProcessMiningService
import pm4py

pms = ProcessMiningService()
el = pms.event_log
variants = pm4py.get_variants_as_tuples(el)
print(variants)

total_count = len(variants)
attribute = 'gender'
attribute_classes = el[attribute].unique()
my_variants = []
for variant, traces in variants:
    freq = {}
    for trace in traces:
        val = trace[0][attribute]
        if val not in freq:
            freq[val] = 0
        freq[val] += 1
    variant_info = {
        'variant': variant,
        'freq': freq,
    }
    my_variants.append(variant_info)
print(my_variants)