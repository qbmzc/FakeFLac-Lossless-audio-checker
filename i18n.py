import os
import gettext
import locale

# 支持的语言列表
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'zh_CN': '简体中文',
    'ja': '日本語',
    'ko': '한국어',
    'ru': 'Русский',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch'
}

# 翻译函数
_ = None

# 当前语言
current_language = None

# 翻译目录
LOCALE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')

def setup_i18n(language=None):
    """
    设置国际化环境
    
    Parameters
    ----------
    language : str
        语言代码 (例如 'en', 'zh_CN', 'ja')
        如果为None，则尝试使用系统默认语言
    """
    global _, current_language
    
    # 如果未指定语言，尝试获取系统语言
    if language is None:
        try:
            system_lang, _ = locale.getdefaultlocale()
            # 检查系统语言是否在支持的语言列表中
            if system_lang in SUPPORTED_LANGUAGES:
                language = system_lang
            else:
                # 如果完整语言代码不匹配，尝试匹配主要语言部分
                main_lang = system_lang.split('_')[0] if system_lang and '_' in system_lang else ''
                for lang_code in SUPPORTED_LANGUAGES:
                    if lang_code.startswith(main_lang):
                        language = lang_code
                        break
        except:
            pass
    
    # 如果仍未确定语言或语言不受支持，默认使用英语
    if language is None or language not in SUPPORTED_LANGUAGES:
        language = 'en'
    
    # 设置当前语言
    current_language = language
    
    # 设置翻译
    try:
        translation = gettext.translation('fakeflac', LOCALE_DIR, languages=[language])
        _ = translation.gettext
    except FileNotFoundError:
        # 如果翻译文件不存在，使用空翻译（返回原始字符串）
        _ = gettext.NullTranslations().gettext

def get_current_language():
    """
    获取当前语言代码
    
    Returns
    -------
    str
        当前语言代码
    """
    return current_language

def get_language_name(language_code):
    """
    获取语言名称
    
    Parameters
    ----------
    language_code : str
        语言代码
        
    Returns
    -------
    str
        语言名称
    """
    return SUPPORTED_LANGUAGES.get(language_code, language_code)

def get_supported_languages():
    """
    获取支持的语言列表
    
    Returns
    -------
    dict
        语言代码和名称的字典
    """
    return SUPPORTED_LANGUAGES

# 初始化国际化设置
setup_i18n()