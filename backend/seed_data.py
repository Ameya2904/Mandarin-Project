"""NPCR Lesson seed data - lessons 1-20 of New Practical Chinese Reader."""

NPCR_LESSONS = [
    {
        "lesson_number": 1,
        "title": "你好 (Hello)",
        "subtitle": "Greetings",
        "description": "Learn basic Chinese greetings and simple introductions.",
        "level": "Beginner",
        "video_url": "https://www.youtube.com/playlist?list=PLB1B262B05A6992FD",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "你好!", "pinyin": "Nǐ hǎo!", "english": "Hello!"},
            {"speaker": "Lu Yuping", "chinese": "你好!", "pinyin": "Nǐ hǎo!", "english": "Hello!"}
        ],
        "grammar_notes": [
            {"title": "Greetings with 你好", "explanation": "你好 (nǐ hǎo) is the most common Chinese greeting, used at any time of day. Literally 'you good'."}
        ],
        "vocabulary": [
            {"simplified": "你", "traditional": "你", "pinyin": "nǐ", "english": "you", "part_of_speech": "pronoun", "example_chinese": "你好", "example_pinyin": "Nǐ hǎo", "example_english": "Hello"},
            {"simplified": "好", "traditional": "好", "pinyin": "hǎo", "english": "good; well", "part_of_speech": "adjective", "example_chinese": "你好", "example_pinyin": "Nǐ hǎo", "example_english": "Hello"},
            {"simplified": "你好", "traditional": "你好", "pinyin": "nǐ hǎo", "english": "hello", "part_of_speech": "phrase", "example_chinese": "你好,林娜", "example_pinyin": "Nǐ hǎo, Lín Nà", "example_english": "Hello, Lin Na"},
            {"simplified": "吗", "traditional": "嗎", "pinyin": "ma", "english": "question particle", "part_of_speech": "particle", "example_chinese": "你好吗?", "example_pinyin": "Nǐ hǎo ma?", "example_english": "How are you?"},
            {"simplified": "我", "traditional": "我", "pinyin": "wǒ", "english": "I; me", "part_of_speech": "pronoun", "example_chinese": "我很好", "example_pinyin": "Wǒ hěn hǎo", "example_english": "I am well"},
            {"simplified": "很", "traditional": "很", "pinyin": "hěn", "english": "very", "part_of_speech": "adverb", "example_chinese": "我很好", "example_pinyin": "Wǒ hěn hǎo", "example_english": "I am very well"}
        ]
    },
    {
        "lesson_number": 2,
        "title": "你忙吗 (Are You Busy?)",
        "subtitle": "Asking About Wellbeing",
        "description": "Ask how someone is doing and respond about your own state.",
        "level": "Beginner",
        "video_url": "https://www.youtube.com/playlist?list=PLB1B262B05A6992FD",
        "dialogue": [
            {"speaker": "Lu Yuping", "chinese": "你好,林娜。", "pinyin": "Nǐ hǎo, Lín Nà.", "english": "Hello, Lin Na."},
            {"speaker": "Lin Na", "chinese": "你好,陆雨平。你忙吗?", "pinyin": "Nǐ hǎo, Lù Yǔpíng. Nǐ máng ma?", "english": "Hello, Lu Yuping. Are you busy?"},
            {"speaker": "Lu Yuping", "chinese": "我很忙。你呢?", "pinyin": "Wǒ hěn máng. Nǐ ne?", "english": "I'm very busy. And you?"},
            {"speaker": "Lin Na", "chinese": "我不忙。", "pinyin": "Wǒ bù máng.", "english": "I'm not busy."}
        ],
        "grammar_notes": [
            {"title": "Yes/No questions with 吗", "explanation": "Add 吗 (ma) at the end of a statement to turn it into a yes/no question. Example: 你忙 (you busy) → 你忙吗? (Are you busy?)"},
            {"title": "Negation with 不", "explanation": "不 (bù) negates verbs and adjectives. Example: 我忙 (I am busy) → 我不忙 (I am not busy)."}
        ],
        "vocabulary": [
            {"simplified": "忙", "traditional": "忙", "pinyin": "máng", "english": "busy", "part_of_speech": "adjective", "example_chinese": "我很忙", "example_pinyin": "Wǒ hěn máng", "example_english": "I am very busy"},
            {"simplified": "不", "traditional": "不", "pinyin": "bù", "english": "not; no", "part_of_speech": "adverb", "example_chinese": "我不忙", "example_pinyin": "Wǒ bù máng", "example_english": "I am not busy"},
            {"simplified": "呢", "traditional": "呢", "pinyin": "ne", "english": "and you? (question particle)", "part_of_speech": "particle", "example_chinese": "你呢?", "example_pinyin": "Nǐ ne?", "example_english": "And you?"},
            {"simplified": "也", "traditional": "也", "pinyin": "yě", "english": "also; too", "part_of_speech": "adverb", "example_chinese": "我也很好", "example_pinyin": "Wǒ yě hěn hǎo", "example_english": "I am also very well"},
            {"simplified": "都", "traditional": "都", "pinyin": "dōu", "english": "all; both", "part_of_speech": "adverb", "example_chinese": "我们都很忙", "example_pinyin": "Wǒmen dōu hěn máng", "example_english": "We are all busy"},
            {"simplified": "他", "traditional": "他", "pinyin": "tā", "english": "he; him", "part_of_speech": "pronoun", "example_chinese": "他很忙", "example_pinyin": "Tā hěn máng", "example_english": "He is busy"},
            {"simplified": "她", "traditional": "她", "pinyin": "tā", "english": "she; her", "part_of_speech": "pronoun", "example_chinese": "她很好", "example_pinyin": "Tā hěn hǎo", "example_english": "She is well"}
        ]
    },
    {
        "lesson_number": 3,
        "title": "她是哪国人 (Where Is She From?)",
        "subtitle": "Nationality and Identity",
        "description": "Talk about people, nationalities, and ask 'who' questions.",
        "level": "Beginner",
        "video_url": "https://www.youtube.com/playlist?list=PL76C77D2229EAF542",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "陆雨平,那是谁?", "pinyin": "Lù Yǔpíng, nà shì shéi?", "english": "Lu Yuping, who is that?"},
            {"speaker": "Lu Yuping", "chinese": "那是我朋友。", "pinyin": "Nà shì wǒ péngyǒu.", "english": "That is my friend."},
            {"speaker": "Lin Na", "chinese": "她是哪国人?", "pinyin": "Tā shì nǎ guó rén?", "english": "What nationality is she?"},
            {"speaker": "Lu Yuping", "chinese": "她是中国人。", "pinyin": "Tā shì Zhōngguó rén.", "english": "She is Chinese."}
        ],
        "grammar_notes": [
            {"title": "是 (shì) — the verb 'to be'", "explanation": "是 connects two nouns. Structure: A 是 B (A is B). Example: 他是中国人 (He is Chinese)."},
            {"title": "Question word 哪 (nǎ)", "explanation": "哪 means 'which' and forms questions: 哪国人 = 'which country person' = 'what nationality'."}
        ],
        "vocabulary": [
            {"simplified": "是", "traditional": "是", "pinyin": "shì", "english": "to be (is/am/are)", "part_of_speech": "verb", "example_chinese": "我是学生", "example_pinyin": "Wǒ shì xuéshēng", "example_english": "I am a student"},
            {"simplified": "那", "traditional": "那", "pinyin": "nà", "english": "that", "part_of_speech": "pronoun", "example_chinese": "那是书", "example_pinyin": "Nà shì shū", "example_english": "That is a book"},
            {"simplified": "这", "traditional": "這", "pinyin": "zhè", "english": "this", "part_of_speech": "pronoun", "example_chinese": "这是茶", "example_pinyin": "Zhè shì chá", "example_english": "This is tea"},
            {"simplified": "谁", "traditional": "誰", "pinyin": "shéi", "english": "who", "part_of_speech": "pronoun", "example_chinese": "他是谁?", "example_pinyin": "Tā shì shéi?", "example_english": "Who is he?"},
            {"simplified": "朋友", "traditional": "朋友", "pinyin": "péngyǒu", "english": "friend", "part_of_speech": "noun", "example_chinese": "我的朋友", "example_pinyin": "Wǒ de péngyǒu", "example_english": "My friend"},
            {"simplified": "哪", "traditional": "哪", "pinyin": "nǎ", "english": "which", "part_of_speech": "pronoun", "example_chinese": "哪国人?", "example_pinyin": "Nǎ guó rén?", "example_english": "What nationality?"},
            {"simplified": "国", "traditional": "國", "pinyin": "guó", "english": "country", "part_of_speech": "noun", "example_chinese": "中国", "example_pinyin": "Zhōngguó", "example_english": "China"},
            {"simplified": "人", "traditional": "人", "pinyin": "rén", "english": "person; people", "part_of_speech": "noun", "example_chinese": "中国人", "example_pinyin": "Zhōngguó rén", "example_english": "Chinese person"},
            {"simplified": "中国", "traditional": "中國", "pinyin": "Zhōngguó", "english": "China", "part_of_speech": "noun", "example_chinese": "我爱中国", "example_pinyin": "Wǒ ài Zhōngguó", "example_english": "I love China"}
        ]
    },
    {
        "lesson_number": 4,
        "title": "认识你很高兴 (Nice to Meet You)",
        "subtitle": "Introductions",
        "description": "Introduce yourself, ask names, and express pleasure in meeting someone.",
        "level": "Beginner",
        "video_url": "https://www.youtube.com/playlist?list=PL9E5EA79F9466CB49",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "你叫什么名字?", "pinyin": "Nǐ jiào shénme míngzì?", "english": "What is your name?"},
            {"speaker": "Ma Dawei", "chinese": "我叫马大为。你呢?", "pinyin": "Wǒ jiào Mǎ Dàwéi. Nǐ ne?", "english": "My name is Ma Dawei. And you?"},
            {"speaker": "Lin Na", "chinese": "我叫林娜。认识你很高兴。", "pinyin": "Wǒ jiào Lín Nà. Rènshí nǐ hěn gāoxìng.", "english": "My name is Lin Na. Nice to meet you."},
            {"speaker": "Ma Dawei", "chinese": "认识你我也很高兴。", "pinyin": "Rènshí nǐ wǒ yě hěn gāoxìng.", "english": "Nice to meet you too."}
        ],
        "grammar_notes": [
            {"title": "叫 (jiào) — to be called", "explanation": "叫 expresses one's name. 你叫什么名字? = What is your name? Response: 我叫... = I am called..."},
            {"title": "什么 (shénme) — what", "explanation": "什么 is a question word for 'what'. Place it where the answer would appear: 你叫什么? = You called what?"}
        ],
        "vocabulary": [
            {"simplified": "叫", "traditional": "叫", "pinyin": "jiào", "english": "to be called; to call", "part_of_speech": "verb", "example_chinese": "我叫林娜", "example_pinyin": "Wǒ jiào Lín Nà", "example_english": "My name is Lin Na"},
            {"simplified": "什么", "traditional": "什麼", "pinyin": "shénme", "english": "what", "part_of_speech": "pronoun", "example_chinese": "你叫什么?", "example_pinyin": "Nǐ jiào shénme?", "example_english": "What's your name?"},
            {"simplified": "名字", "traditional": "名字", "pinyin": "míngzì", "english": "name", "part_of_speech": "noun", "example_chinese": "我的名字", "example_pinyin": "Wǒ de míngzì", "example_english": "My name"},
            {"simplified": "认识", "traditional": "認識", "pinyin": "rènshí", "english": "to know; to be acquainted with", "part_of_speech": "verb", "example_chinese": "认识你", "example_pinyin": "Rènshí nǐ", "example_english": "To know you"},
            {"simplified": "高兴", "traditional": "高興", "pinyin": "gāoxìng", "english": "happy; glad", "part_of_speech": "adjective", "example_chinese": "我很高兴", "example_pinyin": "Wǒ hěn gāoxìng", "example_english": "I am happy"},
            {"simplified": "请", "traditional": "請", "pinyin": "qǐng", "english": "please", "part_of_speech": "verb", "example_chinese": "请进", "example_pinyin": "Qǐng jìn", "example_english": "Please come in"},
            {"simplified": "问", "traditional": "問", "pinyin": "wèn", "english": "to ask", "part_of_speech": "verb", "example_chinese": "请问", "example_pinyin": "Qǐng wèn", "example_english": "Excuse me (may I ask)"},
            {"simplified": "贵姓", "traditional": "貴姓", "pinyin": "guìxìng", "english": "your honorable surname", "part_of_speech": "phrase", "example_chinese": "您贵姓?", "example_pinyin": "Nín guìxìng?", "example_english": "What is your surname?"}
        ]
    },
    {
        "lesson_number": 5,
        "title": "餐厅在哪儿 (Where Is the Restaurant?)",
        "subtitle": "Locations and Directions",
        "description": "Ask and give directions, discuss locations of places.",
        "level": "Beginner",
        "video_url": "https://www.youtube.com/playlist?list=PL14D5D3A4D4A01B8A",
        "dialogue": [
            {"speaker": "Ma Dawei", "chinese": "请问,餐厅在哪儿?", "pinyin": "Qǐng wèn, cāntīng zài nǎr?", "english": "Excuse me, where is the restaurant?"},
            {"speaker": "Lin Na", "chinese": "餐厅在那儿。", "pinyin": "Cāntīng zài nàr.", "english": "The restaurant is over there."},
            {"speaker": "Ma Dawei", "chinese": "谢谢!", "pinyin": "Xièxie!", "english": "Thank you!"},
            {"speaker": "Lin Na", "chinese": "不客气。", "pinyin": "Bú kèqì.", "english": "You're welcome."}
        ],
        "grammar_notes": [
            {"title": "在 (zài) — to be at/in", "explanation": "在 indicates location. Structure: [Subject] + 在 + [Place]. Example: 我在家 (I am at home)."},
            {"title": "哪儿 (nǎr) — where", "explanation": "哪儿 asks for location. 餐厅在哪儿? = Where is the restaurant?"}
        ],
        "vocabulary": [
            {"simplified": "在", "traditional": "在", "pinyin": "zài", "english": "to be at; in", "part_of_speech": "verb", "example_chinese": "我在家", "example_pinyin": "Wǒ zài jiā", "example_english": "I am at home"},
            {"simplified": "哪儿", "traditional": "哪兒", "pinyin": "nǎr", "english": "where", "part_of_speech": "pronoun", "example_chinese": "你在哪儿?", "example_pinyin": "Nǐ zài nǎr?", "example_english": "Where are you?"},
            {"simplified": "这儿", "traditional": "這兒", "pinyin": "zhèr", "english": "here", "part_of_speech": "pronoun", "example_chinese": "我在这儿", "example_pinyin": "Wǒ zài zhèr", "example_english": "I am here"},
            {"simplified": "那儿", "traditional": "那兒", "pinyin": "nàr", "english": "there", "part_of_speech": "pronoun", "example_chinese": "他在那儿", "example_pinyin": "Tā zài nàr", "example_english": "He is there"},
            {"simplified": "餐厅", "traditional": "餐廳", "pinyin": "cāntīng", "english": "dining hall; restaurant", "part_of_speech": "noun", "example_chinese": "学校的餐厅", "example_pinyin": "Xuéxiào de cāntīng", "example_english": "School cafeteria"},
            {"simplified": "谢谢", "traditional": "謝謝", "pinyin": "xièxie", "english": "thank you", "part_of_speech": "phrase", "example_chinese": "谢谢你", "example_pinyin": "Xièxie nǐ", "example_english": "Thank you"},
            {"simplified": "不客气", "traditional": "不客氣", "pinyin": "bú kèqì", "english": "you're welcome", "part_of_speech": "phrase", "example_chinese": "不客气", "example_pinyin": "Bú kèqì", "example_english": "You're welcome"},
            {"simplified": "家", "traditional": "家", "pinyin": "jiā", "english": "home; family", "part_of_speech": "noun", "example_chinese": "我的家", "example_pinyin": "Wǒ de jiā", "example_english": "My home"},
            {"simplified": "学校", "traditional": "學校", "pinyin": "xuéxiào", "english": "school", "part_of_speech": "noun", "example_chinese": "我们的学校", "example_pinyin": "Wǒmen de xuéxiào", "example_english": "Our school"},
            {"simplified": "去", "traditional": "去", "pinyin": "qù", "english": "to go", "part_of_speech": "verb", "example_chinese": "我去学校", "example_pinyin": "Wǒ qù xuéxiào", "example_english": "I go to school"}
        ]
    },
    {
        "lesson_number": 6,
        "title": "我们去游泳，好吗 (Let's Go Swimming)",
        "subtitle": "Making Suggestions",
        "description": "Suggest activities, ask for opinions, and accept invitations.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Wang Xiaoyun", "chinese": "今天天气真好。", "pinyin": "Jīntiān tiānqì zhēn hǎo.", "english": "The weather is really nice today."},
            {"speaker": "Lin Na", "chinese": "是啊。我们去游泳，好吗?", "pinyin": "Shì a. Wǒmen qù yóuyǒng, hǎo ma?", "english": "Yes. Shall we go swimming?"},
            {"speaker": "Wang Xiaoyun", "chinese": "太好了!我们什么时候去?", "pinyin": "Tài hǎo le! Wǒmen shénme shíhòu qù?", "english": "Great! When shall we go?"},
            {"speaker": "Lin Na", "chinese": "下午四点。", "pinyin": "Xiàwǔ sì diǎn.", "english": "Four o'clock in the afternoon."}
        ],
        "grammar_notes": [
            {"title": "Suggestions with ...，好吗?", "explanation": "Add ，好吗? after a statement to make a suggestion: 我们去看电影，好吗? (Shall we go to a movie?)"},
            {"title": "Telling Time", "explanation": "Use number + 点 for hours: 三点 (3 o'clock), 八点 (8 o'clock). 下午 = afternoon, 上午 = morning."}
        ],
        "vocabulary": [
            {"simplified": "今天", "traditional": "今天", "pinyin": "jīntiān", "english": "today", "part_of_speech": "noun", "example_chinese": "今天很忙", "example_pinyin": "Jīntiān hěn máng", "example_english": "Today is busy"},
            {"simplified": "天气", "traditional": "天氣", "pinyin": "tiānqì", "english": "weather", "part_of_speech": "noun", "example_chinese": "天气好", "example_pinyin": "Tiānqì hǎo", "example_english": "Weather is good"},
            {"simplified": "真", "traditional": "真", "pinyin": "zhēn", "english": "really; truly", "part_of_speech": "adverb", "example_chinese": "真好", "example_pinyin": "Zhēn hǎo", "example_english": "Really good"},
            {"simplified": "我们", "traditional": "我們", "pinyin": "wǒmen", "english": "we; us", "part_of_speech": "pronoun", "example_chinese": "我们走吧", "example_pinyin": "Wǒmen zǒu ba", "example_english": "Let's go"},
            {"simplified": "游泳", "traditional": "游泳", "pinyin": "yóuyǒng", "english": "to swim", "part_of_speech": "verb", "example_chinese": "我去游泳", "example_pinyin": "Wǒ qù yóuyǒng", "example_english": "I go swimming"},
            {"simplified": "时候", "traditional": "時候", "pinyin": "shíhòu", "english": "time; moment", "part_of_speech": "noun", "example_chinese": "什么时候?", "example_pinyin": "Shénme shíhòu?", "example_english": "When?"},
            {"simplified": "下午", "traditional": "下午", "pinyin": "xiàwǔ", "english": "afternoon", "part_of_speech": "noun", "example_chinese": "下午见", "example_pinyin": "Xiàwǔ jiàn", "example_english": "See you this afternoon"},
            {"simplified": "点", "traditional": "點", "pinyin": "diǎn", "english": "o'clock", "part_of_speech": "measure word", "example_chinese": "三点", "example_pinyin": "Sān diǎn", "example_english": "Three o'clock"}
        ]
    },
    {
        "lesson_number": 7,
        "title": "你认识不认识他 (Do You Know Him?)",
        "subtitle": "V-not-V Questions",
        "description": "Form questions by repeating the verb with 不 between.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Ma Dawei", "chinese": "林娜，你认识不认识他?", "pinyin": "Lín Nà, nǐ rènshí bú rènshí tā?", "english": "Lin Na, do you know him?"},
            {"speaker": "Lin Na", "chinese": "我不认识他。他是谁?", "pinyin": "Wǒ bú rènshí tā. Tā shì shéi?", "english": "I don't know him. Who is he?"},
            {"speaker": "Ma Dawei", "chinese": "他是我的同学，叫王小云。", "pinyin": "Tā shì wǒ de tóngxué, jiào Wáng Xiǎoyún.", "english": "He's my classmate, Wang Xiaoyun."}
        ],
        "grammar_notes": [
            {"title": "V-not-V Questions", "explanation": "Repeat the verb with 不 to make a question: 你认识不认识他? = 你认识他吗? (Do you know him?). 你忙不忙? = Are you busy?"}
        ],
        "vocabulary": [
            {"simplified": "同学", "traditional": "同學", "pinyin": "tóngxué", "english": "classmate", "part_of_speech": "noun", "example_chinese": "我的同学", "example_pinyin": "Wǒ de tóngxué", "example_english": "My classmate"},
            {"simplified": "老师", "traditional": "老師", "pinyin": "lǎoshī", "english": "teacher", "part_of_speech": "noun", "example_chinese": "我们的老师", "example_pinyin": "Wǒmen de lǎoshī", "example_english": "Our teacher"},
            {"simplified": "学生", "traditional": "學生", "pinyin": "xuéshēng", "english": "student", "part_of_speech": "noun", "example_chinese": "我是学生", "example_pinyin": "Wǒ shì xuéshēng", "example_english": "I am a student"},
            {"simplified": "的", "traditional": "的", "pinyin": "de", "english": "possessive particle", "part_of_speech": "particle", "example_chinese": "我的书", "example_pinyin": "Wǒ de shū", "example_english": "My book"},
            {"simplified": "书", "traditional": "書", "pinyin": "shū", "english": "book", "part_of_speech": "noun", "example_chinese": "一本书", "example_pinyin": "Yì běn shū", "example_english": "A book"}
        ]
    },
    {
        "lesson_number": 8,
        "title": "你们家有几口人 (How Many in Your Family?)",
        "subtitle": "Family & Numbers",
        "description": "Discuss family members and use measure words for people.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Wang Xiaoyun", "chinese": "林娜，你们家有几口人?", "pinyin": "Lín Nà, nǐmen jiā yǒu jǐ kǒu rén?", "english": "Lin Na, how many people are in your family?"},
            {"speaker": "Lin Na", "chinese": "我们家有四口人。爸爸、妈妈、哥哥和我。", "pinyin": "Wǒmen jiā yǒu sì kǒu rén. Bàba, māma, gēge hé wǒ.", "english": "We have four people: dad, mom, older brother, and me."}
        ],
        "grammar_notes": [
            {"title": "有 (yǒu) — to have", "explanation": "有 means 'to have' or 'there is/are'. Negation: 没有 (méi yǒu). Example: 我有一个哥哥 (I have an older brother)."},
            {"title": "几 (jǐ) — how many (small numbers)", "explanation": "几 asks 'how many' for small numbers (usually <10). 你有几本书? = How many books do you have?"}
        ],
        "vocabulary": [
            {"simplified": "有", "traditional": "有", "pinyin": "yǒu", "english": "to have; there is", "part_of_speech": "verb", "example_chinese": "我有书", "example_pinyin": "Wǒ yǒu shū", "example_english": "I have a book"},
            {"simplified": "几", "traditional": "幾", "pinyin": "jǐ", "english": "how many (small)", "part_of_speech": "pronoun", "example_chinese": "几个人?", "example_pinyin": "Jǐ ge rén?", "example_english": "How many people?"},
            {"simplified": "口", "traditional": "口", "pinyin": "kǒu", "english": "measure word for family members", "part_of_speech": "measure word", "example_chinese": "四口人", "example_pinyin": "Sì kǒu rén", "example_english": "Four people"},
            {"simplified": "爸爸", "traditional": "爸爸", "pinyin": "bàba", "english": "father", "part_of_speech": "noun", "example_chinese": "我爸爸", "example_pinyin": "Wǒ bàba", "example_english": "My dad"},
            {"simplified": "妈妈", "traditional": "媽媽", "pinyin": "māma", "english": "mother", "part_of_speech": "noun", "example_chinese": "我妈妈", "example_pinyin": "Wǒ māma", "example_english": "My mom"},
            {"simplified": "哥哥", "traditional": "哥哥", "pinyin": "gēge", "english": "older brother", "part_of_speech": "noun", "example_chinese": "我哥哥", "example_pinyin": "Wǒ gēge", "example_english": "My older brother"},
            {"simplified": "和", "traditional": "和", "pinyin": "hé", "english": "and", "part_of_speech": "conjunction", "example_chinese": "我和你", "example_pinyin": "Wǒ hé nǐ", "example_english": "You and I"},
            {"simplified": "四", "traditional": "四", "pinyin": "sì", "english": "four", "part_of_speech": "number", "example_chinese": "四个人", "example_pinyin": "Sì ge rén", "example_english": "Four people"}
        ]
    },
    {
        "lesson_number": 9,
        "title": "他今年二十岁 (He's Twenty This Year)",
        "subtitle": "Numbers & Ages",
        "description": "Talk about ages, birthdays, and use larger numbers.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "马大为，你今年多大?", "pinyin": "Mǎ Dàwéi, nǐ jīnnián duō dà?", "english": "Ma Dawei, how old are you this year?"},
            {"speaker": "Ma Dawei", "chinese": "我今年二十岁。你呢?", "pinyin": "Wǒ jīnnián èrshí suì. Nǐ ne?", "english": "I'm twenty this year. And you?"},
            {"speaker": "Lin Na", "chinese": "我十九岁。", "pinyin": "Wǒ shíjiǔ suì.", "english": "I'm nineteen."}
        ],
        "grammar_notes": [
            {"title": "Asking Age: 多大?", "explanation": "你今年多大? = How old are you this year? (for adults). For children: 你几岁? Response: 我...岁."},
            {"title": "Numbers 1-100", "explanation": "一(1), 二(2), 三(3), 四(4), 五(5), 六(6), 七(7), 八(8), 九(9), 十(10). Combine: 二十(20), 二十一(21), 一百(100)."}
        ],
        "vocabulary": [
            {"simplified": "今年", "traditional": "今年", "pinyin": "jīnnián", "english": "this year", "part_of_speech": "noun", "example_chinese": "今年很忙", "example_pinyin": "Jīnnián hěn máng", "example_english": "This year is busy"},
            {"simplified": "多大", "traditional": "多大", "pinyin": "duō dà", "english": "how old", "part_of_speech": "phrase", "example_chinese": "你多大?", "example_pinyin": "Nǐ duō dà?", "example_english": "How old are you?"},
            {"simplified": "岁", "traditional": "歲", "pinyin": "suì", "english": "years (of age)", "part_of_speech": "measure word", "example_chinese": "二十岁", "example_pinyin": "Èrshí suì", "example_english": "20 years old"},
            {"simplified": "二十", "traditional": "二十", "pinyin": "èrshí", "english": "twenty", "part_of_speech": "number", "example_chinese": "二十个", "example_pinyin": "Èrshí ge", "example_english": "Twenty (of something)"},
            {"simplified": "十", "traditional": "十", "pinyin": "shí", "english": "ten", "part_of_speech": "number", "example_chinese": "十本书", "example_pinyin": "Shí běn shū", "example_english": "Ten books"},
            {"simplified": "生日", "traditional": "生日", "pinyin": "shēngrì", "english": "birthday", "part_of_speech": "noun", "example_chinese": "我的生日", "example_pinyin": "Wǒ de shēngrì", "example_english": "My birthday"},
            {"simplified": "月", "traditional": "月", "pinyin": "yuè", "english": "month", "part_of_speech": "noun", "example_chinese": "三月", "example_pinyin": "Sān yuè", "example_english": "March"},
            {"simplified": "号", "traditional": "號", "pinyin": "hào", "english": "day of month", "part_of_speech": "noun", "example_chinese": "五号", "example_pinyin": "Wǔ hào", "example_english": "The 5th"}
        ]
    },
    {
        "lesson_number": 10,
        "title": "我在这儿买光盘 (I'm Buying CDs Here)",
        "subtitle": "Shopping & Activities",
        "description": "Express what you are doing now using 在 + verb.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "马大为，你在做什么?", "pinyin": "Mǎ Dàwéi, nǐ zài zuò shénme?", "english": "Ma Dawei, what are you doing?"},
            {"speaker": "Ma Dawei", "chinese": "我在这儿买光盘。", "pinyin": "Wǒ zài zhèr mǎi guāngpán.", "english": "I'm buying CDs here."},
            {"speaker": "Lin Na", "chinese": "你想买什么光盘?", "pinyin": "Nǐ xiǎng mǎi shénme guāngpán?", "english": "What kind of CDs do you want to buy?"},
            {"speaker": "Ma Dawei", "chinese": "中文音乐。", "pinyin": "Zhōngwén yīnyuè.", "english": "Chinese music."}
        ],
        "grammar_notes": [
            {"title": "在 + Verb (progressive)", "explanation": "在 before a verb expresses an ongoing action: 我在吃饭 (I am eating). 你在做什么? = What are you doing?"},
            {"title": "想 (xiǎng) — want to", "explanation": "想 + verb expresses desire: 我想买书 (I want to buy a book). 你想去吗? = Do you want to go?"}
        ],
        "vocabulary": [
            {"simplified": "做", "traditional": "做", "pinyin": "zuò", "english": "to do; to make", "part_of_speech": "verb", "example_chinese": "做饭", "example_pinyin": "Zuò fàn", "example_english": "To cook"},
            {"simplified": "买", "traditional": "買", "pinyin": "mǎi", "english": "to buy", "part_of_speech": "verb", "example_chinese": "买书", "example_pinyin": "Mǎi shū", "example_english": "Buy a book"},
            {"simplified": "光盘", "traditional": "光盤", "pinyin": "guāngpán", "english": "CD; disc", "part_of_speech": "noun", "example_chinese": "买光盘", "example_pinyin": "Mǎi guāngpán", "example_english": "Buy a CD"},
            {"simplified": "想", "traditional": "想", "pinyin": "xiǎng", "english": "to want; to think", "part_of_speech": "verb", "example_chinese": "我想吃", "example_pinyin": "Wǒ xiǎng chī", "example_english": "I want to eat"},
            {"simplified": "音乐", "traditional": "音樂", "pinyin": "yīnyuè", "english": "music", "part_of_speech": "noun", "example_chinese": "听音乐", "example_pinyin": "Tīng yīnyuè", "example_english": "Listen to music"},
            {"simplified": "中文", "traditional": "中文", "pinyin": "Zhōngwén", "english": "Chinese (language)", "part_of_speech": "noun", "example_chinese": "学中文", "example_pinyin": "Xué Zhōngwén", "example_english": "Study Chinese"},
            {"simplified": "钱", "traditional": "錢", "pinyin": "qián", "english": "money", "part_of_speech": "noun", "example_chinese": "多少钱?", "example_pinyin": "Duōshǎo qián?", "example_english": "How much?"}
        ]
    },
    {
        "lesson_number": 11,
        "title": "我会说一点儿汉语 (I Can Speak a Little Chinese)",
        "subtitle": "Abilities & Languages",
        "description": "Talk about what you can do using 会 and 能.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Wang Xiaoyun", "chinese": "你会说汉语吗?", "pinyin": "Nǐ huì shuō Hànyǔ ma?", "english": "Can you speak Chinese?"},
            {"speaker": "Ma Dawei", "chinese": "我会说一点儿汉语。", "pinyin": "Wǒ huì shuō yìdiǎnr Hànyǔ.", "english": "I can speak a little Chinese."},
            {"speaker": "Wang Xiaoyun", "chinese": "你说得很好!", "pinyin": "Nǐ shuō de hěn hǎo!", "english": "You speak very well!"}
        ],
        "grammar_notes": [
            {"title": "会 (huì) — learned ability", "explanation": "会 expresses learned skills: 我会游泳 (I can swim). Negation: 我不会..."},
            {"title": "一点儿 (yìdiǎnr) — a little", "explanation": "一点儿 means 'a little'. 我会说一点儿英语 = I can speak a little English."}
        ],
        "vocabulary": [
            {"simplified": "会", "traditional": "會", "pinyin": "huì", "english": "can; able to (learned)", "part_of_speech": "modal verb", "example_chinese": "我会游泳", "example_pinyin": "Wǒ huì yóuyǒng", "example_english": "I can swim"},
            {"simplified": "说", "traditional": "說", "pinyin": "shuō", "english": "to speak; to say", "part_of_speech": "verb", "example_chinese": "说汉语", "example_pinyin": "Shuō Hànyǔ", "example_english": "Speak Chinese"},
            {"simplified": "汉语", "traditional": "漢語", "pinyin": "Hànyǔ", "english": "Chinese language", "part_of_speech": "noun", "example_chinese": "学汉语", "example_pinyin": "Xué Hànyǔ", "example_english": "Study Chinese"},
            {"simplified": "英语", "traditional": "英語", "pinyin": "Yīngyǔ", "english": "English language", "part_of_speech": "noun", "example_chinese": "说英语", "example_pinyin": "Shuō Yīngyǔ", "example_english": "Speak English"},
            {"simplified": "一点儿", "traditional": "一點兒", "pinyin": "yìdiǎnr", "english": "a little", "part_of_speech": "phrase", "example_chinese": "一点儿水", "example_pinyin": "Yìdiǎnr shuǐ", "example_english": "A little water"},
            {"simplified": "得", "traditional": "得", "pinyin": "de", "english": "particle (degree)", "part_of_speech": "particle", "example_chinese": "说得好", "example_pinyin": "Shuō de hǎo", "example_english": "Speaks well"},
            {"simplified": "学", "traditional": "學", "pinyin": "xué", "english": "to study; to learn", "part_of_speech": "verb", "example_chinese": "学中文", "example_pinyin": "Xué Zhōngwén", "example_english": "Study Chinese"}
        ]
    },
    {
        "lesson_number": 12,
        "title": "我全身都不舒服 (I'm Not Feeling Well)",
        "subtitle": "Health & Body",
        "description": "Describe how you feel and discuss being sick.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "马大为，你怎么了?", "pinyin": "Mǎ Dàwéi, nǐ zěnme le?", "english": "Ma Dawei, what's wrong?"},
            {"speaker": "Ma Dawei", "chinese": "我全身都不舒服。头疼，发烧。", "pinyin": "Wǒ quánshēn dōu bù shūfu. Tóu téng, fāshāo.", "english": "My whole body feels bad. My head hurts and I have a fever."},
            {"speaker": "Lin Na", "chinese": "你应该去医院。", "pinyin": "Nǐ yīnggāi qù yīyuàn.", "english": "You should go to the hospital."}
        ],
        "grammar_notes": [
            {"title": "怎么了? (zěnme le?)", "explanation": "怎么了? asks 'what's wrong?' or 'what happened?'. Used to inquire about a problem."},
            {"title": "应该 (yīnggāi) — should", "explanation": "应该 + verb expresses obligation: 你应该休息 (You should rest)."}
        ],
        "vocabulary": [
            {"simplified": "怎么", "traditional": "怎麼", "pinyin": "zěnme", "english": "how; what", "part_of_speech": "pronoun", "example_chinese": "怎么去?", "example_pinyin": "Zěnme qù?", "example_english": "How to go?"},
            {"simplified": "舒服", "traditional": "舒服", "pinyin": "shūfu", "english": "comfortable; well", "part_of_speech": "adjective", "example_chinese": "不舒服", "example_pinyin": "Bù shūfu", "example_english": "Not feeling well"},
            {"simplified": "头", "traditional": "頭", "pinyin": "tóu", "english": "head", "part_of_speech": "noun", "example_chinese": "我的头", "example_pinyin": "Wǒ de tóu", "example_english": "My head"},
            {"simplified": "疼", "traditional": "疼", "pinyin": "téng", "english": "to hurt; painful", "part_of_speech": "adjective", "example_chinese": "头疼", "example_pinyin": "Tóu téng", "example_english": "Headache"},
            {"simplified": "发烧", "traditional": "發燒", "pinyin": "fāshāo", "english": "to have a fever", "part_of_speech": "verb", "example_chinese": "我发烧", "example_pinyin": "Wǒ fāshāo", "example_english": "I have a fever"},
            {"simplified": "应该", "traditional": "應該", "pinyin": "yīnggāi", "english": "should", "part_of_speech": "modal verb", "example_chinese": "应该休息", "example_pinyin": "Yīnggāi xiūxi", "example_english": "Should rest"},
            {"simplified": "医院", "traditional": "醫院", "pinyin": "yīyuàn", "english": "hospital", "part_of_speech": "noun", "example_chinese": "去医院", "example_pinyin": "Qù yīyuàn", "example_english": "Go to hospital"},
            {"simplified": "休息", "traditional": "休息", "pinyin": "xiūxi", "english": "to rest", "part_of_speech": "verb", "example_chinese": "好好休息", "example_pinyin": "Hǎohǎo xiūxi", "example_english": "Rest well"}
        ]
    },
    {
        "lesson_number": 13,
        "title": "我认识了一个漂亮的姑娘 (I Met a Beautiful Girl)",
        "subtitle": "Past Actions with 了",
        "description": "Talk about completed actions using the particle 了.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Ma Dawei", "chinese": "昨天我认识了一个漂亮的姑娘。", "pinyin": "Zuótiān wǒ rènshí le yí ge piàoliang de gūniang.", "english": "Yesterday I met a beautiful girl."},
            {"speaker": "Lin Na", "chinese": "真的吗?她是哪国人?", "pinyin": "Zhēn de ma? Tā shì nǎ guó rén?", "english": "Really? What nationality is she?"},
            {"speaker": "Ma Dawei", "chinese": "她是中国人。她叫王小云。", "pinyin": "Tā shì Zhōngguó rén. Tā jiào Wáng Xiǎoyún.", "english": "She's Chinese. Her name is Wang Xiaoyun."}
        ],
        "grammar_notes": [
            {"title": "了 (le) — completed action", "explanation": "了 after a verb indicates a completed action: 我吃了饭 (I ate). Past time markers like 昨天 (yesterday) often appear with 了."},
            {"title": "Adjective + 的 + Noun", "explanation": "Use 的 to link adjectives to nouns: 漂亮的姑娘 (beautiful girl), 好的朋友 (good friend)."}
        ],
        "vocabulary": [
            {"simplified": "昨天", "traditional": "昨天", "pinyin": "zuótiān", "english": "yesterday", "part_of_speech": "noun", "example_chinese": "昨天来", "example_pinyin": "Zuótiān lái", "example_english": "Came yesterday"},
            {"simplified": "了", "traditional": "了", "pinyin": "le", "english": "particle (completed action)", "part_of_speech": "particle", "example_chinese": "吃了饭", "example_pinyin": "Chī le fàn", "example_english": "Ate"},
            {"simplified": "漂亮", "traditional": "漂亮", "pinyin": "piàoliang", "english": "pretty; beautiful", "part_of_speech": "adjective", "example_chinese": "很漂亮", "example_pinyin": "Hěn piàoliang", "example_english": "Very pretty"},
            {"simplified": "姑娘", "traditional": "姑娘", "pinyin": "gūniang", "english": "girl; young woman", "part_of_speech": "noun", "example_chinese": "好姑娘", "example_pinyin": "Hǎo gūniang", "example_english": "Good girl"},
            {"simplified": "明天", "traditional": "明天", "pinyin": "míngtiān", "english": "tomorrow", "part_of_speech": "noun", "example_chinese": "明天见", "example_pinyin": "Míngtiān jiàn", "example_english": "See you tomorrow"},
            {"simplified": "来", "traditional": "來", "pinyin": "lái", "english": "to come", "part_of_speech": "verb", "example_chinese": "他来了", "example_pinyin": "Tā lái le", "example_english": "He came"},
            {"simplified": "吃", "traditional": "吃", "pinyin": "chī", "english": "to eat", "part_of_speech": "verb", "example_chinese": "吃饭", "example_pinyin": "Chī fàn", "example_english": "Eat"},
            {"simplified": "饭", "traditional": "飯", "pinyin": "fàn", "english": "rice; meal", "part_of_speech": "noun", "example_chinese": "吃饭", "example_pinyin": "Chī fàn", "example_english": "Eat a meal"}
        ]
    },
    {
        "lesson_number": 14,
        "title": "祝你圣诞快乐 (Merry Christmas)",
        "subtitle": "Wishes & Celebrations",
        "description": "Express good wishes and talk about holidays.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "马大为，祝你圣诞快乐!", "pinyin": "Mǎ Dàwéi, zhù nǐ Shèngdàn kuàilè!", "english": "Ma Dawei, Merry Christmas!"},
            {"speaker": "Ma Dawei", "chinese": "谢谢!也祝你圣诞快乐!", "pinyin": "Xièxie! Yě zhù nǐ Shèngdàn kuàilè!", "english": "Thank you! Merry Christmas to you too!"},
            {"speaker": "Lin Na", "chinese": "这是给你的礼物。", "pinyin": "Zhè shì gěi nǐ de lǐwù.", "english": "This is a gift for you."}
        ],
        "grammar_notes": [
            {"title": "祝 (zhù) — to wish", "explanation": "祝 + Person + Wish expresses good wishes: 祝你生日快乐 (Happy birthday), 祝你健康 (Wishing you health)."},
            {"title": "给 (gěi) — for; give", "explanation": "给 + Person + 的 + Noun: 给你的礼物 (a gift for you). Also a verb: 我给他书 (I give him a book)."}
        ],
        "vocabulary": [
            {"simplified": "祝", "traditional": "祝", "pinyin": "zhù", "english": "to wish", "part_of_speech": "verb", "example_chinese": "祝你好运", "example_pinyin": "Zhù nǐ hǎoyùn", "example_english": "Good luck"},
            {"simplified": "圣诞", "traditional": "聖誕", "pinyin": "Shèngdàn", "english": "Christmas", "part_of_speech": "noun", "example_chinese": "圣诞节", "example_pinyin": "Shèngdàn jié", "example_english": "Christmas Day"},
            {"simplified": "快乐", "traditional": "快樂", "pinyin": "kuàilè", "english": "happy", "part_of_speech": "adjective", "example_chinese": "很快乐", "example_pinyin": "Hěn kuàilè", "example_english": "Very happy"},
            {"simplified": "给", "traditional": "給", "pinyin": "gěi", "english": "to give; for", "part_of_speech": "verb", "example_chinese": "给我书", "example_pinyin": "Gěi wǒ shū", "example_english": "Give me a book"},
            {"simplified": "礼物", "traditional": "禮物", "pinyin": "lǐwù", "english": "gift; present", "part_of_speech": "noun", "example_chinese": "生日礼物", "example_pinyin": "Shēngrì lǐwù", "example_english": "Birthday gift"},
            {"simplified": "节", "traditional": "節", "pinyin": "jié", "english": "festival; holiday", "part_of_speech": "noun", "example_chinese": "春节", "example_pinyin": "Chūnjié", "example_english": "Spring Festival"},
            {"simplified": "新年", "traditional": "新年", "pinyin": "xīnnián", "english": "new year", "part_of_speech": "noun", "example_chinese": "新年快乐", "example_pinyin": "Xīnnián kuàilè", "example_english": "Happy New Year"}
        ]
    },
    {
        "lesson_number": 15,
        "title": "银行在哪儿 (Where Is the Bank?)",
        "subtitle": "Getting Around Town",
        "description": "Ask for directions to common city locations.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Ma Dawei", "chinese": "请问，银行在哪儿?", "pinyin": "Qǐng wèn, yínháng zài nǎr?", "english": "Excuse me, where is the bank?"},
            {"speaker": "Stranger", "chinese": "银行在邮局旁边。", "pinyin": "Yínháng zài yóujú pángbiān.", "english": "The bank is next to the post office."},
            {"speaker": "Ma Dawei", "chinese": "邮局远不远?", "pinyin": "Yóujú yuǎn bu yuǎn?", "english": "Is the post office far?"},
            {"speaker": "Stranger", "chinese": "不远，走五分钟就到。", "pinyin": "Bù yuǎn, zǒu wǔ fēnzhōng jiù dào.", "english": "Not far, five minutes' walk."}
        ],
        "grammar_notes": [
            {"title": "Location words: 旁边, 前面, 后面", "explanation": "旁边 (beside), 前面 (in front), 后面 (behind), 里面 (inside), 外面 (outside). A 在 B 旁边 = A is beside B."}
        ],
        "vocabulary": [
            {"simplified": "银行", "traditional": "銀行", "pinyin": "yínháng", "english": "bank", "part_of_speech": "noun", "example_chinese": "去银行", "example_pinyin": "Qù yínháng", "example_english": "Go to the bank"},
            {"simplified": "邮局", "traditional": "郵局", "pinyin": "yóujú", "english": "post office", "part_of_speech": "noun", "example_chinese": "邮局开门", "example_pinyin": "Yóujú kāimén", "example_english": "Post office is open"},
            {"simplified": "旁边", "traditional": "旁邊", "pinyin": "pángbiān", "english": "beside; next to", "part_of_speech": "noun", "example_chinese": "我旁边", "example_pinyin": "Wǒ pángbiān", "example_english": "Beside me"},
            {"simplified": "远", "traditional": "遠", "pinyin": "yuǎn", "english": "far", "part_of_speech": "adjective", "example_chinese": "很远", "example_pinyin": "Hěn yuǎn", "example_english": "Very far"},
            {"simplified": "走", "traditional": "走", "pinyin": "zǒu", "english": "to walk", "part_of_speech": "verb", "example_chinese": "走路", "example_pinyin": "Zǒu lù", "example_english": "Walk"},
            {"simplified": "分钟", "traditional": "分鐘", "pinyin": "fēnzhōng", "english": "minute", "part_of_speech": "noun", "example_chinese": "十分钟", "example_pinyin": "Shí fēnzhōng", "example_english": "Ten minutes"},
            {"simplified": "到", "traditional": "到", "pinyin": "dào", "english": "to arrive; to reach", "part_of_speech": "verb", "example_chinese": "到了", "example_pinyin": "Dào le", "example_english": "Arrived"}
        ]
    },
    {
        "lesson_number": 16,
        "title": "你想喝什么 (What Do You Want to Drink?)",
        "subtitle": "Ordering Food & Drink",
        "description": "Order at a restaurant and discuss preferences.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Waiter", "chinese": "你想喝什么?", "pinyin": "Nǐ xiǎng hē shénme?", "english": "What would you like to drink?"},
            {"speaker": "Lin Na", "chinese": "我要一杯茶。", "pinyin": "Wǒ yào yì bēi chá.", "english": "I'd like a cup of tea."},
            {"speaker": "Waiter", "chinese": "好的，请稍等。", "pinyin": "Hǎo de, qǐng shāo děng.", "english": "OK, please wait a moment."}
        ],
        "grammar_notes": [
            {"title": "要 (yào) — want; will", "explanation": "要 expresses wanting or ordering: 我要茶 (I want tea). Also used as future: 我要去 (I will go)."},
            {"title": "Measure words: 杯, 个, 本", "explanation": "Chinese requires measure words between numbers and nouns: 一杯茶 (a cup of tea), 一个人 (one person), 一本书 (one book)."}
        ],
        "vocabulary": [
            {"simplified": "喝", "traditional": "喝", "pinyin": "hē", "english": "to drink", "part_of_speech": "verb", "example_chinese": "喝水", "example_pinyin": "Hē shuǐ", "example_english": "Drink water"},
            {"simplified": "要", "traditional": "要", "pinyin": "yào", "english": "to want; will", "part_of_speech": "verb", "example_chinese": "我要茶", "example_pinyin": "Wǒ yào chá", "example_english": "I want tea"},
            {"simplified": "杯", "traditional": "杯", "pinyin": "bēi", "english": "cup; measure word", "part_of_speech": "measure word", "example_chinese": "一杯水", "example_pinyin": "Yì bēi shuǐ", "example_english": "A cup of water"},
            {"simplified": "茶", "traditional": "茶", "pinyin": "chá", "english": "tea", "part_of_speech": "noun", "example_chinese": "喝茶", "example_pinyin": "Hē chá", "example_english": "Drink tea"},
            {"simplified": "水", "traditional": "水", "pinyin": "shuǐ", "english": "water", "part_of_speech": "noun", "example_chinese": "一杯水", "example_pinyin": "Yì bēi shuǐ", "example_english": "A cup of water"},
            {"simplified": "咖啡", "traditional": "咖啡", "pinyin": "kāfēi", "english": "coffee", "part_of_speech": "noun", "example_chinese": "喝咖啡", "example_pinyin": "Hē kāfēi", "example_english": "Drink coffee"},
            {"simplified": "等", "traditional": "等", "pinyin": "děng", "english": "to wait", "part_of_speech": "verb", "example_chinese": "等一下", "example_pinyin": "Děng yíxià", "example_english": "Wait a moment"}
        ]
    },
    {
        "lesson_number": 17,
        "title": "这件衣服多少钱 (How Much Is This?)",
        "subtitle": "Shopping & Prices",
        "description": "Ask about prices and shop for clothing.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "这件衣服多少钱?", "pinyin": "Zhè jiàn yīfu duōshǎo qián?", "english": "How much is this piece of clothing?"},
            {"speaker": "Clerk", "chinese": "一百二十块。", "pinyin": "Yìbǎi èrshí kuài.", "english": "120 yuan."},
            {"speaker": "Lin Na", "chinese": "太贵了。便宜一点儿吧。", "pinyin": "Tài guì le. Piányi yìdiǎnr ba.", "english": "Too expensive. A bit cheaper, please."}
        ],
        "grammar_notes": [
            {"title": "多少 (duōshǎo) — how much; how many", "explanation": "多少 asks for amounts (especially large): 多少钱? (how much money?), 多少人? (how many people?)"},
            {"title": "太...了 — too ...", "explanation": "太 + adjective + 了 expresses 'too...': 太贵了 (too expensive), 太好了 (great/too good)."}
        ],
        "vocabulary": [
            {"simplified": "件", "traditional": "件", "pinyin": "jiàn", "english": "measure word (clothing)", "part_of_speech": "measure word", "example_chinese": "一件衣服", "example_pinyin": "Yí jiàn yīfu", "example_english": "A piece of clothing"},
            {"simplified": "衣服", "traditional": "衣服", "pinyin": "yīfu", "english": "clothes", "part_of_speech": "noun", "example_chinese": "买衣服", "example_pinyin": "Mǎi yīfu", "example_english": "Buy clothes"},
            {"simplified": "多少", "traditional": "多少", "pinyin": "duōshǎo", "english": "how much/many", "part_of_speech": "pronoun", "example_chinese": "多少钱?", "example_pinyin": "Duōshǎo qián?", "example_english": "How much?"},
            {"simplified": "百", "traditional": "百", "pinyin": "bǎi", "english": "hundred", "part_of_speech": "number", "example_chinese": "一百", "example_pinyin": "Yìbǎi", "example_english": "One hundred"},
            {"simplified": "块", "traditional": "塊", "pinyin": "kuài", "english": "yuan (colloquial)", "part_of_speech": "measure word", "example_chinese": "十块钱", "example_pinyin": "Shí kuài qián", "example_english": "Ten yuan"},
            {"simplified": "太", "traditional": "太", "pinyin": "tài", "english": "too; very", "part_of_speech": "adverb", "example_chinese": "太好了", "example_pinyin": "Tài hǎo le", "example_english": "Great!"},
            {"simplified": "贵", "traditional": "貴", "pinyin": "guì", "english": "expensive", "part_of_speech": "adjective", "example_chinese": "很贵", "example_pinyin": "Hěn guì", "example_english": "Very expensive"},
            {"simplified": "便宜", "traditional": "便宜", "pinyin": "piányi", "english": "cheap", "part_of_speech": "adjective", "example_chinese": "很便宜", "example_pinyin": "Hěn piányi", "example_english": "Very cheap"}
        ]
    },
    {
        "lesson_number": 18,
        "title": "我每天七点起床 (I Get Up at 7 Every Day)",
        "subtitle": "Daily Routines",
        "description": "Describe your daily schedule and routines.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "你每天几点起床?", "pinyin": "Nǐ měitiān jǐ diǎn qǐchuáng?", "english": "What time do you get up every day?"},
            {"speaker": "Ma Dawei", "chinese": "我每天七点起床。你呢?", "pinyin": "Wǒ měitiān qī diǎn qǐchuáng. Nǐ ne?", "english": "I get up at 7 every day. And you?"},
            {"speaker": "Lin Na", "chinese": "我八点起床。", "pinyin": "Wǒ bā diǎn qǐchuáng.", "english": "I get up at 8."}
        ],
        "grammar_notes": [
            {"title": "每 (měi) — every", "explanation": "每 + time expresses 'every': 每天 (every day), 每年 (every year), 每个星期 (every week)."}
        ],
        "vocabulary": [
            {"simplified": "每天", "traditional": "每天", "pinyin": "měitiān", "english": "every day", "part_of_speech": "noun", "example_chinese": "每天学习", "example_pinyin": "Měitiān xuéxí", "example_english": "Study every day"},
            {"simplified": "起床", "traditional": "起床", "pinyin": "qǐchuáng", "english": "to get up", "part_of_speech": "verb", "example_chinese": "早起床", "example_pinyin": "Zǎo qǐchuáng", "example_english": "Get up early"},
            {"simplified": "睡觉", "traditional": "睡覺", "pinyin": "shuìjiào", "english": "to sleep", "part_of_speech": "verb", "example_chinese": "去睡觉", "example_pinyin": "Qù shuìjiào", "example_english": "Go to sleep"},
            {"simplified": "上班", "traditional": "上班", "pinyin": "shàngbān", "english": "to go to work", "part_of_speech": "verb", "example_chinese": "去上班", "example_pinyin": "Qù shàngbān", "example_english": "Go to work"},
            {"simplified": "学习", "traditional": "學習", "pinyin": "xuéxí", "english": "to study", "part_of_speech": "verb", "example_chinese": "学习汉语", "example_pinyin": "Xuéxí Hànyǔ", "example_english": "Study Chinese"},
            {"simplified": "早上", "traditional": "早上", "pinyin": "zǎoshang", "english": "morning", "part_of_speech": "noun", "example_chinese": "早上好", "example_pinyin": "Zǎoshang hǎo", "example_english": "Good morning"},
            {"simplified": "晚上", "traditional": "晚上", "pinyin": "wǎnshang", "english": "evening", "part_of_speech": "noun", "example_chinese": "晚上见", "example_pinyin": "Wǎnshang jiàn", "example_english": "See you tonight"}
        ]
    },
    {
        "lesson_number": 19,
        "title": "今天比昨天冷 (Today Is Colder Than Yesterday)",
        "subtitle": "Comparisons",
        "description": "Compare two things using 比.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "今天比昨天冷。", "pinyin": "Jīntiān bǐ zuótiān lěng.", "english": "Today is colder than yesterday."},
            {"speaker": "Ma Dawei", "chinese": "是啊。我喜欢热天。", "pinyin": "Shì a. Wǒ xǐhuān rè tiān.", "english": "Yes. I like hot days."},
            {"speaker": "Lin Na", "chinese": "我也是。", "pinyin": "Wǒ yě shì.", "english": "Me too."}
        ],
        "grammar_notes": [
            {"title": "A 比 B + Adjective", "explanation": "Use 比 to compare: 我比他高 (I am taller than him). 今天比昨天冷 = Today is colder than yesterday."},
            {"title": "喜欢 (xǐhuān) — to like", "explanation": "喜欢 + Noun/Verb: 我喜欢中国 (I like China), 我喜欢学汉语 (I like to study Chinese)."}
        ],
        "vocabulary": [
            {"simplified": "比", "traditional": "比", "pinyin": "bǐ", "english": "compared to", "part_of_speech": "preposition", "example_chinese": "我比你高", "example_pinyin": "Wǒ bǐ nǐ gāo", "example_english": "I'm taller than you"},
            {"simplified": "冷", "traditional": "冷", "pinyin": "lěng", "english": "cold", "part_of_speech": "adjective", "example_chinese": "很冷", "example_pinyin": "Hěn lěng", "example_english": "Very cold"},
            {"simplified": "热", "traditional": "熱", "pinyin": "rè", "english": "hot", "part_of_speech": "adjective", "example_chinese": "很热", "example_pinyin": "Hěn rè", "example_english": "Very hot"},
            {"simplified": "喜欢", "traditional": "喜歡", "pinyin": "xǐhuān", "english": "to like", "part_of_speech": "verb", "example_chinese": "喜欢中国", "example_pinyin": "Xǐhuān Zhōngguó", "example_english": "Like China"},
            {"simplified": "高", "traditional": "高", "pinyin": "gāo", "english": "tall; high", "part_of_speech": "adjective", "example_chinese": "很高", "example_pinyin": "Hěn gāo", "example_english": "Very tall"},
            {"simplified": "大", "traditional": "大", "pinyin": "dà", "english": "big", "part_of_speech": "adjective", "example_chinese": "很大", "example_pinyin": "Hěn dà", "example_english": "Very big"},
            {"simplified": "小", "traditional": "小", "pinyin": "xiǎo", "english": "small", "part_of_speech": "adjective", "example_chinese": "很小", "example_pinyin": "Hěn xiǎo", "example_english": "Very small"}
        ]
    },
    {
        "lesson_number": 20,
        "title": "我打算去中国 (I Plan to Go to China)",
        "subtitle": "Plans & Future",
        "description": "Talk about plans and future actions.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"speaker": "Lin Na", "chinese": "明年我打算去中国学习。", "pinyin": "Míngnián wǒ dǎsuàn qù Zhōngguó xuéxí.", "english": "Next year I plan to go study in China."},
            {"speaker": "Ma Dawei", "chinese": "真的吗?你要去哪个城市?", "pinyin": "Zhēn de ma? Nǐ yào qù nǎ ge chéngshì?", "english": "Really? Which city will you go to?"},
            {"speaker": "Lin Na", "chinese": "北京。你想一起来吗?", "pinyin": "Běijīng. Nǐ xiǎng yìqǐ lái ma?", "english": "Beijing. Do you want to come along?"}
        ],
        "grammar_notes": [
            {"title": "打算 (dǎsuàn) — to plan", "explanation": "打算 + verb: 我打算学汉语 (I plan to study Chinese). Talks about intentions or plans."},
            {"title": "一起 (yìqǐ) — together", "explanation": "一起 + verb: 一起去 (go together), 我们一起吃饭 (Let's eat together)."}
        ],
        "vocabulary": [
            {"simplified": "明年", "traditional": "明年", "pinyin": "míngnián", "english": "next year", "part_of_speech": "noun", "example_chinese": "明年去中国", "example_pinyin": "Míngnián qù Zhōngguó", "example_english": "Go to China next year"},
            {"simplified": "打算", "traditional": "打算", "pinyin": "dǎsuàn", "english": "to plan", "part_of_speech": "verb", "example_chinese": "打算学习", "example_pinyin": "Dǎsuàn xuéxí", "example_english": "Plan to study"},
            {"simplified": "城市", "traditional": "城市", "pinyin": "chéngshì", "english": "city", "part_of_speech": "noun", "example_chinese": "大城市", "example_pinyin": "Dà chéngshì", "example_english": "Big city"},
            {"simplified": "北京", "traditional": "北京", "pinyin": "Běijīng", "english": "Beijing", "part_of_speech": "noun", "example_chinese": "去北京", "example_pinyin": "Qù Běijīng", "example_english": "Go to Beijing"},
            {"simplified": "一起", "traditional": "一起", "pinyin": "yìqǐ", "english": "together", "part_of_speech": "adverb", "example_chinese": "一起去", "example_pinyin": "Yìqǐ qù", "example_english": "Go together"},
            {"simplified": "上海", "traditional": "上海", "pinyin": "Shànghǎi", "english": "Shanghai", "part_of_speech": "noun", "example_chinese": "在上海", "example_pinyin": "Zài Shànghǎi", "example_english": "In Shanghai"},
            {"simplified": "回", "traditional": "回", "pinyin": "huí", "english": "to return", "part_of_speech": "verb", "example_chinese": "回家", "example_pinyin": "Huí jiā", "example_english": "Go home"}
        ]
    }
]

# Sentence drill templates by lesson number
SENTENCE_DRILLS = [
    # Lesson 1
    {"lesson_number": 1, "drill_type": "substitution", "prompt_chinese": "我很好", "prompt_english": "I am very well", "instruction_english": "Replace 好 (good) with 忙 (busy)", "instruction_chinese": "用'忙'替换'好'", "expected_answer": "我很忙", "expected_pinyin": "Wǒ hěn máng", "expected_english": "I am very busy"},
    {"lesson_number": 1, "drill_type": "substitution", "prompt_chinese": "你好", "prompt_english": "Hello (you good)", "instruction_english": "Replace 你 (you) with 他 (he)", "instruction_chinese": "用'他'替换'你'", "expected_answer": "他好", "expected_pinyin": "Tā hǎo", "expected_english": "He is good"},
    # Lesson 2
    {"lesson_number": 2, "drill_type": "transformation", "prompt_chinese": "我忙", "prompt_english": "I am busy", "instruction_english": "Make this sentence negative", "instruction_chinese": "把句子变成否定句", "expected_answer": "我不忙", "expected_pinyin": "Wǒ bù máng", "expected_english": "I am not busy"},
    {"lesson_number": 2, "drill_type": "transformation", "prompt_chinese": "你忙", "prompt_english": "You are busy", "instruction_english": "Turn this into a yes/no question with 吗", "instruction_chinese": "用'吗'变成疑问句", "expected_answer": "你忙吗", "expected_pinyin": "Nǐ máng ma?", "expected_english": "Are you busy?"},
    {"lesson_number": 2, "drill_type": "substitution", "prompt_chinese": "我很忙", "prompt_english": "I am very busy", "instruction_english": "Replace 我 (I) with 他 (he)", "instruction_chinese": "用'他'替换'我'", "expected_answer": "他很忙", "expected_pinyin": "Tā hěn máng", "expected_english": "He is very busy"},
    # Lesson 3
    {"lesson_number": 3, "drill_type": "substitution", "prompt_chinese": "她是中国人", "prompt_english": "She is Chinese", "instruction_english": "Replace 她 (she) with 他 (he)", "instruction_chinese": "用'他'替换'她'", "expected_answer": "他是中国人", "expected_pinyin": "Tā shì Zhōngguó rén", "expected_english": "He is Chinese"},
    {"lesson_number": 3, "drill_type": "transformation", "prompt_chinese": "她是中国人", "prompt_english": "She is Chinese", "instruction_english": "Turn this into a question using 吗", "instruction_chinese": "用'吗'变成疑问句", "expected_answer": "她是中国人吗", "expected_pinyin": "Tā shì Zhōngguó rén ma?", "expected_english": "Is she Chinese?"},
    {"lesson_number": 3, "drill_type": "substitution", "prompt_chinese": "那是我朋友", "prompt_english": "That is my friend", "instruction_english": "Replace 那 (that) with 这 (this)", "instruction_chinese": "用'这'替换'那'", "expected_answer": "这是我朋友", "expected_pinyin": "Zhè shì wǒ péngyǒu", "expected_english": "This is my friend"},
    # Lesson 4
    {"lesson_number": 4, "drill_type": "substitution", "prompt_chinese": "我叫林娜", "prompt_english": "My name is Lin Na", "instruction_english": "Replace 林娜 with 马大为", "instruction_chinese": "用'马大为'替换'林娜'", "expected_answer": "我叫马大为", "expected_pinyin": "Wǒ jiào Mǎ Dàwéi", "expected_english": "My name is Ma Dawei"},
    {"lesson_number": 4, "drill_type": "transformation", "prompt_chinese": "我认识他", "prompt_english": "I know him", "instruction_english": "Make this a question with 吗", "instruction_chinese": "用'吗'变成疑问句", "expected_answer": "我认识他吗", "expected_pinyin": "Wǒ rènshí tā ma?", "expected_english": "Do I know him?"},
    # Lesson 5
    {"lesson_number": 5, "drill_type": "substitution", "prompt_chinese": "餐厅在那儿", "prompt_english": "The restaurant is over there", "instruction_english": "Replace 餐厅 (restaurant) with 学校 (school)", "instruction_chinese": "用'学校'替换'餐厅'", "expected_answer": "学校在那儿", "expected_pinyin": "Xuéxiào zài nàr", "expected_english": "The school is over there"},
    {"lesson_number": 5, "drill_type": "substitution", "prompt_chinese": "我在家", "prompt_english": "I am at home", "instruction_english": "Replace 家 (home) with 学校 (school)", "instruction_chinese": "用'学校'替换'家'", "expected_answer": "我在学校", "expected_pinyin": "Wǒ zài xuéxiào", "expected_english": "I am at school"},
    {"lesson_number": 5, "drill_type": "transformation", "prompt_chinese": "餐厅在那儿", "prompt_english": "The restaurant is over there", "instruction_english": "Turn into a question: where is the restaurant?", "instruction_chinese": "改为'餐厅在哪儿?'", "expected_answer": "餐厅在哪儿", "expected_pinyin": "Cāntīng zài nǎr?", "expected_english": "Where is the restaurant?"},
    # Lesson 6
    {"lesson_number": 6, "drill_type": "substitution", "prompt_chinese": "我们去游泳", "prompt_english": "We are going swimming", "instruction_english": "Replace 游泳 with 吃饭", "instruction_chinese": "用'吃饭'替换'游泳'", "expected_answer": "我们去吃饭", "expected_pinyin": "Wǒmen qù chī fàn", "expected_english": "We are going to eat"},
    {"lesson_number": 6, "drill_type": "transformation", "prompt_chinese": "我们去游泳", "prompt_english": "We go swimming", "instruction_english": "Turn into suggestion with 好吗?", "instruction_chinese": "加上'好吗?'", "expected_answer": "我们去游泳好吗", "expected_pinyin": "Wǒmen qù yóuyǒng hǎo ma?", "expected_english": "Shall we go swimming?"},
    # Lesson 7
    {"lesson_number": 7, "drill_type": "transformation", "prompt_chinese": "你认识他吗", "prompt_english": "Do you know him? (with 吗)", "instruction_english": "Convert to V-not-V question form", "instruction_chinese": "改为正反问句", "expected_answer": "你认识不认识他", "expected_pinyin": "Nǐ rènshí bú rènshí tā?", "expected_english": "Do you know him?"},
    # Lesson 8
    {"lesson_number": 8, "drill_type": "substitution", "prompt_chinese": "我们家有四口人", "prompt_english": "We have four family members", "instruction_english": "Replace 四 with 五 (five)", "instruction_chinese": "用'五'替换'四'", "expected_answer": "我们家有五口人", "expected_pinyin": "Wǒmen jiā yǒu wǔ kǒu rén", "expected_english": "We have five family members"},
    # Lesson 9
    {"lesson_number": 9, "drill_type": "substitution", "prompt_chinese": "我今年二十岁", "prompt_english": "I am 20 this year", "instruction_english": "Replace 二十 with 三十 (thirty)", "instruction_chinese": "用'三十'替换'二十'", "expected_answer": "我今年三十岁", "expected_pinyin": "Wǒ jīnnián sānshí suì", "expected_english": "I am 30 this year"},
    # Lesson 10
    {"lesson_number": 10, "drill_type": "transformation", "prompt_chinese": "我买光盘", "prompt_english": "I buy CDs", "instruction_english": "Make it progressive: I am buying CDs (use 在)", "instruction_chinese": "用'在'变成进行式", "expected_answer": "我在买光盘", "expected_pinyin": "Wǒ zài mǎi guāngpán", "expected_english": "I am buying CDs"},
    # Lesson 11
    {"lesson_number": 11, "drill_type": "substitution", "prompt_chinese": "我会说汉语", "prompt_english": "I can speak Chinese", "instruction_english": "Replace 汉语 with 英语 (English)", "instruction_chinese": "用'英语'替换'汉语'", "expected_answer": "我会说英语", "expected_pinyin": "Wǒ huì shuō Yīngyǔ", "expected_english": "I can speak English"},
    # Lesson 12
    {"lesson_number": 12, "drill_type": "transformation", "prompt_chinese": "我不舒服", "prompt_english": "I'm not feeling well", "instruction_english": "Turn into a question with 吗", "instruction_chinese": "用'吗'变成疑问句", "expected_answer": "你不舒服吗", "expected_pinyin": "Nǐ bù shūfu ma?", "expected_english": "Are you unwell?"},
    # Lesson 13
    {"lesson_number": 13, "drill_type": "transformation", "prompt_chinese": "我认识一个姑娘", "prompt_english": "I know a girl", "instruction_english": "Add 了 to indicate completed past action", "instruction_chinese": "加上'了'表示完成", "expected_answer": "我认识了一个姑娘", "expected_pinyin": "Wǒ rènshí le yí ge gūniang", "expected_english": "I met a girl"},
    # Lesson 14
    {"lesson_number": 14, "drill_type": "substitution", "prompt_chinese": "祝你圣诞快乐", "prompt_english": "Merry Christmas", "instruction_english": "Replace 圣诞 with 新年 (New Year)", "instruction_chinese": "用'新年'替换'圣诞'", "expected_answer": "祝你新年快乐", "expected_pinyin": "Zhù nǐ xīnnián kuàilè", "expected_english": "Happy New Year"},
    # Lesson 15
    {"lesson_number": 15, "drill_type": "substitution", "prompt_chinese": "银行在邮局旁边", "prompt_english": "The bank is beside the post office", "instruction_english": "Replace 旁边 with 后面 (behind)", "instruction_chinese": "用'后面'替换'旁边'", "expected_answer": "银行在邮局后面", "expected_pinyin": "Yínháng zài yóujú hòumiàn", "expected_english": "The bank is behind the post office"},
    # Lesson 16
    {"lesson_number": 16, "drill_type": "substitution", "prompt_chinese": "我要一杯茶", "prompt_english": "I want a cup of tea", "instruction_english": "Replace 茶 with 咖啡 (coffee)", "instruction_chinese": "用'咖啡'替换'茶'", "expected_answer": "我要一杯咖啡", "expected_pinyin": "Wǒ yào yì bēi kāfēi", "expected_english": "I want a cup of coffee"},
    # Lesson 17
    {"lesson_number": 17, "drill_type": "transformation", "prompt_chinese": "这件衣服贵", "prompt_english": "This clothing is expensive", "instruction_english": "Add 太...了 to make 'too expensive'", "instruction_chinese": "用'太...了'", "expected_answer": "这件衣服太贵了", "expected_pinyin": "Zhè jiàn yīfu tài guì le", "expected_english": "This clothing is too expensive"},
    # Lesson 18
    {"lesson_number": 18, "drill_type": "substitution", "prompt_chinese": "我每天七点起床", "prompt_english": "I get up at 7 every day", "instruction_english": "Replace 七 with 八 (eight)", "instruction_chinese": "用'八'替换'七'", "expected_answer": "我每天八点起床", "expected_pinyin": "Wǒ měitiān bā diǎn qǐchuáng", "expected_english": "I get up at 8 every day"},
    # Lesson 19
    {"lesson_number": 19, "drill_type": "substitution", "prompt_chinese": "今天比昨天冷", "prompt_english": "Today is colder than yesterday", "instruction_english": "Replace 冷 with 热 (hot)", "instruction_chinese": "用'热'替换'冷'", "expected_answer": "今天比昨天热", "expected_pinyin": "Jīntiān bǐ zuótiān rè", "expected_english": "Today is hotter than yesterday"},
    # Lesson 20
    {"lesson_number": 20, "drill_type": "substitution", "prompt_chinese": "我打算去北京", "prompt_english": "I plan to go to Beijing", "instruction_english": "Replace 北京 with 上海 (Shanghai)", "instruction_chinese": "用'上海'替换'北京'", "expected_answer": "我打算去上海", "expected_pinyin": "Wǒ dǎsuàn qù Shànghǎi", "expected_english": "I plan to go to Shanghai"}
]
