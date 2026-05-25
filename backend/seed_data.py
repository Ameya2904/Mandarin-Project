"""NPCR (New Practical Chinese Reader) seed data — Lessons 1 to 14.

Source: NPCR 1-14.docx provided by the user (full dialogue extraction).
Each lesson is split into Part 1 and Part 2 (matches the textbook structure).

Drills are stored as individual substitution variants. Each variant has
`repeat_count` so the API can expand it (the learner sees each variant
6 times for spaced repetition / drilling).
"""

# ---------- Helper to build substitution-drill variants ----------

def _expand_drill(
    lesson_number: int,
    part: int,
    group: str,
    instruction_en: str,
    instruction_zh: str,
    pattern_zh: str,
    pattern_en: str,
    variants,                # list[dict] with chinese / pinyin / english
    repeat_count: int = 6,
):
    """Expand one drill template into a list of variant entries."""
    out = []
    for v in variants:
        out.append({
            "lesson_number": lesson_number,
            "part": part,
            "drill_group": group,
            "drill_type": "substitution",
            "prompt_chinese": pattern_zh,
            "prompt_english": pattern_en,
            "instruction_english": instruction_en,
            "instruction_chinese": instruction_zh,
            "expected_answer": v["chinese"],
            "expected_pinyin": v["pinyin"],
            "expected_english": v["english"],
            "repeat_count": repeat_count,
        })
    return out


# =====================================================================
# NPCR LESSONS 1 - 14
# =====================================================================

NPCR_LESSONS = [
    # ---------------------------- L1 ----------------------------
    {
        "lesson_number": 1,
        "title": "你好 (Hello)",
        "subtitle": "Greetings",
        "description": "Greet people in Mandarin and ask how they are.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Lu Yuping", "chinese": "力波，你好！", "pinyin": "Lìbō, nǐ hǎo!", "english": "Libo, hello!"},
            {"part": 1, "speaker": "Libo",      "chinese": "你好，陆雨平。", "pinyin": "Nǐ hǎo, Lù Yǔpíng.", "english": "Hello, Lu Yuping."},
            {"part": 2, "speaker": "Wang Xiaoyun", "chinese": "林娜，你好吗？", "pinyin": "Lín Nà, nǐ hǎo ma?", "english": "Lin Na, how are you?"},
            {"part": 2, "speaker": "Lin Na",       "chinese": "我很好，你呢？",   "pinyin": "Wǒ hěn hǎo, nǐ ne?", "english": "I’m good, and you?"},
            {"part": 2, "speaker": "Wang Xiaoyun", "chinese": "也很好。",         "pinyin": "Yě hěn hǎo.",         "english": "I’m also good."},
        ],
        "grammar_notes": [
            {"title": "你好 (nǐ hǎo) — Greeting", "explanation": "你好 literally means 'you good'. It is used at any time of day."},
            {"title": "...吗？ — Yes/No question", "explanation": "Add 吗 to a statement to turn it into a yes/no question: 你好 → 你好吗?"},
            {"title": "...呢？ — And you?", "explanation": "After saying something about yourself, 你呢? returns the same question."},
        ],
        "vocabulary": [
            {"simplified": "你",  "traditional": "你",  "pinyin": "nǐ",   "english": "you", "part_of_speech": "pronoun", "example_chinese": "你好", "example_pinyin": "Nǐ hǎo", "example_english": "Hello"},
            {"simplified": "好",  "traditional": "好",  "pinyin": "hǎo",  "english": "good; well", "part_of_speech": "adjective", "example_chinese": "你好吗?", "example_pinyin": "Nǐ hǎo ma?", "example_english": "How are you?"},
            {"simplified": "吗",  "traditional": "嗎",  "pinyin": "ma",   "english": "question particle", "part_of_speech": "particle", "example_chinese": "你好吗?", "example_pinyin": "Nǐ hǎo ma?", "example_english": "How are you?"},
            {"simplified": "我",  "traditional": "我",  "pinyin": "wǒ",   "english": "I; me", "part_of_speech": "pronoun", "example_chinese": "我很好", "example_pinyin": "Wǒ hěn hǎo", "example_english": "I am well"},
            {"simplified": "很",  "traditional": "很",  "pinyin": "hěn",  "english": "very", "part_of_speech": "adverb", "example_chinese": "我很好", "example_pinyin": "Wǒ hěn hǎo", "example_english": "I am very well"},
            {"simplified": "呢",  "traditional": "呢",  "pinyin": "ne",   "english": "and ...? (particle)", "part_of_speech": "particle", "example_chinese": "你呢?", "example_pinyin": "Nǐ ne?", "example_english": "And you?"},
            {"simplified": "也",  "traditional": "也",  "pinyin": "yě",   "english": "also; too", "part_of_speech": "adverb", "example_chinese": "也很好", "example_pinyin": "Yě hěn hǎo", "example_english": "Also good"},
        ],
    },

    # ---------------------------- L2 ----------------------------
    {
        "lesson_number": 2,
        "title": "你忙吗？ (Are You Busy?)",
        "subtitle": "Asking about wellbeing",
        "description": "Ask whether someone is busy and talk about family.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Lin Na", "chinese": "陆雨平，你好吗？", "pinyin": "Lù Yǔpíng, nǐ hǎo ma?", "english": "Lu Yuping, how are you?"},
            {"part": 1, "speaker": "Lu Yuping", "chinese": "我很好。你爸爸、妈妈好吗？", "pinyin": "Wǒ hěn hǎo. Nǐ bàba, māma hǎo ma?", "english": "I’m good. How are your dad and mom?"},
            {"part": 1, "speaker": "Lin Na", "chinese": "他们都很好。你忙吗？", "pinyin": "Tāmen dōu hěn hǎo. Nǐ máng ma?", "english": "They are both well. Are you busy?"},
            {"part": 1, "speaker": "Lu Yuping", "chinese": "我不忙。你男朋友呢？", "pinyin": "Wǒ bù máng. Nǐ nán péngyou ne?", "english": "I’m not busy. How about your boyfriend?"},
            {"part": 1, "speaker": "Lin Na", "chinese": "他很忙。", "pinyin": "Tā hěn máng.", "english": "He is busy."},
            {"part": 2, "speaker": "Libo", "chinese": "哥哥，你要咖啡吗？", "pinyin": "Gēge, nǐ yào kāfēi ma?", "english": "Brother, do you want coffee?"},
            {"part": 2, "speaker": "Brother", "chinese": "我要咖啡。", "pinyin": "Wǒ yào kāfēi.", "english": "I want coffee."},
            {"part": 2, "speaker": "Libo", "chinese": "我也要咖啡。", "pinyin": "Wǒ yě yào kāfēi.", "english": "I also want coffee."},
            {"part": 2, "speaker": "Brother", "chinese": "好。我们都喝咖啡。", "pinyin": "Hǎo. Wǒmen dōu hē kāfēi.", "english": "OK. We all drink coffee."},
        ],
        "grammar_notes": [
            {"title": "Negation with 不 (bù)", "explanation": "Place 不 before a verb or adjective to negate it: 不忙 = not busy."},
            {"title": "都 (dōu) — all / both", "explanation": "都 means 'all' or 'both' and is placed before the verb: 我们都喝咖啡."},
            {"title": "也 (yě) — also", "explanation": "也 is placed before the verb: 我也要咖啡."},
        ],
        "vocabulary": [
            {"simplified": "忙",  "traditional": "忙",  "pinyin": "máng", "english": "busy", "part_of_speech": "adjective", "example_chinese": "我很忙", "example_pinyin": "Wǒ hěn máng", "example_english": "I am very busy"},
            {"simplified": "不",  "traditional": "不",  "pinyin": "bù",   "english": "not; no", "part_of_speech": "adverb", "example_chinese": "我不忙", "example_pinyin": "Wǒ bù máng", "example_english": "I am not busy"},
            {"simplified": "都",  "traditional": "都",  "pinyin": "dōu",  "english": "all; both", "part_of_speech": "adverb", "example_chinese": "我们都很好", "example_pinyin": "Wǒmen dōu hěn hǎo", "example_english": "We are all well"},
            {"simplified": "他",  "traditional": "他",  "pinyin": "tā",   "english": "he; him", "part_of_speech": "pronoun", "example_chinese": "他很忙", "example_pinyin": "Tā hěn máng", "example_english": "He is busy"},
            {"simplified": "她",  "traditional": "她",  "pinyin": "tā",   "english": "she; her", "part_of_speech": "pronoun", "example_chinese": "她很好", "example_pinyin": "Tā hěn hǎo", "example_english": "She is well"},
            {"simplified": "他们","traditional": "他們","pinyin": "tāmen","english": "they (m./mixed)", "part_of_speech": "pronoun", "example_chinese": "他们都好", "example_pinyin": "Tāmen dōu hǎo", "example_english": "They are all good"},
            {"simplified": "爸爸","traditional": "爸爸","pinyin": "bàba", "english": "father", "part_of_speech": "noun", "example_chinese": "我爸爸", "example_pinyin": "Wǒ bàba", "example_english": "My dad"},
            {"simplified": "妈妈","traditional": "媽媽","pinyin": "māma", "english": "mother", "part_of_speech": "noun", "example_chinese": "我妈妈", "example_pinyin": "Wǒ māma", "example_english": "My mom"},
            {"simplified": "哥哥","traditional": "哥哥","pinyin": "gēge", "english": "older brother", "part_of_speech": "noun", "example_chinese": "我哥哥", "example_pinyin": "Wǒ gēge", "example_english": "My older brother"},
            {"simplified": "男朋友","traditional": "男朋友","pinyin": "nán péngyou","english": "boyfriend", "part_of_speech": "noun", "example_chinese": "我男朋友", "example_pinyin": "Wǒ nán péngyou", "example_english": "My boyfriend"},
            {"simplified": "要",  "traditional": "要",  "pinyin": "yào",  "english": "to want", "part_of_speech": "verb", "example_chinese": "我要咖啡", "example_pinyin": "Wǒ yào kāfēi", "example_english": "I want coffee"},
            {"simplified": "咖啡","traditional": "咖啡","pinyin": "kāfēi","english": "coffee", "part_of_speech": "noun", "example_chinese": "喝咖啡", "example_pinyin": "Hē kāfēi", "example_english": "Drink coffee"},
            {"simplified": "喝",  "traditional": "喝",  "pinyin": "hē",   "english": "to drink", "part_of_speech": "verb", "example_chinese": "喝咖啡", "example_pinyin": "Hē kāfēi", "example_english": "Drink coffee"},
            {"simplified": "我们","traditional": "我們","pinyin": "wǒmen","english": "we; us", "part_of_speech": "pronoun", "example_chinese": "我们都好", "example_pinyin": "Wǒmen dōu hǎo", "example_english": "We are all well"},
        ],
    },

    # ---------------------------- L3 ----------------------------
    {
        "lesson_number": 3,
        "title": "她是哪国人？ (Where Is She From?)",
        "subtitle": "Identity & nationality",
        "description": "Use 是 to introduce people and ask about nationality.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Lin Na", "chinese": "力波，那是谁？", "pinyin": "Lìbō, nà shì shéi?", "english": "Libo, who is that?"},
            {"part": 1, "speaker": "Libo", "chinese": "那是我们老师。", "pinyin": "Nà shì wǒmen lǎoshī.", "english": "That is our teacher."},
            {"part": 1, "speaker": "Lin Na", "chinese": "她是哪国人？", "pinyin": "Tā shì nǎ guó rén?", "english": "Which country is she from?"},
            {"part": 1, "speaker": "Libo", "chinese": "她是中国人。我们老师都是中国人。", "pinyin": "Tā shì Zhōngguó rén. Wǒmen lǎoshī dōu shì Zhōngguó rén.", "english": "She is Chinese. All our teachers are Chinese."},
            {"part": 2, "speaker": "Libo", "chinese": "陈老师，您好！这是我哥哥，他是外语老师。", "pinyin": "Chén lǎoshī, nín hǎo! Zhè shì wǒ gēge, tā shì wàiyǔ lǎoshī.", "english": "Teacher Chen, hello! This is my elder brother, he is a foreign-language teacher."},
            {"part": 2, "speaker": "Teacher Chen", "chinese": "你好！", "pinyin": "Nǐ hǎo!", "english": "Hello!"},
            {"part": 2, "speaker": "Libo", "chinese": "这是我朋友。", "pinyin": "Zhè shì wǒ péngyǒu.", "english": "This is my friend."},
            {"part": 2, "speaker": "Teacher Chen", "chinese": "你也是老师吗？", "pinyin": "Nǐ yě shì lǎoshī ma?", "english": "Are you also a teacher?"},
            {"part": 2, "speaker": "Friend", "chinese": "我不是老师。我是医生。", "pinyin": "Wǒ bú shì lǎoshī. Wǒ shì yīshēng.", "english": "I am not a teacher. I am a doctor."},
        ],
        "grammar_notes": [
            {"title": "是 (shì) — to be", "explanation": "Structure: A 是 B (A is B). Negation: A 不是 B."},
            {"title": "哪 (nǎ) — which", "explanation": "哪国人? literally 'which-country-person?' = What nationality?"},
            {"title": "这 / 那 — this / that", "explanation": "Use 这是 (this is) and 那是 (that is) when pointing at or introducing someone."},
        ],
        "vocabulary": [
            {"simplified": "是",   "traditional": "是",   "pinyin": "shì",   "english": "to be (is/am/are)", "part_of_speech": "verb", "example_chinese": "我是学生", "example_pinyin": "Wǒ shì xuésheng", "example_english": "I am a student"},
            {"simplified": "那",   "traditional": "那",   "pinyin": "nà",    "english": "that", "part_of_speech": "pronoun", "example_chinese": "那是书", "example_pinyin": "Nà shì shū", "example_english": "That is a book"},
            {"simplified": "这",   "traditional": "這",   "pinyin": "zhè",   "english": "this", "part_of_speech": "pronoun", "example_chinese": "这是茶", "example_pinyin": "Zhè shì chá", "example_english": "This is tea"},
            {"simplified": "谁",   "traditional": "誰",   "pinyin": "shéi",  "english": "who", "part_of_speech": "pronoun", "example_chinese": "他是谁?", "example_pinyin": "Tā shì shéi?", "example_english": "Who is he?"},
            {"simplified": "哪",   "traditional": "哪",   "pinyin": "nǎ",    "english": "which", "part_of_speech": "pronoun", "example_chinese": "哪国人?", "example_pinyin": "Nǎ guó rén?", "example_english": "Which nationality?"},
            {"simplified": "国",   "traditional": "國",   "pinyin": "guó",   "english": "country", "part_of_speech": "noun", "example_chinese": "中国", "example_pinyin": "Zhōngguó", "example_english": "China"},
            {"simplified": "人",   "traditional": "人",   "pinyin": "rén",   "english": "person; people", "part_of_speech": "noun", "example_chinese": "中国人", "example_pinyin": "Zhōngguó rén", "example_english": "Chinese person"},
            {"simplified": "中国", "traditional": "中國", "pinyin": "Zhōngguó", "english": "China", "part_of_speech": "noun", "example_chinese": "我爱中国", "example_pinyin": "Wǒ ài Zhōngguó", "example_english": "I love China"},
            {"simplified": "老师", "traditional": "老師", "pinyin": "lǎoshī", "english": "teacher", "part_of_speech": "noun", "example_chinese": "我们老师", "example_pinyin": "Wǒmen lǎoshī", "example_english": "Our teacher"},
            {"simplified": "朋友", "traditional": "朋友", "pinyin": "péngyǒu", "english": "friend", "part_of_speech": "noun", "example_chinese": "我朋友", "example_pinyin": "Wǒ péngyǒu", "example_english": "My friend"},
            {"simplified": "外语", "traditional": "外語", "pinyin": "wàiyǔ", "english": "foreign language", "part_of_speech": "noun", "example_chinese": "外语老师", "example_pinyin": "Wàiyǔ lǎoshī", "example_english": "Foreign-language teacher"},
            {"simplified": "医生", "traditional": "醫生", "pinyin": "yīshēng", "english": "doctor", "part_of_speech": "noun", "example_chinese": "我是医生", "example_pinyin": "Wǒ shì yīshēng", "example_english": "I am a doctor"},
            {"simplified": "您",   "traditional": "您",   "pinyin": "nín",   "english": "you (formal)", "part_of_speech": "pronoun", "example_chinese": "您好", "example_pinyin": "Nín hǎo", "example_english": "Hello (formal)"},
        ],
    },

    # ---------------------------- L4 ----------------------------
    {
        "lesson_number": 4,
        "title": "认识你很高兴 (Nice to Meet You)",
        "subtitle": "Names, introductions",
        "description": "Introduce yourself, ask names, and respond politely.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Lu Yuping", "chinese": "可以进来吗？", "pinyin": "Kěyǐ jìnlái ma?", "english": "May I come in?"},
            {"part": 1, "speaker": "Teacher Yang", "chinese": "请进！", "pinyin": "Qǐng jìn!", "english": "Please come in!"},
            {"part": 1, "speaker": "Lu Yuping", "chinese": "这是我朋友，他是记者。请问，您贵姓？", "pinyin": "Zhè shì wǒ péngyou, tā shì jìzhě. Qǐngwèn, nín guìxìng?", "english": "This is my friend, he is a journalist. May I ask, what is your surname?"},
            {"part": 1, "speaker": "Mr. Lu", "chinese": "我姓陆，叫陆雨平。", "pinyin": "Wǒ xìng Lù, jiào Lù Yǔpíng.", "english": "My surname is Lu, my name is Lu Yuping."},
            {"part": 1, "speaker": "Teacher Yang", "chinese": "你好，陆先生，认识你很高兴。", "pinyin": "Nǐ hǎo, Lù xiānsheng, rènshi nǐ hěn gāoxìng.", "english": "Hello, Mr. Lu, very pleased to meet you."},
            {"part": 2, "speaker": "Lin Na", "chinese": "你好！我是语言学院的学生，我姓林，叫林娜。我是英国人。你姓什么？", "pinyin": "Nǐ hǎo! Wǒ shì yǔyán xuéyuàn de xuésheng, wǒ xìng Lín, jiào Lín Nà. Wǒ shì Yīngguó rén. Nǐ xìng shénme?", "english": "Hello! I am a student of the Language Institute, my surname is Lin, my name is Lin Na. I am British. What is your surname?"},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "我姓马，叫马大为。", "pinyin": "Wǒ xìng Mǎ, jiào Mǎ Dàwéi.", "english": "My surname is Ma, my name is Ma Dawei."},
            {"part": 2, "speaker": "Lin Na", "chinese": "你是加拿大人吗？", "pinyin": "Nǐ shì Jiānádà rén ma?", "english": "Are you Canadian?"},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "我不是加拿大人，我是美国人。我学习汉语。", "pinyin": "Wǒ bú shì Jiānádà rén, wǒ shì Měiguó rén. Wǒ xuéxí Hànyǔ.", "english": "I’m not Canadian, I’m American. I study Chinese."},
        ],
        "grammar_notes": [
            {"title": "姓 vs 叫", "explanation": "姓 introduces the family name only (我姓林). 叫 gives the full name (我叫林娜)."},
            {"title": "请问 / 您贵姓?", "explanation": "Polite ways to ask: 请问 (may I ask), 您贵姓? (what is your honorable surname?)."},
            {"title": "Adjective predicate", "explanation": "认识你很高兴 — '(I’m) very glad to know you'. 很 + adjective is the normal predicate form."},
        ],
        "vocabulary": [
            {"simplified": "请",   "traditional": "請",   "pinyin": "qǐng",  "english": "please", "part_of_speech": "verb", "example_chinese": "请进", "example_pinyin": "Qǐng jìn", "example_english": "Please come in"},
            {"simplified": "问",   "traditional": "問",   "pinyin": "wèn",   "english": "to ask", "part_of_speech": "verb", "example_chinese": "请问", "example_pinyin": "Qǐngwèn", "example_english": "Excuse me"},
            {"simplified": "贵姓", "traditional": "貴姓", "pinyin": "guìxìng","english": "honorable surname", "part_of_speech": "phrase", "example_chinese": "您贵姓?", "example_pinyin": "Nín guìxìng?", "example_english": "Your surname?"},
            {"simplified": "姓",   "traditional": "姓",   "pinyin": "xìng",  "english": "surname; to be surnamed", "part_of_speech": "verb", "example_chinese": "我姓林", "example_pinyin": "Wǒ xìng Lín", "example_english": "My surname is Lin"},
            {"simplified": "叫",   "traditional": "叫",   "pinyin": "jiào",  "english": "to be called", "part_of_speech": "verb", "example_chinese": "我叫林娜", "example_pinyin": "Wǒ jiào Lín Nà", "example_english": "I’m called Lin Na"},
            {"simplified": "什么", "traditional": "什麼", "pinyin": "shénme","english": "what", "part_of_speech": "pronoun", "example_chinese": "你叫什么?", "example_pinyin": "Nǐ jiào shénme?", "example_english": "What is your name?"},
            {"simplified": "名字", "traditional": "名字", "pinyin": "míngzi","english": "name", "part_of_speech": "noun", "example_chinese": "我的名字", "example_pinyin": "Wǒ de míngzi", "example_english": "My name"},
            {"simplified": "认识", "traditional": "認識", "pinyin": "rènshi","english": "to know (someone)", "part_of_speech": "verb", "example_chinese": "认识你", "example_pinyin": "Rènshi nǐ", "example_english": "To meet you"},
            {"simplified": "高兴", "traditional": "高興", "pinyin": "gāoxìng","english": "happy; glad", "part_of_speech": "adjective", "example_chinese": "很高兴", "example_pinyin": "Hěn gāoxìng", "example_english": "Very glad"},
            {"simplified": "学习", "traditional": "學習", "pinyin": "xuéxí", "english": "to study", "part_of_speech": "verb", "example_chinese": "学习汉语", "example_pinyin": "Xuéxí Hànyǔ", "example_english": "Study Chinese"},
            {"simplified": "汉语", "traditional": "漢語", "pinyin": "Hànyǔ", "english": "Chinese language", "part_of_speech": "noun", "example_chinese": "说汉语", "example_pinyin": "Shuō Hànyǔ", "example_english": "Speak Chinese"},
            {"simplified": "学生", "traditional": "學生", "pinyin": "xuésheng","english": "student", "part_of_speech": "noun", "example_chinese": "我是学生", "example_pinyin": "Wǒ shì xuésheng", "example_english": "I am a student"},
            {"simplified": "英国", "traditional": "英國", "pinyin": "Yīngguó","english": "Britain; UK", "part_of_speech": "noun", "example_chinese": "英国人", "example_pinyin": "Yīngguó rén", "example_english": "British person"},
            {"simplified": "美国", "traditional": "美國", "pinyin": "Měiguó","english": "America; USA", "part_of_speech": "noun", "example_chinese": "美国人", "example_pinyin": "Měiguó rén", "example_english": "American person"},
            {"simplified": "加拿大","traditional": "加拿大","pinyin": "Jiānádà","english": "Canada", "part_of_speech": "noun", "example_chinese": "加拿大人", "example_pinyin": "Jiānádà rén", "example_english": "Canadian"},
        ],
    },

    # ---------------------------- L5 ----------------------------
    {
        "lesson_number": 5,
        "title": "餐厅在哪儿？ (Where Is the Cafeteria?)",
        "subtitle": "Locations & directions",
        "description": "Ask whether a place or person is there; give location.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Ma Dawei", "chinese": "请问，这是王小云的宿舍吗？", "pinyin": "Qǐngwèn, zhè shì Wáng Xiǎoyún de sùshè ma?", "english": "Excuse me, is this Wang Xiaoyun’s dormitory?"},
            {"part": 1, "speaker": "Roommate", "chinese": "是。请进，请坐。", "pinyin": "Shì. Qǐng jìn, qǐng zuò.", "english": "Yes. Please come in, please sit."},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "王小云在吗？", "pinyin": "Wáng Xiǎoyún zài ma?", "english": "Is Wang Xiaoyun here?"},
            {"part": 1, "speaker": "Roommate", "chinese": "她不在。", "pinyin": "Tā bú zài.", "english": "She isn’t here."},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "她在哪儿？", "pinyin": "Tā zài nǎr?", "english": "Where is she?"},
            {"part": 1, "speaker": "Roommate", "chinese": "对不起，我不知道。", "pinyin": "Duìbuqǐ, wǒ bù zhīdào.", "english": "Sorry, I don’t know."},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "没关系。好，再见。", "pinyin": "Méi guānxi. Hǎo, zàijiàn.", "english": "It doesn’t matter. OK, see you."},
            {"part": 2, "speaker": "Lin Na", "chinese": "小姐，请问餐厅在哪儿？", "pinyin": "Xiǎojiě, qǐngwèn cāntīng zài nǎr?", "english": "Miss, excuse me, where is the cafeteria?"},
            {"part": 2, "speaker": "Staff", "chinese": "在二层二零四号。", "pinyin": "Zài èr céng èr líng sì hào.", "english": "On the second floor, number 204."},
            {"part": 2, "speaker": "Lin Na", "chinese": "谢谢。", "pinyin": "Xièxie.", "english": "Thanks."},
            {"part": 2, "speaker": "Staff", "chinese": "不用谢。", "pinyin": "Bú yòng xiè.", "english": "You’re welcome."},
        ],
        "grammar_notes": [
            {"title": "在 (zài) — to be at", "explanation": "Subject + 在 + place: 她在家. 在 can also be used alone: 王小云在吗?"},
            {"title": "哪儿 (nǎr) — where", "explanation": "哪儿 asks for location: 餐厅在哪儿? "},
            {"title": "对不起 / 没关系", "explanation": "Politeness pair: 对不起 (sorry) → 没关系 (it doesn’t matter)."},
        ],
        "vocabulary": [
            {"simplified": "在",   "traditional": "在",   "pinyin": "zài",   "english": "to be at; in", "part_of_speech": "verb", "example_chinese": "我在家", "example_pinyin": "Wǒ zài jiā", "example_english": "I am at home"},
            {"simplified": "哪儿", "traditional": "哪兒", "pinyin": "nǎr",   "english": "where", "part_of_speech": "pronoun", "example_chinese": "你在哪儿?", "example_pinyin": "Nǐ zài nǎr?", "example_english": "Where are you?"},
            {"simplified": "这儿", "traditional": "這兒", "pinyin": "zhèr",  "english": "here", "part_of_speech": "pronoun", "example_chinese": "我在这儿", "example_pinyin": "Wǒ zài zhèr", "example_english": "I am here"},
            {"simplified": "那儿", "traditional": "那兒", "pinyin": "nàr",   "english": "there", "part_of_speech": "pronoun", "example_chinese": "他在那儿", "example_pinyin": "Tā zài nàr", "example_english": "He is there"},
            {"simplified": "餐厅", "traditional": "餐廳", "pinyin": "cāntīng","english": "cafeteria; restaurant", "part_of_speech": "noun", "example_chinese": "去餐厅", "example_pinyin": "Qù cāntīng", "example_english": "Go to the cafeteria"},
            {"simplified": "宿舍", "traditional": "宿舍", "pinyin": "sùshè", "english": "dormitory", "part_of_speech": "noun", "example_chinese": "我的宿舍", "example_pinyin": "Wǒ de sùshè", "example_english": "My dorm"},
            {"simplified": "对不起","traditional": "對不起","pinyin": "duìbuqǐ","english": "sorry", "part_of_speech": "phrase", "example_chinese": "对不起!", "example_pinyin": "Duìbuqǐ!", "example_english": "Sorry!"},
            {"simplified": "没关系","traditional": "沒關係","pinyin": "méi guānxi","english": "it’s OK", "part_of_speech": "phrase", "example_chinese": "没关系", "example_pinyin": "Méi guānxi", "example_english": "Never mind"},
            {"simplified": "知道", "traditional": "知道", "pinyin": "zhīdào","english": "to know (info)", "part_of_speech": "verb", "example_chinese": "我不知道", "example_pinyin": "Wǒ bù zhīdào", "example_english": "I don’t know"},
            {"simplified": "再见", "traditional": "再見", "pinyin": "zàijiàn","english": "goodbye", "part_of_speech": "phrase", "example_chinese": "再见!", "example_pinyin": "Zàijiàn!", "example_english": "Goodbye!"},
            {"simplified": "谢谢", "traditional": "謝謝", "pinyin": "xièxie","english": "thanks", "part_of_speech": "phrase", "example_chinese": "谢谢你", "example_pinyin": "Xièxie nǐ", "example_english": "Thank you"},
            {"simplified": "请坐", "traditional": "請坐", "pinyin": "qǐng zuò","english": "please sit", "part_of_speech": "phrase", "example_chinese": "请坐", "example_pinyin": "Qǐng zuò", "example_english": "Please sit"},
        ],
    },

    # ---------------------------- L6 ----------------------------
    {
        "lesson_number": 6,
        "title": "我们去游泳，好吗？ (Let’s Go Swimming)",
        "subtitle": "Suggestions",
        "description": "Suggest activities and react to invitations.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Lin Na", "chinese": "林娜，昨天的京剧怎么样？", "pinyin": "Lín Nà, zuótiān de jīngjù zěnmeyàng?", "english": "Lin Na, how was yesterday’s Beijing Opera?"},
            {"part": 1, "speaker": "Wang Xiaoyun", "chinese": "很有意思。今天天气很好，我们去游泳，好吗？", "pinyin": "Hěn yǒuyìsi. Jīntiān tiānqì hěn hǎo, wǒmen qù yóuyǒng, hǎo ma?", "english": "Very interesting. The weather is good today. Shall we go swimming?"},
            {"part": 1, "speaker": "Lin Na", "chinese": "太好了！什么时候去？", "pinyin": "Tài hǎo le! Shénme shíhou qù?", "english": "Great! When are we going?"},
            {"part": 1, "speaker": "Wang Xiaoyun", "chinese": "现在去可以吗？", "pinyin": "Xiànzài qù kěyǐ ma?", "english": "Is it OK to go now?"},
            {"part": 1, "speaker": "Lin Na", "chinese": "可以。", "pinyin": "Kěyǐ.", "english": "OK."},
            {"part": 2, "speaker": "Libo", "chinese": "杨老师，明天您有时间吗？", "pinyin": "Yáng Lǎoshī, míngtiān nín yǒu shíjiān ma?", "english": "Teacher Yang, do you have time tomorrow?"},
            {"part": 2, "speaker": "Teacher Yang", "chinese": "对不起，请再说一遍。", "pinyin": "Duìbuqǐ, qǐng zài shuō yí biàn.", "english": "Sorry, please say that again."},
            {"part": 2, "speaker": "Libo", "chinese": "明天您有时间吗？我们去打球，好吗？", "pinyin": "Míngtiān nín yǒu shíjiān ma? Wǒmen qù dǎqiú, hǎo ma?", "english": "Do you have time tomorrow? How about we go play ball?"},
            {"part": 2, "speaker": "Teacher Yang", "chinese": "很抱歉，明天我很忙，恐怕不行。", "pinyin": "Hěn bàoqiàn, míngtiān wǒ hěn máng, kǒngpà bù xíng.", "english": "Very sorry, I’m busy tomorrow, I’m afraid I can’t."},
        ],
        "grammar_notes": [
            {"title": "...，好吗？ — Suggestions", "explanation": "Append 好吗? to invite agreement: 我们去吃饭，好吗?"},
            {"title": "什么时候?", "explanation": "什么时候 asks 'when?': 你什么时候去? = When are you going?"},
            {"title": "可以 (kěyǐ) — may; permission", "explanation": "可以 expresses permission/possibility: 现在去可以吗? (Is it OK to go now?)"},
        ],
        "vocabulary": [
            {"simplified": "今天", "traditional": "今天", "pinyin": "jīntiān","english": "today", "part_of_speech": "noun", "example_chinese": "今天很忙", "example_pinyin": "Jīntiān hěn máng", "example_english": "Today is busy"},
            {"simplified": "昨天", "traditional": "昨天", "pinyin": "zuótiān","english": "yesterday", "part_of_speech": "noun", "example_chinese": "昨天好", "example_pinyin": "Zuótiān hǎo", "example_english": "Yesterday was good"},
            {"simplified": "明天", "traditional": "明天", "pinyin": "míngtiān","english": "tomorrow", "part_of_speech": "noun", "example_chinese": "明天见", "example_pinyin": "Míngtiān jiàn", "example_english": "See you tomorrow"},
            {"simplified": "天气", "traditional": "天氣", "pinyin": "tiānqì", "english": "weather", "part_of_speech": "noun", "example_chinese": "天气好", "example_pinyin": "Tiānqì hǎo", "example_english": "Good weather"},
            {"simplified": "游泳", "traditional": "游泳", "pinyin": "yóuyǒng","english": "to swim", "part_of_speech": "verb", "example_chinese": "去游泳", "example_pinyin": "Qù yóuyǒng", "example_english": "Go swimming"},
            {"simplified": "打球", "traditional": "打球", "pinyin": "dǎqiú",  "english": "to play ball", "part_of_speech": "verb", "example_chinese": "去打球", "example_pinyin": "Qù dǎqiú", "example_english": "Go play ball"},
            {"simplified": "去",   "traditional": "去",   "pinyin": "qù",    "english": "to go", "part_of_speech": "verb", "example_chinese": "我去学校", "example_pinyin": "Wǒ qù xuéxiào", "example_english": "I go to school"},
            {"simplified": "时候", "traditional": "時候", "pinyin": "shíhou","english": "time; moment", "part_of_speech": "noun", "example_chinese": "什么时候?", "example_pinyin": "Shénme shíhou?", "example_english": "When?"},
            {"simplified": "现在", "traditional": "現在", "pinyin": "xiànzài","english": "now", "part_of_speech": "noun", "example_chinese": "现在去", "example_pinyin": "Xiànzài qù", "example_english": "Go now"},
            {"simplified": "可以", "traditional": "可以", "pinyin": "kěyǐ",  "english": "may; can (permission)", "part_of_speech": "modal", "example_chinese": "可以进", "example_pinyin": "Kěyǐ jìn", "example_english": "May come in"},
            {"simplified": "有",   "traditional": "有",   "pinyin": "yǒu",   "english": "to have", "part_of_speech": "verb", "example_chinese": "我有时间", "example_pinyin": "Wǒ yǒu shíjiān", "example_english": "I have time"},
            {"simplified": "时间", "traditional": "時間", "pinyin": "shíjiān","english": "time", "part_of_speech": "noun", "example_chinese": "有时间", "example_pinyin": "Yǒu shíjiān", "example_english": "Have time"},
            {"simplified": "有意思","traditional": "有意思","pinyin": "yǒuyìsi","english": "interesting", "part_of_speech": "adjective", "example_chinese": "很有意思", "example_pinyin": "Hěn yǒuyìsi", "example_english": "Very interesting"},
            {"simplified": "京剧", "traditional": "京劇", "pinyin": "jīngjù","english": "Beijing Opera", "part_of_speech": "noun", "example_chinese": "看京剧", "example_pinyin": "Kàn jīngjù", "example_english": "Watch Beijing Opera"},
        ],
    },

    # ---------------------------- L7 ----------------------------
    {
        "lesson_number": 7,
        "title": "你认识不认识他？ (Do You Know Him?)",
        "subtitle": "V-not-V questions",
        "description": "Form yes/no questions by repeating the verb with 不.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Lin Na", "chinese": "力波，明天开学，我很高兴。", "pinyin": "Lìbō, míngtiān kāixué, wǒ hěn gāoxìng.", "english": "Libo, school starts tomorrow, I’m very happy."},
            {"part": 1, "speaker": "Lin Na", "chinese": "你看，他是不是我们学院的老师？", "pinyin": "Nǐ kàn, tā shì bu shì wǒmen xuéyuàn de lǎoshī?", "english": "Look — isn’t he a teacher from our institute?"},
            {"part": 1, "speaker": "Libo", "chinese": "我问一下。请问，您是我们学院的老师吗？", "pinyin": "Wǒ wèn yíxià. Qǐngwèn, nín shì wǒmen xuéyuàn de lǎoshī ma?", "english": "Let me ask. Excuse me, are you a teacher from our institute?"},
            {"part": 1, "speaker": "Professor Zhang", "chinese": "是，我是语言学院的老师。我姓张。", "pinyin": "Shì, wǒ shì yǔyán xuéyuàn de lǎoshī. Wǒ xìng Zhāng.", "english": "Yes, I’m a teacher of the Language Institute. My surname is Zhang."},
            {"part": 1, "speaker": "Libo", "chinese": "认识您，我们很高兴。", "pinyin": "Rènshi nín, wǒmen hěn gāoxìng.", "english": "We are pleased to meet you."},
            {"part": 2, "speaker": "Lin Na", "chinese": "那是马大为。你认识不认识他？", "pinyin": "Nà shì Mǎ Dàwéi. Nǐ rènshi bu rènshi tā?", "english": "That is Ma Dawei. Do you know him?"},
            {"part": 2, "speaker": "Libo", "chinese": "我不认识他。", "pinyin": "Wǒ bú rènshi tā.", "english": "I don’t know him."},
            {"part": 2, "speaker": "Lin Na", "chinese": "我来介绍一下。大为，这是我朋友。", "pinyin": "Wǒ lái jièshào yíxià. Dàwéi, zhè shì wǒ péngyou.", "english": "Let me introduce you. Dawei, this is my friend."},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "你学习什么专业？", "pinyin": "Nǐ xuéxí shénme zhuānyè?", "english": "What major are you studying?"},
            {"part": 2, "speaker": "Libo", "chinese": "我学习美术专业。你呢？", "pinyin": "Wǒ xuéxí měishù zhuānyè. Nǐ ne?", "english": "I study fine arts. And you?"},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "我学习文学专业。现在我学习汉语。", "pinyin": "Wǒ xuéxí wénxué zhuānyè. Xiànzài wǒ xuéxí Hànyǔ.", "english": "I study literature. Right now I’m learning Chinese."},
        ],
        "grammar_notes": [
            {"title": "V-不-V questions", "explanation": "Repeat the verb with 不 between: 你认识不认识他? = 你认识他吗? Both ask the same yes/no question."},
            {"title": "的 (de) — possessive", "explanation": "Place 的 between possessor and possessed: 我们学院的老师 (a teacher of our institute)."},
            {"title": "一下 (yíxià)", "explanation": "Softens the verb: 我问一下 (let me ask). 我来介绍一下 (let me introduce briefly)."},
        ],
        "vocabulary": [
            {"simplified": "学院", "traditional": "學院", "pinyin": "xuéyuàn","english": "institute; college", "part_of_speech": "noun", "example_chinese": "语言学院", "example_pinyin": "Yǔyán xuéyuàn", "example_english": "Language Institute"},
            {"simplified": "语言", "traditional": "語言", "pinyin": "yǔyán", "english": "language", "part_of_speech": "noun", "example_chinese": "学语言", "example_pinyin": "Xué yǔyán", "example_english": "Study language"},
            {"simplified": "介绍", "traditional": "介紹", "pinyin": "jièshào","english": "to introduce", "part_of_speech": "verb", "example_chinese": "介绍朋友", "example_pinyin": "Jièshào péngyou", "example_english": "Introduce a friend"},
            {"simplified": "教授", "traditional": "教授", "pinyin": "jiàoshòu","english": "professor", "part_of_speech": "noun", "example_chinese": "张教授", "example_pinyin": "Zhāng jiàoshòu", "example_english": "Professor Zhang"},
            {"simplified": "专业", "traditional": "專業", "pinyin": "zhuānyè","english": "major; specialty", "part_of_speech": "noun", "example_chinese": "什么专业?", "example_pinyin": "Shénme zhuānyè?", "example_english": "Which major?"},
            {"simplified": "美术", "traditional": "美術", "pinyin": "měishù","english": "fine arts", "part_of_speech": "noun", "example_chinese": "美术专业", "example_pinyin": "Měishù zhuānyè", "example_english": "Fine-arts major"},
            {"simplified": "文学", "traditional": "文學", "pinyin": "wénxué","english": "literature", "part_of_speech": "noun", "example_chinese": "文学专业", "example_pinyin": "Wénxué zhuānyè", "example_english": "Literature major"},
            {"simplified": "的",   "traditional": "的",   "pinyin": "de",    "english": "possessive particle", "part_of_speech": "particle", "example_chinese": "我的书", "example_pinyin": "Wǒ de shū", "example_english": "My book"},
            {"simplified": "名片", "traditional": "名片", "pinyin": "míngpiàn","english": "business card", "part_of_speech": "noun", "example_chinese": "我的名片", "example_pinyin": "Wǒ de míngpiàn", "example_english": "My business card"},
            {"simplified": "开学", "traditional": "開學", "pinyin": "kāixué","english": "to start school", "part_of_speech": "verb", "example_chinese": "明天开学", "example_pinyin": "Míngtiān kāixué", "example_english": "School starts tomorrow"},
        ],
    },

    # ---------------------------- L8 ----------------------------
    {
        "lesson_number": 8,
        "title": "你们家有几口人？ (How Many in Your Family?)",
        "subtitle": "Family & quantities",
        "description": "Talk about family members and ask 'how many?'.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Libo", "chinese": "这是不是你们家的照片？", "pinyin": "Zhè shì bu shì nǐmen jiā de zhàopiàn?", "english": "Is this a photo of your family?"},
            {"part": 1, "speaker": "Lin Na", "chinese": "是啊。", "pinyin": "Shì a.", "english": "Yes."},
            {"part": 1, "speaker": "Libo", "chinese": "我看一下。你们家有几口人？", "pinyin": "Wǒ kàn yíxià. Nǐmen jiā yǒu jǐ kǒu rén?", "english": "Let me see. How many people are in your family?"},
            {"part": 1, "speaker": "Lin Na", "chinese": "我们家有四口人：爸爸、妈妈、哥哥和我。", "pinyin": "Wǒmen jiā yǒu sì kǒu rén: bàba, māma, gēge hé wǒ.", "english": "We have four: dad, mom, my older brother and me."},
            {"part": 1, "speaker": "Lin Na", "chinese": "你呢？", "pinyin": "Nǐ ne?", "english": "And you?"},
            {"part": 1, "speaker": "Libo", "chinese": "我有妈妈，有一个姐姐和两个弟弟。我们家一共有六口人。", "pinyin": "Wǒ yǒu māma, yǒu yí ge jiějie hé liǎng ge dìdi. Wǒmen jiā yígòng yǒu liù kǒu rén.", "english": "I have a mother, an older sister and two younger brothers. Six in total."},
            {"part": 2, "speaker": "Lin Na", "chinese": "语言学院大不大？", "pinyin": "Yǔyán xuéyuàn dà bu dà?", "english": "Is the Language Institute big?"},
            {"part": 2, "speaker": "Libo", "chinese": "不太大。", "pinyin": "Bú tài dà.", "english": "Not too big."},
            {"part": 2, "speaker": "Lin Na", "chinese": "语言学院有多少个系？", "pinyin": "Yǔyán xuéyuàn yǒu duōshao ge xì?", "english": "How many departments does it have?"},
            {"part": 2, "speaker": "Libo", "chinese": "有十二个系。", "pinyin": "Yǒu shí’èr ge xì.", "english": "Twelve departments."},
        ],
        "grammar_notes": [
            {"title": "几 vs 多少", "explanation": "几 asks for small numbers (<10); 多少 asks any quantity. Both require/allow a measure word."},
            {"title": "口 — measure for family", "explanation": "Use 口 to count people in a family: 四口人."},
            {"title": "两 vs 二", "explanation": "Use 两 (not 二) before measure words for quantity: 两个弟弟."},
        ],
        "vocabulary": [
            {"simplified": "家",   "traditional": "家",   "pinyin": "jiā",   "english": "home; family", "part_of_speech": "noun", "example_chinese": "我家", "example_pinyin": "Wǒ jiā", "example_english": "My family"},
            {"simplified": "几",   "traditional": "幾",   "pinyin": "jǐ",    "english": "how many (small)", "part_of_speech": "pronoun", "example_chinese": "几个?", "example_pinyin": "Jǐ ge?", "example_english": "How many?"},
            {"simplified": "口",   "traditional": "口",   "pinyin": "kǒu",   "english": "MW for family members", "part_of_speech": "measure", "example_chinese": "四口人", "example_pinyin": "Sì kǒu rén", "example_english": "Four people"},
            {"simplified": "多少", "traditional": "多少", "pinyin": "duōshao","english": "how many; how much", "part_of_speech": "pronoun", "example_chinese": "多少钱?", "example_pinyin": "Duōshao qián?", "example_english": "How much?"},
            {"simplified": "个",   "traditional": "個",   "pinyin": "ge",    "english": "general measure word", "part_of_speech": "measure", "example_chinese": "一个人", "example_pinyin": "Yí ge rén", "example_english": "One person"},
            {"simplified": "和",   "traditional": "和",   "pinyin": "hé",    "english": "and", "part_of_speech": "conjunction", "example_chinese": "你和我", "example_pinyin": "Nǐ hé wǒ", "example_english": "You and I"},
            {"simplified": "姐姐", "traditional": "姐姐", "pinyin": "jiějie","english": "older sister", "part_of_speech": "noun", "example_chinese": "我姐姐", "example_pinyin": "Wǒ jiějie", "example_english": "My older sister"},
            {"simplified": "弟弟", "traditional": "弟弟", "pinyin": "dìdi",  "english": "younger brother", "part_of_speech": "noun", "example_chinese": "我弟弟", "example_pinyin": "Wǒ dìdi", "example_english": "My younger brother"},
            {"simplified": "妹妹", "traditional": "妹妹", "pinyin": "mèimei","english": "younger sister", "part_of_speech": "noun", "example_chinese": "我妹妹", "example_pinyin": "Wǒ mèimei", "example_english": "My younger sister"},
            {"simplified": "两",   "traditional": "兩",   "pinyin": "liǎng", "english": "two (with MW)", "part_of_speech": "number", "example_chinese": "两个", "example_pinyin": "Liǎng ge", "example_english": "Two"},
            {"simplified": "一共", "traditional": "一共", "pinyin": "yígòng","english": "in total", "part_of_speech": "adverb", "example_chinese": "一共五个", "example_pinyin": "Yígòng wǔ ge", "example_english": "Five in total"},
            {"simplified": "照片", "traditional": "照片", "pinyin": "zhàopiàn","english": "photo", "part_of_speech": "noun", "example_chinese": "看照片", "example_pinyin": "Kàn zhàopiàn", "example_english": "Look at a photo"},
            {"simplified": "系",   "traditional": "系",   "pinyin": "xì",    "english": "department (school)", "part_of_speech": "noun", "example_chinese": "外语系", "example_pinyin": "Wàiyǔ xì", "example_english": "Foreign-language dept"},
            {"simplified": "工作", "traditional": "工作", "pinyin": "gōngzuò","english": "work; to work", "part_of_speech": "verb/noun", "example_chinese": "什么工作?", "example_pinyin": "Shénme gōngzuò?", "example_english": "What work?"},
        ],
    },

    # ---------------------------- L9 ----------------------------
    {
        "lesson_number": 9,
        "title": "他今年二十岁 (He’s Twenty This Year)",
        "subtitle": "Dates, ages, parties",
        "description": "Talk about days of the week, dates, ages, and birthdays.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Libo", "chinese": "林娜，明天上午你有没有课？", "pinyin": "Lín Nà, míngtiān shàngwǔ nǐ yǒu méi yǒu kè?", "english": "Lin Na, do you have class tomorrow morning?"},
            {"part": 1, "speaker": "Lin Na", "chinese": "明天是星期几？", "pinyin": "Míngtiān shì xīngqī jǐ?", "english": "What day is tomorrow?"},
            {"part": 1, "speaker": "Libo", "chinese": "明天是星期四。", "pinyin": "Míngtiān shì xīngqīsì.", "english": "Tomorrow is Thursday."},
            {"part": 1, "speaker": "Lin Na", "chinese": "我上午、下午都有课。", "pinyin": "Wǒ shàngwǔ, xiàwǔ dōu yǒu kè.", "english": "I have classes both morning and afternoon."},
            {"part": 1, "speaker": "Libo", "chinese": "你星期日有时间吗？", "pinyin": "Nǐ xīngqīrì yǒu shíjiān ma?", "english": "Do you have time on Sunday?"},
            {"part": 1, "speaker": "Libo", "chinese": "星期日是十月二十七号，是宋华的生日。他今年二十岁。", "pinyin": "Xīngqīrì shì shí yuè èrshíqī hào, shì Sòng Huá de shēngrì. Tā jīnnián èrshí suì.", "english": "Sunday is October 27th, Song Hua’s birthday. He is 20 this year."},
            {"part": 1, "speaker": "Lin Na", "chinese": "太好了！我当然参加。", "pinyin": "Tài hǎo le! Wǒ dāngrán cānjiā.", "english": "Great! Of course I’ll join."},
            {"part": 2, "speaker": "Friends", "chinese": "宋华，祝你生日快乐！", "pinyin": "Sòng Huá, zhù nǐ shēngrì kuàilè!", "english": "Song Hua, happy birthday!"},
            {"part": 2, "speaker": "Song Hua", "chinese": "谢谢。今天我们吃北京烤鸭。", "pinyin": "Xièxie. Jīntiān wǒmen chī Běijīng kǎoyā.", "english": "Thanks. Today we’re eating Beijing roast duck."},
            {"part": 2, "speaker": "Lin Na", "chinese": "我们喝什么酒？", "pinyin": "Wǒmen hē shénme jiǔ?", "english": "What wine are we drinking?"},
            {"part": 2, "speaker": "Song Hua", "chinese": "当然喝红葡萄酒。", "pinyin": "Dāngrán hē hóng pútáojiǔ.", "english": "Red wine, of course."},
        ],
        "grammar_notes": [
            {"title": "Days, dates, ages", "explanation": "星期一/二/.../日 = Mon/Tue/.../Sun. 几月几号 = month/day. 多大 = how old (adult), 几岁 = (child)."},
            {"title": "Affirmative-negative questions", "explanation": "你有没有课? = 你有课吗? (Do you have class?)"},
            {"title": "祝...快乐", "explanation": "祝你生日快乐 = Happy birthday. Pattern: 祝 + person + happy/celebration."},
        ],
        "vocabulary": [
            {"simplified": "今年", "traditional": "今年", "pinyin": "jīnnián","english": "this year", "part_of_speech": "noun", "example_chinese": "今年很忙", "example_pinyin": "Jīnnián hěn máng", "example_english": "Busy this year"},
            {"simplified": "多大", "traditional": "多大", "pinyin": "duō dà","english": "how old (adult)", "part_of_speech": "phrase", "example_chinese": "你多大?", "example_pinyin": "Nǐ duō dà?", "example_english": "How old are you?"},
            {"simplified": "岁",   "traditional": "歲",   "pinyin": "suì",   "english": "years (of age)", "part_of_speech": "measure", "example_chinese": "二十岁", "example_pinyin": "Èrshí suì", "example_english": "20 years old"},
            {"simplified": "星期", "traditional": "星期", "pinyin": "xīngqī","english": "week", "part_of_speech": "noun", "example_chinese": "星期一", "example_pinyin": "Xīngqīyī", "example_english": "Monday"},
            {"simplified": "课",   "traditional": "課",   "pinyin": "kè",    "english": "class; lesson", "part_of_speech": "noun", "example_chinese": "上课", "example_pinyin": "Shàngkè", "example_english": "Have class"},
            {"simplified": "上午", "traditional": "上午", "pinyin": "shàngwǔ","english": "morning", "part_of_speech": "noun", "example_chinese": "上午来", "example_pinyin": "Shàngwǔ lái", "example_english": "Come in the morning"},
            {"simplified": "下午", "traditional": "下午", "pinyin": "xiàwǔ", "english": "afternoon", "part_of_speech": "noun", "example_chinese": "下午去", "example_pinyin": "Xiàwǔ qù", "example_english": "Go in the afternoon"},
            {"simplified": "月",   "traditional": "月",   "pinyin": "yuè",   "english": "month", "part_of_speech": "noun", "example_chinese": "十月", "example_pinyin": "Shí yuè", "example_english": "October"},
            {"simplified": "号",   "traditional": "號",   "pinyin": "hào",   "english": "day of month", "part_of_speech": "noun", "example_chinese": "二十七号", "example_pinyin": "Èrshíqī hào", "example_english": "27th"},
            {"simplified": "生日", "traditional": "生日", "pinyin": "shēngrì","english": "birthday", "part_of_speech": "noun", "example_chinese": "我的生日", "example_pinyin": "Wǒ de shēngrì", "example_english": "My birthday"},
            {"simplified": "快乐", "traditional": "快樂", "pinyin": "kuàilè","english": "happy", "part_of_speech": "adjective", "example_chinese": "生日快乐", "example_pinyin": "Shēngrì kuàilè", "example_english": "Happy birthday"},
            {"simplified": "祝",   "traditional": "祝",   "pinyin": "zhù",   "english": "to wish", "part_of_speech": "verb", "example_chinese": "祝你好运", "example_pinyin": "Zhù nǐ hǎoyùn", "example_english": "Good luck"},
            {"simplified": "参加", "traditional": "參加", "pinyin": "cānjiā","english": "to attend; join", "part_of_speech": "verb", "example_chinese": "参加聚会", "example_pinyin": "Cānjiā jùhuì", "example_english": "Join the party"},
            {"simplified": "吃",   "traditional": "吃",   "pinyin": "chī",   "english": "to eat", "part_of_speech": "verb", "example_chinese": "吃饭", "example_pinyin": "Chī fàn", "example_english": "Eat"},
            {"simplified": "烤鸭", "traditional": "烤鴨", "pinyin": "kǎoyā", "english": "roast duck", "part_of_speech": "noun", "example_chinese": "北京烤鸭", "example_pinyin": "Běijīng kǎoyā", "example_english": "Beijing roast duck"},
            {"simplified": "葡萄酒","traditional": "葡萄酒","pinyin": "pútáojiǔ","english": "wine (grape)", "part_of_speech": "noun", "example_chinese": "红葡萄酒", "example_pinyin": "Hóng pútáojiǔ", "example_english": "Red wine"},
        ],
    },

    # ---------------------------- L10 ----------------------------
    {
        "lesson_number": 10,
        "title": "我在这儿买光盘 (I’m Buying CDs Here)",
        "subtitle": "Shopping & prices",
        "description": "Express current actions and buy things; ask the price.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Lin Na", "chinese": "大为！你在这儿买什么？", "pinyin": "Dàwéi! Nǐ zài zhèr mǎi shénme?", "english": "Dawei! What are you buying here?"},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "我买音乐光盘。", "pinyin": "Wǒ mǎi yīnyuè guāngpán.", "english": "I’m buying music CDs."},
            {"part": 1, "speaker": "Lin Na", "chinese": "你常常来这儿吗？", "pinyin": "Nǐ chángcháng lái zhèr ma?", "english": "Do you often come here?"},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "我不常来。星期天我常跟林娜去小商场。", "pinyin": "Wǒ bù cháng lái. Xīngqītiān wǒ cháng gēn Lín Nà qù xiǎo shāngchǎng.", "english": "I don’t come often. On Sundays I usually go to the small mall with Lin Na."},
            {"part": 1, "speaker": "Lin Na", "chinese": "你喜欢什么音乐？", "pinyin": "Nǐ xǐhuan shénme yīnyuè?", "english": "What kind of music do you like?"},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "我喜欢中国音乐。", "pinyin": "Wǒ xǐhuan Zhōngguó yīnyuè.", "english": "I like Chinese music."},
            {"part": 2, "speaker": "Vendor", "chinese": "先生，您要什么？", "pinyin": "Xiānsheng, nín yào shénme?", "english": "Sir, what do you want?"},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "一斤苹果多少钱？", "pinyin": "Yì jīn píngguǒ duōshao qián?", "english": "How much is one jin of apples?"},
            {"part": 2, "speaker": "Vendor", "chinese": "一斤三块二毛钱。", "pinyin": "Yì jīn sān kuài èr máo qián.", "english": "3.20 yuan per jin."},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "我买三斤香蕉和两斤苹果。", "pinyin": "Wǒ mǎi sān jīn xiāngjiāo hé liǎng jīn píngguǒ.", "english": "I’ll buy 3 jin of bananas and 2 jin of apples."},
            {"part": 2, "speaker": "Vendor", "chinese": "一共十四块钱。", "pinyin": "Yígòng shísì kuài qián.", "english": "14 yuan in total."},
        ],
        "grammar_notes": [
            {"title": "在 + place + verb", "explanation": "我在这儿买光盘 = I’m buying CDs here. The 在 phrase precedes the verb."},
            {"title": "常常 / 不常", "explanation": "常常 = often (placed before the verb). Negate as 不常."},
            {"title": "Asking price", "explanation": "Quantity + Noun + 多少钱? — 一斤苹果多少钱? = How much for one jin of apples?"},
            {"title": "块 / 毛 / 分", "explanation": "Currency units (colloquial): 块 (yuan), 毛 (10 cents), 分 (cent)."},
        ],
        "vocabulary": [
            {"simplified": "买",   "traditional": "買",   "pinyin": "mǎi",   "english": "to buy", "part_of_speech": "verb", "example_chinese": "买书", "example_pinyin": "Mǎi shū", "example_english": "Buy a book"},
            {"simplified": "卖",   "traditional": "賣",   "pinyin": "mài",   "english": "to sell", "part_of_speech": "verb", "example_chinese": "卖水果", "example_pinyin": "Mài shuǐguǒ", "example_english": "Sell fruit"},
            {"simplified": "光盘", "traditional": "光盤", "pinyin": "guāngpán","english": "CD; disc", "part_of_speech": "noun", "example_chinese": "买光盘", "example_pinyin": "Mǎi guāngpán", "example_english": "Buy a CD"},
            {"simplified": "音乐", "traditional": "音樂", "pinyin": "yīnyuè","english": "music", "part_of_speech": "noun", "example_chinese": "听音乐", "example_pinyin": "Tīng yīnyuè", "example_english": "Listen to music"},
            {"simplified": "常常", "traditional": "常常", "pinyin": "chángcháng","english": "often", "part_of_speech": "adverb", "example_chinese": "常常来", "example_pinyin": "Chángcháng lái", "example_english": "Often come"},
            {"simplified": "跟",   "traditional": "跟",   "pinyin": "gēn",   "english": "with", "part_of_speech": "preposition", "example_chinese": "跟我来", "example_pinyin": "Gēn wǒ lái", "example_english": "Come with me"},
            {"simplified": "商场", "traditional": "商場", "pinyin": "shāngchǎng","english": "mall; shop", "part_of_speech": "noun", "example_chinese": "去商场", "example_pinyin": "Qù shāngchǎng", "example_english": "Go to mall"},
            {"simplified": "喜欢", "traditional": "喜歡", "pinyin": "xǐhuan","english": "to like", "part_of_speech": "verb", "example_chinese": "喜欢音乐", "example_pinyin": "Xǐhuan yīnyuè", "example_english": "Like music"},
            {"simplified": "钱",   "traditional": "錢",   "pinyin": "qián",  "english": "money", "part_of_speech": "noun", "example_chinese": "多少钱?", "example_pinyin": "Duōshao qián?", "example_english": "How much?"},
            {"simplified": "块",   "traditional": "塊",   "pinyin": "kuài",  "english": "yuan (colloq.)", "part_of_speech": "measure", "example_chinese": "三块钱", "example_pinyin": "Sān kuài qián", "example_english": "3 yuan"},
            {"simplified": "毛",   "traditional": "毛",   "pinyin": "máo",   "english": "0.1 yuan", "part_of_speech": "measure", "example_chinese": "两毛", "example_pinyin": "Liǎng máo", "example_english": "20 cents"},
            {"simplified": "斤",   "traditional": "斤",   "pinyin": "jīn",   "english": "jin (500 g)", "part_of_speech": "measure", "example_chinese": "一斤", "example_pinyin": "Yì jīn", "example_english": "One jin"},
            {"simplified": "苹果", "traditional": "蘋果", "pinyin": "píngguǒ","english": "apple", "part_of_speech": "noun", "example_chinese": "买苹果", "example_pinyin": "Mǎi píngguǒ", "example_english": "Buy apples"},
            {"simplified": "香蕉", "traditional": "香蕉", "pinyin": "xiāngjiāo","english": "banana", "part_of_speech": "noun", "example_chinese": "吃香蕉", "example_pinyin": "Chī xiāngjiāo", "example_english": "Eat a banana"},
            {"simplified": "贵",   "traditional": "貴",   "pinyin": "guì",   "english": "expensive", "part_of_speech": "adjective", "example_chinese": "很贵", "example_pinyin": "Hěn guì", "example_english": "Very expensive"},
        ],
    },

    # ---------------------------- L11 ----------------------------
    {
        "lesson_number": 11,
        "title": "我会说一点儿汉语 (I Can Speak a Little Chinese)",
        "subtitle": "Modal verbs 会 / 能 / 应该",
        "description": "Express ability, possibility and obligation.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Driver", "chinese": "小姐，您去哪儿？", "pinyin": "Xiǎojiě, nín qù nǎr?", "english": "Miss, where are you going?"},
            {"part": 1, "speaker": "Lin Na", "chinese": "我去语言学院。", "pinyin": "Wǒ qù yǔyán xuéyuàn.", "english": "I’m going to the Language Institute."},
            {"part": 1, "speaker": "Lin Na", "chinese": "师傅，请问现在几点？", "pinyin": "Shīfu, qǐngwèn xiànzài jǐ diǎn?", "english": "Driver, what time is it now?"},
            {"part": 1, "speaker": "Driver", "chinese": "差一刻八点。您会说汉语啊！", "pinyin": "Chà yí kè bā diǎn. Nín huì shuō Hànyǔ a!", "english": "Quarter to eight. You can speak Chinese!"},
            {"part": 1, "speaker": "Lin Na", "chinese": "我会说一点儿汉语。师傅，我们八点能到吗？", "pinyin": "Wǒ huì shuō yìdiǎnr Hànyǔ. Shīfu, wǒmen bā diǎn néng dào ma?", "english": "I can speak a little Chinese. Can we arrive by 8?"},
            {"part": 1, "speaker": "Driver", "chinese": "能到。", "pinyin": "Néng dào.", "english": "Yes, we can."},
            {"part": 2, "speaker": "Wang Xiaoyun", "chinese": "陈老师，马大为今天不能来上课。", "pinyin": "Chén lǎoshī, Mǎ Dàwéi jīntiān bù néng lái shàngkè.", "english": "Teacher Chen, Ma Dawei can’t come to class today."},
            {"part": 2, "speaker": "Teacher Chen", "chinese": "他为什么不能来上课？", "pinyin": "Tā wèishénme bù néng lái shàngkè?", "english": "Why can’t he come?"},
            {"part": 2, "speaker": "Wang Xiaoyun", "chinese": "昨天他十二点写汉字，两点钟睡觉。现在还没起床。", "pinyin": "Zuótiān tā shí’èr diǎn xiě Hànzì, liǎng diǎn zhōng shuìjiào. Xiànzài hái méi qǐchuáng.", "english": "Yesterday he wrote characters at 12 and slept at 2. He still hasn’t got up."},
            {"part": 2, "speaker": "Teacher Chen", "chinese": "他应该来上课。", "pinyin": "Tā yīnggāi lái shàngkè.", "english": "He should come to class."},
        ],
        "grammar_notes": [
            {"title": "会 vs 能 vs 可以", "explanation": "会 = learned ability; 能 = capability/circumstance; 可以 = permission. All come before the verb."},
            {"title": "Time-of-day", "explanation": "几点 = what o’clock; 差一刻八点 = 7:45 (a quarter to 8). 八点上课 = class at 8."},
            {"title": "Negative modals", "explanation": "Negate with 不 + modal: 不会, 不能, 不可以."},
        ],
        "vocabulary": [
            {"simplified": "会",   "traditional": "會",   "pinyin": "huì",   "english": "can; able to (learned)", "part_of_speech": "modal", "example_chinese": "我会游泳", "example_pinyin": "Wǒ huì yóuyǒng", "example_english": "I can swim"},
            {"simplified": "能",   "traditional": "能",   "pinyin": "néng",  "english": "can; able to", "part_of_speech": "modal", "example_chinese": "能到", "example_pinyin": "Néng dào", "example_english": "Can arrive"},
            {"simplified": "应该", "traditional": "應該", "pinyin": "yīnggāi","english": "should", "part_of_speech": "modal", "example_chinese": "应该来", "example_pinyin": "Yīnggāi lái", "example_english": "Should come"},
            {"simplified": "说",   "traditional": "說",   "pinyin": "shuō",  "english": "to speak", "part_of_speech": "verb", "example_chinese": "说汉语", "example_pinyin": "Shuō Hànyǔ", "example_english": "Speak Chinese"},
            {"simplified": "点",   "traditional": "點",   "pinyin": "diǎn",  "english": "o’clock", "part_of_speech": "measure", "example_chinese": "三点", "example_pinyin": "Sān diǎn", "example_english": "3 o’clock"},
            {"simplified": "刻",   "traditional": "刻",   "pinyin": "kè",    "english": "quarter (15 min)", "part_of_speech": "measure", "example_chinese": "一刻", "example_pinyin": "Yí kè", "example_english": "A quarter"},
            {"simplified": "分",   "traditional": "分",   "pinyin": "fēn",   "english": "minute", "part_of_speech": "measure", "example_chinese": "五分钟", "example_pinyin": "Wǔ fēnzhōng", "example_english": "5 minutes"},
            {"simplified": "一点儿","traditional": "一點兒","pinyin": "yìdiǎnr","english": "a little", "part_of_speech": "phrase", "example_chinese": "一点儿汉语", "example_pinyin": "Yìdiǎnr Hànyǔ", "example_english": "A little Chinese"},
            {"simplified": "为什么","traditional": "為什麼","pinyin": "wèishénme","english": "why", "part_of_speech": "pronoun", "example_chinese": "为什么不来?", "example_pinyin": "Wèishénme bù lái?", "example_english": "Why aren’t you coming?"},
            {"simplified": "上课", "traditional": "上課", "pinyin": "shàngkè","english": "to attend class", "part_of_speech": "verb", "example_chinese": "去上课", "example_pinyin": "Qù shàngkè", "example_english": "Go to class"},
            {"simplified": "起床", "traditional": "起床", "pinyin": "qǐchuáng","english": "to get up", "part_of_speech": "verb", "example_chinese": "早起床", "example_pinyin": "Zǎo qǐchuáng", "example_english": "Get up early"},
            {"simplified": "睡觉", "traditional": "睡覺", "pinyin": "shuìjiào","english": "to sleep", "part_of_speech": "verb", "example_chinese": "去睡觉", "example_pinyin": "Qù shuìjiào", "example_english": "Go to sleep"},
            {"simplified": "汉字", "traditional": "漢字", "pinyin": "Hànzì", "english": "Chinese character", "part_of_speech": "noun", "example_chinese": "写汉字", "example_pinyin": "Xiě Hànzì", "example_english": "Write characters"},
            {"simplified": "回",   "traditional": "回",   "pinyin": "huí",   "english": "to return", "part_of_speech": "verb", "example_chinese": "回家", "example_pinyin": "Huí jiā", "example_english": "Go home"},
        ],
    },

    # ---------------------------- L12 ----------------------------
    {
        "lesson_number": 12,
        "title": "我全身不舒服 (I’m Not Feeling Well)",
        "subtitle": "Health & body",
        "description": "Describe ailments and visit the doctor.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Roommate", "chinese": "大为，你每天都六点起床去锻炼，现在九点一刻，你怎么还不起床？", "pinyin": "Dàwéi, nǐ měitiān dōu liù diǎn qǐchuáng qù duànliàn, xiànzài jiǔ diǎn yí kè, nǐ zěnme hái bù qǐchuáng?", "english": "Dawei, you get up at six every day to exercise. It’s 9:15 — why aren’t you up?"},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "我头疼。嗓子也疼。", "pinyin": "Wǒ tóu téng. Sǎngzi yě téng.", "english": "My head hurts. My throat also hurts."},
            {"part": 1, "speaker": "Roommate", "chinese": "我想，你应该去医院看病。", "pinyin": "Wǒ xiǎng, nǐ yīnggāi qù yīyuàn kànbìng.", "english": "I think you should go to the hospital."},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "我身体没问题，不用去看病。", "pinyin": "Wǒ shēntǐ méi wèntí, bú yòng qù kànbìng.", "english": "I’m fine, no need to see a doctor."},
            {"part": 1, "speaker": "Roommate", "chinese": "你不去看病，明天还不能上课。", "pinyin": "Nǐ bú qù kànbìng, míngtiān hái bù néng shàngkè.", "english": "If you don’t see one, tomorrow you still won’t make class."},
            {"part": 2, "speaker": "Nurse", "chinese": "八号——你叫马大为，是不是？", "pinyin": "Bā hào — nǐ jiào Mǎ Dàwéi, shì bu shì?", "english": "Number 8 — you’re Ma Dawei, right?"},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "是，我叫马大为。", "pinyin": "Shì, wǒ jiào Mǎ Dàwéi.", "english": "Yes, I am Ma Dawei."},
            {"part": 2, "speaker": "Doctor", "chinese": "你哪儿不舒服？", "pinyin": "Nǐ nǎr bù shūfu?", "english": "Where do you feel uncomfortable?"},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "我头疼，全身都不舒服。", "pinyin": "Wǒ tóu téng, quánshēn dōu bù shūfu.", "english": "My head hurts and my whole body feels bad."},
            {"part": 2, "speaker": "Doctor", "chinese": "你嗓子有点儿发炎，还有点儿发烧，是感冒。你要多喝水，还要吃点儿药。", "pinyin": "Nǐ sǎngzi yǒudiǎnr fāyán, hái yǒudiǎnr fāshāo, shì gǎnmào. Nǐ yào duō hē shuǐ, hái yào chī diǎnr yào.", "english": "Your throat is a bit inflamed, you have a slight fever — it’s a cold. Drink plenty of water and take some medicine."},
        ],
        "grammar_notes": [
            {"title": "Body + 疼", "explanation": "Body part + 疼 = X hurts: 头疼, 嗓子疼, 肚子疼."},
            {"title": "应该 + V vs 要 + V", "explanation": "应该 = should (advice). 要 = need to / will (intent)."},
            {"title": "有点儿 vs 一点儿", "explanation": "有点儿 + adj. = a bit + adj. (used negatively, before adj.). 一点儿 follows verbs: 吃一点儿药."},
        ],
        "vocabulary": [
            {"simplified": "舒服", "traditional": "舒服", "pinyin": "shūfu", "english": "comfortable", "part_of_speech": "adjective", "example_chinese": "不舒服", "example_pinyin": "Bù shūfu", "example_english": "Not well"},
            {"simplified": "头",   "traditional": "頭",   "pinyin": "tóu",   "english": "head", "part_of_speech": "noun", "example_chinese": "头疼", "example_pinyin": "Tóu téng", "example_english": "Headache"},
            {"simplified": "疼",   "traditional": "疼",   "pinyin": "téng",  "english": "to hurt", "part_of_speech": "adjective", "example_chinese": "嗓子疼", "example_pinyin": "Sǎngzi téng", "example_english": "Sore throat"},
            {"simplified": "嗓子", "traditional": "嗓子", "pinyin": "sǎngzi","english": "throat", "part_of_speech": "noun", "example_chinese": "嗓子疼", "example_pinyin": "Sǎngzi téng", "example_english": "Sore throat"},
            {"simplified": "发烧", "traditional": "發燒", "pinyin": "fāshāo","english": "to have a fever", "part_of_speech": "verb", "example_chinese": "我发烧", "example_pinyin": "Wǒ fāshāo", "example_english": "I have a fever"},
            {"simplified": "感冒", "traditional": "感冒", "pinyin": "gǎnmào","english": "cold (illness)", "part_of_speech": "noun/verb", "example_chinese": "感冒了", "example_pinyin": "Gǎnmào le", "example_english": "Caught a cold"},
            {"simplified": "医院", "traditional": "醫院", "pinyin": "yīyuàn","english": "hospital", "part_of_speech": "noun", "example_chinese": "去医院", "example_pinyin": "Qù yīyuàn", "example_english": "Go to hospital"},
            {"simplified": "看病", "traditional": "看病", "pinyin": "kànbìng","english": "to see a doctor", "part_of_speech": "verb", "example_chinese": "去看病", "example_pinyin": "Qù kànbìng", "example_english": "See a doctor"},
            {"simplified": "药",   "traditional": "藥",   "pinyin": "yào",   "english": "medicine", "part_of_speech": "noun", "example_chinese": "吃药", "example_pinyin": "Chī yào", "example_english": "Take medicine"},
            {"simplified": "水",   "traditional": "水",   "pinyin": "shuǐ",  "english": "water", "part_of_speech": "noun", "example_chinese": "喝水", "example_pinyin": "Hē shuǐ", "example_english": "Drink water"},
            {"simplified": "全身", "traditional": "全身", "pinyin": "quánshēn","english": "whole body", "part_of_speech": "noun", "example_chinese": "全身疼", "example_pinyin": "Quánshēn téng", "example_english": "Whole body aches"},
            {"simplified": "锻炼", "traditional": "鍛煉", "pinyin": "duànliàn","english": "to exercise", "part_of_speech": "verb", "example_chinese": "去锻炼", "example_pinyin": "Qù duànliàn", "example_english": "Go exercise"},
            {"simplified": "身体", "traditional": "身體", "pinyin": "shēntǐ","english": "body; health", "part_of_speech": "noun", "example_chinese": "身体好", "example_pinyin": "Shēntǐ hǎo", "example_english": "Healthy"},
            {"simplified": "穿",   "traditional": "穿",   "pinyin": "chuān", "english": "to wear", "part_of_speech": "verb", "example_chinese": "穿衣服", "example_pinyin": "Chuān yīfu", "example_english": "Wear clothes"},
            {"simplified": "冷",   "traditional": "冷",   "pinyin": "lěng",  "english": "cold", "part_of_speech": "adjective", "example_chinese": "天气冷", "example_pinyin": "Tiānqì lěng", "example_english": "It’s cold"},
        ],
    },

    # ---------------------------- L13 ----------------------------
    {
        "lesson_number": 13,
        "title": "我认识了一个漂亮的姑娘 (I Met a Beautiful Girl)",
        "subtitle": "Completed actions with 了",
        "description": "Talk about completed actions and renting an apartment.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Song Hua", "chinese": "大为，听说你得了感冒，现在你身体怎么样？", "pinyin": "Dàwéi, tīng shuō nǐ déle gǎnmào, xiànzài nǐ shēntǐ zěnmeyàng?", "english": "Dawei, I heard you caught a cold. How are you feeling now?"},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "我去了医院，吃了很多中药。", "pinyin": "Wǒ qùle yīyuàn, chīle hěn duō zhōngyào.", "english": "I went to the hospital and took a lot of Chinese medicine."},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "宋华，我想告诉你一件事儿。", "pinyin": "Sòng Huá, wǒ xiǎng gàosu nǐ yí jiàn shìr.", "english": "Song Hua, I want to tell you something."},
            {"part": 1, "speaker": "Song Hua", "chinese": "什么事儿？", "pinyin": "Shénme shìr?", "english": "What is it?"},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "我认识了一个漂亮的姑娘，她愿意做我女朋友。", "pinyin": "Wǒ rènshile yí ge piàoliang de gūniang, tā yuànyì zuò wǒ nǚ péngyou.", "english": "I met a beautiful girl, and she’s willing to be my girlfriend."},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "可是我的宿舍太小，我想租一间房子。", "pinyin": "Kěshì wǒ de sùshè tài xiǎo, wǒ xiǎng zū yì jiān fángzi.", "english": "But my dorm is too small. I want to rent a room."},
            {"part": 2, "speaker": "Ma Dawei", "chinese": "那间房子房租太贵，你说，我应该怎么办？", "pinyin": "Nà jiān fángzi fángzū tài guì, nǐ shuō, wǒ yīnggāi zěnme bàn?", "english": "That room is too expensive — what should I do?"},
            {"part": 2, "speaker": "Song Hua", "chinese": "我给陆雨平打个电话，让他来帮助我们。", "pinyin": "Wǒ gěi Lù Yǔpíng dǎ ge diànhuà, ràng tā lái bāngzhù wǒmen.", "english": "I’ll give Lu Yuping a call and ask him to help us."},
            {"part": 2, "speaker": "Lu Yuping", "chinese": "这个公司的经理是我朋友，我跟他说一下。", "pinyin": "Zhège gōngsī de jīnglǐ shì wǒ péngyou, wǒ gēn tā shuō yíxià.", "english": "The manager of this company is my friend, I’ll have a word with him."},
        ],
        "grammar_notes": [
            {"title": "Verb + 了", "explanation": "Append 了 to a verb to mark a completed action: 我吃了饭, 我去了医院."},
            {"title": "Adj + 的 + Noun", "explanation": "Use 的 to connect adjective and noun: 漂亮的姑娘 = beautiful girl."},
            {"title": "给 (gěi) + person + 打电话", "explanation": "给 marks the recipient: 我给妈妈打电话 = I phone my mother."},
        ],
        "vocabulary": [
            {"simplified": "了",   "traditional": "了",   "pinyin": "le",    "english": "completion particle", "part_of_speech": "particle", "example_chinese": "吃了饭", "example_pinyin": "Chī le fàn", "example_english": "Ate"},
            {"simplified": "得",   "traditional": "得",   "pinyin": "dé",    "english": "to get; obtain", "part_of_speech": "verb", "example_chinese": "得了感冒", "example_pinyin": "Déle gǎnmào", "example_english": "Caught a cold"},
            {"simplified": "中药", "traditional": "中藥", "pinyin": "zhōngyào","english": "Chinese medicine", "part_of_speech": "noun", "example_chinese": "吃中药", "example_pinyin": "Chī zhōngyào", "example_english": "Take Chinese medicine"},
            {"simplified": "告诉", "traditional": "告訴", "pinyin": "gàosu", "english": "to tell", "part_of_speech": "verb", "example_chinese": "告诉我", "example_pinyin": "Gàosu wǒ", "example_english": "Tell me"},
            {"simplified": "事儿", "traditional": "事兒", "pinyin": "shìr",  "english": "matter; thing", "part_of_speech": "noun", "example_chinese": "什么事儿?", "example_pinyin": "Shénme shìr?", "example_english": "What’s up?"},
            {"simplified": "漂亮", "traditional": "漂亮", "pinyin": "piàoliang","english": "pretty; beautiful", "part_of_speech": "adjective", "example_chinese": "很漂亮", "example_pinyin": "Hěn piàoliang", "example_english": "Very pretty"},
            {"simplified": "姑娘", "traditional": "姑娘", "pinyin": "gūniang","english": "girl", "part_of_speech": "noun", "example_chinese": "好姑娘", "example_pinyin": "Hǎo gūniang", "example_english": "Good girl"},
            {"simplified": "女朋友","traditional": "女朋友","pinyin": "nǚ péngyou","english": "girlfriend", "part_of_speech": "noun", "example_chinese": "我女朋友", "example_pinyin": "Wǒ nǚ péngyou", "example_english": "My girlfriend"},
            {"simplified": "愿意", "traditional": "願意", "pinyin": "yuànyì","english": "be willing to", "part_of_speech": "modal", "example_chinese": "我愿意去", "example_pinyin": "Wǒ yuànyì qù", "example_english": "I’m willing to go"},
            {"simplified": "租",   "traditional": "租",   "pinyin": "zū",    "english": "to rent", "part_of_speech": "verb", "example_chinese": "租房子", "example_pinyin": "Zū fángzi", "example_english": "Rent a house"},
            {"simplified": "房子", "traditional": "房子", "pinyin": "fángzi","english": "house; flat", "part_of_speech": "noun", "example_chinese": "找房子", "example_pinyin": "Zhǎo fángzi", "example_english": "Find a house"},
            {"simplified": "房租", "traditional": "房租", "pinyin": "fángzū","english": "rent", "part_of_speech": "noun", "example_chinese": "房租贵", "example_pinyin": "Fángzū guì", "example_english": "Rent is expensive"},
            {"simplified": "公司", "traditional": "公司", "pinyin": "gōngsī","english": "company", "part_of_speech": "noun", "example_chinese": "去公司", "example_pinyin": "Qù gōngsī", "example_english": "Go to the company"},
            {"simplified": "经理", "traditional": "經理", "pinyin": "jīnglǐ","english": "manager", "part_of_speech": "noun", "example_chinese": "找经理", "example_pinyin": "Zhǎo jīnglǐ", "example_english": "Look for the manager"},
            {"simplified": "电话", "traditional": "電話", "pinyin": "diànhuà","english": "phone", "part_of_speech": "noun", "example_chinese": "打电话", "example_pinyin": "Dǎ diànhuà", "example_english": "Make a call"},
            {"simplified": "帮助", "traditional": "幫助", "pinyin": "bāngzhù","english": "to help", "part_of_speech": "verb", "example_chinese": "帮助我", "example_pinyin": "Bāngzhù wǒ", "example_english": "Help me"},
            {"simplified": "怎么办","traditional": "怎麼辦","pinyin": "zěnme bàn","english": "what to do?", "part_of_speech": "phrase", "example_chinese": "怎么办?", "example_pinyin": "Zěnme bàn?", "example_english": "What to do?"},
        ],
    },

    # ---------------------------- L14 ----------------------------
    {
        "lesson_number": 14,
        "title": "祝你圣诞快乐 (Merry Christmas)",
        "subtitle": "Phone calls & holidays",
        "description": "Make phone calls, talk about holidays, and give wishes.",
        "level": "Beginner",
        "video_url": "",
        "dialogue": [
            {"part": 1, "speaker": "Ma Dawei", "chinese": "力波，上午十点半，你妈妈给你打了一个电话。", "pinyin": "Lìbō, shàngwǔ shí diǎn bàn, nǐ māma gěi nǐ dǎle yí ge diànhuà.", "english": "Libo, your mom called at 10:30 this morning."},
            {"part": 1, "speaker": "Libo", "chinese": "谢谢。我刚才去邮局给我妈妈寄了点儿东西。", "pinyin": "Xièxie. Wǒ gāngcái qù yóujú gěi wǒ māma jìle diǎnr dōngxi.", "english": "Thanks. I just went to the post office to send my mom some things."},
            {"part": 1, "speaker": "Ma Dawei", "chinese": "我今天打扫了宿舍，你的脏衣服太多了。", "pinyin": "Wǒ jīntiān dǎsǎole sùshè, nǐ de zāng yīfu tài duō le.", "english": "I cleaned the dorm today; you have way too many dirty clothes."},
            {"part": 1, "speaker": "Libo", "chinese": "不好意思。这两天我太忙了。", "pinyin": "Bù hǎoyìsi. Zhè liǎng tiān wǒ tài máng le.", "english": "Sorry. I’ve been very busy these last few days."},
            {"part": 2, "speaker": "Libo", "chinese": "妈妈，你好！", "pinyin": "Māma, nǐ hǎo!", "english": "Hello mom!"},
            {"part": 2, "speaker": "Mother", "chinese": "力波，你好吗？", "pinyin": "Lìbō, nǐ hǎo ma?", "english": "Libo, how are you?"},
            {"part": 2, "speaker": "Libo", "chinese": "我很好。你和爸爸身体怎么样？", "pinyin": "Wǒ hěn hǎo. Nǐ hé bàba shēntǐ zěnmeyàng?", "english": "I’m fine. How are you and dad?"},
            {"part": 2, "speaker": "Mother", "chinese": "我们工作都很忙。今年你要在中国过圣诞节，不能回家。我和你爸爸要送你一件圣诞礼物。", "pinyin": "Wǒmen gōngzuò dōu hěn máng. Jīnnián nǐ yào zài Zhōngguó guò Shèngdànjié, bù néng huí jiā. Wǒ hé nǐ bàba yào sòng nǐ yí jiàn Shèngdàn lǐwù.", "english": "We are very busy. This year you spend Christmas in China and can’t come home. Dad and I will send you a Christmas gift."},
            {"part": 2, "speaker": "Libo", "chinese": "谢谢你们。我也祝你和爸爸圣诞快乐！", "pinyin": "Xièxie nǐmen. Wǒ yě zhù nǐ hé bàba Shèngdàn kuàilè!", "english": "Thank you both. Merry Christmas to you and dad too!"},
        ],
        "grammar_notes": [
            {"title": "给 + person + 打电话", "explanation": "Place 给 + person before the verb 打电话: 我给妈妈打电话."},
            {"title": "Verb + 了 + Object", "explanation": "Place 了 right after the verb to mark completion: 打了一个电话, 去了邮局."},
            {"title": "祝 + person + wish", "explanation": "祝你圣诞快乐 = Merry Christmas to you. Pattern: 祝 + person + holiday-adjective."},
        ],
        "vocabulary": [
            {"simplified": "打电话","traditional": "打電話","pinyin": "dǎ diànhuà","english": "to phone", "part_of_speech": "verb", "example_chinese": "给我打电话", "example_pinyin": "Gěi wǒ dǎ diànhuà", "example_english": "Call me"},
            {"simplified": "给",   "traditional": "給",   "pinyin": "gěi",   "english": "to give; for", "part_of_speech": "verb", "example_chinese": "给我书", "example_pinyin": "Gěi wǒ shū", "example_english": "Give me a book"},
            {"simplified": "邮局", "traditional": "郵局", "pinyin": "yóujú", "english": "post office", "part_of_speech": "noun", "example_chinese": "去邮局", "example_pinyin": "Qù yóujú", "example_english": "Go to post office"},
            {"simplified": "寄",   "traditional": "寄",   "pinyin": "jì",    "english": "to send (mail)", "part_of_speech": "verb", "example_chinese": "寄信", "example_pinyin": "Jì xìn", "example_english": "Send a letter"},
            {"simplified": "东西", "traditional": "東西", "pinyin": "dōngxi","english": "thing(s)", "part_of_speech": "noun", "example_chinese": "买东西", "example_pinyin": "Mǎi dōngxi", "example_english": "Buy things"},
            {"simplified": "打扫", "traditional": "打掃", "pinyin": "dǎsǎo", "english": "to clean (sweep)", "part_of_speech": "verb", "example_chinese": "打扫房间", "example_pinyin": "Dǎsǎo fángjiān", "example_english": "Clean the room"},
            {"simplified": "脏",   "traditional": "髒",   "pinyin": "zāng",  "english": "dirty", "part_of_speech": "adjective", "example_chinese": "脏衣服", "example_pinyin": "Zāng yīfu", "example_english": "Dirty clothes"},
            {"simplified": "衣服", "traditional": "衣服", "pinyin": "yīfu",  "english": "clothes", "part_of_speech": "noun", "example_chinese": "买衣服", "example_pinyin": "Mǎi yīfu", "example_english": "Buy clothes"},
            {"simplified": "圣诞", "traditional": "聖誕", "pinyin": "Shèngdàn","english": "Christmas", "part_of_speech": "noun", "example_chinese": "圣诞节", "example_pinyin": "Shèngdàn jié", "example_english": "Christmas"},
            {"simplified": "节",   "traditional": "節",   "pinyin": "jié",   "english": "holiday; festival", "part_of_speech": "noun", "example_chinese": "春节", "example_pinyin": "Chūnjié", "example_english": "Spring Festival"},
            {"simplified": "礼物", "traditional": "禮物", "pinyin": "lǐwù",  "english": "gift", "part_of_speech": "noun", "example_chinese": "圣诞礼物", "example_pinyin": "Shèngdàn lǐwù", "example_english": "Christmas gift"},
            {"simplified": "过",   "traditional": "過",   "pinyin": "guò",   "english": "to celebrate; pass", "part_of_speech": "verb", "example_chinese": "过节", "example_pinyin": "Guò jié", "example_english": "Celebrate a holiday"},
            {"simplified": "送",   "traditional": "送",   "pinyin": "sòng",  "english": "to give (a gift)", "part_of_speech": "verb", "example_chinese": "送礼物", "example_pinyin": "Sòng lǐwù", "example_english": "Give a gift"},
            {"simplified": "旅行", "traditional": "旅行", "pinyin": "lǚxíng","english": "to travel", "part_of_speech": "verb", "example_chinese": "去旅行", "example_pinyin": "Qù lǚxíng", "example_english": "Go traveling"},
            {"simplified": "件",   "traditional": "件",   "pinyin": "jiàn",  "english": "MW (clothing, items)", "part_of_speech": "measure", "example_chinese": "一件衣服", "example_pinyin": "Yí jiàn yīfu", "example_english": "One piece of clothing"},
            {"simplified": "刚才", "traditional": "剛才", "pinyin": "gāngcái","english": "just now", "part_of_speech": "adverb", "example_chinese": "刚才来", "example_pinyin": "Gāngcái lái", "example_english": "Just came"},
        ],
    },
]


# =====================================================================
# SUBSTITUTION DRILLS — Lessons 1 to 14
# Each lesson has 3-5 drill templates per part. Each template has 4-5
# substitution variants. Every variant is repeated 6 times by the API.
# =====================================================================

SENTENCE_DRILLS = []

def _add(items):
    SENTENCE_DRILLS.extend(items)


# ---------------------------- L1 ----------------------------
# Part 1 — Greetings 你好 / Hello pattern
_add(_expand_drill(1, 1, "L1.P1.D1", "Greet this person in Mandarin.", "用中文打招呼。",
    "[Person], 你好！", "Hello, [Person]!",
    [
        {"chinese": "力波，你好！",   "pinyin": "Lìbō, nǐ hǎo!",     "english": "Hello, Libo!"},
        {"chinese": "陆雨平，你好！", "pinyin": "Lù Yǔpíng, nǐ hǎo!","english": "Hello, Lu Yuping!"},
        {"chinese": "老师，你好！",   "pinyin": "Lǎoshī, nǐ hǎo!",   "english": "Hello, teacher!"},
        {"chinese": "林娜，你好！",   "pinyin": "Lín Nà, nǐ hǎo!",   "english": "Hello, Lin Na!"},
        {"chinese": "大为，你好！",   "pinyin": "Dàwéi, nǐ hǎo!",    "english": "Hello, Dawei!"},
    ]))
_add(_expand_drill(1, 1, "L1.P1.D2", "Say how the person is using 很 + adjective.", "用'很 + 形容词'造句。",
    "[Subject] 很 [adjective].", "[Subject] is very [adjective].",
    [
        {"chinese": "我很好。",   "pinyin": "Wǒ hěn hǎo.",   "english": "I’m well."},
        {"chinese": "他很好。",   "pinyin": "Tā hěn hǎo.",   "english": "He’s well."},
        {"chinese": "她很忙。",   "pinyin": "Tā hěn máng.",  "english": "She’s busy."},
        {"chinese": "我们很好。", "pinyin": "Wǒmen hěn hǎo.","english": "We’re well."},
    ]))
_add(_expand_drill(1, 1, "L1.P1.D3", "Turn the statement into a 吗 question.", "用'吗'变成疑问句。",
    "[Subject] 好/忙 吗？", "Is [Subject] well/busy?",
    [
        {"chinese": "你好吗？",   "pinyin": "Nǐ hǎo ma?",     "english": "How are you?"},
        {"chinese": "你忙吗？",   "pinyin": "Nǐ máng ma?",    "english": "Are you busy?"},
        {"chinese": "他好吗？",   "pinyin": "Tā hǎo ma?",     "english": "How is he?"},
        {"chinese": "老师好吗？", "pinyin": "Lǎoshī hǎo ma?", "english": "How is the teacher?"},
    ]))

# Part 2 — 我也很好 / Reciprocal greetings
_add(_expand_drill(1, 2, "L1.P2.D1", "Say 'I am also ...' with 也.", "用'也'造句。",
    "我也 [predicate].", "I am also [predicate].",
    [
        {"chinese": "我也很好。",  "pinyin": "Wǒ yě hěn hǎo.",  "english": "I’m also well."},
        {"chinese": "我也很忙。",  "pinyin": "Wǒ yě hěn máng.", "english": "I’m also busy."},
        {"chinese": "他也很好。",  "pinyin": "Tā yě hěn hǎo.",  "english": "He’s also well."},
        {"chinese": "她也很忙。",  "pinyin": "Tā yě hěn máng.", "english": "She’s also busy."},
    ]))
_add(_expand_drill(1, 2, "L1.P2.D2", "Reply 'And you?' with 呢.", "用'呢'反问。",
    "[Pronoun] 呢？", "And [Pronoun]?",
    [
        {"chinese": "你呢？",   "pinyin": "Nǐ ne?",    "english": "And you?"},
        {"chinese": "他呢？",   "pinyin": "Tā ne?",    "english": "And he?"},
        {"chinese": "她呢？",   "pinyin": "Tā ne?",    "english": "And she?"},
        {"chinese": "老师呢？", "pinyin": "Lǎoshī ne?","english": "And the teacher?"},
    ]))


# ---------------------------- L2 ----------------------------
# Part 1
_add(_expand_drill(2, 1, "L2.P1.D1", "Use 不 to negate the predicate.", "用'不'否定。",
    "[Subject] 不 [predicate].", "[Subject] is not [predicate].",
    [
        {"chinese": "我不忙。",   "pinyin": "Wǒ bù máng.",   "english": "I’m not busy."},
        {"chinese": "他不忙。",   "pinyin": "Tā bù máng.",   "english": "He’s not busy."},
        {"chinese": "她不忙。",   "pinyin": "Tā bù máng.",   "english": "She’s not busy."},
        {"chinese": "我不好。",   "pinyin": "Wǒ bù hǎo.",    "english": "I’m not well."},
        {"chinese": "他们不忙。", "pinyin": "Tāmen bù máng.","english": "They’re not busy."},
    ]))
_add(_expand_drill(2, 1, "L2.P1.D2", "Use 都 to mean 'all/both'.", "用'都'表示'全部'。",
    "[Subject] 都 [predicate].", "[Subject] all are [predicate].",
    [
        {"chinese": "他们都很好。", "pinyin": "Tāmen dōu hěn hǎo.", "english": "They are all well."},
        {"chinese": "我们都很忙。", "pinyin": "Wǒmen dōu hěn máng.","english": "We are all busy."},
        {"chinese": "他们都很忙。", "pinyin": "Tāmen dōu hěn máng.","english": "They are all busy."},
        {"chinese": "你们都好。",   "pinyin": "Nǐmen dōu hǎo.",     "english": "You all are well."},
    ]))
_add(_expand_drill(2, 1, "L2.P1.D3", "Ask about family members.", "询问家人的情况。",
    "你 [family] 好吗？", "How is your [family]?",
    [
        {"chinese": "你爸爸好吗？",   "pinyin": "Nǐ bàba hǎo ma?",    "english": "How is your dad?"},
        {"chinese": "你妈妈好吗？",   "pinyin": "Nǐ māma hǎo ma?",    "english": "How is your mom?"},
        {"chinese": "你哥哥好吗？",   "pinyin": "Nǐ gēge hǎo ma?",    "english": "How is your older brother?"},
        {"chinese": "你男朋友好吗？", "pinyin": "Nǐ nán péngyou hǎo ma?","english": "How is your boyfriend?"},
    ]))

# Part 2 — Coffee dialogue
_add(_expand_drill(2, 2, "L2.P2.D1", "Say what someone wants to drink.", "说明谁要什么饮料。",
    "[Subject] 要 [drink].", "[Subject] wants [drink].",
    [
        {"chinese": "我要咖啡。",   "pinyin": "Wǒ yào kāfēi.",   "english": "I want coffee."},
        {"chinese": "他要咖啡。",   "pinyin": "Tā yào kāfēi.",   "english": "He wants coffee."},
        {"chinese": "她要咖啡。",   "pinyin": "Tā yào kāfēi.",   "english": "She wants coffee."},
        {"chinese": "哥哥要咖啡。", "pinyin": "Gēge yào kāfēi.", "english": "Older brother wants coffee."},
        {"chinese": "我们要咖啡。", "pinyin": "Wǒmen yào kāfēi.","english": "We want coffee."},
    ]))
_add(_expand_drill(2, 2, "L2.P2.D2", "Use 都 + 喝 to say 'all drink'.", "用'都喝'造句。",
    "[Subject] 都喝 [drink].", "[Subject] all drink [drink].",
    [
        {"chinese": "我们都喝咖啡。", "pinyin": "Wǒmen dōu hē kāfēi.","english": "We all drink coffee."},
        {"chinese": "他们都喝咖啡。", "pinyin": "Tāmen dōu hē kāfēi.","english": "They all drink coffee."},
        {"chinese": "我们都喝茶。",   "pinyin": "Wǒmen dōu hē chá.",  "english": "We all drink tea."},
        {"chinese": "你们都喝咖啡？", "pinyin": "Nǐmen dōu hē kāfēi?", "english": "Do you all drink coffee?"},
    ]))


# ---------------------------- L3 ----------------------------
# Part 1
_add(_expand_drill(3, 1, "L3.P1.D1", "Introduce 'That is ...'", "用'那是...'介绍。",
    "那是 [noun].", "That is [noun].",
    [
        {"chinese": "那是我们老师。",  "pinyin": "Nà shì wǒmen lǎoshī.", "english": "That is our teacher."},
        {"chinese": "那是我朋友。",    "pinyin": "Nà shì wǒ péngyou.",   "english": "That is my friend."},
        {"chinese": "那是我哥哥。",    "pinyin": "Nà shì wǒ gēge.",      "english": "That is my older brother."},
        {"chinese": "那是中国人。",    "pinyin": "Nà shì Zhōngguó rén.", "english": "That is a Chinese person."},
        {"chinese": "那是我爸爸。",    "pinyin": "Nà shì wǒ bàba.",      "english": "That is my dad."},
    ]))
_add(_expand_drill(3, 1, "L3.P1.D2", "Say the nationality of a person.", "说出某人的国籍。",
    "她/他 是 [nationality].", "She/he is [nationality].",
    [
        {"chinese": "她是中国人。",     "pinyin": "Tā shì Zhōngguó rén.",  "english": "She is Chinese."},
        {"chinese": "他是美国人。",     "pinyin": "Tā shì Měiguó rén.",    "english": "He is American."},
        {"chinese": "她是英国人。",     "pinyin": "Tā shì Yīngguó rén.",   "english": "She is British."},
        {"chinese": "他是加拿大人。",   "pinyin": "Tā shì Jiānádà rén.",   "english": "He is Canadian."},
    ]))
_add(_expand_drill(3, 1, "L3.P1.D3", "Ask 'Who is ...?'", "用'谁'提问。",
    "[Pronoun] 是谁？", "Who is [Pronoun]?",
    [
        {"chinese": "那是谁？", "pinyin": "Nà shì shéi?", "english": "Who is that?"},
        {"chinese": "这是谁？", "pinyin": "Zhè shì shéi?","english": "Who is this?"},
        {"chinese": "他是谁？", "pinyin": "Tā shì shéi?", "english": "Who is he?"},
        {"chinese": "她是谁？", "pinyin": "Tā shì shéi?", "english": "Who is she?"},
    ]))

# Part 2 — introductions, professions
_add(_expand_drill(3, 2, "L3.P2.D1", "Introduce 'This is my ...'", "用'这是我的...'介绍。",
    "这是我 [relation].", "This is my [relation].",
    [
        {"chinese": "这是我哥哥。", "pinyin": "Zhè shì wǒ gēge.",  "english": "This is my older brother."},
        {"chinese": "这是我朋友。", "pinyin": "Zhè shì wǒ péngyou.","english": "This is my friend."},
        {"chinese": "这是我奶奶。", "pinyin": "Zhè shì wǒ nǎinai.","english": "This is my grandma."},
        {"chinese": "这是我妈妈。", "pinyin": "Zhè shì wǒ māma.",  "english": "This is my mom."},
        {"chinese": "这是我爸爸。", "pinyin": "Zhè shì wǒ bàba.",  "english": "This is my dad."},
    ]))
_add(_expand_drill(3, 2, "L3.P2.D2", "Say what someone’s profession is.", "说出某人的职业。",
    "他/她 是 [profession].", "He/she is a [profession].",
    [
        {"chinese": "他是老师。",     "pinyin": "Tā shì lǎoshī.",     "english": "He is a teacher."},
        {"chinese": "她是医生。",     "pinyin": "Tā shì yīshēng.",    "english": "She is a doctor."},
        {"chinese": "他是外语老师。", "pinyin": "Tā shì wàiyǔ lǎoshī.","english": "He is a foreign-language teacher."},
        {"chinese": "他是学生。",     "pinyin": "Tā shì xuésheng.",   "english": "He is a student."},
    ]))
_add(_expand_drill(3, 2, "L3.P2.D3", "Negate with 不是.", "用'不是'否定。",
    "[Subject] 不是 [noun].", "[Subject] is not [noun].",
    [
        {"chinese": "我不是老师。",   "pinyin": "Wǒ bú shì lǎoshī.",   "english": "I am not a teacher."},
        {"chinese": "他不是医生。",   "pinyin": "Tā bú shì yīshēng.",  "english": "He is not a doctor."},
        {"chinese": "她不是中国人。", "pinyin": "Tā bú shì Zhōngguó rén.","english": "She is not Chinese."},
        {"chinese": "我不是学生。",   "pinyin": "Wǒ bú shì xuésheng.", "english": "I am not a student."},
    ]))


# ---------------------------- L4 ----------------------------
# Part 1 — Names & polite intro
_add(_expand_drill(4, 1, "L4.P1.D1", "State your surname.", "说出姓氏。",
    "我姓 [surname].", "My surname is [surname].",
    [
        {"chinese": "我姓陆。", "pinyin": "Wǒ xìng Lù.",    "english": "My surname is Lu."},
        {"chinese": "我姓林。", "pinyin": "Wǒ xìng Lín.",   "english": "My surname is Lin."},
        {"chinese": "我姓马。", "pinyin": "Wǒ xìng Mǎ.",    "english": "My surname is Ma."},
        {"chinese": "我姓张。", "pinyin": "Wǒ xìng Zhāng.", "english": "My surname is Zhang."},
        {"chinese": "我姓丁。", "pinyin": "Wǒ xìng Dīng.",  "english": "My surname is Ding."},
    ]))
_add(_expand_drill(4, 1, "L4.P1.D2", "State your full name with 我叫 ...", "用'我叫...'介绍全名。",
    "我叫 [full name].", "My name is [full name].",
    [
        {"chinese": "我叫陆雨平。", "pinyin": "Wǒ jiào Lù Yǔpíng.","english": "I’m called Lu Yuping."},
        {"chinese": "我叫林娜。",   "pinyin": "Wǒ jiào Lín Nà.",   "english": "I’m called Lin Na."},
        {"chinese": "我叫马大为。", "pinyin": "Wǒ jiào Mǎ Dàwéi.", "english": "I’m called Ma Dawei."},
        {"chinese": "我叫丁力波。", "pinyin": "Wǒ jiào Dīng Lìbō.","english": "I’m called Ding Libo."},
    ]))
_add(_expand_drill(4, 1, "L4.P1.D3", "Express 'pleased to meet you'.", "表达'很高兴认识你'。",
    "认识 [person] 很高兴.", "Pleased to meet [person].",
    [
        {"chinese": "认识你很高兴。",     "pinyin": "Rènshi nǐ hěn gāoxìng.",     "english": "Pleased to meet you."},
        {"chinese": "认识您很高兴。",     "pinyin": "Rènshi nín hěn gāoxìng.",    "english": "Pleased to meet you (formal)."},
        {"chinese": "认识陆先生很高兴。", "pinyin": "Rènshi Lù xiānsheng hěn gāoxìng.","english": "Pleased to meet Mr. Lu."},
        {"chinese": "认识老师很高兴。",   "pinyin": "Rènshi lǎoshī hěn gāoxìng.", "english": "Pleased to meet the teacher."},
    ]))

# Part 2 — Identity / nationality / study
_add(_expand_drill(4, 2, "L4.P2.D1", "Describe what someone studies with 学习.", "用'学习'造句。",
    "[Subject] 学习 [subject].", "[Subject] studies [subject].",
    [
        {"chinese": "我学习汉语。",     "pinyin": "Wǒ xuéxí Hànyǔ.",       "english": "I study Chinese."},
        {"chinese": "他学习英语。",     "pinyin": "Tā xuéxí Yīngyǔ.",      "english": "He studies English."},
        {"chinese": "她学习文学专业。", "pinyin": "Tā xuéxí wénxué zhuānyè.","english": "She studies literature."},
        {"chinese": "我们学习汉语。",   "pinyin": "Wǒmen xuéxí Hànyǔ.",    "english": "We study Chinese."},
    ]))
_add(_expand_drill(4, 2, "L4.P2.D2", "Say a person’s nationality.", "说出国籍。",
    "[Subject] 是 [country]人.", "[Subject] is from [country].",
    [
        {"chinese": "我是英国人。",   "pinyin": "Wǒ shì Yīngguó rén.",   "english": "I am British."},
        {"chinese": "他是美国人。",   "pinyin": "Tā shì Měiguó rén.",    "english": "He is American."},
        {"chinese": "她是加拿大人。", "pinyin": "Tā shì Jiānádà rén.",   "english": "She is Canadian."},
        {"chinese": "我们是中国人。", "pinyin": "Wǒmen shì Zhōngguó rén.","english": "We are Chinese."},
    ]))


# ---------------------------- L5 ----------------------------
# Part 1
_add(_expand_drill(5, 1, "L5.P1.D1", "Ask where someone is.", "询问位置。",
    "[Subject] 在哪儿？", "Where is [Subject]?",
    [
        {"chinese": "他在哪儿？",     "pinyin": "Tā zài nǎr?",      "english": "Where is he?"},
        {"chinese": "她在哪儿？",     "pinyin": "Tā zài nǎr?",      "english": "Where is she?"},
        {"chinese": "王小云在哪儿？", "pinyin": "Wáng Xiǎoyún zài nǎr?","english": "Where is Wang Xiaoyun?"},
        {"chinese": "餐厅在哪儿？",   "pinyin": "Cāntīng zài nǎr?", "english": "Where is the cafeteria?"},
        {"chinese": "宿舍在哪儿？",   "pinyin": "Sùshè zài nǎr?",   "english": "Where is the dormitory?"},
    ]))
_add(_expand_drill(5, 1, "L5.P1.D2", "State that someone is/is not at a place.", "说明某人在/不在某地。",
    "[Subject] (不)在 [place].", "[Subject] is (not) at [place].",
    [
        {"chinese": "她不在。",     "pinyin": "Tā bú zài.",      "english": "She is not here."},
        {"chinese": "他在宿舍。",   "pinyin": "Tā zài sùshè.",   "english": "He is in the dorm."},
        {"chinese": "我在餐厅。",   "pinyin": "Wǒ zài cāntīng.", "english": "I am at the cafeteria."},
        {"chinese": "老师在那儿。", "pinyin": "Lǎoshī zài nàr.", "english": "The teacher is over there."},
    ]))
_add(_expand_drill(5, 1, "L5.P1.D3", "Use 请 + verb politely.", "用'请+动词'表达礼貌。",
    "请 [verb].", "Please [verb].",
    [
        {"chinese": "请进。",   "pinyin": "Qǐng jìn.",   "english": "Please come in."},
        {"chinese": "请坐。",   "pinyin": "Qǐng zuò.",   "english": "Please sit."},
        {"chinese": "请问。",   "pinyin": "Qǐng wèn.",   "english": "Excuse me / may I ask."},
        {"chinese": "请喝茶。", "pinyin": "Qǐng hē chá.","english": "Please drink tea."},
    ]))

# Part 2 — directions
_add(_expand_drill(5, 2, "L5.P2.D1", "Give a location with 在 + place.", "用'在+地点'表达位置。",
    "[Place] 在 [location].", "[Place] is at [location].",
    [
        {"chinese": "餐厅在二层。",   "pinyin": "Cāntīng zài èr céng.",   "english": "The cafeteria is on the 2nd floor."},
        {"chinese": "餐厅在那儿。",   "pinyin": "Cāntīng zài nàr.",       "english": "The cafeteria is over there."},
        {"chinese": "宿舍在这儿。",   "pinyin": "Sùshè zài zhèr.",        "english": "The dorm is here."},
        {"chinese": "餐厅在二零四号。","pinyin": "Cāntīng zài èr líng sì hào.","english": "Cafeteria is at #204."},
    ]))
_add(_expand_drill(5, 2, "L5.P2.D2", "Thank / reply politely.", "礼貌的感谢和回应。",
    "[Phrase]", "[Phrase]",
    [
        {"chinese": "谢谢。",   "pinyin": "Xièxie.",   "english": "Thanks."},
        {"chinese": "不用谢。", "pinyin": "Bú yòng xiè.","english": "You’re welcome."},
        {"chinese": "对不起。", "pinyin": "Duìbuqǐ.",  "english": "Sorry."},
        {"chinese": "没关系。", "pinyin": "Méi guānxi.","english": "It’s OK."},
    ]))


# ---------------------------- L6 ----------------------------
# Part 1
_add(_expand_drill(6, 1, "L6.P1.D1", "Suggest an activity with 好吗?", "用'好吗?'提出建议。",
    "我们去 [activity]，好吗？", "Shall we go [activity]?",
    [
        {"chinese": "我们去游泳，好吗？", "pinyin": "Wǒmen qù yóuyǒng, hǎo ma?", "english": "Shall we go swimming?"},
        {"chinese": "我们去吃饭，好吗？", "pinyin": "Wǒmen qù chī fàn, hǎo ma?", "english": "Shall we go eat?"},
        {"chinese": "我们去打球，好吗？", "pinyin": "Wǒmen qù dǎqiú, hǎo ma?",   "english": "Shall we go play ball?"},
        {"chinese": "我们去看京剧，好吗？","pinyin": "Wǒmen qù kàn jīngjù, hǎo ma?","english": "Shall we go watch Beijing Opera?"},
        {"chinese": "我们去买东西，好吗？","pinyin": "Wǒmen qù mǎi dōngxi, hǎo ma?","english": "Shall we go shopping?"},
    ]))
_add(_expand_drill(6, 1, "L6.P1.D2", "Comment on something with 很 + adjective.", "用'很+形容词'评论。",
    "[Subject] 很 [adjective].", "[Subject] is very [adjective].",
    [
        {"chinese": "京剧很有意思。", "pinyin": "Jīngjù hěn yǒuyìsi.", "english": "Beijing Opera is interesting."},
        {"chinese": "天气很好。",     "pinyin": "Tiānqì hěn hǎo.",     "english": "Weather is good."},
        {"chinese": "他很高兴。",     "pinyin": "Tā hěn gāoxìng.",     "english": "He is happy."},
        {"chinese": "她很漂亮。",     "pinyin": "Tā hěn piàoliang.",   "english": "She is pretty."},
    ]))
_add(_expand_drill(6, 1, "L6.P1.D3", "Ask 'When do we go?'", "用'什么时候'提问。",
    "什么时候去 [activity]？", "When are we going [activity]?",
    [
        {"chinese": "什么时候去游泳？", "pinyin": "Shénme shíhou qù yóuyǒng?","english": "When are we going swimming?"},
        {"chinese": "什么时候去吃饭？", "pinyin": "Shénme shíhou qù chī fàn?", "english": "When are we going to eat?"},
        {"chinese": "什么时候去打球？", "pinyin": "Shénme shíhou qù dǎqiú?",   "english": "When are we going to play ball?"},
        {"chinese": "什么时候去学校？", "pinyin": "Shénme shíhou qù xuéxiào?", "english": "When are we going to school?"},
    ]))

# Part 2
_add(_expand_drill(6, 2, "L6.P2.D1", "Ask if someone has time tomorrow.", "询问明天是否有时间。",
    "明天 [Subject] 有时间吗？", "Does [Subject] have time tomorrow?",
    [
        {"chinese": "明天您有时间吗？", "pinyin": "Míngtiān nín yǒu shíjiān ma?","english": "Do you have time tomorrow? (formal)"},
        {"chinese": "明天你有时间吗？", "pinyin": "Míngtiān nǐ yǒu shíjiān ma?", "english": "Do you have time tomorrow?"},
        {"chinese": "明天他有时间吗？", "pinyin": "Míngtiān tā yǒu shíjiān ma?", "english": "Does he have time tomorrow?"},
        {"chinese": "明天她有时间吗？", "pinyin": "Míngtiān tā yǒu shíjiān ma?", "english": "Does she have time tomorrow?"},
    ]))
_add(_expand_drill(6, 2, "L6.P2.D2", "Politely refuse using 恐怕 / 抱歉.", "用'恐怕/抱歉'委婉拒绝。",
    "很抱歉，[reason]，恐怕不行。", "Sorry, [reason], I’m afraid I can’t.",
    [
        {"chinese": "很抱歉，明天我很忙，恐怕不行。", "pinyin": "Hěn bàoqiàn, míngtiān wǒ hěn máng, kǒngpà bù xíng.","english": "Sorry, I’m busy tomorrow, I’m afraid I can’t."},
        {"chinese": "很抱歉，今天我有课，恐怕不行。", "pinyin": "Hěn bàoqiàn, jīntiān wǒ yǒu kè, kǒngpà bù xíng.",  "english": "Sorry, I have class today, I can’t."},
        {"chinese": "很抱歉，我没时间，恐怕不行。",   "pinyin": "Hěn bàoqiàn, wǒ méi shíjiān, kǒngpà bù xíng.",     "english": "Sorry, I don’t have time, I can’t."},
        {"chinese": "对不起，请再说一遍。",           "pinyin": "Duìbuqǐ, qǐng zài shuō yí biàn.",                  "english": "Sorry, please say that again."},
    ]))


# ---------------------------- L7 ----------------------------
# Part 1
_add(_expand_drill(7, 1, "L7.P1.D1", "Confirm someone’s role with 是不是.", "用'是不是'确认。",
    "[Subject] 是不是 [noun]？", "Is [Subject] a [noun]?",
    [
        {"chinese": "他是不是老师？",         "pinyin": "Tā shì bu shì lǎoshī?",        "english": "Is he a teacher?"},
        {"chinese": "他是不是我们学院的老师？","pinyin": "Tā shì bu shì wǒmen xuéyuàn de lǎoshī?","english": "Is he a teacher of our institute?"},
        {"chinese": "她是不是学生？",         "pinyin": "Tā shì bu shì xuésheng?",      "english": "Is she a student?"},
        {"chinese": "他是不是教授？",         "pinyin": "Tā shì bu shì jiàoshòu?",      "english": "Is he a professor?"},
    ]))
_add(_expand_drill(7, 1, "L7.P1.D2", "Identify yourself as a member of an organization.", "说明自己来自某机构。",
    "我是 [org] 的 [role].", "I am a [role] of [org].",
    [
        {"chinese": "我是语言学院的老师。",   "pinyin": "Wǒ shì yǔyán xuéyuàn de lǎoshī.",  "english": "I am a teacher of the Language Institute."},
        {"chinese": "我是语言学院的学生。",   "pinyin": "Wǒ shì yǔyán xuéyuàn de xuésheng.","english": "I am a student of the Language Institute."},
        {"chinese": "他是语言学院的教授。",   "pinyin": "Tā shì yǔyán xuéyuàn de jiàoshòu.","english": "He is a professor of the Language Institute."},
        {"chinese": "我们是语言学院的学生。", "pinyin": "Wǒmen shì yǔyán xuéyuàn de xuésheng.","english": "We are students of the Language Institute."},
    ]))
_add(_expand_drill(7, 1, "L7.P1.D3", "Offer your business card with 这是我的 ...", "递名片或介绍。",
    "这是我的 [item].", "This is my [item].",
    [
        {"chinese": "这是我的名片。", "pinyin": "Zhè shì wǒ de míngpiàn.","english": "This is my business card."},
        {"chinese": "这是我的书。",   "pinyin": "Zhè shì wǒ de shū.",     "english": "This is my book."},
        {"chinese": "这是我的朋友。", "pinyin": "Zhè shì wǒ de péngyou.", "english": "This is my friend."},
        {"chinese": "这是我的老师。", "pinyin": "Zhè shì wǒ de lǎoshī.",  "english": "This is my teacher."},
    ]))

# Part 2 — V-not-V
_add(_expand_drill(7, 2, "L7.P2.D1", "Form a V-not-V question.", "构造正反问句。",
    "你 V 不 V (它/他/她)？", "Do you [verb] (him/her/it)?",
    [
        {"chinese": "你认识不认识他？", "pinyin": "Nǐ rènshi bu rènshi tā?","english": "Do you know him?"},
        {"chinese": "你忙不忙？",       "pinyin": "Nǐ máng bu máng?",      "english": "Are you busy?"},
        {"chinese": "你好不好？",       "pinyin": "Nǐ hǎo bu hǎo?",        "english": "Are you well?"},
        {"chinese": "他来不来？",       "pinyin": "Tā lái bu lái?",        "english": "Is he coming?"},
        {"chinese": "你去不去？",       "pinyin": "Nǐ qù bu qù?",          "english": "Are you going?"},
    ]))
_add(_expand_drill(7, 2, "L7.P2.D2", "Introduce yourself + your major.", "介绍自己和专业。",
    "我学习 [major] 专业。", "I study [major] as my major.",
    [
        {"chinese": "我学习美术专业。",   "pinyin": "Wǒ xuéxí měishù zhuānyè.",  "english": "I major in fine arts."},
        {"chinese": "我学习文学专业。",   "pinyin": "Wǒ xuéxí wénxué zhuānyè.",  "english": "I major in literature."},
        {"chinese": "他学习汉语专业。",   "pinyin": "Tā xuéxí Hànyǔ zhuānyè.",   "english": "He majors in Chinese."},
        {"chinese": "她学习外语专业。",   "pinyin": "Tā xuéxí wàiyǔ zhuānyè.",   "english": "She majors in foreign languages."},
    ]))


# ---------------------------- L8 ----------------------------
# Part 1 — family / numbers
_add(_expand_drill(8, 1, "L8.P1.D1", "State the size of someone’s family.", "说出家有几口人。",
    "我们家有 [number] 口人。", "Our family has [number] people.",
    [
        {"chinese": "我们家有三口人。", "pinyin": "Wǒmen jiā yǒu sān kǒu rén.", "english": "Our family has 3 people."},
        {"chinese": "我们家有四口人。", "pinyin": "Wǒmen jiā yǒu sì kǒu rén.",  "english": "Our family has 4 people."},
        {"chinese": "我们家有五口人。", "pinyin": "Wǒmen jiā yǒu wǔ kǒu rén.",  "english": "Our family has 5 people."},
        {"chinese": "我们家有六口人。", "pinyin": "Wǒmen jiā yǒu liù kǒu rén.", "english": "Our family has 6 people."},
        {"chinese": "我们家一共有六口人。","pinyin": "Wǒmen jiā yígòng yǒu liù kǒu rén.","english": "Our family has 6 people in total."},
    ]))
_add(_expand_drill(8, 1, "L8.P1.D2", "Say what relatives someone has.", "说说家中有什么亲属。",
    "我有 [number/MW] [relative].", "I have [number/MW] [relative].",
    [
        {"chinese": "我有一个哥哥。",   "pinyin": "Wǒ yǒu yí ge gēge.",   "english": "I have an older brother."},
        {"chinese": "我有一个姐姐。",   "pinyin": "Wǒ yǒu yí ge jiějie.", "english": "I have an older sister."},
        {"chinese": "我有两个弟弟。",   "pinyin": "Wǒ yǒu liǎng ge dìdi.","english": "I have two younger brothers."},
        {"chinese": "我有一个妹妹。",   "pinyin": "Wǒ yǒu yí ge mèimei.", "english": "I have a younger sister."},
        {"chinese": "我有妈妈和爸爸。", "pinyin": "Wǒ yǒu māma hé bàba.", "english": "I have a mom and a dad."},
    ]))
_add(_expand_drill(8, 1, "L8.P1.D3", "Ask 'How many ... do you have?' with 几.", "用'几'询问数量。",
    "你有几个 [noun]？", "How many [noun] do you have?",
    [
        {"chinese": "你有几个哥哥？", "pinyin": "Nǐ yǒu jǐ ge gēge?", "english": "How many older brothers do you have?"},
        {"chinese": "你有几个姐姐？", "pinyin": "Nǐ yǒu jǐ ge jiějie?","english": "How many older sisters?"},
        {"chinese": "你有几个弟弟？", "pinyin": "Nǐ yǒu jǐ ge dìdi?", "english": "How many younger brothers?"},
        {"chinese": "你们家有几口人？","pinyin": "Nǐmen jiā yǒu jǐ kǒu rén?","english": "How many people in your family?"},
    ]))

# Part 2
_add(_expand_drill(8, 2, "L8.P2.D1", "Ask 'How many ... ?' with 多少.", "用'多少'询问。",
    "[Subject] 有多少 [noun]？", "How many [noun] does [Subject] have?",
    [
        {"chinese": "语言学院有多少个系？",   "pinyin": "Yǔyán xuéyuàn yǒu duōshao ge xì?","english": "How many departments does the institute have?"},
        {"chinese": "你们系有多少老师？",     "pinyin": "Nǐmen xì yǒu duōshao lǎoshī?",    "english": "How many teachers in your department?"},
        {"chinese": "你们系有多少学生？",     "pinyin": "Nǐmen xì yǒu duōshao xuésheng?",  "english": "How many students in your department?"},
        {"chinese": "外语系有多少外国老师？", "pinyin": "Wàiyǔ xì yǒu duōshao wàiguó lǎoshī?","english": "How many foreign teachers in the foreign-lang dept?"},
    ]))
_add(_expand_drill(8, 2, "L8.P2.D2", "Describe how big/small.", "用'大不大'/'小不小'描述。",
    "[Subject] 大不大？", "Is [Subject] big?",
    [
        {"chinese": "语言学院大不大？", "pinyin": "Yǔyán xuéyuàn dà bu dà?", "english": "Is the institute big?"},
        {"chinese": "宿舍大不大？",     "pinyin": "Sùshè dà bu dà?",         "english": "Is the dorm big?"},
        {"chinese": "餐厅大不大？",     "pinyin": "Cāntīng dà bu dà?",       "english": "Is the cafeteria big?"},
        {"chinese": "你们家大不大？",   "pinyin": "Nǐmen jiā dà bu dà?",     "english": "Is your home big?"},
    ]))


# ---------------------------- L9 ----------------------------
# Part 1 — schedule, dates, ages
_add(_expand_drill(9, 1, "L9.P1.D1", "Ask which day of the week.", "用'星期几'询问。",
    "[Day] 是星期几？", "What day of the week is [Day]?",
    [
        {"chinese": "明天是星期几？", "pinyin": "Míngtiān shì xīngqī jǐ?","english": "What day is tomorrow?"},
        {"chinese": "今天是星期几？", "pinyin": "Jīntiān shì xīngqī jǐ?", "english": "What day is today?"},
        {"chinese": "昨天是星期几？", "pinyin": "Zuótiān shì xīngqī jǐ?", "english": "What day was yesterday?"},
        {"chinese": "星期日是几号？", "pinyin": "Xīngqīrì shì jǐ hào?",   "english": "What date is Sunday?"},
    ]))
_add(_expand_drill(9, 1, "L9.P1.D2", "State your age using 今年 + 岁.", "用'今年...岁'表达年龄。",
    "[Subject] 今年 [number] 岁.", "[Subject] is [number] this year.",
    [
        {"chinese": "我今年二十岁。",   "pinyin": "Wǒ jīnnián èrshí suì.",  "english": "I’m 20 this year."},
        {"chinese": "他今年二十二岁。", "pinyin": "Tā jīnnián èrshí’èr suì.","english": "He’s 22 this year."},
        {"chinese": "她今年十九岁。",   "pinyin": "Tā jīnnián shíjiǔ suì.", "english": "She’s 19 this year."},
        {"chinese": "弟弟今年六岁。",   "pinyin": "Dìdi jīnnián liù suì.",  "english": "Little brother is 6 this year."},
    ]))
_add(_expand_drill(9, 1, "L9.P1.D3", "Talk about having class on a given time.", "说什么时候有课。",
    "[time period] [Subject] 有课。", "[Subject] has class on [time period].",
    [
        {"chinese": "明天上午我有课。",   "pinyin": "Míngtiān shàngwǔ wǒ yǒu kè.",  "english": "I have class tomorrow morning."},
        {"chinese": "明天下午我有课。",   "pinyin": "Míngtiān xiàwǔ wǒ yǒu kè.",    "english": "I have class tomorrow afternoon."},
        {"chinese": "星期一我有课。",     "pinyin": "Xīngqīyī wǒ yǒu kè.",          "english": "I have class on Monday."},
        {"chinese": "星期日我没有课。",   "pinyin": "Xīngqīrì wǒ méi yǒu kè.",       "english": "I don’t have class on Sunday."},
    ]))

# Part 2 — birthday party
_add(_expand_drill(9, 2, "L9.P2.D1", "Wish someone happy birthday/holiday.", "用'祝...快乐'祝福。",
    "祝你 [holiday] 快乐！", "Happy [holiday]!",
    [
        {"chinese": "祝你生日快乐！",     "pinyin": "Zhù nǐ shēngrì kuàilè!",   "english": "Happy birthday!"},
        {"chinese": "祝你圣诞快乐！",     "pinyin": "Zhù nǐ Shèngdàn kuàilè!",  "english": "Merry Christmas!"},
        {"chinese": "祝你新年快乐！",     "pinyin": "Zhù nǐ xīnnián kuàilè!",   "english": "Happy New Year!"},
        {"chinese": "祝你旅行快乐！",     "pinyin": "Zhù nǐ lǚxíng kuàilè!",    "english": "Happy travels!"},
    ]))
_add(_expand_drill(9, 2, "L9.P2.D2", "State what we’re eating today.", "今天我们吃什么。",
    "今天我们吃 [food].", "Today we’re eating [food].",
    [
        {"chinese": "今天我们吃北京烤鸭。", "pinyin": "Jīntiān wǒmen chī Běijīng kǎoyā.","english": "Today we’re eating Beijing roast duck."},
        {"chinese": "今天我们吃蛋糕。",     "pinyin": "Jīntiān wǒmen chī dàngāo.",       "english": "Today we’re eating cake."},
        {"chinese": "今天我们吃寿面。",     "pinyin": "Jīntiān wǒmen chī shòumiàn.",     "english": "Today we’re eating longevity noodles."},
        {"chinese": "今天我们喝红葡萄酒。", "pinyin": "Jīntiān wǒmen hē hóng pútáojiǔ.", "english": "Today we’re drinking red wine."},
    ]))


# ---------------------------- L10 ----------------------------
# Part 1
_add(_expand_drill(10, 1, "L10.P1.D1", "Say what you’re buying with 在 + 这儿 + verb.", "用'在这儿买'造句。",
    "我在这儿买 [item].", "I’m buying [item] here.",
    [
        {"chinese": "我在这儿买光盘。",   "pinyin": "Wǒ zài zhèr mǎi guāngpán.","english": "I’m buying CDs here."},
        {"chinese": "我在这儿买书。",     "pinyin": "Wǒ zài zhèr mǎi shū.",     "english": "I’m buying books here."},
        {"chinese": "我在这儿买苹果。",   "pinyin": "Wǒ zài zhèr mǎi píngguǒ.", "english": "I’m buying apples here."},
        {"chinese": "我在这儿买东西。",   "pinyin": "Wǒ zài zhèr mǎi dōngxi.",  "english": "I’m buying things here."},
    ]))
_add(_expand_drill(10, 1, "L10.P1.D2", "Express your preferences with 喜欢.", "用'喜欢'表达喜好。",
    "我喜欢 [object].", "I like [object].",
    [
        {"chinese": "我喜欢中国音乐。",   "pinyin": "Wǒ xǐhuan Zhōngguó yīnyuè.","english": "I like Chinese music."},
        {"chinese": "我喜欢喝咖啡。",     "pinyin": "Wǒ xǐhuan hē kāfēi.",       "english": "I like drinking coffee."},
        {"chinese": "我喜欢学汉语。",     "pinyin": "Wǒ xǐhuan xué Hànyǔ.",      "english": "I like learning Chinese."},
        {"chinese": "我喜欢吃苹果。",     "pinyin": "Wǒ xǐhuan chī píngguǒ.",    "english": "I like eating apples."},
    ]))
_add(_expand_drill(10, 1, "L10.P1.D3", "Use 跟...去 to say 'go with someone'.", "用'跟...去'造句。",
    "我跟 [person] 去 [place].", "I go to [place] with [person].",
    [
        {"chinese": "我跟林娜去小商场。",   "pinyin": "Wǒ gēn Lín Nà qù xiǎo shāngchǎng.","english": "I go to the small mall with Lin Na."},
        {"chinese": "我跟朋友去餐厅。",     "pinyin": "Wǒ gēn péngyou qù cāntīng.",        "english": "I go to the cafeteria with a friend."},
        {"chinese": "我跟哥哥去学校。",     "pinyin": "Wǒ gēn gēge qù xuéxiào.",            "english": "I go to school with my older brother."},
        {"chinese": "我跟妈妈去医院。",     "pinyin": "Wǒ gēn māma qù yīyuàn.",             "english": "I go to the hospital with my mom."},
    ]))

# Part 2
_add(_expand_drill(10, 2, "L10.P2.D1", "Ask the price 多少钱?", "询问价格。",
    "[quantity] [item] 多少钱？", "How much is [quantity] [item]?",
    [
        {"chinese": "一斤苹果多少钱？", "pinyin": "Yì jīn píngguǒ duōshao qián?",   "english": "How much for 1 jin of apples?"},
        {"chinese": "一斤香蕉多少钱？", "pinyin": "Yì jīn xiāngjiāo duōshao qián?", "english": "How much for 1 jin of bananas?"},
        {"chinese": "一张光盘多少钱？", "pinyin": "Yì zhāng guāngpán duōshao qián?","english": "How much for one CD?"},
        {"chinese": "一杯咖啡多少钱？", "pinyin": "Yì bēi kāfēi duōshao qián?",     "english": "How much for one cup of coffee?"},
    ]))
_add(_expand_drill(10, 2, "L10.P2.D2", "Say what you’d like to buy with quantity.", "说出要买的数量。",
    "我买 [quantity] [item].", "I want to buy [quantity] [item].",
    [
        {"chinese": "我买三斤香蕉。", "pinyin": "Wǒ mǎi sān jīn xiāngjiāo.","english": "I’ll buy 3 jin of bananas."},
        {"chinese": "我买两斤苹果。", "pinyin": "Wǒ mǎi liǎng jīn píngguǒ.","english": "I’ll buy 2 jin of apples."},
        {"chinese": "我买一张光盘。", "pinyin": "Wǒ mǎi yì zhāng guāngpán.","english": "I’ll buy one CD."},
        {"chinese": "我买两个苹果。", "pinyin": "Wǒ mǎi liǎng ge píngguǒ.", "english": "I’ll buy two apples."},
    ]))


# ---------------------------- L11 ----------------------------
# Part 1
_add(_expand_drill(11, 1, "L11.P1.D1", "Express learned ability with 会.", "用'会'表达学得的能力。",
    "我会 [verb] [object].", "I can [verb] [object].",
    [
        {"chinese": "我会说汉语。",   "pinyin": "Wǒ huì shuō Hànyǔ.",   "english": "I can speak Chinese."},
        {"chinese": "我会说英语。",   "pinyin": "Wǒ huì shuō Yīngyǔ.",  "english": "I can speak English."},
        {"chinese": "我会说一点儿汉语。","pinyin": "Wǒ huì shuō yìdiǎnr Hànyǔ.","english": "I can speak a little Chinese."},
        {"chinese": "我会写汉字。",   "pinyin": "Wǒ huì xiě Hànzì.",    "english": "I can write Chinese characters."},
    ]))
_add(_expand_drill(11, 1, "L11.P1.D2", "Express capability with 能 + time.", "用'能'表达情境下的能力。",
    "[Subject] [time] 能 [verb]?", "Can [Subject] [verb] by [time]?",
    [
        {"chinese": "我们八点能到吗？", "pinyin": "Wǒmen bā diǎn néng dào ma?","english": "Can we arrive by 8?"},
        {"chinese": "你今天能来吗？",   "pinyin": "Nǐ jīntiān néng lái ma?",   "english": "Can you come today?"},
        {"chinese": "他明天能上课吗？", "pinyin": "Tā míngtiān néng shàngkè ma?","english": "Can he attend class tomorrow?"},
        {"chinese": "我们现在能去吗？", "pinyin": "Wǒmen xiànzài néng qù ma?", "english": "Can we go now?"},
    ]))
_add(_expand_drill(11, 1, "L11.P1.D3", "Ask the time of day.", "询问时间。",
    "现在几点？", "What time is it?",
    [
        {"chinese": "现在几点？",     "pinyin": "Xiànzài jǐ diǎn?",     "english": "What time is it?"},
        {"chinese": "现在八点。",     "pinyin": "Xiànzài bā diǎn.",     "english": "It’s 8 o’clock."},
        {"chinese": "差一刻八点。",   "pinyin": "Chà yí kè bā diǎn.",   "english": "Quarter to 8."},
        {"chinese": "现在差五分八点。","pinyin": "Xiànzài chà wǔ fēn bā diǎn.","english": "5 to 8 now."},
    ]))

# Part 2
_add(_expand_drill(11, 2, "L11.P2.D1", "Say what someone should do with 应该.", "用'应该'表义务。",
    "[Subject] 应该 [verb].", "[Subject] should [verb].",
    [
        {"chinese": "他应该来上课。",   "pinyin": "Tā yīnggāi lái shàngkè.",   "english": "He should come to class."},
        {"chinese": "你应该多休息。",   "pinyin": "Nǐ yīnggāi duō xiūxi.",     "english": "You should rest more."},
        {"chinese": "你应该多喝水。",   "pinyin": "Nǐ yīnggāi duō hē shuǐ.",   "english": "You should drink more water."},
        {"chinese": "我应该去看病。",   "pinyin": "Wǒ yīnggāi qù kànbìng.",    "english": "I should see a doctor."},
    ]))
_add(_expand_drill(11, 2, "L11.P2.D2", "Negate ability/capability with 不能 / 不会.", "用'不能/不会'否定。",
    "[Subject] 不能/不会 [verb].", "[Subject] can’t [verb].",
    [
        {"chinese": "他今天不能来上课。", "pinyin": "Tā jīntiān bù néng lái shàngkè.","english": "He can’t attend class today."},
        {"chinese": "我不会说英语。",     "pinyin": "Wǒ bú huì shuō Yīngyǔ.",         "english": "I can’t speak English."},
        {"chinese": "我明天不能去。",     "pinyin": "Wǒ míngtiān bù néng qù.",        "english": "I can’t go tomorrow."},
        {"chinese": "他不会写汉字。",     "pinyin": "Tā bú huì xiě Hànzì.",           "english": "He can’t write characters."},
    ]))


# ---------------------------- L12 ----------------------------
# Part 1
_add(_expand_drill(12, 1, "L12.P1.D1", "Describe a body part hurting.", "描述身体哪儿疼。",
    "我 [body] 疼.", "My [body] hurts.",
    [
        {"chinese": "我头疼。",     "pinyin": "Wǒ tóu téng.",    "english": "My head hurts."},
        {"chinese": "我嗓子疼。",   "pinyin": "Wǒ sǎngzi téng.", "english": "My throat hurts."},
        {"chinese": "我全身都不舒服。","pinyin": "Wǒ quánshēn dōu bù shūfu.","english": "My whole body feels bad."},
        {"chinese": "我发烧。",     "pinyin": "Wǒ fāshāo.",      "english": "I have a fever."},
        {"chinese": "我感冒了。",   "pinyin": "Wǒ gǎnmào le.",   "english": "I’ve caught a cold."},
    ]))
_add(_expand_drill(12, 1, "L12.P1.D2", "Give advice with 你应该 + verb.", "用'你应该...'提建议。",
    "你应该 [verb].", "You should [verb].",
    [
        {"chinese": "你应该去医院看病。", "pinyin": "Nǐ yīnggāi qù yīyuàn kànbìng.","english": "You should go see a doctor."},
        {"chinese": "你应该多喝水。",     "pinyin": "Nǐ yīnggāi duō hē shuǐ.",       "english": "You should drink more water."},
        {"chinese": "你应该多休息。",     "pinyin": "Nǐ yīnggāi duō xiūxi.",         "english": "You should rest more."},
        {"chinese": "你应该多穿衣服。",   "pinyin": "Nǐ yīnggāi duō chuān yīfu.",    "english": "You should wear more clothes."},
    ]))
_add(_expand_drill(12, 1, "L12.P1.D3", "Reject with 不用 + verb.", "用'不用'拒绝。",
    "不用 [verb].", "No need to [verb].",
    [
        {"chinese": "不用去看病。",   "pinyin": "Bú yòng qù kànbìng.","english": "No need to see a doctor."},
        {"chinese": "不用谢。",       "pinyin": "Bú yòng xiè.",       "english": "You’re welcome."},
        {"chinese": "不用吃药。",     "pinyin": "Bú yòng chī yào.",   "english": "No need to take medicine."},
        {"chinese": "不用住院。",     "pinyin": "Bú yòng zhùyuàn.",   "english": "No need to be hospitalized."},
    ]))

# Part 2
_add(_expand_drill(12, 2, "L12.P2.D1", "Doctor asks where it hurts.", "医生询问哪里不舒服。",
    "你哪儿不舒服？", "Where does it hurt?",
    [
        {"chinese": "你哪儿不舒服？", "pinyin": "Nǐ nǎr bù shūfu?", "english": "Where do you feel unwell?"},
        {"chinese": "你头疼吗？",     "pinyin": "Nǐ tóu téng ma?",  "english": "Does your head hurt?"},
        {"chinese": "你嗓子疼吗？",   "pinyin": "Nǐ sǎngzi téng ma?","english": "Does your throat hurt?"},
        {"chinese": "你发烧吗？",     "pinyin": "Nǐ fāshāo ma?",    "english": "Do you have a fever?"},
    ]))
_add(_expand_drill(12, 2, "L12.P2.D2", "Take medicine instruction.", "服药指示。",
    "你要 [verb-action].", "You need to [verb-action].",
    [
        {"chinese": "你要多喝水。",     "pinyin": "Nǐ yào duō hē shuǐ.",     "english": "You need to drink lots of water."},
        {"chinese": "你要吃点儿药。",   "pinyin": "Nǐ yào chī diǎnr yào.",   "english": "You need to take some medicine."},
        {"chinese": "你要吃中药。",     "pinyin": "Nǐ yào chī zhōngyào.",    "english": "You need to take Chinese medicine."},
        {"chinese": "你要多穿点儿衣服。","pinyin": "Nǐ yào duō chuān diǎnr yīfu.","english": "You need to wear more clothes."},
    ]))


# ---------------------------- L13 ----------------------------
# Part 1
_add(_expand_drill(13, 1, "L13.P1.D1", "Talk about a completed action with 了.", "用'了'表示完成。",
    "我 [verb] 了 [object].", "I [verb-ed] [object].",
    [
        {"chinese": "我去了医院。",         "pinyin": "Wǒ qùle yīyuàn.",          "english": "I went to the hospital."},
        {"chinese": "我吃了很多中药。",     "pinyin": "Wǒ chīle hěn duō zhōngyào.","english": "I took a lot of Chinese medicine."},
        {"chinese": "我认识了一个姑娘。",   "pinyin": "Wǒ rènshile yí ge gūniang.","english": "I met a girl."},
        {"chinese": "我看了一间房子。",     "pinyin": "Wǒ kànle yì jiān fángzi.",  "english": "I looked at a room."},
        {"chinese": "他得了感冒。",         "pinyin": "Tā déle gǎnmào.",            "english": "He caught a cold."},
    ]))
_add(_expand_drill(13, 1, "L13.P1.D2", "Use Adjective + 的 + Noun.", "用'形容词+的+名词'。",
    "[adj] 的 [noun]", "[adj] [noun]",
    [
        {"chinese": "漂亮的姑娘",   "pinyin": "piàoliang de gūniang", "english": "a beautiful girl"},
        {"chinese": "好的朋友",     "pinyin": "hǎo de péngyou",       "english": "a good friend"},
        {"chinese": "贵的房子",     "pinyin": "guì de fángzi",        "english": "an expensive house"},
        {"chinese": "忙的工作",     "pinyin": "máng de gōngzuò",      "english": "a busy job"},
    ]))
_add(_expand_drill(13, 1, "L13.P1.D3", "Talk about renting/wanting something.", "表达想租/想要。",
    "我想 [verb] [object].", "I want to [verb] [object].",
    [
        {"chinese": "我想租一间房子。",       "pinyin": "Wǒ xiǎng zū yì jiān fángzi.",       "english": "I want to rent a room."},
        {"chinese": "我想告诉你一件事儿。",   "pinyin": "Wǒ xiǎng gàosu nǐ yí jiàn shìr.",   "english": "I want to tell you something."},
        {"chinese": "我想买一张光盘。",       "pinyin": "Wǒ xiǎng mǎi yì zhāng guāngpán.",   "english": "I want to buy a CD."},
        {"chinese": "我想认识她。",           "pinyin": "Wǒ xiǎng rènshi tā.",                "english": "I want to get to know her."},
    ]))

# Part 2
_add(_expand_drill(13, 2, "L13.P2.D1", "Use 给 + person + 打电话.", "用'给...打电话'造句。",
    "我给 [person] 打个电话。", "I’ll give [person] a call.",
    [
        {"chinese": "我给陆雨平打个电话。","pinyin": "Wǒ gěi Lù Yǔpíng dǎ ge diànhuà.","english": "I’ll call Lu Yuping."},
        {"chinese": "我给妈妈打电话。",   "pinyin": "Wǒ gěi māma dǎ diànhuà.",        "english": "I’ll call mom."},
        {"chinese": "我给老师打电话。",   "pinyin": "Wǒ gěi lǎoshī dǎ diànhuà.",      "english": "I’ll call the teacher."},
        {"chinese": "我给朋友打电话。",   "pinyin": "Wǒ gěi péngyou dǎ diànhuà.",     "english": "I’ll call a friend."},
    ]))
_add(_expand_drill(13, 2, "L13.P2.D2", "Use 让 + person + verb (ask to do).", "用'让+人+动词'表示请求。",
    "让 [person] 来 [verb].", "Ask [person] to come and [verb].",
    [
        {"chinese": "让他来帮助我们。", "pinyin": "Ràng tā lái bāngzhù wǒmen.","english": "Have him come help us."},
        {"chinese": "让她来吃饭。",     "pinyin": "Ràng tā lái chī fàn.",      "english": "Have her come eat."},
        {"chinese": "让他来上课。",     "pinyin": "Ràng tā lái shàngkè.",      "english": "Have him come to class."},
        {"chinese": "让朋友来帮助我。", "pinyin": "Ràng péngyou lái bāngzhù wǒ.","english": "Have a friend come help me."},
    ]))


# ---------------------------- L14 ----------------------------
# Part 1
_add(_expand_drill(14, 1, "L14.P1.D1", "Use 给 + person + 打了 + 一个电话.", "用'给...打了一个电话'造句。",
    "[Subject] 给 [person] 打了一个电话.", "[Subject] called [person].",
    [
        {"chinese": "妈妈给力波打了一个电话。", "pinyin": "Māma gěi Lìbō dǎle yí ge diànhuà.","english": "Mom called Libo."},
        {"chinese": "我给妈妈打了一个电话。",   "pinyin": "Wǒ gěi māma dǎle yí ge diànhuà.",  "english": "I called my mom."},
        {"chinese": "我给老师打了一个电话。",   "pinyin": "Wǒ gěi lǎoshī dǎle yí ge diànhuà.","english": "I called the teacher."},
        {"chinese": "他给经理打了一个电话。",   "pinyin": "Tā gěi jīnglǐ dǎle yí ge diànhuà.","english": "He called the manager."},
    ]))
_add(_expand_drill(14, 1, "L14.P1.D2", "Say what someone just did with 刚才.", "用'刚才'表示刚刚做。",
    "我刚才 [verb] [object].", "I just [verb-ed] [object].",
    [
        {"chinese": "我刚才去邮局。",     "pinyin": "Wǒ gāngcái qù yóujú.",     "english": "I just went to the post office."},
        {"chinese": "我刚才寄了点儿东西。","pinyin": "Wǒ gāngcái jìle diǎnr dōngxi.","english": "I just mailed some things."},
        {"chinese": "我刚才打扫了宿舍。", "pinyin": "Wǒ gāngcái dǎsǎole sùshè.",    "english": "I just cleaned the dorm."},
        {"chinese": "我刚才吃饭。",       "pinyin": "Wǒ gāngcái chī fàn.",          "english": "I just ate."},
    ]))
_add(_expand_drill(14, 1, "L14.P1.D3", "Apologize for being busy/late.", "为忙/迟到表示歉意。",
    "不好意思，[reason].", "Sorry, [reason].",
    [
        {"chinese": "不好意思，这两天我太忙了。", "pinyin": "Bù hǎoyìsi, zhè liǎng tiān wǒ tài máng le.","english": "Sorry, I’ve been very busy these last days."},
        {"chinese": "对不起，我来晚了。",         "pinyin": "Duìbuqǐ, wǒ lái wǎn le.",                  "english": "Sorry, I’m late."},
        {"chinese": "对不起，我不知道。",         "pinyin": "Duìbuqǐ, wǒ bù zhīdào.",                   "english": "Sorry, I don’t know."},
        {"chinese": "对不起，请再说一遍。",       "pinyin": "Duìbuqǐ, qǐng zài shuō yí biàn.",          "english": "Sorry, please say it again."},
    ]))

# Part 2
_add(_expand_drill(14, 2, "L14.P2.D1", "Send a Christmas/holiday gift with 送.", "用'送'表达赠送。",
    "[Subject] 送 [person] 一件 [gift].", "[Subject] gives [person] a [gift].",
    [
        {"chinese": "爸爸送你一件圣诞礼物。",     "pinyin": "Bàba sòng nǐ yí jiàn Shèngdàn lǐwù.",    "english": "Dad gives you a Christmas gift."},
        {"chinese": "我送你一件礼物。",           "pinyin": "Wǒ sòng nǐ yí jiàn lǐwù.",               "english": "I’ll give you a gift."},
        {"chinese": "妈妈送我一件衣服。",         "pinyin": "Māma sòng wǒ yí jiàn yīfu.",             "english": "Mom gives me a piece of clothing."},
        {"chinese": "我们送老师一件礼物。",       "pinyin": "Wǒmen sòng lǎoshī yí jiàn lǐwù.",        "english": "We give the teacher a gift."},
    ]))
_add(_expand_drill(14, 2, "L14.P2.D2", "Travel intent with 要去 + place + 旅行.", "用'要去...旅行'表达旅行意愿。",
    "[Subject] 要去 [place] 旅行.", "[Subject] will travel to [place].",
    [
        {"chinese": "我要去上海旅行。",     "pinyin": "Wǒ yào qù Shànghǎi lǚxíng.","english": "I’ll travel to Shanghai."},
        {"chinese": "他要去欧洲旅行。",     "pinyin": "Tā yào qù Ōuzhōu lǚxíng.",  "english": "He’ll travel to Europe."},
        {"chinese": "我们要去北京旅行。",   "pinyin": "Wǒmen yào qù Běijīng lǚxíng.","english": "We’ll travel to Beijing."},
        {"chinese": "爸爸要去中国旅行。",   "pinyin": "Bàba yào qù Zhōngguó lǚxíng.","english": "Dad will travel to China."},
    ]))
_add(_expand_drill(14, 2, "L14.P2.D3", "Christmas/holiday wishes.", "圣诞/节日祝福。",
    "祝你 [holiday] 快乐！", "Merry/Happy [holiday]!",
    [
        {"chinese": "祝你圣诞快乐！",     "pinyin": "Zhù nǐ Shèngdàn kuàilè!",  "english": "Merry Christmas!"},
        {"chinese": "祝你新年快乐！",     "pinyin": "Zhù nǐ xīnnián kuàilè!",   "english": "Happy New Year!"},
        {"chinese": "祝你旅行快乐！",     "pinyin": "Zhù nǐ lǚxíng kuàilè!",    "english": "Happy travels!"},
        {"chinese": "祝你生日快乐！",     "pinyin": "Zhù nǐ shēngrì kuàilè!",   "english": "Happy birthday!"},
    ]))


__all__ = ["NPCR_LESSONS", "SENTENCE_DRILLS"]
