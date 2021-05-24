from myNote.models import ProgrammingLanguage
language = {
    'C':{'types':'c','path':'clike/clike.js'},
    'C++':{'types':'cpp','path':'clike/clike.js'},
    'C#':{'types':'cs','path':'clike/clike.js'},
    'CSS':{'types':'css','path':'css/css.js'},
    'Django (templating language)':{'types':'html','path':'django/django.js'},
    'Go':{'types':'go','path':'go/go.js'},
    'Haskell (Literate)':{'types':'lhs','path':'haskell/haskell.js'},
    'HTML':{'types':'html','path':'htmlmixed/htmlmixed.js'},
    'Java':{'types':'java','path':'clike/clike.js'},
    'JavaScript (JSX)':{'types':'js','path':'javascript/javascript.js'},
    'Markdown (GitHub-flavour)':{'types':'md','path':'markdown/markdown.js'},
    'Objective C':{'types':'m','path':'clike/clike.js'},
    'Pascal':{'types':'pas','path':'pascal/pascal.js'},
    'Perl':{'types':'pl','path':'perl/perl.js'},
    'PHP':{'types':'php','path':'php/php.js'},
    'Python':{'types':'py','path':'python/python.js'},
    'R':{'types':'r','path':'r/r.js'},
    'Ruby':{'types':'rb','path':'ruby/ruby.js'},
    'Rust':{'types':'rs','path':'rust/rust.js'},
    'SQL (several dialects)':{'types':'sql','path':'sql/spl.js'},
    'Swift':{'types':'swift','path':'swift/swift.js'},
    'XML':{'types':'xml','path':'xml/xml.js'},
}

for key,item in language.items():
    obj =  ProgrammingLanguage(language=key,extension=item['types'],path_to_file=item['path'])
    obj.save()