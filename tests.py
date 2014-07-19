test_strings = {
    # "ай-ай 1 кусает аистец 1    в   правая ступня, прокусывая кожа и повреждая":"",
#    "из железа индив выбор, дальн"
    "из красного дерева щитs/баклерs":"щиты/баклеры из красного дерева",
    "из ребра цереуса щитs/баклерs":"щиты/баклеры из ребра цереуса",
    "птица-носорог из кожи обувь":"обувь из кожи птицы-носорог",
    "гигантская летучая мышь кожа":"кожа гигантской летучей мыши",
    "гигантская полярная сова кожа":"кожа гигантской полярной совы",
    "гигантский белый аист кожа":"кожа гигантского белого аиста",
    "гигантский длиннохвостый попугай кожа":"кожа гигантского длиннохвостого попугая",
    "акула-молот кожа":"кожа акулы-молота",
    # "гнейс лестница вверх/вниз":"",
    "(гигантский пещерный паук из шёлка шапка)":"(шапка из шёлка гигантского пещерного паука)",
    "Заснеженный Густой овсяница":"Заснеженная густая овсяница",
    "Заснеженный конгламерат подъем":"Заснеженный подъем из конгламерата",
    "риз алевролита мемориалр":"≡алевролитовый мемориал≡",
    "трупs [2]":"трупы [2]",
    "из алевролита доспешная стойка":"алевролитовая доспешная стойка",
#    "сырой прудовая черепаха,♀"
    "(из меди кирки [3])":"(медные кирки [3])",
    "(из меди боевые топоры [3])":"(медные боевые топоры [3])",
    "(из висмутовой бронзы короткие мечи [3])":"(короткие мечи из висмутовой бронзы [3])",
    "(белый аист яйцо)":"(яйцо белого аиста)",
    "(приготовленные гигантский земляной червь кишки)":"(приготовленные кишки гигантского земляного червя)",
    "(приготовленные гигантский земляной цесарка кишки)":"(приготовленные кишки гигантской земляной цесарки)", # в игре нет, но для тестирования сойдет
    "як требуха":"требуха яка",
    "горный козёл из кожи":"кожа горного козла",
    "горный коза из кожи":"кожа горной козы",
    "гигантский земляной червь из кожи":"кожа гигантского земляного червя",
    "як из кожи":"кожа яка",
    "свинохвост из волокон ткань":"ткань из волокон свинохвоста",
    "древесина дуба брёвна":"дубовые брёвна",
    "большой шерлы":"большие шерлы",
    "большой желейные опалы":"большие желейные опалы",
    "(бриолетовый восковые опалы)":"(бриолетовые восковые опалы)",
    # "(большой восьмиугольной огранки горный хрусталь)":"",
    "большой, зазубренный из берёзы диски":"большие зазубренные берёзовые диски",
    "из висмутовой бронзы кольчуги":"кольчуги из висмутовой бронзы",
    "гигантский из висмутовой бронзы колья":"гигантские колья из висмутовой бронзы",
    "горный козёл из кожи доспехи":"доспехи из кожи горного козла",
    "(омутник из кожи плащи [3])":"(плащи из кожи омутника [3])",
    "(альпака из шерсти плащи [3])":"(плащи из шерсти альпаки [3])",
    "(овца из шерсти верёвкаs [3])":"(верёвки из шерсти овцы [3])",
    "(овца из шерсти пряжа)":"(пряжа из шерсти овцы)",
    "(большой таракан сукровица)":"(сукровица большого таракана)",
    "синий павлин кровь":"кровь синего павлина",
    "коза из копыт кольцоs":"кольца из копыт козы",
    "горный козёл из рогов кольцоs":"кольца из рогов горного козла",
    # "красная шпинель кольцоs":"кольца из красной шпинели",
#    "большой изысканные огненные опалы"
#    "(большой плоскогранный изысканный огненный опал)"
#    "большой яшмовые опалы"
#    "большой светло-жёлтые алмазы"
#    "из висмутовой бронзы кирки"
#    "из самородного серебра флейты-пикколо"
#    "гигантский из висмутовой бронзы лезвия топоров"
#    "гигантский из меди лезвия топоров"
#    "большой из золота горшки"
#    "большой из роговой обманки горшки"
#    "(большой из роговой обманки горшок)"
#    "из ясеня тренировочные топоры"
#    "(свинохвост из волокон левый перчатка)"
#    "(из висмутовой бронзы кольчужный рейтузы)"      
#    "(из железа кольчужный рейтузы)"
#    "(из берёзы стол)"
#    "риз берёзы гробр"
#    "(из берёзы стол)"
#    "*из берёзы гроб*"
#    "*из кремня статуя Vadane Tundraslips*"  
#    "горный козёл из рогов кольцоs"
#    "(прудовая черепаха из панциря амулет)"
#    "-прудовая черепаха из панциря кольцо-"
#    "прудовая черепаха из панциря кольцоs [2]"
#    "охотничий собака, ♀"    
#    "Ничей боевой собака (Ручной)"
#    "Ничей боевой собака, ♀(Ручной)"
#    "Xпрудовая черепаха из панциря шлемX"
#    "прудовая черепаха из панциря шлем"
#    "☼из кремня дверь☼"
#    "+из кремня механизмы+"
#    "-«+из кремня дверь+»-"
#    "+«риз кремня дверьр»+"
#    "(из меди боевой топор)"
#    "(из башнегриба бочка <#3>)"
#    "(чёрный песок мешок (свинохвост из волокон"
#    "(дварфийское пиво бочка (из ольхи"
#    "(дварфийское пиво бочка (из ольхи"
#    "(коричневый песок мешок (гигантский земляной червь из кожи"
#    "(лошадиное молоко бочка (из клёна"
#    "(споры толстошлемника мешок (вапитица из кожи"
#    "(семена сладкого стручка мешок (пещерный паук из шёлка"
#    "(Рыба бочка (из каштана"
#    "(Мясо бочка (из ивы"
#    "(Рыба бочка (из ребра цереуса"
#    "(Рыба бочка (из каштана) <#3>)"
#    "(Рыба бочка (из ребра цереуса) <#3>)"
#    "Густой полевица"
#    "Густой грамова трава"
#    "Редкий горец птичий"
#    "Редкий плевел"
#    "кремень галька"
#    "Мёртвый клён деревце"
#    "берёза деревце"
#    "жёлтый песок Стена"
#    "Густой грамова трава склон"
#    "кремень подъем"
#    "Густой из мятлик луговой подъем"
#    "Густой из морошки подъем"
#    "Заснеженный конгламерат подъем"
#    "Неотесанный дацит Стена"
#    "Неотесанный ониксовый опал Кластер"
#    "Заснеженный конгламерат валун"
#    "конгламерат склон"
#    "Густой белый высокогорный вереск подъем"
#    "Глинистый суглинок Стена"
#    "дацит склон"
#    "Густой куропаточья трава подъем"
#    "мотылёк останки"
#    "прудовая черепаха панцирь"
#    "{крыса останки}"
#    "{большой таракан останки}"
#    "большой таракан останки"
#    "Пятно росомаха кровь"
#    "тигровая яшма Пол Пещеры"
#    "кремень Пол Пещеры"
#    "розовый нефрит Пол Пещеры"
#    "Неотесанный тигровая яшма Кластер"
#    "Делать из хорошего пьютера Поделки"
#    "Кузница из висмутовой бронзы кольчуга"
#    "Кузница из железа булава"
#    "Кузница из железа арбалет"
#    "Кузница из железа копьё"
#    "Кузница из железа короткий меч"
#    "Кузница из железа боевой молот"
#    "Кузница из железа боевой топор"
#    "Кузница из железа кирка"
#    "Кузница из железа болты"
#    "Кузница из железа кольчуга"
#    "Кузница из железа нагрудник"
#    "Кузница из железа рейтузы"
#    "Кузница из железа поножи"
#    "Кузница из железа шапка"
#    "Кузница из железа шлем"
#    "Кузница из железа рукавица"
#    "Кузница из железа сапог"
#    "Кузница из железа ботинок"
#    "Кузница из железа щит"
#    "Кузница из железа баклер"
#    "Кузница из висмутовой бронзы нагрудник"
#    "Кузница из висмутовой бронзы рейтузы"
#    "Кузница из висмутовой бронзы поножи"
#    "Кузница из висмутовой бронзы сапог"
#    "Кузница из железа Наковальня"
#    "Делать из железа Поделки"
#    "Кузница из железа Кубок"
#    "Кузница из железа Инструмент"
#    "Кузница из железа гнездо"
#    "Кузница из железа Фляга"
#    "Чеканить из железа Монеты"
#    "Изготовить Механизмы"
#    "Кузница из адамантина башмак"
#    "Делать из адамантина Колчан"
#    "Кузница из железа бочка"
#    "Изготовить из железа доспешная стойка"
#    "Изготовить из железа ящик"
#    "Кузница из железа Секция трубы"
#    "Изготовить из железа Костыль"
#    "Кузница из железа Наконечники стрел баллисты"
#    "Огранить тигровая яшма"
#    "Огранить бурый железняк"
#    "кремень Лестница Вниз"
#    "кеа труп"
#    "Густой луговник Подъем"
#    "Заснеженный густой мятлик луговой Подъем"
#    "кремень галька"   
#    "известняк галька"
#    "известняк валун"
#    "Густой мюленбергия"
    "илистая глина лестница вниз":"Лестница вниз из илистой глины",
    "известняк лестница вниз":"Лестница вниз из известняка",
    "илистая глина лестница вверх":"Лестница вверх из илистой глины",
    "Инкрустировать Готовые товары с трубчатый агат":"Инкрустировать готовые товары трубчатым агатом",
    "Инкрустировать Готовые товары с розовый нефрит":"Инкрустировать готовые товары розовым нефритом",
    "Инкрустировать Готовые товары с халцедон":"Инкрустировать готовые товары халцедоном",
    # "(семена свинохвоста мешок (седой сурок из кожи":"",
    "из доломита крышка люка":"доломитовая крышка люка",
    "({большой из серебра кинжал})":"({большой серебряный кинжал})",
    "из железа утренняя звезда":"железная утренняя звезда",
    "чёрный медведь из кожи":"кожа чёрного медведя",
    "x(лиса из кожи штаны)x":"x(штаны из кожи лисы)x",
    "лиса из кожи":"кожа лисы",
    "(лама из кожи)":"(кожа ламы)",
    "(из бронзы болт)":"(бронзовый болт)",
    "из талька рычаг":"тальковый рычаг",
    "Густой морошка":"Густая морошка",
    "Заснеженный Густой морошка":"Заснеженная густая морошка",
    "Заснеженный Густой куропаточья трава":"Заснеженная густая куропаточья трава",
    "Заснеженный аргиллит валун":"Заснеженный валун из аргиллита",
    "Заснеженный Густой луговник подъем":"Заснеженный подъем из густого луговника",
    "сланец галька":"Галька из сланца",
    "сланец подъем":"Подъем из сланца",
    "Неотесанный самородное золото Стена":"Неотесанная стена из самородного золота",
    "Неотесанный бирюза Кластер":"Неотесанный кластер из бирюзы",
    # "Требуется 1 не используемый пряжа ткань.":"Требуется 1 не используемая ткань из пряжи.",
    # "Thikut Idenurist, варщик поташа прекращает Делать пряжа верёвка:":"Thikut Idenurist, варщик поташа прекращает делать веревку из пряжи:"
    " дварфы приостановили строительство Стена.":"Дварфы приостановили строительство стены.",
    " людской крепость Belrokalle":"Людская крепость Belrokalle",
    " людской селение ДукаХижер":"Людское селение Дукахижер",
    " дварфийский горный город КилрудОстач":"Дварфийский горный город Килрудостач",
    " эльфийский лесное убежище МелараПевюй":"Эльфийское лесное убежище Меларапевюй",
    " тёмный гоблинский крепость АслотТоксу":"Тёмная гоблинская крепость Аслоттоксу",
    " тёмный крепость АслотТоксу":"Тёмная крепость Аслоттоксу",
    " людской городок ЕбеМалстрал":"Людской городок Ебемалстрал",
    " людской гробница ДапенЦек":"Людская гробница Дапенцек",
    " лесное убежище Cinilidisa":"Лесное убежище Cinilidisa",
    " эльфийский лесное убежище Etathuatha":"Эльфийское лесное убежище Etathuatha",
    "durian wood ведроs":"durian wood вёдра",
    "(durian wood ведроs [3])":"(durian wood вёдра [3])",
    "(свинохвост из волокон мешокs [5])":"(мешки из волокон свинохвоста [5])",
    "(durian wood костыльы [3])":"(durian wood костыли [3])",
    "(durian wood шинаs [3])":"(durian wood шины [3])",
    
    # Clothier's shop
    'Делать ткань роба':'Шить робу из ткани',
    'Делать ткань туника':'Шить тунику из ткани',
    'Делать ткань рубаха':'Шить рубаху из ткани',
    'Делать ткань одежда':'Шить одежду из ткани',
    'Делать ткань мундир':'Шить мундир из ткани',
    'Делать ткань жилет':'Шить жилет из ткани',
    'Делать ткань плащ':'Шить плащ из ткани',
    'Делать ткань штаны':'Шить штаны из ткани',
    'Делать ткань шапка':'Шить шапку из ткани',
    'Делать ткань капюшон':'Шить капюшон из ткани',
    'Делать ткань перчатка':'Шить перчатку из ткани',
    'Делать ткань варежка':'Шить варежку из ткани',
    'Делать ткань носок':'Шить носок из ткани',
    'Делать ткань башмак':'Шить башмак из ткани',
    'Изготовить ткань мешок':'Шить мешок из ткани',
    'Делать ткань верёвка':'Вить верёвку из ткани',
    'Делать шёлк роба':'Шить шёлковую робу',
    'Делать шёлк туника':'Шить шёлковую тунику',
    'Делать шёлк рубаха':'Шить шёлковую рубаху',
    'Делать шёлк одежда':'Шить шёлковую одежду',
    'Делать шёлк мундир':'Шить шёлковый мундир',
    'Делать шёлк жилет':'Шить шёлковый жилет',
    'Делать шёлк плащ':'Шить шёлковый плащ',
    'Делать шёлк штаны':'Шить шёлковые штаны',
    'Делать шёлк шапка':'Шить шёлковую шапку',
    'Делать шёлк капюшон':'Шить шёлковый капюшон',
    'Делать шёлк перчатка':'Шить шёлковую перчатку',
    'Делать шёлк варежка':'Шить шёлковую варежку',
    'Делать шёлк носок':'Шить шёлковый носок',
    'Делать шёлк башмак':'Шить шёлковый башмак',
    'Изготовить шёлк мешок':'Шить шёлковый мешок',
    'Делать шёлк верёвка':'Вить шёлковую верёвку',
    'Делать пряжа роба':'Вязать робу из пряжи',
    'Делать пряжа туника':'Вязать тунику из пряжи',
    'Делать пряжа рубаха':'Вязать рубаху из пряжи',
    'Делать пряжа одежда':'Вязать одежду из пряжи',
    'Делать пряжа мундир':'Вязать мундир из пряжи',
    'Делать пряжа жилет':'Вязать жилет из пряжи',
    'Делать пряжа плащ':'Вязать плащ из пряжи',
    'Делать пряжа штаны':'Вязать штаны из пряжи',
    'Делать пряжа шапка':'Вязать шапку из пряжи',
    'Делать пряжа капюшон':'Вязать капюшон из пряжи',
    'Делать пряжа перчатка':'Вязать перчатку из пряжи',
    'Делать пряжа варежка':'Вязать варежку из пряжи',
    'Делать пряжа носок':'Вязать носок из пряжи',
    'Делать пряжа башмак':'Вязать башмак из пряжи',
    'Изготовить пряжа мешок':'Вязать мешок из пряжи',
    'Делать пряжа верёвка':'Вить верёвку из пряжи',
    '(вомбат из кожи башмак)!':'(башмак из кожи вомбата)!',
    
    # Werebeasts
    'Ura Wuspinicen, былимуравьед':'Ura Wuspinicen, муравьед-оборотень',
    # ' былимуравьед крепко держится!':'Муравьед-оборотень крепко держится!',
    
    'Неотесанный из каменной соли Стена':'Неотесанная стена из каменной соли',
    'Влажный Неотесанный из каменной соли Стена':'Влажная неотесанная стена из каменной соли',
    
    # @todo:
    # '{сипуха левая голень}':'{левая голень сипухи}',
    '{сипуха голень}':'{голень сипухи}',
    'сипуха искалеченный труп':'Искалеченный труп сипухи',
    
    "Udil Vuthiltobul стал рекрут.":"Udil Vuthiltobul стал рекрутом.",
    "Udil Vuthiltobul стал рыбник.":"Udil Vuthiltobul стал рыбником.",
    # "Животное вырос и стал Ничей козёл.":"Животное выросло и стало ничьим козлом.",
    
    # "ладонь с его левое предплечье!":"ладонь своим левым предплечьем!"
    
    # "({малый гигантский пещерный паук из шёлка набедренная повязка})":"({маленькая набедренная повязка из ш1лка гигантского пещерного паука})"
}
