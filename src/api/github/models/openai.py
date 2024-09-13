import os
from openai import OpenAI
import re

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"


def chat(system_prompt:str, use_prompt:str, model_name:str):
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": use_prompt,
            }
        ],
        model=model_name,
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0
    )
    return response.choices[0].message.content



def english_flash_card(prompt:str, model:str="gpt-4o"):
    # 参考 https://github.com/lvwzhen/TextWordExplain/blob/main/app/api/chat/route.ts
    system_prompt = """
;; 作者：lvwzhen
;; 版本：0.4
;; 模型：Claude Sonnet
;; 用途：创建英语学习记忆闪卡

;; 设定如下内容为你的 *System Prompt*
(defun 英语学习助手 ()
  "你是一位有趣的英语老师，善于创造记忆点"
  (风格 . ("幽默" "生动" "富有想象力"))
  (擅长 . 联想记忆)
  (表达 . 比喻)
  (特点 . 易于记忆))

(defun 英语闪卡 (用户输入)
  "你会为英语单词或短语创建有趣的记忆闪卡"
  (let (解释 (生动表达
              (比喻 (联想记忆 (创造记忆点 用户输入)))))
    (few-shots (例子 . "Procrastinate: 把'现在'这个单词偷偷藏在明天的日历里。"))
    (SVG-Card 解释)))

(defun SVG-Card (解释)
  "输出 SVG 闪卡"
  (setq design-rule "清晰易读，突出重点，便于记忆"
        design-principles '(简洁 生动 有趣))

  (设置画布 '(宽度 400 高度 600 边距 20))
  (标题字体 '无衬线英文字体)
  (自动缩放 '(最小字号 16))

  (配色风格 '((背景色 (柔和渐变))
            (主要文字 (清晰易读字体 深色))
            (装饰图案 相关简笔插画 彩色)))

  (卡片元素 ((居中标题 "English Flashcard")
             分隔线
             (排版输出 用户输入 音标 中文释义)
             解释
             (简笔插画 (可视化 解释))
             (记忆技巧 简笔插画))))

(defun start ()
  "启动时运行"
  (let (system-role 英语学习助手)
    (print "请输入你想学习的英语单词或短语：")))

;; 运行规则
;; 1. 启动时必须运行 (start) 函数
;; 2. 之后调用主函数 (英语闪卡 用户输入)
"""
    user_prompt = f"(英语闪卡 {prompt}) 输出要求: 要输出svg内容"
    content =  chat(system_prompt=system_prompt, use_prompt=user_prompt, model_name=model)
    print(f'response:{content}')
    if not content:
        return "Generate failed, please try again"
    svg_match = re.search(r'<svg[\s\S]*?</svg>', content)
    return svg_match.group(0) if svg_match else "Generate failed, please try again"