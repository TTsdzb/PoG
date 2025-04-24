subobjective_prompt = """请根据语义分析，将回答问题的过程分解为尽可能少的子目标。
以下是一个例子：
问题：Which of the countries in the Caribbean has the smallest country calling code?
输出：['搜索 Caribbean 地区的国家', '搜索每个 Caribbean 国家的国家呼叫代码', '比较国家呼叫代码，找出最小的一个']

现在，你需要直接以列表格式输出以下问题的子目标，不要包含其他信息或注释。
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
