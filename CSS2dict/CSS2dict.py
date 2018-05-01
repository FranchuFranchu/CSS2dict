
"""
CSS2dict(text) -> dictionary containing processed CSS

Example:

>> var = CSS2dict('
#a {
    color = red
    font-size = 16
}')

>> var['#']['a'].color

red

>> print(var)

{#:{a:{'color':'red','font-size':'16'}}}

This happens because the Style object has a __str__ method

The second argument, if True, will return a real dictionary instead of an object
Example:

>> var = CSS2dict('
#a {
    color = red
    font-size = 16
}',True) #var is {#:{a:{'color':'red','font-size':'16'}}}
 
>> var['#']['a']['color']

red
"""
import sys #I'm laughing at you, PEP


def rw(text,bad=[' ']):
    "Internal for parsing"
    if text == '':
        return ''
    while True:
        if text[0] in bad:
            text = text[1:]
        else:
            break
    while True:
        if text[-1] in bad:
            text = text[:-1]
        else:
            break
    
    return text
class Style:
    "internal too"
    def __init__(self):
        attrs = ['align-content','align-items','align-self','all','animation','animation-delay','animation-direction','animation-duration','animation-fill-mode','animation-iteration-count','animation-name','animation-play-state','animation-timing-function','backface-visibility','background','background-attachment','background-blend-mode','background-clip','background-color','background-image','background-origin','background-position','background-repeat','background-size','border','border-bottom','border-bottom-color','border-bottom-left-radius','border-bottom-right-radius','border-bottom-style','border-bottom-width','border-collapse','border-color','border-image','border-image-outset','border-image-repeat','border-image-slice','border-image-source','border-image-width','border-left','border-left-color','border-left-style','border-left-width','border-radius','border-right','border-right-color','border-right-style','border-right-width','border-spacing','border-style','border-top','border-top-color','border-top-left-radius','border-top-right-radius','border-top-style','border-top-width','border-width','bottom','box-decoration-break','box-shadow','box-sizing','break-after','break-before','break-inside','caption-side','caret-color','@charset','clear','clip','color','column-count','column-fill','column-gap','column-rule','column-rule-color','column-rule-style','column-rule-width','column-span','column-width','columns','content','counter-increment','counter-reset','cursor','direction','display','empty-cells','filter','flex','flex-basis','flex-direction','flex-flow','flex-grow','flex-shrink','flex-wrap','float','font','@font-face','font-family','font-feature-settings','@font-feature-values','font-kerning','font-language-override','font-size','font-size-adjust','font-stretch','font-style','font-synthesis','font-variant','font-variant-alternates','font-variant-caps','font-variant-east-asian','font-variant-ligatures','font-variant-numeric','font-variant-position','font-weight','grid','grid-area','grid-auto-columns','grid-auto-flow','grid-auto-rows','grid-column','grid-column-end','grid-column-gap','grid-column-start','grid-gap','grid-row','grid-row-end','grid-row-gap','grid-row-start','grid-template','grid-template-areas','grid-template-columns','grid-template-rows','hanging-punctuation','height','hyphens','image-orientation','image-rendering','image-resolution','@import','justify-content','@keyframes','left','letter-spacing','line-break','line-height','list-style','list-style-image','list-style-position','list-style-type','margin','margin-bottom','margin-left','margin-right','margin-top','max-height','max-width','@media','min-height','min-width','object-fit','object-position','opacity','order','orphans','outline','outline-color','outline-offset','outline-style','outline-width','overflow','overflow-wrap','overflow-x','overflow-y','padding','padding-bottom','padding-left','padding-right','padding-top','page-break-after','page-break-before','page-break-inside','perspective','perspective-origin','pointer-events','position','quotes','resize','right','tab-size','table-layout','text-align','text-align-last','text-combine-upright','text-decoration','text-decoration-color','text-decoration-line','text-decoration-style','text-indent','text-justify','text-orientation','text-overflow','text-shadow','text-transform','text-underline-position','top','transform','transform-origin','transform-style','transition','transition-delay','transition-duration','transition-property','transition-timing-function','unicode-bidi','user-select','vertical-align','visibility','white-space','widows','width','word-break','word-spacing','word-wrap','writing-mode','z-index']
        for i in attrs:
            self.adop(i,'')
    def adop(self,string, data):
        for i in range(len(string)):
            try:
                string[i]
            except:
                continue
            if string[i]=='-':
                string = string[:i]+string[i+1].upper()+string[i+2:]
        if string[0] == '@':
            string = 'rl'+string[1:]
        data = "'"+data+"'"
        string = 'self.'+str(string)
        ds = string+'='+data
        print(ds)
        exec(ds,{'self':self})
    def __str__(self):
        return str(dict(vars(self)))
    def __sum__(self,other):
        r = Style()
        for i in vars(self):
            r.adop(i,vars(self)[i])
        for i in vars(other):
            r.adop(i,vars(other)[i])     
        return r
    def __getattr__(self,name):
        return None
    __repr__ = __str__
class cssp(sys.modules[__name__].__class__):
    def __call__(self,text,noObject=False):  # module callable
        """
CSS2dict(text) -> dictionary containing processed CSS
Example
>> var = CSS2dict('
#a {
    color = red
    font-size = 16
}') #var is {#:{a:<style object>}}
>> var['#']['a'].color
red
>> print(var)
{#:{a:{'color':'red','font-size':'16'}}}
>> #this happens because the Style object has a __str__ method
>> #the second argument, if True, will return a true dictionary instead of an object
>> var = CSS2dict('
#a {
    color = red
    font-size = 16
}',True) #var is {#:{a:{'color':'red','font-size':'16'}}} 
>> var['#']['a']['color']
red

    """
        a = dict()
        selection = ''
        selector = ''
        key = ''
        value = ''
        readingName = False
        waitForOpen = False
        opened = False
        readingValue = False
        readingKey = False
        for i in text:
            if not(opened):
                if readingName:
                    if i== '{':
                        opened = True
                        waitForOpen = False
                        readingName = False
                        selection = rw(selection)
                    else:
                        selection+=i
                elif waitForOpen:
                    if i == ' ':
                        pass
                    elif i== '{':
                        opened = True
                        waitForOpen = False
                else:
                    if i == '\n':
                        pass
                    elif i=='*':
                        selector = i
                        waitForOpen = True
                    elif i.isalpha():
                        selector = ''
                        readingName = True
                        selection+=i
                    else:
                        selector = i
                        readingName = True
            else:
                if readingKey:

                    if i == ':':
                        readingKey = False
                        readingValue = True
                    else:
                        key+=i
                elif readingValue:
                    if i == ';':
                        readingValue = False
                        try:
                            a[selector]
                        except:
                            a[selector] = dict()
                        try:
                            a[selector][selection]
                        except:
                            a[selector][selection] = Style()
                        key = rw(key)
                        value = rw(value)
                        a[selector][selection].adop(key,value)
                        key,value = ('','')
                    elif i== '}':
                        readingValue = False
                        try:
                            a[selector]
                        except:
                            a[selector] = dict()
                        try:
                            a[selector][selection]
                        except:
                            a[selector][selection] = Style()
                        key = rw(key)
                        value = rw(value)
                        a[selector][selection].adop(key,value)
                        key,value = ('','')
                        opened = False
                        if noObject:
                            a[selector][selection] = vars(a[selector][selection])
                        selection,selector = ('','')
                else:
                    if i == '\n':
                        pass
                    elif i == ' ':
                        pass
                    elif i== '}':
                        opened = False
                        if noObject:
                            a[selector][selection] = vars(a[selector][selection])
                        selection,selector = ('','')
                    else:
                        readingKey = True
                        key+=i
        return a
sys.modules[__name__].__class__ = cssp
if __name__ == '__main__':
    validcss ='a::c{h:1;}'
    a = cssp(__name__)
    print(a(validcss))
    