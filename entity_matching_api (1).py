from AAAI_Rada_Method import AAAI_Rada_Method

def entity_data_extractor(entity,entity_fields):
    #print("entity")
    #print(entity)
    whole_data  = ""
    #print(len(entity_fields))
    for item_key, item_value in entity.items():


        if (not(item_key in entity_fields) and len(entity_fields)!=0):
            continue

        if type(item_value)==dict:
            try:
                data = entity_data_extractor(item_value,entity_fields)
            except:
                do="nothing"

        elif type(item_value)==list:
            data = ""
            for sub_item in item_value:
                try:
                    data +=" "+str(sub_item)
                except:
                    do = "nothing"

        else:
            try:
                data = str(item_value)
            except:
                do="nothing"


        whole_data +=" " +data

    #print(whole_data)
    return whole_data



def get_match_weight(first_item_data, second_item_data, match_source_category, match_list_category,
                                algorithm):
    return AAAI_Rada_Method(first_item_data,second_item_data,algorithm,0,0,1,{},0.4)


def entity_matching_api(match_source,
                        match_list,
                        match_source_category,
                        match_list_category,
                        match_source_fields,
                        match_list_fields,
                        algorithm
                        ):

    final_result = []

    intermediate_result = []

    item_index = -1

    first_item_data = entity_data_extractor(match_source, match_source_fields)

    #print(first_item_data)

    for item in match_list:
        item_index+=1

        second_item_data = entity_data_extractor(item,match_list_fields)
        #print(second_item_data)

        match_weight = get_match_weight(first_item_data,second_item_data,match_source_category,match_list_category,algorithm)

        final_result.append({'rank':0,'weight': match_weight})
        intermediate_result.append([item_index, match_weight])

        print(match_weight)
        print('item:'+str(item_index))

    intermediate_result_sorted = sorted(intermediate_result, key=lambda x: x[1], reverse=True)

    item_rank = 0
    for item in intermediate_result_sorted:
        item_rank +=1
        final_result[item[0]]['rank'] = item_rank

    return final_result












