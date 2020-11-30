

tags = {
    '<mana>'        : '<mana>',
    '</mana>'       : '</mana>',
    '<stats>'       : '</stats>',
    '</stats>'      : '</stats>',
    '<unique>'      : '<unique>',
    '</unique>'     : '</unque>',
    '<br>'          : '<br>',
    '<passive>'     : '<passive>',
    '</passive>'    : '</passive>',
    '<grouplimit>'  : '<grouplimit>',
    '</grouplimit>' : '</grouplimit>'
}


def parse(data, item_details, item_req, item_numbers):
    print('TODO')
    
    if item_req in item_numbers: 
        item_name = data['data'][item_req]['name']
        item_description = data['data'][item_req]['description'] # parse
        item_price = data['data'][item_req]['gold']['base']

        item_description = item_description.replace("<mana>", "")
        item_description = item_description.replace("</mana>", "")
        item_description = item_description.replace("<stats>", "")
        item_description = item_description.replace("</stats>", "")
        item_description = item_description.replace("<unique>", "")
        item_description = item_description.replace("</unique>", "")
        item_description = item_description.replace("<br>", "\n")
        item_description = item_description.replace("<passive>", "")
        item_description = item_description.replace("</passive>", "")

        result = f'{item_name}:\n\n{item_description}\n\nCost: {item_price}'
        return result
    elif item_req in item_details:
        item_name = data['data'][item_details.get(item_req)]['name']
        item_number = item_details[item_req]
        item_description = data['data'][item_number]['description'] # parse
        item_price = data['data'][item_number]['gold']['base']

        item_description = item_description.replace("<mana>", "")
        item_description = item_description.replace("</mana>", "")
        item_description = item_description.replace("<stats>", "")
        item_description = item_description.replace("</stats>", "")
        item_description = item_description.replace("<unique>", "")
        item_description = item_description.replace("</unique>", "")
        item_description = item_description.replace("<br>", "\n")
        item_description = item_description.replace("<grouplimit>", "")
        item_description = item_description.replace("</grouplimit>", "")
        # FIXME
        # parse <a href="[reg a-z]"></a>
        # parse <font color="[reg 0-9]></font>
        item_description = item_description.replace("</a>", "")
        item_description = item_description.replace("</font>", "")

        result = f'{item_name}  {item_number}:\n\n{item_description}\n\nCost: {item_price}'
        return result

# tags.update({'<mana>': '<mana>', '</mana>': None})
# print(tags)
