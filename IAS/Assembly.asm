SETZERO M(251) NOP
SETZERO M(252) NOP
LOAD M(250) ADD M(252)
STORE M(255) WC1 M(255)
ADD M(254) STORE M(255)
WC2 M(255) CHECKC1C2
JUMP+ M(8) JUMP_LEFT M(11)
SC1 M(255) LOAD M(255)
SUB M(254) STORE M(255)
SC2 M(255) NOP
LOAD M(252) ADD M(254)
STORE M(252) LOAD M(253)
SUB M(251) SUB M(252)
JUMP+ M(3) NOP
LOAD M(251) ADD M(254)
STORE M(251) LOAD M(253)
SUB M(251) NOP
JUMP+ M(2) NOP
NOP NOP