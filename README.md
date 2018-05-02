# CSS2dict
CSS2dict is a Python module to parse CSS and make it a dictionary
Features:
 * It is **callable**, that means you can do directly CSS2dict(code) instead of doing CSS2dict.parse(code)
 * It returns a dictionary of this structure:


    {
    'selector':
        {
        'selection': <Style object>
        }
    'other selector:
        {
        'selection': <Style object>
        'other selection': <Style object>
        }
    }
 * Style objects are objects containing all the properties of the selection, like selection.color, selection.font-size, etc.
 * Style objects have a \_\_str\_\_ method wich makes them look as dictionaries, but they aren't
 * If you want Style objects to be dictionaries, you can pass True as the second argument
## How to use

    >> import CSS2py
    >> x = CSS2py(".marquee { color: red}")
    >> x['.']['marquee'].color
    red
    >> type(x['.']['marquee'])
    Style
    >> x
    {'.':{'marquee':{'color':'red'}}}


[Github repository](https://github.com/FranchuFranchu/CSS2dict)
    
    
