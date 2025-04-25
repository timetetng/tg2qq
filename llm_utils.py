# llm_utils.py
import google.generativeai as genai
import config  # 导入 config.py

# 用于处理多行提示词
def multiline_string_to_singleline(multiline_string):
    """Converts a multiline string to a single-line string."""
    lines = multiline_string.strip().splitlines()
    singleline_string = "\\n ".join(lines)
    return singleline_string

def generate_gemini_response(user_input):
    """Generates a response from the Gemini model."""
    try:
        print("开始调用 Gemini API...")  # 添加调试信息
        genai.configure(api_key=config.API_KEY)
        model = genai.GenerativeModel(config.MODEL_NAME)

        # 构建 Prompt
        prompt = multiline_string_to_singleline(config.SYSTEM_PROMPT) + \
                 "用户输入：" + user_input

        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
        else:
            print("Gemini API 返回结果为空！")  # 添加调试信息
            return ""
    except Exception as e:
        print(f"Gemini API 调用失败：{e}")  # 添加调试信息
        return ""
