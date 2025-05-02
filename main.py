import datetime, argparse, feedparser
from openai import OpenAI
import os

def main(api_key:str,
         base_url:str,
         model:str):
    day = datetime.datetime.now()
    url="https://rss.arxiv.org/rss/cond-mat"
    feed = feedparser.parse(url)
    update_date = datetime.datetime.strptime("-".join(feed['feed']['published'].split(' ')[1:4]),'%d-%b-%Y')
    if update_date.strftime("%Y-%m-%d") == day.strftime("%Y-%m-%d"):
        content = ""
        for entry in feed.entries:
            abstract=entry['summary'].split('Abstract: ')[-1]
            content += f"title:{entry['title']}\nlink:{entry['link']}\nauthors:{entry['author']}abstract:{abstract}"
        messages = [
                    {"role": "system", "content": "用户将发送当天arXiv有关凝聚态物理的论文，请用中文总结今天凝聚态相关文章，包括新的理论、计算和实验的进展，带上文章链接"},
                    {"role": "user", "content": content},
                   ]
        try:
            client = OpenAI(api_key=api_key,
                            base_url=base_url)
            response = client.chat.completions.create(
                                                      model=model,
                                                      messages=messages,
                                                      stream=False,
                                                      )
            os.remove("README.md")
            content = f"""
            ### 标题
            自动更新arXiv凝聚态物理的文章
             - **代码更新时间** {day.isoformat()}
             - **arXiv更新时间** {update_date.isoformat()}
            {response.choices[0].message.content}
            """
            with open("README.md",'a') as f:
                f.write(content)
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', required=True)
    parser.add_argument('--base_url', required=False,default="https://models.github.ai/inference")
    parser.add_argument('--model', required=False,default="deepseek/DeepSeek-V3-0324")
    
    args = parser.parse_args()
    main(api_key=args.api_key,
         base_url=args.base_url,
         model=args.model)
