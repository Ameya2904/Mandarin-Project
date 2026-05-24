"""NPCR Lesson seed data - first 5 lessons of New Practical Chinese Reader."""

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
            {
                "title": "Greetings with 你好",
                "explanation": "你好 (nǐ hǎo) is the most common Chinese greeting, used at any time of day. Literally 'you good'."
            }
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
            {
                "title": "Yes/No questions with 吗",
                "explanation": "Add 吗 (ma) at the end of a statement to turn it into a yes/no question. Example: 你忙 (you busy) → 你忙吗? (Are you busy?)"
            },
            {
                "title": "Negation with 不",
                "explanation": "不 (bù) negates verbs and adjectives. Example: 我忙 (I am busy) → 我不忙 (I am not busy)."
            }
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
            {
                "title": "是 (shì) — the verb 'to be'",
                "explanation": "是 connects two nouns. Structure: A 是 B (A is B). Example: 他是中国人 (He is Chinese)."
            },
            {
                "title": "Question word 哪 (nǎ)",
                "explanation": "哪 means 'which' and forms questions: 哪国人 = 'which country person' = 'what nationality'."
            }
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
            {
                "title": "叫 (jiào) — to be called",
                "explanation": "叫 expresses one's name. 你叫什么名字? = What is your name? Response: 我叫... = I am called..."
            },
            {
                "title": "什么 (shénme) — what",
                "explanation": "什么 is a question word for 'what'. Place it where the answer would appear: 你叫什么? = You called what?"
            }
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
            {
                "title": "在 (zài) — to be at/in",
                "explanation": "在 indicates location. Structure: [Subject] + 在 + [Place]. Example: 我在家 (I am at home)."
            },
            {
                "title": "哪儿 (nǎr) — where",
                "explanation": "哪儿 asks for location. 餐厅在哪儿? = Where is the restaurant?"
            }
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
    {"lesson_number": 5, "drill_type": "transformation", "prompt_chinese": "餐厅在那儿", "prompt_english": "The restaurant is over there", "instruction_english": "Turn into a question: where is the restaurant?", "instruction_chinese": "改为'餐厅在哪儿?'", "expected_answer": "餐厅在哪儿", "expected_pinyin": "Cāntīng zài nǎr?", "expected_english": "Where is the restaurant?"}
]
