subobjective_prompt = """请根据语义分析，将回答问题的过程分解为尽可能少的子目标。
以下是一个例子：
问题：Which of the countries in the Caribbean has the smallest country calling code?
输出：['搜索 Caribbean 地区的国家', '搜索每个 Caribbean 国家的国家呼叫代码', '比较国家呼叫代码，找出最小的一个']

现在，你需要直接以列表格式输出以下问题的子目标，不要包含其他信息或注释。
问题："""

sparql_system_prompt = """你是一个 SPARQL 大师，但你从没用过 Freebase 数据库。给定一个问题、相关子目标和起始节点（用英文逗号“,”分隔），要求你使用 SPARQL 语句在 Freebase 数据库中逐步查询给定问题的答案。在每一步推理中，你需要改进你的 SPARQL 语句继续进行下一步查询，或对问题进行回答。
如果你认为当前信息足以回答问题，你需要以 JSON 格式（必须包括 "A" 和 "R"，"A" 包括 "Sufficient" 与 "Answer"，为相关答案；"R" 为作此回答的理由）向上级程序输出问题的答案。注意答案必须按原样输出，如果无法回答，"Answer" 应为空字符串。
如果你仍要改进你的 SPARQL 语句，你需要以 JSON 格式（必须包括 "R"、"Q" 和 "isRel"，"R" 为查询的原因、查询语句的解释及下一步行动，"Q" 为对应的 SPARQL 语句，"isRel" 表示查询目标是否为关系）向上级程序输出改进方案。

以下是两个例子：
问题：Of the countries that are in the Caribbean, which has the Dutch Language as an official language?
子目标：['搜索 Caribbean 地区的国家', '搜索每个 Caribbean 国家的官方语言', '筛选官方语言为 Dutch 的国家']
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
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?name\\nWHERE {\\nns:m.0261m ns:location.location.contains ?country .\\n?country ns:location.country.official_language ns:m.02bv9 .\\n}",
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
子目标：['搜索 Steve Bisciotti 拥有的球队', '搜索 Steve Bisciotti 拥有的球队的教练']
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
    "Q": "PREFIX ns: <http://rdf.freebase.com/ns/>\\nSELECT DISTINCT ?name\\nWHERE {\\nns:m.06x8mf ns:sports.sports_team_owner.teams_owned ?team .\\n?team ns:american_football.football_team.current_head_coach ?coach .\\n}",
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
"""

init_sparql_prompt = """现在，你需要以 JSON 格式（必须包括 "R" 和 "Q"，"R" 为查询的原因、查询语句的解释及下一步行动，"Q" 为对应的 SPARQL 语句）直接输出以下问题的结果，不要包含其他信息或注释。查询过程中你的查询语句必须包含起始节点。
问题："""

next_query_prompt_head = """数据库返回了如下结果：
"""

next_query_prompt_tail = """
现在请你改进你的 SPARQL 语句继续进行下一步查询，或对问题进行回答。

如果你认为当前信息足以回答问题，你需要以 JSON 格式（必须包括 "A" 和 "R"，"A" 包括 "Sufficient" 与 "Answer"，为相关答案；"R" 为作此回答的理由）向上级程序输出问题的答案。注意答案必须按原样输出，如果无法回答，"Answer" 应为空字符串。
如果你仍要改进你的 SPARQL 语句，你需要以 JSON 格式（必须包括 "R"、"Q" 和 "isRel"，"R" 为查询的原因、查询语句的解释及下一步行动，"Q" 为对应的 SPARQL 语句，"isRel" 表示查询目标是否为关系）向上级程序输出改进方案。

现在请你给出 JSON 格式的回复，不包含任何其他信息或注释。注意改进过程中你的查询语句必须包含起始节点。
问题："""

extract_relation_prompt = """请从下列关系（用英文分号分隔）中提供尽可能少的与问题及其子目标高度相关的关系。关系必须按原样输出。
以下是一个例子：
问题：Name the president of the country whose main spoken language was Brahui in 1980?
子目标：['找出主要使用 Brahui 语言的国家', '查找每个国家的总统', '确定 1980 年以来的总统']
话题实体：Brahui Language
关系：language.human_language.main_country; language.human_language.language_family; language.human_language.iso_639_3_code; base.rosetta.languoid.parent; language.human_language.writing_system; base.rosetta.languoid.languoid_class; language.human_language.countries_spoken_in; kg.object_profile.prominent_type; base.rosetta.languoid.document; base.ontologies.ontology_instance.equivalent_instances; base.rosetta.languoid.local_name; language.human_language.region
输出为：
['language.human_language.main_country','language.human_language.countries_spoken_in','base.rosetta.languoid.parent']

现在，你需要以列表形式直接输出与以下问题及其子目标高度相关的关系，不要包含其他信息或注释。
问题："""

answer_prompt = """给定一个问题和检索到的相关的知识图谱三元组（实体、关系、实体），要求你用这些三元组和你的知识回答问题。答案必须按原样输出。

以下是五个例子：
问题：Find the person who said \"Taste cannot be controlled by law\", what did this person die from?
知识三元组：Taste cannot be controlled by law., media_common.quotation.author, Thomas Jefferson
输出为：
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "根据给出的知识三元组，不足以回答整个问题。三元组只提供了关于说过“Taste cannot be controlled by law”的人的信息，这个人就是 Thomas Jefferson。要回答问题的第二部分，有必要进一步了解 Thomas Jefferson 的死亡地点。"
}

问题：The artist nominated for The Long Winter lived where?
知识三元组：The Long Winter, book.written_work.author, Laura Ingalls Wilder
Laura Ingalls Wilder, people.person.places_lived, Unknown-Entity
Unknown-Entity, people.place_lived.location, De Smet
输出为：
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "De Smet"
    },
    "R": "根据所给的三元组知识，《The Long Winter》的作者 Laura Ingalls Wilder 住在 De Smet。"
}

问题：Who is the coach of the team owned by Steve Bisciotti?
知识三元组：Steve Bisciotti, sports.professional_sports_team.owner_s, Baltimore Ravens
Steve Bisciotti, sports.sports_team_owner.teams_owned, Baltimore Ravens
Steve Bisciotti, organization.organization_founder.organizations_founded, Allegis Group
输出为：
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "根据给定的知识三元组，没有明确提到 Steve Bisciotti 拥有的球队的教练。但是，可以推断出 Steve Bisciotti 拥有的球队是 Baltimore Ravens，这是一支职业运动队。因此，可以利用有关 Baltimore Ravens 现任教练的其他知识来回答问题。"
}

问题：Rift Valley Province is located in a nation that uses which form of currency?
知识三元组：Rift Valley Province, location.administrative_division.country, Kenya
Rift Valley Province, location.location.geolocation, UnName_Entity
Rift Valley Province, location.mailing_address.state_province_region, UnName_Entity
Kenya, location.country.currency_used, Kenyan shilling
输出为：
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "Kenyan shilling"
    },
    "R": "根据给定的知识三元组，Rift Valley 省位于 Kenya，该国使用 Kenyan shilling 作为货币。"
}

问题：The country with the National Anthem of Bolivia borders which nations?
知识三元组：National Anthem of Bolivia, government.national_anthem_of_a_country.anthem, UnName_Entity
National Anthem of Bolivia, music.composition.composer, Leopoldo Benedetto Vincenti
National Anthem of Bolivia, music.composition.lyricist, José Ignacio de Sanjinés
UnName_Entity, government.national_anthem_of_a_country.country, Bolivia
Bolivia, location.country.national_anthem, UnName_Entity
输出为：
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "根据给出的知识三元组，我们可以推断出《National Anthem of Bolivia》就是 Bolivia 的国歌。因此，国歌为《National Anthem of Bolivia》的国家就是 Bolivia 本身。然而，给定的知识三元组并没有提供哪些国家与 Bolivia 接壤的信息。要回答这个问题，我们需要更多有关 Bolivia 及其邻国的地理知识。"
}

现在，你需要以 JSON 格式（必须包括 "A" 和 "R"）直接输出以下问题的结果，不要包含其他信息或注释。
问题："""

prune_entity_prompt = """
下列列表（三元组中的 []）中哪些实体可用来回答问题？请提供尽可能少的实体，并严格遵守问题中提到的限制条件。实体必须按原样输出。
以下是一个例子：
问题：The movie featured Miley Cyrus and was produced by Tobin Armbrust?
三元组：Tobin Armbrust film.producer.film ['The Resident', 'So Undercover', 'Let Me In', 'Begin Again', 'The Quiet Ones', 'A Walk Among the Tombstones']
输出：['So Undercover']

现在，你需要以列表格式直接输出三元组 [] 中与下面问题相关的实体，不要包含其他信息或注释。
问题："""

update_mem_prompt = """根据提供的信息（可能有缺失部分，需要进一步检索）和自己的知识，输出实现子目标所需的当前已知信息。
以下是一个例子：
问题：Find the person who said "Taste cannot be controlled by law", what did this person die from?
子目标：['查找说过“Taste cannot be controlled by law”的人', '查询该人的死因']
记忆：
知识三元组：Taste cannot be controlled by law. media_common.quotation.author [Thomas Jefferson]
输出：{
    "1": "Thomas Jefferson 说过 “Taste cannot be controlled by law”。",
    "2": "没有提及，我也不知道。"
}

现在，你需要直接以 JSON 格式输出以下问题的结果，不要包含其他信息或注释。
问题："""


answer_depth_prompt = """请根据记忆、相关知识三元组和你的知识回答问题。答案必须按原样输出，或使用英文回答。

以下是五个例子：
问题：Find the person who said \"Taste cannot be controlled by law\", what did this person die from?
记忆：{
    "1": "三元组提供了 Thomas Jefferson 说过这句话的信息。",
    "2": "没有任何三元组提供这一信息。"
}
知识三元组：Taste cannot be controlled by law., media_common.quotation.author, [Thomas Jefferson]
输出：
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "说过“品味不能由法律控制”的人是 Thomas Jefferson。对整个问题的回答还不确定"
}

问题：The artist nominated for The Long Winter lived where?
记忆：{
    "1": "三元组提供的信息表明，《The Long Winter》的作者是 Laura Ingalls Wilder。",
    "2": "三元组提供的信息表明 Laura Ingalls Wilder 居住在 De Smet."
}
知识三元组：The Long Winter, book.written_work.author, [Laura Ingalls Wilder]
Laura Ingalls Wilder, people.person.places_lived, [Unknown-Entity]
Unknown-Entity, people.place_lived.location, [De Smet]
输出：
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "De Smet"
    },
    "R": "《The Long Winter》的作者是 Laura Ingalls Wilder，Laura Ingalls Wilder 住在 De Smet."
}

问题：Who is the coach of the team owned by Steve Bisciotti?
记忆：{
    "1": "三元组提供的信息表明，Steve Bisciotti 拥有 Baltimore Ravens。",
    "2": "没有任何三元组提供这一信息。"
}
知识三元组：Steve Bisciotti, sports.professional_sports_team.owner_s, [Baltimore Ravens]
Steve Bisciotti, sports.sports_team_owner.teams_owned, [Baltimore Ravens]
Steve Bisciotti, organization.organization_founder.organizations_founded, [Allegis Group]
输出：
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "Steve Bisciotti 拥有的球队是 Baltimore Ravens。没有明确提到 Steve Bisciotti 拥有的球队的教练。"
}

问题：Rift Valley Province is located in a nation that uses which form of currency?
记忆：{
    "1": "三元组提供的信息表明，Rift Valley 省位于 Kenya。",
    "2": "三元组提供的信息表明，Kenya 使用 Kenyan shilling 作为货币。"
}
知识三元组：Rift Valley Province, location.administrative_division.country, Kenya
Rift Valley Province, location.location.geolocation, UnName_Entity
Rift Valley Province, location.mailing_address.state_province_region, UnName_Entity
Kenya, location.country.currency_used, Kenyan shilling
输出：
{
    "A": {
        "Sufficient": "Yes",
        "Answer": "Kenyan shilling"
    },
    "R": "根据三元组的知识，Rift Valley 省位于 Kenya，该国使用 Kenyan shilling 作为货币。"
}

问题：The country with the National Anthem of Bolivia borders which nations?
记忆：{
    "1": "三元组提供的信息表明，《National Anthem of Bolivia》是 Bolivia 的国歌",
    "2": "没有任何三元组提供这一信息。"
}
知识三元组：National Anthem of Bolivia, government.national_anthem_of_a_country.anthem, UnName_Entity
National Anthem of Bolivia, music.composition.composer, Leopoldo Benedetto Vincenti
National Anthem of Bolivia, music.composition.lyricist, José Ignacio de Sanjinés
UnName_Entity, government.national_anthem_of_a_country.country, Bolivia
Bolivia, location.country.national_anthem, UnName_Entity
输出：
{
    "A": {
        "Sufficient": "No",
        "Answer": "Null"
    },
    "R": "根据知识三元组，《National Anthem of Bolivia》就是 Bolivia 的国歌。因此，拥有《National Anthem of Bolivia》的国家是 Bolivia。然而，给定的知识三元组并没有提供哪些国家与 Bolivia 接壤的信息。"
}

现在，你需要直接以 JSON 格式（必须包含 "A" 和 "R"）输出以下问题的结果，不要包含其他信息或注释。如果三元组明确包含问题的答案，则应优先考虑三元组提供的事实而不是记忆内容。
问题："""

judge_reverse = """根据当前要检索的实体集和已知信息（包括记忆和三元组），是否有必要为了回答问题而添加其他实体？
以下是两个例子：
问题：Which of the countries in the Caribbean has the smallest country calling code?
要检索的实体集：['Anguilla', 'Saint Lucia']
记忆：Caribbean 地区的国家包含 Antilles 和 Saint Lucia
知识三元组：Caribbean, location.location.contains, ['Antilles', 'Saint Lucia']
输出：
{
    "Add": "Yes",
    "Reason": "该实体集忽略了 Caribbean 地区的其他国家。"
}

问题：The artist nominated for The Long Winter lived where?
要检索的实体集：['Laura Ingalls Wilder']
记忆："《The Long Winter》的作者是 Laura Ingalls Wilder。"
知识三元组：The Long Winter, book.written_work.author, [Laura Ingalls Wilder]
输出：
{
    "Add": "No",
    "Reason": "现在需要搜索 Laura Ingalls Wilder 的居住地。"
}

现在，您需要以 JSON 格式（必须包括 "Add" 和 "Reason"）直接输出以下问题的结果，不要包含其他信息或注释。
问题："""


add_ent_prompt = """请根据当前的已知信息（记忆）、额外检索的原因和你自己的知识，从候选实体中选择最少的必要实体来回答问题。实体必须按原样输出。
以下是一个例子：
问题：Which of the countries in the Caribbean has the smallest country calling code?
理由：该实体集忽略了 Caribbean 地区的其他国家。
候选实体：['Saint Marie', 'Saint Martin (Island)', 'Viceroy Anguilla', 'Lesser Antilles', 'Barbados', 'British Virgin Islands', 'Leeward Islands', 'British West Indies', 'Caribbean', 'Saint Thomas', 'Bronte International University', 'Collectivity of Saint Martin', 'Southern Caribbean', 'University of Medicine and Health Sciences', 'Soufrière Hills', 'Lucayan Archipelago', 'University of the West Indies', 'Aureus University School of Medicine', 'North America', 'Netherlands Antilles', 'Puerto Rico', 'Chances Peak', 'Clarendon Parish', 'Saint Kitts and Nevis', 'Saint Lucia', 'Americas', 'Caribbean special municipalities of the Netherlands', 'Sandy Hill', 'School of Business and Computer Science, Trincity', 'School of Business and Computer Science, San Fernando', 'School of Business and Computer Science, Champs Fleurs', 'School of Business and Computer Science, Port of Spain', 'Bridgetown', 'St. Martinus University School of Medicine, main campus', 'Higher Institute of Medical Sciences. main campus', 'Grace University, main campus', 'Anguilla']
记忆：{
    "1": "Caribbean 地区的国家包含 Antilles 和 Saint Lucia",
    "2": "Antilles 和 Latin America 的国家呼叫代码未被提及。",
    "3": "没有提到哪个国家的国家电话代码最小。"
}
输出：['Barbados', 'Saint Lucia', 'Anguilla']

现在，您需要直接以列表格式输出以下问题的结果，不要包含其他信息或注释。
问题："""


cot_prompt = """请根据你的知识逐步回答问题。问题的答案必须为英文。以下是一个例子：
问题：What state is home to the university that is represented in sports by George Washington Colonials men's basketball?
输出为：
{
    "A": {
        "Known": "Yes",
        "Answer": "Washington, D.C."
    },
    "R": "首先，该教育机构有一支名为 George Washington Colonials 男子篮球队的运动队，它就是 George Washington University；其次，George Washington University 位于 Washington D.C.。"
}

请直接以 JSON 格式输出答案（必须包括 "A" 和 "R"），不要包含其他信息或注释。
"""
