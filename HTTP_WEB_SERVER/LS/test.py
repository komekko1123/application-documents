def custom_unquote(encoded_str):
    encoded_str = encoded_str.replace('+', ' ')
    parts = encoded_str.split('%')
    if len(parts) == 1:
        return encoded_str
    print(parts)
    result = [parts[0]]
    for item in parts[1:]:
        try:
            char = chr(int(item[:2], 16)) ##轉char 2C = ,
            result.append(char + item[2:]) ##  2C後的編碼   
        except ValueError:
            result.append('%' + item)
    
    return ''.join(result)

encoded_data = "username%3Dzhangsan%26password%3Dmima"
decoded_data = custom_unquote(encoded_data)
print(decoded_data)  # Output: Hello, World!