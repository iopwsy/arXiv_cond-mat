import datetime, argparse, feedparser
from openai import OpenAI

def main(api_key:str,
         base_url:str,
         model:str,
         outdir:str):
    url="https://rss.arxiv.org/rss/cond-mat"
    feed = feedparser.parse(url)
    update_date = datetime.datetime.strptime("-".join(feed['feed']['published'].split(' ')[1:4]),'%d-%b-%Y')
    data = []
    if update_date.strftime("%Y-%m-%d") == day.strftime("%Y-%m-%d"):
        for entry in feed.entries:
            data.append(dict(
                title=entry['title'],
                link=entry['link'],
                authors=entry['author'],
                abstract=entry['summary'].split('Abstract: ')[-1]
            ))
        content = "\n\n".join(["\n".join([f"{key}:{value}" for key,value in entry.items()]) for entry in data])
        messages = [
                    {"role": "system", "content": "总结今天arXiv有关凝聚态物理的文章"},
                    {"role": "user", "content": content},
                   ]
        client = OpenAI(api_key=api_key,
                        base_url=base_url)
        response = client.chat.completions.create(
                                                  model=model,
                                                  messages=messages,
                                                  stream=False,
                                                  )
        content = f"""---
        title: 自动更新arXiv凝聚态物理的文章
        date: {datetime.datetime.now().isoformat()}
        ---
        这是自动生成的凝聚态物理的文章总结：
        {response.choices[0].message.content}
        """
        with open(f"{outdir}/arXiv.md",'a') as f:
            f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', required=True)
    parser.add_argument('--base_url', required=False,default="https://models.github.ai/inference")
    parser.add_argument('--model', required=False,default="deepseek/DeepSeek-V3-0324")
    parser.add_argument('--outdir', required=True)
    
    args = parser.parse_args()
    main(api_key=api_key,base_url=base_url,model=model,outdir=outdir)
