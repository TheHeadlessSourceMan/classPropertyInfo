import typing
import re
import inspect


def getClassPropertyComments(cls:typing.Any)->typing.Dict[str,str]:
    """
    returns {varname:comment}
    """
    quote_regex=r"""r?("{3}|"|')(?P<contents>(?:[^\1\\]|\\.)*)\1"""
    line_regex=r"""\s*self\.(?P<membername>[a-zA-Z_][a-zA-Z0-9]*)(:(?P<peptype>[^=]*))?\s*=\s*(?P<assignment>(("""+quote_regex+r""")|[^#])*)([#]\s*(?P<comment>.*))?"""
    classlevel_regex=r"""(?P<membername>[a-zA-Z_][a-zA-Z0-9]*)(:(?P<peptype>[^=]*))?\s*=\s*(?P<assignment>(("""+quote_regex+r""")|[^#])*)([#]\s*(?P<comment>.*))?"""
    ret={}
    # just in case they pass in an instance instead of a class type
    if not inspect.isclass(cls):
        cls=cls.__class__
    # inspect things coming from parent classes
    for parent in cls.__bases__:
        if parent!=object:
            ret.update(getClassPropertyComments(parent))
    # inspect class-level values
    for line in inspect.getsourcelines(cls)[0][1:]:
        noindent=line.lstrip()
        if not noindent or noindent[0]=='#': # blank line or ignore
            continue
        if isinstance(classlevel_regex,str):
            indent=line[0:-len(noindent)]
            classlevel_regex=indent+classlevel_regex
            classlevel_regex=re.compile(classlevel_regex)
        m=classlevel_regex.match(line)
        if m is not None:
            membername=m.group('membername')
            comment=m.group('comment')
            if comment is None:
                comment=ret.get(membername,'')
            ret[membername]=comment
    # inspect variables defined in __init__
    initFn=getattr(cls,'__init__')
    if initFn.__class__.__name__!='wrapper_descriptor':
        line_regex=re.compile(line_regex)
        for line in inspect.getsourcelines(initFn)[0][1:]:
            m=line_regex.match(line)
            if m is not None:
                membername=m.group('membername')
                comment=m.group('comment')
                if comment is None:
                    comment=ret.get(membername,'')
                ret[membername]=comment
    return ret