from prompt_model import Prompt
from prompt_manager import add_prompt,search_prompts,filter_by_category,interactive_add,search_by_title_regex,extract_placeholders,create_prompt,find_by_id,delete_prompt
from file_handler import save_to_json,load_from_json,generate_product_file,JSON_PATH,generate_placeholder_guide,generate_html
from stats import print_stats_report
def init_defaults(prompt_list):
    print("First time startup,initializing default prompts.")
    DEFAULT_PROMPT=[
        (1,"Customer Avatar Builder","Marketing","You are a market research analyst.My business is [BUSINESS TYPE],targeting [AUDIENCE] in [LOCATION].Build a detailed customer avatar including demographics,top 3 pain points,and where they spend time online.","free_sample"),
        (2,"30-Day Content Calendar","Social Media","Create a 30-day social media content calendar for a [BUSINESS TYPE].Include post topic,caption under 150 words,image description,best posting time,and hashtags.Mix:40% educational,30% entertaining,30% promotional.","paid"),
        (3,"Email Subject Line Generator","Email Marketing","Generate 20 email subject line for a [BUSINESS TYPE] promoting [OFFER].Include 5 curiosity-driven,5 benefit-driven,5 urgency-driven,5 social-proof-driven.Each under 50 characters.","paid"),
        (4,"Competitor Differentiator","Strategy","I run a [BUSINESS TYPE] competing with [COMPETITOR NAMES] Analyze what makes each competitor strong,then identify 3 positioning angles I could own that they don't.","paid"),
        (5,"Landing Page Copy Framework","Sales Copy","Write landing page copy for [OFFER] targeting [AUDIENCE].Use PAS framework(problem,agitate,solution).Include headline under 10 words,subheadline,3 benefit bullets,and CTA button text.Total under 200 words.","free_sample"),
        (6,"Customer Service Reply Templates","Customer Service","I am a customer service manager for a [BUSINESS TYPE].for the following complaint:[COMPLAINT],generate 5 reply templates in different tones:empathetic,professional,humorous,assertive,and compensation-oriented.Each includes opening,acknowledgment,solution,and closing.","paid"),
        (7,"Product Description Optimizer","E-commerce","Write an optimized e-commerce product description for [PRODUCT NAME].Target platform:[PLATFORM].Include SEO keywords[KEYWORDS],3 core selling points,use cases,specification,and FAQ.Total 300-500 words.","paid"),
        (8,"Data-Driven Decision Assistant","Business Intelligence","I run a [BUSINESS TYPE].This month's data:[INSERT DATA].Analyze from four dimensions:revenue,cost,customer acquisition,and retention.Identify 3 most urgent problems and provide a specific improvement plan for each.","paid"),
    ]  
    for id,title,category,content,tier in DEFAULT_PROMPT:
        add_prompt(prompt_list,id,title,category,content,tier)
    save_to_json(prompt_list,JSON_PATH)    
def show_menu():
    print("\n"+"="*50)        
    print("PROMPT PACK CLI MANAGER v4.0") 
    print("="*50)  
    print("1.List all prompt")
    print("2.Filter by category") 
    print("3.Search by keyword")
    print("4.Search title by regex")
    print("5.Add a prompt(interactive)") 
    print("6.Edit a prompt (update)")
    print("7.Delete a prompt")
    print("8.Save to JSON")  
    print("9.Generate product TXT file")
    print("10.Generate placeholder guide TXT")
    print("11.Generate HTML product page")
    print("12.Show Gumroad stats report")
    print("13.Demo render")
    print("14.Exit")  
    print("="*50) 
def main():
    print("Launch prompt package management terminal v4.0……")
    prompt_pack=load_from_json(JSON_PATH)
    if not prompt_pack:
        init_defaults(prompt_pack)
    print(f"Total:{len(prompt_pack)} prompts currently.\n")    
    while True:
        show_menu()
        choice=input("Select an option(1-14):").strip()
        if choice=="1":
            if not prompt_pack:
                print("[WARN] Prompt pack is empty.")
            else:
                for p in prompt_pack:
                    print(f"[{p.id}]{p.title}|{p.category}|{p.tier}")   
                    print(f"Preview:{p.preview(40)}") 
        elif choice=="2":
            filter_by_category(prompt_pack)
        elif choice=="3":
            search_prompts(prompt_pack)
        elif choice=="4":
            pattern=input("Please enter a regular expression:").strip()
            if pattern:
                search_by_title_regex(prompt_pack,pattern)
            else:
                print("Pattern can't be empty.")
        elif choice=="5":
            interactive_add(prompt_pack)
        elif choice=="6":
            try:
                edit_id=int(input("Edit id:")).strip()
            except ValueError:
                print("ID must be number.")
                continue
            p=find_by_id(prompt_pack,edit_id)
            if p is None:
                print(f"ID {edit_id} isn't exists.")
                continue
            print(f"Current:{p}")
            print("Leave blank for no changes.Editable fields:title/category/content/tier")
            new_title=input("New title:").strip()
            new_category=input("New category:").strip()
            new_content=input("New content:").strip()
            new_tier=input("New tier:").strip()
            updates={}
            if new_title:updates["title"]=new_title
            if new_category:updates["category"]=new_category
            if new_content:updates["content"]=new_content
            if new_tier:
                if new_tier in ["paid","free_sample"]:
                    updates["tier"]=new_tier
                else: 
                    print("Invalid tier,skip tier change.")
            if updates:
                p.update(**updates)
            else:
                print("No change applied.")          
        elif choice=="7":
            try:
                del_id=int(input("ID to delete:").strip())
            except ValueError:
                print("ID must be number.")
                continue
            delete_prompt(prompt_pack,del_id)    
        elif choice=="8":
            save_to_json(prompt_pack,JSON_PATH)
        elif choice=="9":
            generate_product_file(prompt_pack,"50_AI_prompts_for_small_business_owner.txt")
        elif choice=="10":
            generate_placeholder_guide(prompt_pack,"placeholder_guide.txt")
        elif choice=="11":
            generate_html(prompt_pack,"product_page.html")
        elif choice=="12":
            print_stats_report(prompt_pack)          
        elif choice=="13":
            if prompt_pack:
                p=prompt_pack[0]
                print("\n Demo:Render prompt.")
                print(f"Original:{p.content[:60]}…")
                rendered=p.render(
                    business_type="Coffee Shop",
                    audience="Office Workers",
                    location="New York"
                )
                print(f"Rendered:{rendered[:60]}…")
            else:
                print("No prompts to render.")
        elif choice=="14":
            print("Saving before exit…")        
            save_to_json(prompt_pack,JSON_PATH)    
            print("Goodbye! See you next time.")
            break
        else:
            print("[ERROR] Invalid choice.Please enter 1-11.")
if __name__ == "__main__":
    main()   

    
    
    
    
