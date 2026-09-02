import json
import os
import re
from prompt_manager import prompts_to_dicts,load_prompts_from_dicts
DATA_DIR="data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR) 
JSON_PATH=os.path.join(DATA_DIR,"prompt_pack.json")
def save_to_json(prompt_list,filename=JSON_PATH):
    try:
        dict_list=prompts_to_dicts(prompt_list)
        with open(filename,"w",encoding="utf-8") as file:
            json.dump(dict_list,file,ensure_ascii=False,indent=4)
        print(f"Save to {filename}")  
        return True
    except Exception as e:  
        print(f"Failed to save {e}")  
        return False 
def load_from_json(filename=JSON_PATH):
    try:
        with open(filename,"r",encoding="utf-8") as file:
            dict_list = json.load(file)
        prompts=load_prompts_from_dicts(dict_list)    
        print(f"Loaded {len(prompts)} prompts from {filename}")  
        return prompts
    except FileNotFoundError:
        print(f"[ERROR] {filename} not found.")  
        return []  
    except Exception as e:
        print(f"[ERROR] Failed to loaded: {e}") 
        return []   
def generate_product_file(prompt_pack,filename):
    try:
        with open(filename,"w",encoding="utf-8") as product_file:
            product_file.write("="*60+"\n")
            product_file.write("50 AI Prompts for Small Business Owners \n")
            product_file.write("="*60+"\n\n")
            product_file.write("[HOW TO USE]\n")
            product_file.write("1.Copy any prompt below.\n")
            product_file.write("2.Replace the [BRACKETED] text with your own business info.\n")
            product_file.write("3.Paste into ChatGPT/Claude/Kimi or any AI tool.\n")
            product_file.write("4.Get professional-level business copy instantly.\n\n")
            product_file.write("[WHAT INCLUDED]\n")
            product_file.write(f"{len(prompt_pack)}hand-crafted prompts\n")
            product_file.write(f"Covers 6 categories:Marketing,Social media,Email,Strategy,Service,E-commerce.\n")
            product_file.write("Each prompt tested and optimized for real-world results.\n\n")
            product_file.write("="*60+"\n\n")
            current_category=""
            for p in prompt_pack:
                if p["category"] != current_category:
                    current_category=p["category"]
                    product_file.write(f"\n📂category:{current_category}\n")
                    product_file.write("-"*40+"\n")
                product_file.write(f"\n【{p['id']}】{p['title']}({p['tier']})\n")  
                product_file.write(f"prompt：{p['prompt']}\n")  
            product_file.write("\n"+"="*60+"\n")
            product_file.write("Thank you for your purchase!More industry-specific prompt packs coming soon.\n")
            product_file.write("="*60+"\n") 
        print(f"Product file generated:{filename}")   
        return True
    except Exception as e:
        print(f"[ERROR] Failed to generated {e}")  
        return False  
def generate_placeholder_guide(prompt_pack,filename="placeholder_guide.txt"):
    try:
        placeholder_pattern=re.compile(r'\[([A-Z\s]+)\]')
        placeholder_map={}
        for p in prompt_pack:
            text=p["title"] + " " + p["prompt"]
            matches=placeholder_pattern.findall(text)
            for match in set(matches):
                if match not in placeholder_map:
                    placeholder_map[match]=0
                placeholder_map[match] += 1  
        if not placeholder_map:
            print("No placeholders found,skipping generation.") 
            return False  
        with open(filename,"w",encoding="utf-8") as f:
            f.write("="*60+"\n")
            f.write("PLACEHOLDER FILLING GUIDE\n")
            f.write("How to customize your AI prompts\n")
            f.write("="*60+"\n\n")
            f.write("Replace each [BRACKETED] placeholder below with your own info:\n\n")
            for placeholder,count in sorted(placeholder_map.items(),key=lambda x:x[1],reverse=True):
                f.write(f"[{placeholder}]\n")
                f.write(f"Appear in {count} prompt(s)\n")
                f.write(f"Example: {_generate_example(placeholder)}\n\n")
            f.write("="*60+"\n")
            f.write("Tip:Copy the example,then replace with your real business info.\n")
            f.write("="*60+"\n")
        print(f"Placeholder guide generated:{filename}")  
        return True
    except Exception as e:
        print(f"Failed to generate placeholder guide:{e}")    
        return False   
def _generate_example(placeholder):
    examples={
        "BUSINESS TYPE": "coffee shop / online bakery / consulting firm",
        "AUDIENCE": "working moms aged 30-45 / college students / small business owners",
        "LOCATION": "New York / online globally / London UK",
        "OFFER": "20% off summer sale / free consultation / new product launch",
        "COMPETITOR NAMES": "Starbucks, Blue Bottle / local competitors",
        "COMPLAINT": "late delivery / damaged product / poor customer service",
        "PRODUCT NAME": "Artisan Coffee Beans / Business Strategy Course",
        "PLATFORM": "Shopify / Etsy / Amazon",
        "KEYWORDS": "organic coffee, fair trade, morning energy",
        "INSERT DATA": "Revenue: $5k, Cost: $2k, New customers: 50, Retention: 60%",
        }  
    return examples.get(placeholder,"your specific info here")       
def generate_html(prompt_list,filename="product_page.html"):
    try:
        total=len(prompt_list)
        paid=sum(1 for p in prompt_list if p.tier=="paid")  
        free=total-paid        
        categories={}
        for p in prompt_list:
            categories.setdefault(p.category,[]).append(p)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>50 AI Prompts for Small Business Owners</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #f5f5f5; padding: 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 10px; }}
        .subtitle {{ text-align: center; color: #7f8c8d; margin-bottom: 30px; }}
        .stats {{ display: flex; justify-content: space-around; background: white; padding: 20px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stat {{ text-align: center; }}
        .stat-num {{ font-size: 28px; font-weight: bold; color: #3498db; }}
        .category {{ margin-bottom: 25px; }}
        .category h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 15px; }}
        .prompt-card {{ background: white; padding: 18px; border-radius: 10px; margin-bottom: 12px; box-shadow: 0 1px 5px rgba(0,0,0,0.08); }}
        .prompt-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
        .prompt-title {{ font-weight: bold; color: #2c3e50; }}
        .badge {{ padding: 3px 10px; border-radius: 20px; font-size: 12px; color: white; }}
        .badge-paid {{ background: #e74c3c; }}
        .badge-free {{ background: #27ae60; }}
        .prompt-body {{ color: #555; font-size: 14px; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 50 AI Prompts for Small Business Owners</h1>
        <p class="subtitle">Hand-crafted prompts to 10x your business productivity</p>

        <div class="stats">
            <div class="stat"><div class="stat-num">{total}</div><div>Total Prompts</div></div>
            <div class="stat"><div class="stat-num">{paid}</div><div>Paid</div></div>
            <div class="stat"><div class="stat-num">{free}</div><div>Free Samples</div></div>
        </div>
"""
        for category, prompts in categories.items():
            html += f'        <div class="category">\n'
            html += f'            <h2>📂 {category}</h2>\n'
            for p in prompts:
                badge_class = "badge-paid" if p.tier == "paid" else "badge-free"
                badge_text = "PAID" if p.tier == "paid" else "FREE"
                html += f'            <div class="prompt-card">\n'
                html += f'                <div class="prompt-header">\n'
                html += f'                    <span class="prompt-title">[{p.id}] {p.title}</span>\n'
                html += f'                    <span class="badge {badge_class}">{badge_text}</span>\n'
                html += f'                </div>\n'
                html += f'                <div class="prompt-body">{p.content}</div>\n'
                html += f'            </div>\n'
            html += f'        </div>\n'

        html += """    </div>
</body>
</html>
"""
        with open(filename,"w",encoding="utf-8")as f:
            f.write(html)
        print(f"HTML product page generated:{filename}")
        print("Open it in a browser to preview.")
        return True
    except Exception as e:
        print(f"Failed to generate HTML:{e}")
        return False
