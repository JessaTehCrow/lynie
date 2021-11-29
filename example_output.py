e = [othervar:=1,_while:=lambda test: [othervar:=3*2,_while(othervar<2)] if test else None,_while(othervar<2)]
