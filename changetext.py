import sys
sys.stderr = open('changetext.err', 'w', 1)

phrases = {
    'Slaves to Armok:  God of Blood':'Рабы Армока - бога крови',
    'Chapter II: Dwarf Fortress':'Глава II: Крепость дварфов',
    'Жмите ':'Нажмите ',
    'прокрутка':'для прокрутки',
    'Programmed by Tarn Adams':'Программирование - Тарн Адамс',
    'Designed by Tarn and Zach Adams':'Дизайн - Тарн Адамс и Зак Адамс',
    'Visit Bay 12 Games':'Посетите Bay 12 Games',
    
    'Welcome to the alpha of Dwarf Fortress.':
        'Добро пожаловать в альфа-версию Dwarf Fortress.',
    'As there has been some time between releases, instability is to be expected.':
        'Поскольку между релизами прошло некоторое время, возможна нестабильность.',
    'Report crashes, hangs, lags, bugs and general disappointment at the forums.':
        'Сообщайте о вылетах, зависаниях, тормозах, багах и прочем на форумах',
    'They are at our website, bay12games.com.  Check there for updates.':
        'на нашем вебсайте bay12games.com.  Следите за обновлениями.',
    'You can also find an older yet more stable version of the game there.':
        'Там же вы можете найти более старые и стабильные версии игры.',
    'As of June 2012, you can get help at the fan-created dwarffortresswiki.org.':
        'Кроме того, вы можете получить помощь на dwarffortresswiki.org.',
    'Please make use of and contribute to this valuable resource.':
        'Пожалуйста, пользуйтесь и вносите свой вклад в этот ценный ресурс.',
    'If you enjoy the game, please consider supporting Bay 12 Games.':
        'Если игра вам понравилась, подумайте над тем, чтобы поддержать Bay 12 Games.',
    'There is more information at our web site and in the readme file.':
        'Дополнительную информацию вы можете получить на нашем веб сайте и в файле readme.',
        
    'Dwarf Fortress':'Крепость дварфов',
    'Adventurer':'Приключение',
    'Legends':'Легенды',
    'Пова':'Готовить', 
    'Вари':'Пиво', 
    'готовая едаs':'готовая еда',
    'питьёs':'питьё',
    'ведроs':'вёдра',
    'верёвкаs':'верёвки', 
    'шинаs':'шины',
    'костыльы':'костыли',
    'колчанs':'колчаны',
    'рюкзакs':'рюкзаки',
    'наковальняs':'наковальни',
    'доспешная стойкаs':'доспешные стойки',
    'оружейная стойкаs':'оружейные стойки',
    'дверьs':'двери',
    'шлюзs':'шлюзы',
    'кроватьs':'кровати',
    'тронs':'троны',
    'стулs':'стулья',
    'гробs':'гробы',
    'статуяs':'статуи',
    'дублёная шкураs':'дублёные шкуры',
    'большой самоцветs':'большие самоцветы',
    'монетаs':'монеты',
    'небольшое ручное животноеs':'небольшие ручные животные',
    'небольшое животноеs':'небольшие животные',
    'крышка люкаs':'крышки люка',
    'монетаs':'монеты',
    'решёткаs':'решётки',
    'ручная мельницаs':'ручные мельницы',
    'жёрновs':'жернова',
    'окноs':'окна',
    'ловушка для животныхs':'ловушки для животных',
    'цепьs':'цепи',
    'клеткаs':'клетки',
    'контейнерs':'контейнеры',
    'ящикs':'ящики',
    'бочкаs':'бочки',
    'часть ловушкиs':'части ловушек',
    'флягаs':'фляги',
    'кубокs':'кубки',
    'игрушкаs':'игрушки',
    'инструментs':'инструменты',
    'музыкальный инструментs':'музыкальные инструменты',
    'статуэткаs':'статуэтки',
    'амулетs':'амулеты',
    'скипетрs':'скипетры',
    'коронаs':'короны',
    'кольцоs':'кольца',
    'серьгаs':'серьги',
    'браслетs':'браслеты',
    'наконечник стрелы баллистыs':'наконечники стрелы баллисты',
    'тотемs':'тотемы',
    'трупs':'трупы',
    'часть телаs':'части тела',
    'конечность/тело гипсs':'гипс для конечносте тела',
    'мемориалs':'мемориалы', 
    'шкафs':'шкафы',
    'столs':'столы', 
    'сырой рыба':'свежая рыба', 
    'оружиеs':'оружие',
    'щитs/баклерs':'щиты/баклеры',
    'мешокs':'мешки',
    'дварфийское пиво':'дварфийского пива',
    'дварфийское вино':'дварфийского вина',
    'дварфийский эль':'дварфийского эля',
    'Раст.':'растений',
    'дварфийский ром':'дварфийского рома',
    'ларецs':'ларцы',
    'кружкаs':'кружки',
    'макакарезус':'макака-резус',
    'капканs':'капканы',
    'тракционный столы':'тракционные столы',
    'миникузница':'мини-кузница',
    'миникузницы':'мини-кузницы',
    'Кучка ил':'Кучка ила',
    'Пыль ил':'Остатки ила',
    'из самородного алюминия':'самородный алюминий',
    'из необработанного адаманита':'необработанный адаманит',
    'кожа щитs/баклерs':'щиты/баклеры из кожи',
    'кожа броня':'броня из кожи',
    'кожа головной убор':'головной убор из кожи',
    'кожа брюки':'брюки из кожи',
    'кожа перчатки':'перчатки из кожи',
    'кожа обувь':'обувь из кожи',
    'кожа доспехи':'доспехи из кожи',
    'металл щитs/баклерs':'щиты/баклеры из металла',
    'металл броня':'броня из металла',
    'металл головной убор':'головной убор из металла',
    'металл брюки':'брюки из металла',
    'металл перчатки':'перчатки из металла',
    'металл обувь':'обувь из металла',
    'повозка дерево':'дерево повозки',
    'из жёлтого песка':'Жёлтый песок',
    'Мастерская механика':'Мастерская механика',
    'Изготовить механизмы':'Изготовить механизмы',
    'Делать каменный механизм':'Делать каменный механизм',
    
# мастерская каменщика
    'Изготовить камень дверь':'Делать дверь из камня',
    'Изготовить камень Блоки':'Делать блоки из камня',
    'Изготовить камень доспешная стойка':'Делать доспешную стойку из камня',
    'Изготовить камень трон':'Делать трон из камня',
    'Изготовить камень гроб':'Делать гроб из камня',
    'Изготовить камень Люк':'Делать люк из камня',
    'Изготовить камень Решетка':'Делать решетку из камня',
    'Изготовить камень шкаф':'Делать шкаф из камня',
    'Изготовить камень ларец':'Делать ларец из камня',
    'Изготовить камень шлюз':'Делать шлюз из камня',
    'Изготовить камень Статуя':'Делать статую из камня',
    'Изготовить камень мемориал':'Делать мемориал из камня',
    'Изготовить камень стол':'Делать стол из камня',
    'Изготовить камень оружейная стойка':'Делать оружейную стойку из камня',
    'Изготовить камень Ручная мельница':'Делать ручную мельницу из камня',
    'Изготовить камень Жернов':'Делать жернов из камня',
    
# мастерская столяра
    'Делать деревянный тренировочное копьё':'Делать деревянное тренировочное копьё',
    'Делать деревянный тренировочный меч':'Делать деревянное тренировочный меч',
    'Делать деревянный тренировочный топор':'Делать деревянный тренировочный топор',
    'Делать деревянный бочка':'Делать деревянную бочку',
    'Изготовить деревянный блоки':'Делать деревянные блоки',
    'Делать деревянный ведро':'Делать деревянное ведро',
    'Делать деревянный ловушка для животных':'Делать деревянную ловушку для животных',
    'Делать деревянный клетка':'Делать деревянную клетку',
    'Изготовить деревянный доспешная стойка':'Изготовить деревянную доспешную стойку',
    'Изготовить деревянный кровать':'Делать деревянную кровать',
    'Изготовить деревянный дверь':'Делать деревянную дверь',
    'Изготовить деревянный Шлюз':'Делать деревянный шлюз',
    'Изготовить деревянный Люк':'Делать деревянный люк',
    'Изготовить деревянный Решетка':'Делать деревянную решетку',
    'Изготовить деревянный оружейная стойка':'Делать деревянную оружейную стойку',
    'Делать деревянный вагонетка':'Делать деревянную вагонетку',
    'Делать деревянный тачка':'Делать деревянную тачку',
    'Делать деревянный Секция трубы':'Делать деревянную секцию трубы',
    'Изготовить деревянный Шина':'Делать деревянную шину',
    'Изготовить деревянный Костыль':'Делать деревянный костыль',
    
# мастерская ремесленника
    'Ремесленник мастерская':'Мастерская ремесленника',
    'Украшать панцирь':'Украшать панцирь',
    'Украшать кость':'Украшать кость',
    'Делать камень поделки':'Делать поделки из камня',
    'Делать камень кружка':'Делать каменную кружку',
    'Делать камень инструмент':'Делать каменный инструмент',
    'Делать камень короткий меч':'Делать каменный короткий меч',
    'Делать камень гнездо':'Делать каменное гнездо',
    'Делать камень кувшин':'Делать каменный кувшин',
    'Делать камень горшок':'Делать каменный горшок',
    'Делать камень улей':'Делать каменный улей',
    'Делать камень игрушка':'Делать каменную игрушку',
    'Делать деревянный Поделки':'Делать поделки из дерева',
    'Делать деревянный болты':'Делать деревянные болты',
    'Делать деревянный гнездо':'Делать деревянное гнездо',
    'Делать деревянный кувшин':'Делать деревянный кувшин',
    'Делать кость болты':'Делать болты из кости',
    'Делать кость Поделки':'Делать поделки из кости',
    'Делать кость рейтузы':'Делать рейтузы из кости',
    'Делать кость поножи':'Делать поножи из кости',
    'Делать кость рукавица':'Делать рукавицу из кости',
    'Делать кость шлем':'Делать шлем из кости',
    'Делать панцирь Поделки':'Делать поделки из панциря',
    'Делать панцирь рейтузы':'Делать рейтузы из панциря',
    'Делать панцирь рукавица':'Делать рукавицу из панциря',
    'Делать панцирь шлем':'Делать шлем из панциря',
    'Украшать слоновая кость/зуб':'Украшать слоновую кость/зуб',
    'Делать ткань Поделки':'Делать поделки из ткани',
    'Делать шелк Поделки':'Делать поделки из шелка',
    'Делать пряжа Поделки':'Делать поделки из пряжи',
    'Делать слоновая кость/зуб Поделки':'Делать поделки из слоновой кости/зуба',
    'Делать рог Поделки':'Делать поделки из рога',
    'Делать жемчуг Поделки':'Делать поделки из жемчуга',
    'Делать кожа Поделки':'Делать поделки из кожи',
    'Выполняется в ремесленник мастерская':'Выполняется в мастерской ремесленника',
    
# мастерская лучника
    'Делать кость арбалет':'Делать арбалет из кости',
    
# дубильня
    'Выполняется в Дубильня':'Выполняется в дубильне',
    
# мыловарня
    'Выполняется в Мастерская мыловара':'Выполняется в Мастерской мыловара',
    
# осадная мастерская
    'Изготовить Части баллисты':'Изготовить части балисты',
    'Собрать из железа стрела баллисты':'Собрать железную стрелу баллисты',
    'Собрать из серебра стрела баллисты':'Собрать серебрянную стрелу баллисты',
    'Собрать из меди стрела баллисты':'Собрать медную стрелу баллисты',
    'Собрать из бронзы стрела баллисты':'Собрать бронзовую стрелу баллисты',
    'Собрать из стали стрела баллисты':'Собрать стальную стрелу баллисты',
    'Собрать из висмутовой бронзы стрела баллисты':'Собрать стрелу баллисты из висмутовой бронзы',
    'Собрать из адаманита стрела баллисты':'Собрать адаманитовую стрелу баллисты',
    'Собрать деревянную стрела баллисты':'Собрать деревянную стрелу баллисты',
    
# кожевня
    'Делать кожа доспех':'Делать кожаный доспех',
    'Делать кожа роба':'Делать кожаную роба',
    'Делать кожа одежда':'Делать кожаную одежду',
    'Делать кожа мундир':'Делать кожаный мундир',
    'Делать кожа жилет':'Делать кожаный жилет',
    'Делать кожа плащ':'Делать кожаный плащ',
    'Делать кожа рейтузы':'Делать кожаные рейтузы',
    'Делать кожа штаны':'Делать кожаные штаны',
    'Делать кожа шлем':'Делать кожаный шлем',
    'Делать кожа шапка':'Делать кожаную шапку',
    'Делать кожа капюшон':'Делать кожаный капюшон',
    'Делать кожа перчатка':'Делать кожаную перчатку',
    'Делать кожа варежка':'Делать кожаную варежку',
    'Делать кожа сапог':'Делать кожаный сапог',
    'Делать кожа ботинок':'Делать кожаный ботинок',
    'Делать кожа башмак':'Делать кожаный башмак',
    'Делать кожа щит':'Делать кожаный щит',
    'Делать кожа баклер':'Делать кожаный баклер',
    'Делать кожа мешок':'Делать кожаный мешок',
    'Делать кожа Бурдюк':'Делать кожаный бурдюк',
    'Делать кожа Рюкзак':'Делать кожаный рюкзак',
    'Делать кожа Колчан':'Делать кожаный колчан',
    'Вышивать кожа Изображение':'Вышить изображение на коже',
    
# плавильня
    'Плавка из магнетита Руда':'Плавить руду из магнетита',
    'Плавка из самородного алюминия Руда':'Плавить руду из самородного алюминия',
    'Плавка из красного железняка Руда':'Плавить руду из красного железняка',
    'Плавка из бурого железняка Руда':'Плавить руду из бурого железняка',
    'Плавка из гарниерита Руда':'Плавить руду из гарниерита',
    'Плавка из самородного золото Руда':'Плавить руду из самородного золота',
    'Плавка из самородного серебра Руда':'Плавить руду из самородного серебра',
    'Плавка из самородного меди Руда':'Плавить руду из самородной меди',
    'Плавка из малахита Руда':'Плавить руду из малахита',
    'Плавка из галенита Руда':'Плавить руду из галенита',
    'Плавка из сфалерита Руда':'Плавить руду из сфалерита',
    'Плавка из касситерита Руда':'Плавить руду из касситирита',
    'Плавка из самородной платины Руда':'Плавить руду из самородной платины',
    'Плавка из тетраэдрита Руда':'Плавить руду из тетраэдрита',
    'Плавка из рогового серебра Руда':'Плавить руду из рогового серебра',
    'Плавка из висмутина Руда':'Плавить руду из висмутина',
    
# Печь для обжига
    'Глазировать большой глиной/каменный горшок':'Глазировать глиной/большой каменный горшок',

# Лавка портного
    'Делать ткань роба':'Шить робу из ткани',
    'Делать ткань рубаха':'Шить рубаху из ткани',
    'Делать ткань одежда':'Шить одежду из ткани',
    'Делать ткань мундир':'Шить мундир из ткани',
    'Делать ткань жилет':'Шить жилет из ткани',
    'Делать ткань плащ':'Шить плащ из ткани',
    'Делать ткань штаны':'Шить штаны из ткани',
    'Делать ткань шапка':'Шить шапка из ткани',
    'Делать ткань капюшон':'Шить капюшон из ткани',
    'Делать ткань перчатка':'Шить перчатку из ткани',
    'Делать ткань варежка':'Шить варежку из ткани',
    'Делать ткань носок':'Шить носок из ткани',
    'Делать ткань башмак':'Шить башмак из ткани',
    'Делать ткань мешок':'Делать мешок из ткани',
    'Делать ткань Верёвка':'Вить верёвку из ткани',
    'Вышивать ткань Изображение':'Вышить изображение тканью',
    
    'Делать шелк роба':'Шить робу из шелка',
    'Делать шелк рубаха':'Шить рубаху из шелка',
    'Делать шелк одежда':'Шить одежду из шелка',
    'Делать шелк мундир':'Шить мундир из шелка',
    'Делать шелк жилет':'Шить жилет из шелка',
    'Делать шелк плащ':'Шить плащ из шелка',
    'Делать шелк штаны':'Шить штаны из шелка',
    'Делать шелк шапка':'Шить шапка из шелка',
    'Делать шелк капюшон':'Шить капюшон из шелка',
    'Делать шелк перчатка':'Шить перчатку из шелка',
    'Делать шелк варежка':'Шить варежку из шелка',
    'Делать шелк носок':'Шить носок из шелка',
    'Делать шелк башмак':'Шить башмак из шелка',
    'Делать шелк мешок':'Делать мешок из шелка',
    'Делать шелк Верёвка':'Вить верёвку из шелка',
    'Вышивать шелк Изображение':'Вышить изображение шелком',
    
    'Делать шелк роба':'Вязать робу из пряжи',
    'Делать пряжа рубаха':'Вязать рубаху из пряжи ',
    'Делать пряжа одежда':'Вязать одежду из пряжи',
    'Делать пряжа мундир':'Вязать мундир из пряжи',
    'Делать пряжа жилет':'Вязать жилет из пряжи',
    'Делать пряжа плащ':'Вязать плащ из пряжи',
    'Делать пряжа штаны':'Вязать штаны из пряжи',
    'Делать пряжа шапка':'Вязать шапка из пряжи',
    'Делать пряжа капюшон':'Вязать капюшон из пряжи',
    'Делать пряжа перчатка':'Вязать перчатку из пряжи',
    'Делать пряжа варежка':'Вязать варежку из пряжи',
    'Делать пряжа носок':'Вязать носок из пряжи',
    'Делать пряжа башмак':'Вязать башмак из пряжи',
    'Делать пряжа мешок':'Вязать мешок из пряжи',
    'Делать пряжа Верёвка':'Вить верёвку из пряжи',
    'Вышивать пряжа Изображение':'Вязать изображение из пряжи',
    
# Кузница
    'Ковать гигантский из железа лезвие топора':'Ковать из железа гигантское лезвие топора',
    'Ковать огромный из железа винт':'Ковать из железа огромный винт',
    'Ковать шированный из железа шар':'Ковать из железа шированный шар',
    'Ковать большой, зазубренный из железа диск':'Ковать из железа большой и зазубренный  диск',
    'Ковать заточенный из железа кол':'Ковать из железа заточенный кол', 
    
    'Ковать гигантский из серебра лезвие топора':'Ковать из серебра гигантское лезвие топора',
    'Ковать огромный из серебра винт':'Ковать из серебра огромный винт',
    'Ковать шированный из серебра шар':'Ковать из серебра шированный шар',
    'Ковать большой, зазубренный из серебра диск':'Ковать из серебра большой и зазубренный  диск',
    'Ковать заточенный из серебра кол':'Ковать из серебра заточенный кол', 
    
    'Ковать гигантский из меди лезвие топора':'Ковать из меди гигантское лезвие топора',
    'Ковать огромный из меди винт':'Ковать из меди огромный винт',
    'Ковать шированный из меди шар':'Ковать из меди шированный шар',
    'Ковать большой, зазубренный из меди диск':'Ковать из меди большой и зазубренный  диск',
    'Ковать заточенный из меди кол':'Ковать из меди заточенный кол',
        
    'Ковать гигантский из бронзы лезвие топора':'Ковать из бронзы гигантское лезвие топора',
    'Ковать огромный из бронзы винт':'Ковать из бронзы огромный винт',
    'Ковать шированный из бронзы шар':'Ковать из серебра шированный шар',
    'Ковать большой, зазубренный из бронзы диск':'Ковать из бронзы большой и зазубренный  диск',
    'Ковать заточенный из бронзы кол':'Ковать из бронзы заточенный кол', 
    
    'Ковать гигантский из стали лезвие топора':'Ковать из стали гигантское лезвие топора',
    'Ковать огромный из стали винт':'Ковать из стали огромный винт',
    'Ковать шированный из стали шар':'Ковать из стали шированный шар',
    'Ковать большой, зазубренный из стали диск':'Ковать из стали большой и зазубренный  диск',
    'Ковать заточенный из стали кол':'Ковать из стали заточенный кол',
    
    'Ковать гигантский из висмутовой бронзы лезвие топора':'Ковать из висмутовой бронзы гигантское лезвие топора',
    'Ковать огромный из висмутовой бронзы винт':'Ковать из висмутовой бронзы огромный винт',
    'Ковать шированный из висмутовой бронзы шар':'Ковать из висмутовой бронзы шированный шар',
    'Ковать большой, зазубренный из висмутовой бронзы диск':'Ковать из висмутовой бронзы большой и зазубренный  диск',
    'Ковать заточенный из висмутовой бронзы кол':'Ковать из висмутовой бронзы заточенный кол',
    
    'Ковать гигантский из адаманита лезвие топора':'Ковать из адаманита гигантское лезвие топора',
    'Ковать огромный из адаманита винт':'Ковать из адаманита огромный винт',
    'Ковать шированный из адаманита шар':'Ковать из адаманита шированный шар',
    'Ковать большой, зазубренный из адаманита диск':'Ковать из адаманита большой и зазубренный  диск',
    'Ковать заточенный из адаманита кол':'Ковать из адаманита заточенный кол',

#Стекловареннная печь
    'Делать грубый зеленое стекло':'Варить грубое зеленое стекло',
    'Делать грубый бесцветное стекло':'Варить грубое бесцветное стекло',
    'Делать грубый хрусталь':'Варить грубый хрусталь',
}



#оружие
############################################################################



adjectives = {
#металл
   'из меди':('медный','медная','медное','медные'),
   'из железа':('железный','железная','железное','железные'),
   'из серебра':('серебряный','серебряная','серебряное','серебряные'),
   'из бронзы':('бронзовый','бронзовая',"бронзовое","бронзовые"),
   'из стали':('стальной',"стальной","стальное","стальные"),
   'из золота':('золотой',"золотая","золотое","золотые"),
   'из никеля':('никелевый',"никелевая","никилевое","никелевые"),
   'из цинка':('цинковый',"цинковая","цинковое","цинковые"),
   'из латуни':('латунный',"латунная","латунное","латунные"),
   'из стали':('стальной',"стальная","стальное","стальные"),
   'из чугуна':('чугунный',"чугунная","чугунное","чугунные"),
   'из платины':('платинный',"платиновая","платиновое","платиновые"),
   'из электрума':('электрумный',"электрумная","электрумное","электрумные"),
   'из олова':('оловянный',"оловянная","оловянное","оловянные"),
   'из свинца':('свинцовый',"свинцовая","свинцовое","свинцовые"),
   'из алюминия':('алюминиевый',"алюминиевая","алюминиевое","алюминиевые"),
   'из нейзильбора':('нейзильборовый',"нейзильборовая","нейзильборовое","нейзильборовые"),
   'из биллона':('билонный',"билонная","билонное","билонные"),
   'из стерлинга':('стерлинговый',"стерлинговая","стерлинговое","стерлинговые"),
   'из висмута':('висмутовый',"висмутовая","висмутовое","висмутовые"),
   'из адамантина':('адамантиновый',"адамантиновая","адамантиновое","адамантиновые"),
#  дерево             
   'из сосны':('сосновый',"сосновая","сосновое","сосновые"),
   'из кедра':('кедровый',"кедровая","кедровое","кедровые"),
   'из дуба':('дубовый',"дубовая","дубовое","дубовые"),
   'из акации':('акациевый',"акациевая","акациевое","акациевые"), # не очень благозвучно
   'из клёна':('кленовый',"кленовая","кленовое","кленовые"),
   'из ивы':('ивовый',"ивавая","ивовое","ивовые"),
   'из башнегриба':('башнегрибовый',"башнегрибовая","башнегрибовое","башнегрибовые"),
   'из черношляпника':('черношляпниковый',"черношляпниковая","черношляпниковое","черношляпниковые"),
   'из нижнешляпника':('нижнешляпниковый',"нижнешляпниковая","нижнешляпниковое","нижнешляпниковые"),
   'из гоблошляпника':('гоблошляпниковый',"гоблошляпниковая","гоблошляпниковое","гоблошляпниковые"),
   'из древогриба':('древогрибовый',"древогрибовая","древогрибовое","древогрибовые"),
   'из кривошипника':('кривошипниковый',"кривошипниковая","кривошипниковое","кривошипниковые"),
   'из глампронга':('глампронговый',"глампронговая","глампронговое","глампронговые"),
   'из цереуса':('цереусные',"цереусная","цереусное","цереусные"),
   'из мангров':('мангровый',"мангровая","мангровое","мангровые"),
   'из пальмы':('пальмовый',"пальмовая","пальмовое","пальмовые"),
   'из гевеи':('гевейный',"гевейная","гевейное","гевейные"),
   'из вышедрева':('вышедревный',"вышедревная","вышедревное","вышедревные"),
   'из лиственницы':('лиственничный',"лиственничная","лиственничное","лиственничные"),
   'из каштана':('каштановый',"каштановая","каштановое","каштановые"),
   'из ольхи':('ольховый',"ольховая","ольховое","ольховые"),
   'из берёзы':('берёзовый',"берёзовая","берёзовое","берёзовые"),
   'из ясеня':('ясеневый',"ясеневая","ясеневое","ясеневые"),
   'из лумбанга':('лумбанговый',"лумбанговая","лумбанговое","лумбанговые"),
   
#неорганическое
   'из кремня':('кремневый','кремневая',"кремневое","кремневые"),
   'из аргиллита':('аргилитовый',"аргилитовая","аргилитовое","аргилитовые"),
   'из песчаника':('песчаниковый',"песчаниковая","песчаниковое","песчаниковые"),
   'из алевролита':('алевролитовый',"алевролитовая","алевролитовое","алевролитовые"),
   'из сланца':('сланцевый',"сланцевая","сланцевое","сланцевые"),
   'из известняка':('известняковый',"известняковая","известняковое","известняковые"),
   'из конгломерата':('конгломератный',"конгломератная","конгломератное","конгломератные"),
   'из доломита':('доломитовый',"доломитовая","доломитовое","доломитовые"),
   'из мела':('меловый',"меловая","меловое","меловые"),
   'из гранита':('гранитный',"гранитная","гранитное","гранитные"),
   'из диорита':('диоритовый',"диоритовая","диоритовое","диоритовые"),
   'из габбро':('габбровый',"габбровая","габбровое","габбровые"),
   'из риолита':('риолитовый',"риолитовая","риолитовое","риолитовые"),
   'из базальта':('базальтовый',"базальтовая","базальтовое","базальтовые"),
   'из андезита':('андезитовый',"андезитовая","андезитовое","андезитовые"),
   'из дацита':('дацитовый',"дацитовая","дацитовое","дацитовые"),
   'из обсидиана':('обсидиановый',"обсидиановая","обсидиановое","обсидиановые"),
   'из кварцита':('кварцитовый',"кварциовая","кварцитовое","кварцитовые"),
   'из филита':('филитовый',"филитовая","филитовое","филитовые"),
   'из гнейса':('гнейсовый',"гнейсовая","гнейсовое","гнейсовые"),
   'из мрамора':('мраморный',"мраморная","мраморное","мраморные")
}

masculine = 0 # м. род
feminine = 1 # ж. род
neuter = 2 # ср. род
plural = 3 # мн. ч.

weapon_gender = {
# masculine
    "топор":masculine, "щит":masculine, "баклер":masculine, "шлюз":masculine,
    "стол":masculine, "трон":masculine, "горшок":masculine, "шкаф":masculine,
    "ларец":masculine, "гроб":masculine, "игрушечный кораблик":masculine,
    "игрушечный молоток":masculine, "игрушечный топорик":masculine,
# feminine
    "кирка":feminine, "наковальня":feminine, "булава":feminine,
    "кружка":feminine, "кровать":feminine, "головоломка":feminine,
    "статуя":feminine, "бочка":feminine, "дверь":feminine,
    "миникузница":feminine, "Дверь":feminine, # duplicate дверь
# neuter
    "копьё":neuter, "гнездо":neuter, "ведро":neuter,
# plural
    "кирки":plural, "топоры":plural, "наковальни":plural, "булавы":plural,
    "копья":plural, "короткие":plural, "кружки":plural,
    "боевые топоры":plural, "болты":plural, "боевые молоты":plural,
    "арбалеты":plural, "щиты":plural, "рукавицы":plural, "поножи":plural,
    "нагрудники":plural, "брёвна":plural, "тренировочные":plural,
    "цереуса":plural, "ведра":plural, "столы":plural, "гробы":plural,
    "статуи":plural, "ларцы":plural, "механизмы":plural, "головоломки":plural,
    "игрушечные кораблики":plural, "столs":plural, "гробs":plural,
    "ларецs":plural, "статуяs":plural, "кружкаs":plural,
    "игрушечные молотоки":plural, "игрушечные топорики":plural,
    "миникузницы":plural, "стрелы":plural, "дротики":plural
}

############################################################################


def corr_weapon(s):
    trigger=0
    symbol=""
    letters=""
    count_let=0
    for let in s:
        if not let.isalpha() :
            if let.isspace():
                letters=letters+" "
            else:
                if let=="[":
                    let= " ["
                symbol=symbol+let
        else:
            letters=letters+let
            count_let=count_let+1
            if count_let<2:
                symbol=symbol+"%s"
    s_temp=letters.strip()

    if s_temp.startswith("р") and s_temp.endswith("р"):
        s_temp=s_temp[1:-1]
        trigger=1

    s_temp_sp=s_temp.split(" ")
    for word in s_temp_sp:
        if word in phrases:
            new_word=phrases[word]
            s_temp=s_temp.replace(word, new_word) 
   
    if "большой" in s_temp:
        s_temp=(s_temp.replace("большой","")).strip()
        big="большой "
    else:
        big=""

#если материал из двух слов

    if s_temp_sp[0]+" "+s_temp_sp[1]==adjectives[s_temp_sp[0]+" "+s_temp_sp[1]][3]:
        if s_temp_sp[0]=="древесина":
            s_temp=s_temp_sp[3]+" "+s_temp_sp[1]+" "+s_temp_sp[2]
        else:
            s_temp=s_temp_sp[3]+" "+s_temp_sp[0]+" "+s_temp_sp[1]+" "+s_temp_sp[2] 

#если материал из одного слова

    if s_temp_sp[-1] in weapon_gender:
        material= s_temp_sp[0]+" "+s_temp_sp[1]
        gender=weapon_gender[s_temp_sp[-1]]
        new_word=adjectives[material][gender]
        s_temp=s_temp.replace(material, new_word)
    
# самоцветы
    s_temp=big+s_temp+" "
    if symbol.count("-")!=2:
        symbol=symbol.replace("s-", "s")
       
    if trigger==1:
        s=symbol%("≡"+s_temp+"≡" )
    else:
        s=symbol%s_temp
   
    return s

#inventory
############################################################################

def rod_pad(word):
###################### существительные+ прилаг  ######################
#заканчивается гласной
    glas_let={
        'ца':'цы', 'ма':'мы', 'ка':'ки', 'фа':'фы', 'ба':'бы', 'са':'сы',
        'ья':'ьи', 'на':'ны', 'да':'ды', 'ха':'хи', 'ва':'вы', 'за':'зы',
        'га':'ги', 'ра':'ры',
#                прилагат
        'ая':'ой',
    }

    soglas_let_2={
        'ай':'ая', 'ёл':'ла', 'ок':'ка', 'сь':'ся', 'ль':'ли', 'ец':'ца',
        'вь':'вя', 'нь':'ня', 'ёс':'са', 'дь':'дя', 'ль':'ля', 'рь':'ри',
        'сь':'си', 'ус':'ус', 'ий':'ого', 'ый':'ого', 'ой':'ого', 'ви':'ви',
    }

    soglas_let_3={
        'адь':'ади', 'едь':'едя', 'ось':'ося', 'ысь':'ыси', 'лёк':'лька',
        'орь':'ря', 'бей':'бья', 'тей':'тея', 'очь':'очь', 'ами':'и', 
        'ней':'ней',
    }
                
    glas={"а", "о", "э", "у", "ы", "е", "ё", "ю", "я"}
    soglas={"б", "в", "г", "д", "ж", "з", "й", "к", "л", "м", "н", "п", "р", "с", "т", "ф", "х", "ц", "ч", "ш", "щ", "ь", "и",}
    iskl={
        'барсук-медоед':'барсука-медоеда',
        'птица-носорог':'птицы-носорог',
        'угорь-конгер':'угря-конгера',
        'макака-резус':'макаки-резус',
        'паук-отшельник':'паука-отшельника',
        'пауканец-отшельник':'пауканца-отшельника',
    }

    word_temp1=""
 
    for word_temp in word.split():
        if word_temp in iskl:
            word_temp=iskl[word_temp]
        if word_temp.startswith("были"):
            word_temp="вер"+word_temp[4:]

    if word_temp[-1] in glas:
        if word_temp[-2:] in glas_let:
            word_temp=word_temp[:-2]+glas_let[word_temp[-2:]]
    
    elif word_temp[-1] in soglas:
        if word_temp[-3:] in soglas_let_3:
            word_temp=word_temp[:-3]+soglas_let_3[word_temp[-3:]]
        elif word_temp[-2:] in soglas_let_2:
            word_temp=word_temp[:-2]+soglas_let_2[word_temp[-2:]]
        else:
            word_temp=word_temp+"а"
    word_temp1=(word_temp1+" "+word_temp).strip()
   
    return word_temp1


item_mat_skin=("из кожи", "из шерсти", "из волокон", "из шёлка", "из панциря","мясо", "из кости")

def corr_inv(s):
    if s.startswith("X") and s.endswith("X") :
        s=s[1:-1]
        s="."+s+"."

    symbol=""
    letters=""
    count_let=0
    for let in s:
        if not let.isalpha():
            if let.isspace():
                 letters=letters+" "
            else:
              if let=="[":
                 let= " ["
              symbol=symbol+let     
        else:
            letters=letters+let
            count_let=count_let+1
            if count_let<2:
                symbol=symbol+"%s"
    s_temp=letters.strip()

    for word in s_temp.split(" "):
        if word in phrases:
            new_word=phrases[word]
            s_temp=s_temp.replace(word, new_word)         

    if s_temp.find("левый")>-1:
        s_temp=s_temp.replace("левый", "левая")
    elif s_temp.find("правый")>-1:
        s_temp=s_temp.replace("правый", "правая")
                       
    s_word=s_temp.split()
    count=0
   
    for iz in s_word:
        if iz=='из':
            sec_word=s_word[count]+" "+s_word[count+1]
        count=count+1
                
    s_temp=s_temp.split(sec_word)

    it_dec= rod_pad(s_temp[0])
                
    s_temp=s_temp[1]+" "+sec_word+" "+it_dec
    s_temp=str(s_temp.strip())
   
    if symbol.count("-")!=2:
        symbol=symbol.replace("s-", "s")
   
    s=symbol%s_temp
    if s.startswith(".") and s.endswith(".") is True:
        s="X"+s[1:-1]+"X"
    return s
 
#gems и трава
##############################################################################
item_other=("панцирь", "скелет", "хвост", "искалеченный труп","останки","кость","кожа","шёлк","волокна","шерсть","мех",)
def corr_other(s):
    for item in item_other:
        if s.find(item)!=-1: 
            item_temp=item
            s_temp=(s.replace(item, "")).strip()
            s_temp=rod_pads_temp
    s= item_temp +" "+s_temp
    return s

############################################################################

words=("трупs", "часть телаs",)
def word(s):
    for item in words:
        if s.find(item)!=-1: 
            s=phrases[item]+" "+s[-3:]
    return s

############################################################################

def corr_sklad(s):
    s_temp_1_1= (((s.split("(", 2) ) [1] ).split())[1]
    s_temp_1_2= rod_pad((((s.split("(", 2) ) [1] ).split())[0])
    s_temp_2= (s.split("(", 2) ) [2] 
    s="("+s_temp_1_1+" "+(s_temp_1_2).lower()+" ("+s_temp_2
    return s

############################################################################
#элементы крепости.Для упрощения материал указал в скобках после названия элемента
 #самоцветы+травы
elem_forts=("Пол Пещеры", "Стена","Кластер","Пол","Лестница вверх",
    "Лестница вниз","Подъем","Валун","Склон","Галька","Деревце","грубый","Густой","Лужа" ,"Брызги")
okonch_met=("ль","ма","ля")
okonch_trav=("ия","ца","ая","ва","яя","ка","ки","ии",)

def elem_fort(s):
    words=s.split(" ")
    
    if words[0]=="Лужа" or words[0]=="Брызги":
        s=words[0]+" "+"крови"+" "+rod_pad(' '.join(words[1:2]))
        return s
    
    
    if ' '.join(words[-2:]) in elem_forts:
        k=-2
    elif ' '.join(words[-1:]) in elem_forts:
        k=-1
    else:
        k=0
    
    if k:
        s=' '.join(words[k:])+" "+' '.join(words[:k])
    if s[-2:] in okonch_met:
        s=s.replace("Неотесанный","Неотёсанная")
    elif s[-2:] in okonch_trav:
        s=s.replace("Густой","Густая")
        s=s.replace("из морошки","морошка")
        s=s.replace("из пузырьковой луковицы","пузырьковая луковица")
        s=s.replace("из фенестрарии","фенестрария")
    else:
        s=s.replace("из открытых глазок","открытый глазик")
        s=s.replace("из напольного грибка","напольный грибок")
        s=s.replace("из литопса","литопс")
        s=s.replace("из бодяка болотного","бодяк болотный")
        s=s.replace("из тростника обыкновенного","тростник обыкновенный")
        s=s.replace("из рогозы","рогоз")
        s=s.replace("из камыша","камыш")
        s=s.replace("из червеусиков","червеусик")
    if k:
       s=' '.join((s.split(" "))[:-k])+" "+"("+' '.join((s.split(" "))[-k:])+")"
    return s
############################################################################
#ковать-корректировка "ковать из"
#заканчивается гласной

forg_word= {"Ковать ", "Изготовить ", "Чеканить ","Делать "}

forg_ch={
    'булава':'булаву',
    'кирка':'кирку',
    'шапка':'шапку',
    'руковица':'рукавицу',
    'кольчуга':'кольчугу',
    'бочка':'бочку',
    'Клетка':'клетку',
    'доспешная стойка':'доспешную стойку',
    'Решетка':'решетку',
    'статуя':'статую',
    'оружейная стойка':'оружейную стойку',
    'Секция трубы':'секцию трубы',
    'Шина':'шину',
    'Наковальня':'наковальню',
    'Игрушка':'игрушку',
    'вагонетка':'вагонетку',
    'Фляга':'флягу',
    'роба':'робу',
    'рубаха':'рубаху',
    'одежда':'одежду',
    'перчатка':'перчатку',
    'варежка':'варежку',
}
                
glass_mat={
    'зеленое стекло':'из зеленого стекла',
    'бесцветное стекло':'из бесцветного стекла',
    'хрусталь':'из хрусталя',
}

def forg(s):
    s=s.replace("зеленое стекло","из зеленого стекла")
    s=s.replace("бесцветное стекло","из бесцветного стекла")
    s=s.replace("хрусталь","из хрусталя")
    s_temp_1=' '.join((s.split(" "))[:-2])
    s_temp=(s.replace(s_temp_1, "")).strip()

    if s_temp in forg_ch:
        s=s.replace(s_temp,forg_ch[s_temp])
        

    return s.capitalize()



############################################################################
def Init():
    # phrases['Test'] = 'Тест'
    pass
Init()

debug = True
if debug:
    log_file = open('changetext.log', 'a', 1)
#    log_file = open('changetext.log', 'a', 1, encoding='cp65001')
not_translated = set()

def ChangeText(s):
    
    if s in phrases:
        return phrases[s]
    elif any(s.find(item)!=-1 for item in forg_word):
            return forg(s)
    elif s.find(") <#")!=-1 :
            return corr_sklad(s)
    elif any(s.find(item)!=-1 for item in item_mat_skin):
            return corr_inv(s)
    elif any(s.find(item)!=-1 for item in adjectives):
            return corr_weapon(s)
    elif any(s.find(item)!=-1 for item in item_other):
            return corr_other(s)
    elif any(s.find(item)!=-1 for item in words):
            return word(s)
    elif any(s.find(item)!=-1 for item in elem_forts):
            return elem_fort(s)
    else :
        if debug and s not in not_translated:
            log_file.write('"%s"\n' % s)
            log_file.flush()
        not_translated.add(s)
        return None

if __name__ == '__main__':
    print(ChangeText("Изготовить из железа доспешная стойка"))
    print(ChangeText("Изготовить зеленое стекло доспешная стойка"))
    print(ChangeText("Делать хрусталь кубок"))
    print(ChangeText("из кремня топор"))
    print(ChangeText("из кремня бочка"))
    input()



