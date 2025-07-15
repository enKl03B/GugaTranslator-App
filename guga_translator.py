import base64
import binascii

# 定义自定义字符集和标准Base64字符集
ALPHABET = ['咕', '嘎', '🐧', '🍄', '哇擦']
BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def generate_encoding_table():
    """
    生成从标准Base64索引到自定义字符组合的映射表。
    这个逻辑直接从原始的JavaScript代码 `generateEncodingTable` 翻译而来。
    它将一个0-63的索引 i 转换为一个基于5的三位数，然后用这个三位数
    作为 ALPHABET 的索引来创建三字符的组合。
    """
    table = []
    for i in range(64):
        n = i
        d2 = n // 25
        n %= 25
        d1 = n // 5
        d0 = n % 5
        table.append(f"{ALPHABET[d2]}{ALPHABET[d1]}{ALPHABET[d0]}")
    return table

# 生成编码表和解码表
ENCODING_TABLE = generate_encoding_table()
DECODING_TABLE = {code: index for index, code in enumerate(ENCODING_TABLE)}

def encode(text: str) -> str:
    """
    将普通文本编码为自定义的“企鹅语”。
    """
    if not text:
        return ""
    # 1. 将输入文本转换为UTF-8字节
    utf8_bytes = text.encode('utf-8')
    # 2. 使用标准Base64进行编码
    standard_base64 = base64.b64encode(utf8_bytes).decode('ascii')
    
    # 3. 将标准Base64字符映射到自定义字符组合
    custom_encoded_parts = []
    for char in standard_base64:
        if char == '=':
            continue
        index = BASE64_CHARS.find(char)
        if index != -1:
            custom_encoded_parts.append(ENCODING_TABLE[index])
            
    return "".join(custom_encoded_parts)

def decode(custom_text: str) -> str:
    """
    将自定义的“企鹅语”解码为普通文本。
    """
    if not custom_text:
        return ""
        
    # 1. 将输入的自定义字符串按3个字符一组进行分割
    # 因为编码表中的每个组合都是3个字符长
    if len(custom_text) % 3 != 0:
        raise ValueError("输入包含无效的字符组合或长度错误")

    codes = [custom_text[i:i+3] for i in range(0, len(custom_text), 3)]
    
    # 2. 将每个自定义字符组合映射回标准Base64字符
    base64_chars = []
    for code in codes:
        index = DECODING_TABLE.get(code)
        if index is None:
            raise ValueError(f'输入包含无法解码的符号组合: "{code}"')
        base64_chars.append(BASE64_CHARS[index])
    
    # 3. 拼接并添加必要的 '=' 填充
    standard_base64 = "".join(base64_chars)
    padding_needed = (4 - len(standard_base64) % 4) % 4
    standard_base64 += "=" * padding_needed
    
    # 4. 使用标准Base64解码
    try:
        decoded_bytes = base64.b64decode(standard_base64)
        return decoded_bytes.decode('utf-8')
    except (binascii.Error, UnicodeDecodeError) as e:
        raise ValueError(f"Base64解码失败: {e}")

