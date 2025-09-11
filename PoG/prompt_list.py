subobjective_prompt = """Please break down the process of answering the question into as few subobjectives as possible based on semantic analysis.
Here is an example: 
Q: Which of the countries in the Caribbean has the smallest country calling code?
Output: ['Search the countries in the Caribbean', 'Search the country calling code for each Caribbean country', 'Compare the country calling codes to find the smallest one']

Now you need to directly output subobjectives of the following question in list format without other information or notes. 
Q: """

sparql_system_prompt = """你是一个 SPARQL 大师，但你从没用过 Freebase 数据库。给定一个问题和起始节点（用英文逗号“,”分隔），要求你使用 SPARQL 语句在 Freebase 数据库中逐步查询给定问题的答案。在每一步推理中，你需要改进你的 SPARQL 语句继续进行下一步查询，或对问题进行回答。
如果你认为当前信息足以回答问题，你需要以 JSON 格式（必须包括 "A" 和 "R"，"A" 包括 "Sufficient" 与 "Answer"，为相关答案；"R" 为作此回答的理由）向上级程序输出问题的答案。注意答案必须按原样输出，如果无法回答，请继续改善查询语句。
如果你仍要改进你的 SPARQL 语句，你需要以 JSON 格式（必须包括 "R"、"Q" 和 "isRel"，"R" 为查询的原因、查询语句的解释及下一步行动，"Q" 为对应的 SPARQL 语句，"isRel" 表示查询目标是否为关系）向上级程序输出改进方案。

以下是两个例子：
问题：Of the countries that are in the Caribbean, which has the Dutch Language as an official language?
起始节点："m.0261m": "Caribbean","m.02bv9": "Dutch Language"
输出为：
{
    "R": "我不知道在 Freebase 数据库中代表地区所包含国家的关系名，为了避免随意地猜测，我需要先查询可能代表包含国家的关系。对应查询语句查询了所有与 Caribbean 地区实体正向相连的关系。下一步是利用查询到的关系搜索 Caribbean 地区的国家。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?rel\\nWHERE {\\nns:m.0261m ?rel ?any .\\n}",
    "isRel": true
}
（数据库返回结果省略）
{
    "R": "从返回的关系中，`ns:location.location.contains` 关系可能可以用于搜索 Caribbean 地区包含的国家。对应查询语句利用这个关系查询 Caribbean 地区的国家。下一步是查询可能表示官方语言的关系。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?country\\nWHERE {\\nns:m.0261m ns:location.location.contains ?country .\\n}",
    "isRel": false
}
（数据库返回结果省略）
{
    "R": "现在我们已经能够获得 Caribbean 地区的国家列表，接下来要查询这些国家的官方语言，但我不知道 Freebase 数据库中表示官方语言的关系名。对应查询语句查询所有与国家实体正向相连的关系。下一步是利用可能表示官方语言的关系构建最终的查询语句。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?rel\\nWHERE {\\nns:m.0261m ns:location.location.contains ?country .\\n?country ?rel ns:m.02bv9 .\\n}",
    "isRel": true
}
（数据库返回结果省略）
{
    "R": "现在我们已经找到了表示官方语言的关系 `ns:location.country.official_language`。对应查询语句查询哪些 Caribbean 国家将 Dutch Language 作为官方语言。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?country\\nWHERE {\\nns:m.0261m ns:location.location.contains ?country .\\nns:m.02bv9 ns:location.country.official_language ?country .\\n}",
    "isRel": false
}
（数据库未返回任何结果）
{
    "R": "数据库没有返回任何可用的结果。在重新检查查询语句后，我认为我对关系 `ns:location.country.official_language` 的理解可能有误，它可能代表“某国家的官方语言是某语言”而非“某语言是某国家的官方语言”，我应重新组织查询语句。对应查询语句查询哪些 Caribbean 国家将 Dutch Language 作为官方语言。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?country\\nWHERE {\\nns:m.0261m ns:location.location.contains ?country .\\n?country ns:location.country.official_language ns:m.02bv9 .\\n}",
    "isRel": false
}
（数据库返回结果省略）
{
    "R": "数据库成功返回了将 Dutch Language 作为官方语言的国家实体节点 ID，但我需要知道这些国家的名称。对应查询语句通过关系 `ns:type.object.name` 获取其名称。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?name\\nWHERE {\\nns:m.0261m ns:location.location.contains ?country .\\n?country ns:location.country.official_language ns:m.02bv9 .\\n?country ns:type.object.name ?name .\\n}",
    "isRel": false
}
（数据库返回结果省略）
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "Netherlands Antilles"
    },
    "R": "根据数据库返回的查询结果，Caribbean 地区官方语言为 Dutch 的国家仅有 Netherlands Antilles。"
}

问题：Who is the coach of the team owned by Steve Bisciotti?
起始节点："m.06x8mf": "Steve Bisciotti"
输出为：
{
    "R": "我不知道 Freebase 数据库中代表球队所有者的关系名，为了避免随意地猜测，我需要先查询可能代表球队所有者的关系。对应查询语句查询了所有与 Steve Bisciotti 实体正向相连的关系。下一步是利用查询到的关系搜索 Steve Bisciotti 拥有的球队。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?rel\\nWHERE {\\nns:m.06x8mf ?rel ?any .\\n}",
    "isRel": true
}
（数据库返回结果省略）
{
    "R": "从返回结果中，我发现了 `ns:sports.sports_team_owner.teams_owned` 这个关系可能用于查询 Steve Bisciotti 拥有的球队。对应查询语句使用这个关系来搜索 Steve Bisciotti 拥有的具体球队。下一步是查询球队的所有关系以确定表示教练的关系名。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\nSELECT DISTINCT ?team\nWHERE {\nns:m.06x8mf ns:sports.sports_team_owner.teams_owned ?team .\n}",
    "isRel": false
}
（数据库返回结果省略）
{
    "R": "现在我们已经能找到了 Steve Bisciotti 拥有的球队，但我不知道 Freebase 数据库中表示球队教练的关系名。对应查询语句查找球队实体所有正向连接的关系。下一步是利用可能包含教练信息的关系构建最终的查询语句。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?rel\\nWHERE {\\nns:m.06x8mf ns:sports.sports_team_owner.teams_owned ?team .\\n?team ?rel ?any .\\n}",
    "isRel": true
}
（数据库返回结果省略）
{
    "R": "从返回结果中，我发现了 `ns:american_football.football_team.current_head_coach` 和 `ns:sports.sports_team.coaches` 这两个可能包含教练信息的关系，需要依次尝试。对应查询语句使用更具体的 `ns:american_football.football_team.current_head_coach` 关系来查询当前主教练。如果查询失败，下一步是使用 `ns:sports.sports_team.coaches` 关系做更宽泛的查询。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?coach\\nWHERE {\\nns:m.06x8mf ns:sports.sports_team_owner.teams_owned ?team .\\n?team ns:american_football.football_team.current_head_coach ?coach .\\n}",
    "isRel": false
}
（数据库返回结果省略）
{
    "R": "数据库成功查询到了教练的实体节点 ID，但我需要获取其姓名。对应查询语句使用关系 `ns:type.object.name` 获取其名称。如果查询失败，下一步是使用 `ns:sports.sports_team.coaches` 关系对主教练进行更宽泛的查询。",
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?name\\nWHERE {\\nns:m.06x8mf ns:sports.sports_team_owner.teams_owned ?team .\\n?team ns:american_football.football_team.current_head_coach ?coach .\\n?coach ns:type.object.name ?name .\\n}",
    "isRel": false
}
（数据库返回结果省略）
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "John Harbaugh"
    },
    "R": "根据数据库返回的查询结果，Steve Bisciotti 拥有的球队的教练姓名为 John Harbaugh。"
}

不论何时，查询应始终分为多步进行，且只应使用在之前查询中出现过的关系。根据已有关系推测未知关系名应被视为不可接受的。
"""

init_sparql_prompt = """现在，你需要以 JSON 格式（必须包括 "R" 和 "Q"，"R" 为查询的原因、查询语句的解释及下一步行动，"Q" 为对应的 SPARQL 语句）直接输出以下问题的结果，不要包含其他信息或注释。查询过程中你的查询语句必须包含起始节点。
问题："""

next_query_prompt_head = """数据库返回了如下结果：
"""

next_query_prompt_tail = """
现在请你改进你的 SPARQL 语句继续进行下一步查询，或对问题进行回答。

如果你认为当前信息足以回答问题，你需要以 JSON 格式（必须包括 "A" 和 "R"，"A" 包括 "Sufficient" 与 "Answer"，为相关答案；"R" 为作此回答的理由）向上级程序输出问题的答案。注意答案必须按原样输出，如果无法回答，请继续改善查询语句。
如果你仍要改进你的 SPARQL 语句，你需要以 JSON 格式（必须包括 "R"、"Q" 和 "isRel"，"R" 为查询的原因、查询语句的解释及下一步行动，"Q" 为对应的 SPARQL 语句，"isRel" 表示查询目标是否为关系）向上级程序输出改进方案。

现在请你给出 JSON 格式的回复，不包含任何其他信息或注释。注意改进过程中你的查询语句必须包含起始节点。
问题："""

extract_relation_prompt = """Please provide as few highly relevant relations as possible to the question and its subobjectives from the following relations (separated by semicolons).
Here is an example:
Q: Name the president of the country whose main spoken language was Brahui in 1980?
Subobjectives: ['Identify the countries where the main spoken language is Brahui', 'Find the president of each country', 'Determine the president from 1980']
Topic Entity: Brahui Language
Relations: language.human_language.main_country; language.human_language.language_family; language.human_language.iso_639_3_code; base.rosetta.languoid.parent; language.human_language.writing_system; base.rosetta.languoid.languoid_class; language.human_language.countries_spoken_in; kg.object_profile.prominent_type; base.rosetta.languoid.document; base.ontologies.ontology_instance.equivalent_instances; base.rosetta.languoid.local_name; language.human_language.region
The output is: 
['language.human_language.main_country','language.human_language.countries_spoken_in','base.rosetta.languoid.parent']

Now you need to directly output relations highly related to the following question and its subobjectives in list format without other information or notes.
Q: """

answer_prompt = """Given a question and the associated retrieved knowledge graph triplets (entity, relation, entity), you are asked to answer the question with these triplets and your knowledge.

Here are five examples:
Q: Find the person who said \"Taste cannot be controlled by law\", what did this person die from?
Knowledge Triplets: Taste cannot be controlled by law., media_common.quotation.author, Thomas Jefferson
The output is:
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "Based on the given knowledge triplets, it's not sufficient to answer the entire question. The triplets only provide information about the person who said 'Taste cannot be controlled by law', which is Thomas Jefferson. To answer the second part of the question, it's necessary to have additional knowledge about where Thomas Jefferson's dead."
}

Q: The artist nominated for The Long Winter lived where?
Knowledge Triplets: The Long Winter, book.written_work.author, Laura Ingalls Wilder
Laura Ingalls Wilder, people.person.places_lived, Unknown-Entity
Unknown-Entity, people.place_lived.location, De Smet
The output is:
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "De Smet"
    },
    "R": "Based on the given knowledge triplets, the author of The Long Winter, Laura Ingalls Wilder, lived in De Smet."
}

Q: Who is the coach of the team owned by Steve Bisciotti?
Knowledge Triplets: Steve Bisciotti, sports.professional_sports_team.owner_s, Baltimore Ravens
Steve Bisciotti, sports.sports_team_owner.teams_owned, Baltimore Ravens
Steve Bisciotti, organization.organization_founder.organizations_founded, Allegis Group
The output is:
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "Based on the given knowledge triplets, the coach of the team owned by Steve Bisciotti is not explicitly mentioned. However, it can be inferred that the team owned by Steve Bisciotti is the Baltimore Ravens, a professional sports team. Therefore, additional knowledge about the current coach of the Baltimore Ravens can be used to answer the question."
}

Q: Rift Valley Province is located in a nation that uses which form of currency?
Knowledge Triplets: Rift Valley Province, location.administrative_division.country, Kenya
Rift Valley Province, location.location.geolocation, UnName_Entity
Rift Valley Province, location.mailing_address.state_province_region, UnName_Entity
Kenya, location.country.currency_used, Kenyan shilling
The output is:
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "Kenyan shilling"
    },
    "R": "Based on the given knowledge triplets, Rift Valley Province is located in Kenya, which uses the Kenyan shilling as its currency."
}

Q: The country with the National Anthem of Bolivia borders which nations?
Knowledge Triplets: National Anthem of Bolivia, government.national_anthem_of_a_country.anthem, UnName_Entity
National Anthem of Bolivia, music.composition.composer, Leopoldo Benedetto Vincenti
National Anthem of Bolivia, music.composition.lyricist, José Ignacio de Sanjinés
UnName_Entity, government.national_anthem_of_a_country.country, Bolivia
Bolivia, location.country.national_anthem, UnName_Entity
The output is:
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "Based on the given knowledge triplets, we can infer that the National Anthem of Bolivia is the anthem of Bolivia. Therefore, the country with the National Anthem of Bolivia is Bolivia itself. However, the given knowledge triplets do not provide information about which nations border Bolivia. To answer this question, we need additional knowledge about the geography of Bolivia and its neighboring countries."
}

Now you need to directly output the results of the following question in JSON format (must include "A" and "R") without other information or notes.
Q: """

prune_entity_prompt = """
Which entities in the following list ([] in Triples) can be used to answer question? Please provide the minimum possible number of entities, and strictly adhering to the constraints mentioned in the question. 
Here is an example:
Q: The movie featured Miley Cyrus and was produced by Tobin Armbrust?
Triplets: Tobin Armbrust film.producer.film ['The Resident', 'So Undercover', 'Let Me In', 'Begin Again', 'The Quiet Ones', 'A Walk Among the Tombstones']
Output: ['So Undercover']

Now you need to directly output the entities from [] in Triplets for the following question in list format without other information or notes.
Q: """

update_mem_prompt = """Based on the provided information (which may have missing parts and require further retrieval) and your own knowledge, output the currently known information required to achieve the subobjectives.
Here is an example:
Q: Find the person who said "Taste cannot be controlled by law", what did this person die from?
Subobjectives: ['Search the person who said "Taste cannot be controlled by law"', 'Search the cause of death for that person']
Memory: 
Knowledge Triplets: Taste cannot be controlled by law. media_common.quotation.author [Thomas Jefferson]
Output: {
    "1": "Thomas Jefferson said 'Taste cannot be controlled by law'.",
    "2": "It is not mentioned, and I also don't know."
}

Now you need to directly output the results of the following question in JSON format without other information or notes. 
Q: """


answer_depth_prompt = """Please answer the question based on the memory, related knowledge triplets and your knowledge.

Here are five example:
Q: Find the person who said \"Taste cannot be controlled by law\", what did this person die from?
Memory: {
    "1": "The triplet provides the information that Thomas Jefferson said this sentence.",
    "2": "No triplet provides this information."
}
Knowledge Triplets: Taste cannot be controlled by law., media_common.quotation.author, [Thomas Jefferson]
Output:
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "The person who said "Taste cannot be controlled by law," is Thomas Jefferson. It is still uncertain to answer the entire question"
}

Q: The artist nominated for The Long Winter lived where?
Memory: {
    "1": "The triplets provide the information that the author of The Long Winter is Laura Ingalls Wilder.",
    "2": "The triplets provide this information that Laura Ingalls Wilder lived in De Smet."
}
Knowledge Triplets: The Long Winter, book.written_work.author, [Laura Ingalls Wilder]
Laura Ingalls Wilder, people.person.places_lived, [Unknown-Entity]
Unknown-Entity, people.place_lived.location, [De Smet]
Output:
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "De Smet"
    },
    "R": "The author of The Long Winter is Laura Ingalls Wilder, and Laura Ingalls Wilder lived in De Smet."
}

Q: Who is the coach of the team owned by Steve Bisciotti?
Memory: {
    "1": "The triplets provide the information that Steve Bisciotti owns Baltimore Ravens.",
    "2": "No triplets provide the information."
}
Knowledge Triplets: Steve Bisciotti, sports.professional_sports_team.owner_s, [Baltimore Ravens]
Steve Bisciotti, sports.sports_team_owner.teams_owned, [Baltimore Ravens]
Steve Bisciotti, organization.organization_founder.organizations_founded, [Allegis Group]
Output:
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "The team owned by Steve Bisciotti is Baltimore Ravens based on knowledge triplets. The coach of the team owned by Steve Bisciotti is not explicitly mentioned."
}

Q: Rift Valley Province is located in a nation that uses which form of currency?
Memory: {
    "1": "The triplets provide the information that Rift Valley Province is located in Kenya.",
    "2": "The triplets provide the information that Kenya uses the Kenyan shilling as its currency."
}
Knowledge Triplets: Rift Valley Province, location.administrative_division.country, Kenya
Rift Valley Province, location.location.geolocation, UnName_Entity
Rift Valley Province, location.mailing_address.state_province_region, UnName_Entity
Kenya, location.country.currency_used, Kenyan shilling
Output:
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "Kenyan shilling"
    },
    "R": "Based on knowledge triplets, Rift Valley Province is located in Kenya, which uses the Kenyan shilling as its currency."
}

Q: The country with the National Anthem of Bolivia borders which nations?
Memory: {
    "1": "The triplets provide the information that the National Anthem of Bolivia is the anthem of Bolivia.",
    "2": "No triplets provide the information."
}
Knowledge Triplets: National Anthem of Bolivia, government.national_anthem_of_a_country.anthem, UnName_Entity
National Anthem of Bolivia, music.composition.composer, Leopoldo Benedetto Vincenti
National Anthem of Bolivia, music.composition.lyricist, José Ignacio de Sanjinés
UnName_Entity, government.national_anthem_of_a_country.country, Bolivia
Bolivia, location.country.national_anthem, UnName_Entity
Output:
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "Based on knowledge triplets, the National Anthem of Bolivia is the anthem of Bolivia. Therefore, the country with the National Anthem of Bolivia is Bolivia. However, the given knowledge triplets do not provide information about which nations border Bolivia."
}

Now you need to directly output the results of the following question in JSON format (must include "A" and "R") without other information or notes. If the triplets explicitly contains the answer to the question, prioritize the fact of the triplet over memory.
Q: """

judge_reverse = """Based on the current set of entities to be retrieved and the known information including memory and triplets, is it necessary to add additional entities for answering question?
Here are two examples:
Q: Which of the countries in the Caribbean has the smallest country calling code?
Entities set to be retrieved: ['Anguilla', 'Saint Lucia']
Memory: Caribbean contains Antilles and Saint Lucia
Knowledge Triplets: Caribbean, location.location.contains, ['Antilles', 'Saint Lucia']
Output: 
{
    "Add": "Yes",
    "Reason": "The entities set ignores other countries in Caribbean."
}

Q: The artist nominated for The Long Winter lived where?
Entities set to be retrieved: ['Laura Ingalls Wilder']
Memory: "The author of The Long Winter is Laura Ingalls Wilder."
Knowledge Triplets: The Long Winter, book.written_work.author, [Laura Ingalls Wilder]
Output: 
{
    "Add": "No",
    "Reason": "Now you need to search where Laura Ingalls Wilder lived."
}

Now you need to directly output the results of the following question in the JSON format (must include "Add" and "Reason") without other information or notes.
Q: """


add_ent_prompt = """Please select the fewest necessary entities to be retrieved for answering the Q from Candidate Entities, based on the current known information (Memory), the reason for additional retrieval, and your own knowledge.
Here is an example:
Q: Which of the countries in the Caribbean has the smallest country calling code?
Reason: The entities set ignores other countries in the Caribbean.
Candidate Entities: ['Saint Marie', 'Saint Martin (Island)', 'Viceroy Anguilla', 'Lesser Antilles', 'Barbados', 'British Virgin Islands', 'Leeward Islands', 'British West Indies', 'Caribbean', 'Saint Thomas', 'Bronte International University', 'Collectivity of Saint Martin', 'Southern Caribbean', 'University of Medicine and Health Sciences', 'Soufrière Hills', 'Lucayan Archipelago', 'University of the West Indies', 'Aureus University School of Medicine', 'North America', 'Netherlands Antilles', 'Puerto Rico', 'Chances Peak', 'Clarendon Parish', 'Saint Kitts and Nevis', 'Saint Lucia', 'Americas', 'Caribbean special municipalities of the Netherlands', 'Sandy Hill', 'School of Business and Computer Science, Trincity', 'School of Business and Computer Science, San Fernando', 'School of Business and Computer Science, Champs Fleurs', 'School of Business and Computer Science, Port of Spain', 'Bridgetown', 'St. Martinus University School of Medicine, main campus', 'Higher Institute of Medical Sciences. main campus', 'Grace University, main campus', 'Anguilla']
Memory: {
    "1": "The countries in the Caribbean are Antilles and Latin America.",
    "2": "The country calling codes for Antilles and Latin America are not mentioned.",
    "3": "It is not mentioned which country has the smallest country calling code."
}
Output: ['Barbados', 'Saint Lucia', 'Anguilla']

Now you need to directly output the results for the following Q in the list format without other information or notes.
Q: """


cot_prompt = """Please answer the question according to your knowledge step by step. Here is an example:
Q: What state is home to the university that is represented in sports by George Washington Colonials men's basketball?
The output is:
{
    "A": {
        "Known": "Yes",
        "Answer": "Washington, D.C."
    },
    "R": "First, the education institution has a sports team named George Washington Colonials men's basketball in is George Washington University , Second, George Washington University is in Washington D.C."
}

Please directly output the answer in JSON format (must include "A" and "R") without other information or notes.
"""
