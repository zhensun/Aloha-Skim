# A bible reader
import codecs

def bot_bible(mess, nick, botCmd):
    """Bible Reader. Example: !bible jhn 3:16"""
    fh = codecs.open("bible.txt", "r", "utf-8")
    message = ''
    if (len(botCmd)==1):
        message =u'旧约\n中文卷名 中文缩写 英文卷名 英文缩写\n创世记 创 Genesis Gen\n出埃及记 出 Exodus Exo\n利未记 利 Levitius Lev\n民数记 民 Numbers Num\n申命记 申 Deuteronomy Deu\n约书亚记 书 Joshua Jos\n士师记 士 Judges Jug\n路得记 得 Ruth Rut\n撒母耳记上 撒上 1 Samuel 1Sa\n撒母耳记下 撒下 2 Samuel 2Sa\n列王纪上 王上 1Kings 1Ki\n列王纪下 王下 2Kings 2Ki\n历代志上 代上 1 Chronicles 1Ch\n历代志下 代下 2 Chronicles 2Ch\n以斯拉记 拉 Ezra Ezr\n尼希米记 尼 Nehemiah Neh\n以斯帖记 斯 Esther Est\n约伯记 伯 Job Job\n诗篇 诗 Psalms Psm\n箴言 箴 Proverbs Pro\n传道书 传 Ecclesiastes Ecc\n雅歌 歌 Song of Songs Son\n以赛亚书 赛 Isaiah Isa\n耶利米书 耶 Jeremiah Jer\n耶利米哀歌 哀 Lamentations Lam\n以西结书 结 Ezekiel Eze\n但以理书 但 Daniel Dan\n何西阿书 何 Hosea Hos\n约珥书 珥 Joel Joe\n阿摩司书 摩 Amos Amo\n俄巴底亚书 俄 Obadiah Oba\n约拿书 拿 Jonah Jon\n弥迦书 弥 Micah Mic\n那鸿书 鸿 Nahum Nah\n哈巴谷书 哈 Habakkuk Hab\n西番雅书 番 Zephaniah Zep\n哈该书 该 Haggai Hag\n撒迦利亚书 亚 Zechariah Zec\n玛拉基书 玛 Malachi Mal\n新约\n中文卷名 中文缩写 英文卷名 英文缩写\n马太福音 太 Matthew Mat\n马可福音 可 Mark Mak\n路加福音 路 Luke Luk\n约翰福音 约 John Jhn\n使徒行传 徒 Acts Act\n罗马书 罗 Romans Rom\n哥林多前书 林前 1 Corinthians 1Co\n哥林多后书 林后 2 Corinthians 2Co\n加拉太书 加 Galatians Gal\n以弗所书 弗 Ephesians Eph\n腓利比书 腓 Philippians Phl\n歌罗西书 西 Colossians Col\n帖撒罗尼迦前书 帖前 1Thessalinians 1Ts\n帖撒罗尼迦后书 帖后 2 Thessalinians 2Ts\n提摩太前书 提前 1 Timothy 1Ti\n提摩太后书 提后 2 Timothy 2Ti\n提多书 多 Titus Tit\n腓利门书 门 Philemon Phm\n希伯来书 来 Hebrews Heb\n雅各书 雅 James Jas\n彼得前书 彼前 1 Peter 1Pe\n彼得后书 彼后 2 Peter 2Pe\n约翰壹书 约一 1 John 1Jn\n约翰贰书 约二 2 John 2Jn\n约翰参书 约三 3 John 3Jn\n犹大书 犹 Jude Jud\n启示录 启 Revelation Rev'
        return "/msg " + nick + " " + message
    if (botCmd[1].find(":") >= 0):
        for i in range (0, 31102):
            message = fh.readline()
            messageclone = message.lower()
            if messageclone.startswith(botCmd[1].lower()):
                fh.close()
                return u'“' + message.strip() + u'”'
    else:
        for i in range (0, 31102):
            messageRead = fh.readline()
            messageclone = messageRead.lower()
            if messageclone.startswith(botCmd[1].lower() + ":"):
                message = message + messageRead
        fh.close()
        if message != "":
            return "/msg " + nick + u" “" + message + u"”"
    return u"Cannot find the chapter."
    pass
