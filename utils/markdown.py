def escape_markdown_v2(text):
    reserved_chars = r"_*[]()~`>#+-=|{}.!"
    return ''.join(['\\' + char if char in reserved_chars else char for char in text])