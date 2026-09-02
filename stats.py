def print_stats_report(prompt_pack):
    try:
        paid=len([p for p in prompt_pack if p["tier"]=="paid"])
        free=len([p for p in prompt_pack if p["tier"]=="free_sample"])
        category_count={}    
        for p in prompt_pack:
            category_count[p["category"]]=category_count.get(p["category"],0)+1
        print("\nPreparing data for Gumroad listing")  
        print("="*50)  
        print(f"Product:50 AI prompts for small business owners")
        print(f"Progress:{len(prompt_pack)}/50 prompts")
        print(f"Paid prompts:{paid}")
        print(f"Free prompts：{free}(for lead magnet)")
        print(f"Pricing:＄19 standard pack(launch at 50 prompts)")
        print(f"category breakdown：")
        for category,count in category_count.items():
            print(f"-{category}:{count}")
        print("="*50)
        return True
    except Exception as e:
        print(f"Failed to generate the report.")   
        return False     
