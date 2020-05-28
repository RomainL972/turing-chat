from pyparsing import Literal, Word, OneOrMore, Combine, nums, alphanums, oneOf, Optional, Empty

listen = Literal("listen")

ipaddr = Word(nums,min=1,max=3) + ('.' + Word(nums,min=1,max=3)) * 3
dnsname = Word(alphanums) + OneOrMore('.' + Word(alphanums))
connect = "connect" + Combine(ipaddr ^ dnsname ^ "last" ^ Empty())

quit = Literal("quit")
help = Literal("help")
nick = "nick" + Word(alphanums,max=15)
trust = "trust" + oneOf("0 1 2")
fingerprint = Literal("fingerprint")
language = "language" + oneOf("en fr")



commands = "/" + (listen ^ connect ^ quit ^ help ^ nick ^ trust ^ fingerprint ^ language)
