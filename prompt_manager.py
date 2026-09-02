import re
from prompt_model import Prompt
def create_prompt(id,title,category,content,tier):
    p=Prompt(id,title,category,content,tier)
    is_valid,error=p.validate()
    if not is_valid:
        print(f"Invalide prompt:{error}")
        return None
    return p
def add_prompt(prompt_list,id,title,category,content,tier):
    if any(p.id==id for p in prompt_list):
        print(f"ID {id} already exists.")
        return False
    p=create_prompt(id,title,category,content,tier)  
    if p is None:
        return False  
    prompt_list.append(p)
    print(f"added:{p.title}")
    return True
def filter_by_category(prompt_list, category_name):
    category_name=category_name.lower()   
    return[p for p in prompt_list if p.category.lower()==category_name]    
def prompts_to_dicts(prompt_list):
    return [p.to_dict() for p in prompt_list]    
def load_prompts_from_dicts(dict_list):
    prompts=[] 
    for d in dict_list:
        p=Prompt(
            id=d["id"],
            title=d["title"],
            category=d["category"],
            content=d["prompt"],
            tier=d["tier"]
        ) 
        prompts.append(p)     
    return prompts                        
def interactive_add(prompt_pack):
    try:
        id_input=input("Enter id (number):").strip()
        if not id_input:
            print("[ERROR] Id can't be empty.")
            return
        try:
            prompt_id=int(id_input)
        except ValueError:
            print("[ERROR] Id must be a number.")
            return
        if any(p.id==prompt_id for p in prompt_pack):
            print("[ERROR] Id already exists. Choose another.")  
            return                  
        title=input("Enter title:").strip() 
        if not title:
            print("[ERROR] Title can't be empty.")  
            return
        category=input("Enter category:").strip() 
        if not category:
            print("[ERROR] Category can't be empty.") 
            return
        content=input("Enter prompt content:").strip() 
        if not content:
            print("[ERROR] Prompt content can't be empty.")  
            return
        tier=input("Enter tier (paid/free_sample):").strip()  
        if tier not in ["paid","free_sample"]:
            print("[ERROR] Tier must be 'paid' or 'free_sample'.") 
            return        
        add_prompt(prompt_pack,prompt_id,title,category,content,tier)    
    except Exception as e:
        print(f"[ERROR] Add failed:{e}")  
def search_prompts(prompt_list,keyword):
    keyword=keyword.lower()
    results=[]
    for p in prompt_list:
        if keyword in p.title.lower() or keyword in p.content.lower():
            results.append(p)
    return results       
def search_by_title_regex(prompt_pack,pattern):
    try: 
        if not pattern:  
            print("Search pattern can't empty!") 
            return
        regex=re.compile(pattern,re.IGNORECASE)
        found=False     
        for p in prompt_pack:
            if regex.search(p.title):
                print(f"[{p.id}]{p.title}({p.category})")
                found=True
        if not found:
            print(f"No title matching pattern '{pattern}'")   
    except re.error as e:
        print(f"Regular expression error:{e}")  
    except Exception as e:
        print(f"Failed search:{e}")
def extract_placeholders(prompt_pack):
    try:
        placeholder_pattern=re.compile(r'\[([A-Z\s]+)\]')   
        placeholder_map={}   
        for p in prompt_pack:
            text=p.title +" "+ p.content  
            matches=placeholder_pattern.findall(text)  
            for match in set(matches):
                if match not in placeholder_map:
                    placeholder_map[match]=[]
                placeholder_map[match].append(p.title)  
        if not placeholder_map:  
            print("No placeholders found.") 
            return{}     
        print("\n"+"="*50)   
        print("Placeholder extraction report.") 
        print("="*50)
        for Placeholder, titles in sorted(placeholder_map.items()):
            print(f"\n [{Placeholder}]-{len(titles)} in prompts")
            for t in titles:
                print(f"  -{t}")
        print("\n"+"="*50) 
        return placeholder_map
    except Exception as e: 
        print(f"Failed extraction:{e}")  
        return  {}    
def find_by_id(prompt_list,prompt_id):
    for p in prompt_list:
        if p.id==prompt_id:
            return p
    return None
def delete_prompt(prompt_list,prompt_id):
    p=find_by_id(prompt_list,prompt_id)
    if p is None:
        print(f"ID{prompt_id} doesn't exist.")
        return False
    prompt_list.remove(p)
    print(f"Deleted: [{p.id}]{p.title}") 
    return True   
            
                    
                                   
                
