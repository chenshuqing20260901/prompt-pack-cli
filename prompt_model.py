import re
class Prompt:
    def __init__(self,id,title,category,content,tier):
        self.id=id
        self.title=title
        self.category=category
        self.content=content
        self.tier=tier
    def preview(self,length=50):
        preview_text=f"{self.title}:{self.content}"
        if len(preview_text)<=length:
            return preview_text
        return preview_text[:length] + "…" 
    def validate(self):
        if not self.title:
            return False
        if not self.content:
            return False 
        if self.tier not in ["paid","free_sample"]:
            return False
        placeholders=re.findall(r'\[([A-Z\s]+)\]',self.content)   
        if not placeholders:
            return False 
        return True 
    def render(self,**kwargs):
        result=self.content
        for key,value in kwargs.items():
            placeholder=f"[{key.upper().replace('_',' ')}]"
            result=result.replace(placeholder,str(value))
        return result
    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "category":self.category,
            "prompt":self.content,
            "tier":self.tier
        }
    def __str__(self):
        return f"[{self.id}]{self.title}({self.category})-{self.tier}"
    def update(self,**kwargs):
        allowed_fields=["title","category","content","tier"]
        updated=[]
        for field,value in kwargs.items():
            if field in allowed_fields:
                setattr(self,field,value)
                updated.append(field)
        if updated:
            print(f"Updated fields:{','.join(updated)}")
        else:
            print("No updatable fields.")
        return len(updated)>0
    def __repr__(self):
        return f"Prompt(id={self.id},title='{self.title}',tier='{self.tier}')"
            
